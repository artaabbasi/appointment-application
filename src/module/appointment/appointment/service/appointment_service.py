from typing import Set, List

from common.appointment.schema.appointment_in_schema import AppointmentInSchema
from common.appointment.schema.appointment_schema import AppointmentSchema
from common.exceptions import BadRequestException
from common.lib.service_action_enum import ServiceActionEnum
from module.account.user.service import CustomerService
from module.gateway.enum.error_code_enum import ErrorCodeEnum
from util.sms_util import SmsUtil
from util.timestamp import DatetimeUtil
from .appointment_item_service import AppointmentItemService
from ..entity.appointment_entity import AppointmentEntity
from common.lib.base_crud_service import BaseCRUDService
from ..entity.appointment_item_entity import AppointmentItemEntity
from ..repository.appointment_repository import AppointmentRepository
from datetime import date

class AppointmentService(BaseCRUDService):
    def __init__(self):
        super().__init__(AppointmentRepository, AppointmentEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.appointment_item_service = AppointmentItemService()

    async def get_appointment_by_id(self, appointment_id: str) -> AppointmentSchema:
        appointment = await self.repository.fetch_by_id(appointment_id)
        return appointment.convert_to_schema()

    async def get_appointment_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[AppointmentSchema]:
        specialities = await self._list(page, size, filters, search)
        return [appointment.convert_to_schema() for appointment in specialities]

    async def update_appointment(self, entity_id: str, schema: AppointmentInSchema) -> AppointmentSchema:
        appointment = await self._update_by_id(schema, entity_id, is_partial=True)
        return appointment.convert_to_schema()

    async def delete_appointment(self, entity_id: str) -> None:
        appointment_items = await self.appointment_item_service.get_appointment_item_list(
            1, -1, filters={AppointmentItemEntity.appointment_id: entity_id}
        )
        for appointment_item in appointment_items:
            await self.appointment_item_service.delete_appointment_item(appointment_item.id)
        return await self._delete_by_id(entity_id)

    async def create_appointment(self, data_in: AppointmentInSchema) -> AppointmentSchema:
        appointment = await self.repository.create(
            AppointmentEntity(
                user_id=data_in.user_id,
                description=data_in.description,
            )
        )
        return appointment.convert_to_schema()

    async def send_appointment_message(self, appointment_id: str) -> None:
        appointment = await self.get_appointment_by_id(appointment_id)
        user = await CustomerService().get_not_detailed_user_by_id(appointment.user_id)
        appointment_items = await self.appointment_item_service.get_appointment_item_list(
            1, -1, filters={AppointmentItemEntity.appointment_id: appointment_id}
        )
        item_date_set = {appointment_item.from_datetime.date() for appointment_item in appointment_items}
        message = self._generate_appointment_message(user.full_name, list(item_date_set))
        await SmsUtil().send_sms([user.phone_number], message)

    def _generate_appointment_message(self, full_name: str, appointment_dates: List[date]) -> str:
        if not appointment_dates:
            raise BadRequestException(ErrorCodeEnum.EMPTY_APPOINTMENT)

        if len(appointment_dates) > 1:
            date_message = f"روزهای {', '.join(DatetimeUtil.utc_to_jalali_date(appointment_date).strftime('%Y/%m/%d') for appointment_date in appointment_dates)}"
        else:
            date_message = f"روز {DatetimeUtil.utc_to_jalali_date(appointment_dates[0]).strftime('%Y/%m/%d')}"
        return f"کاربر {full_name} رزرو شما در {date_message} انجام شد"

    async def _appointment_could_cancelled(self):
        pass

    async def cancel_appointment(self, user_id: str, appointment_id: str) -> None:
        appointment = await self.repository.fetch_by_id(appointment_id)
        await self._appointment_could_cancelled()
        appointment_items = await self.appointment_item_service.get_appointment_item_list(
            1, -1, filters={AppointmentItemEntity.appointment_id: appointment_id}
        )
        for appointment_item in appointment_items:
            await self.appointment_item_service.cancel_appointment_item(appointment_item.id)
        appointment.is_cancelled = True
        appointment.cancelled_at = DatetimeUtil.utc_now_datetime()
        appointment.cancelled_by_id = user_id
        await self.repository.update(appointment)
