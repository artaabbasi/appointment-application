from common.appointment.schema.service_in_schema import ServiceInSchema
from common.appointment.schema.service_schema import ServiceSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.service_entity import ServiceEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.service_repository import ServiceRepository


class ServiceService(BaseCRUDService):
    def __init__(self):
        super().__init__(ServiceRepository, ServiceEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_service_by_id(self, service_id: str) -> ServiceSchema:
        service = await self.repository.fetch_by_id(service_id)
        return service.convert_to_schema()

    async def get_service_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[ServiceSchema]:
        specialities = await self._list(page, size, filters, search)
        return [service.convert_to_schema() for service in specialities]

    async def update_service(self, entity_id: str, schema: ServiceInSchema) -> ServiceSchema:
        service = await self._update_by_id(schema, entity_id, is_partial=True)
        return service.convert_to_schema()

    async def delete_service(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_service(self, data_in: ServiceInSchema) -> ServiceSchema:
        service = await self.repository.create(
            ServiceEntity(
                main_service_id=data_in.main_service_id,
                name=data_in.name,
                duration=data_in.duration,
                description=data_in.description,
                price_as_rial=data_in.price_as_rial,
                deposit_type=data_in.deposit_type,
                deposit_amount=data_in.deposit_amount,
                is_active=data_in.is_active,
            )
        )
        return service.convert_to_schema()
