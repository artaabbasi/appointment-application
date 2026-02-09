from common.appointment.schema.appointment_item_in_schema import AppointmentItemInSchema
from common.appointment.schema.appointment_item_schema import AppointmentItemSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.appointment_item_entity import AppointmentItemEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.appointment_item_repository import AppointmentItemRepository


class AppointmentItemService(BaseCRUDService):
    def __init__(self):
        super().__init__(AppointmentItemRepository, AppointmentItemEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_appointment_item_by_id(self, appointment_item_id: str) -> AppointmentItemSchema:
        appointment_item = await self.repository.fetch_by_id(appointment_item_id)
        return appointment_item.convert_to_schema()

    async def get_appointment_item_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[AppointmentItemSchema]:
        specialities = await self._list(page, size, filters, search)
        return [appointment_item.convert_to_schema() for appointment_item in specialities]

    async def update_appointment_item(self, entity_id: str, schema: AppointmentItemInSchema) -> AppointmentItemSchema:
        appointment_item = await self._update_by_id(schema, entity_id, is_partial=True)
        return appointment_item.convert_to_schema()

    async def delete_appointment_item(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_appointment_item(self, data_in: AppointmentItemInSchema) -> AppointmentItemSchema:
        appointment_item = await self.repository.create(
            AppointmentItemEntity(
                appointment_id=data_in.appointment_id,
                service_id=data_in.service_id,
                operator_id=data_in.operator_id,
                from_datetime=data_in.from_datetime,
                to_datetime=data_in.to_datetime,
            )
        )
        return appointment_item.convert_to_schema()

    async def cancel_appointment_item(self, appointment_item_id: str) -> None:
        appointment_item = await self.repository.fetch_by_id(appointment_item_id)
        appointment_item.is_cancelled = True
        await self.repository.update(appointment_item)
