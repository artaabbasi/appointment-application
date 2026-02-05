from common.appointment.schema.appointment_in_schema import AppointmentInSchema
from common.appointment.schema.appointment_schema import AppointmentSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.appointment_entity import AppointmentEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.appointment_repository import AppointmentRepository


class AppointmentService(BaseCRUDService):
    def __init__(self):
        super().__init__(AppointmentRepository, AppointmentEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

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
        return await self._delete_by_id(entity_id)

    async def create_appointment(self, data_in: AppointmentInSchema) -> AppointmentSchema:
        appointment = await self.repository.create(
            AppointmentEntity(
                user_id=data_in.user_id,
                description=data_in.description,
            )
        )
        return appointment.convert_to_schema()
