
from common.appointment.schema.operator_service_in_schema import OperatorServiceInSchema
from common.appointment.schema.operator_service_schema import OperatorServiceSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.operator_service_entity import OperatorServiceEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.operator_service_repository import OperatorServiceRepository


class OperatorServiceService(BaseCRUDService):
    def __init__(self):
        super().__init__(OperatorServiceRepository, OperatorServiceEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_operator_service_by_id(self, operator_service_id: str) -> OperatorServiceSchema:
        operator_service = await self.repository.fetch_by_id(operator_service_id)
        return operator_service.convert_to_schema()

    async def get_operator_service_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[OperatorServiceSchema]:
        operator_services = await self._list(page, size, filters, search)
        return [operator_service.convert_to_schema() for operator_service in operator_services]

    async def update_operator_service(self, entity_id: str, schema: OperatorServiceInSchema) -> OperatorServiceSchema:
        operator_service = await self._update_by_id(schema, entity_id, is_partial=True)
        return operator_service.convert_to_schema()

    async def delete_operator_service(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_operator_service(self, data_in: OperatorServiceInSchema) -> OperatorServiceSchema:
        operator_service = await self.repository.create(
            OperatorServiceEntity(
                operator_id=data_in.operator_id,
                service_id=data_in.service_id,
            )
        )
        return operator_service.convert_to_schema()
