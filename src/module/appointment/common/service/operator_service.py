from common.appointment.schema.operator_in_schema import OperatorInSchema
from common.appointment.schema.operator_schema import OperatorSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.operator_entity import OperatorEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.operator_repository import OperatorRepository


class OperatorService(BaseCRUDService):
    def __init__(self):
        super().__init__(OperatorRepository, OperatorEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_operator_by_id(self, operator_id: str) -> OperatorSchema:
        operator = await self.repository.fetch_by_id(operator_id)
        return operator.convert_to_schema()

    async def get_operator_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[OperatorSchema]:
        specialities = await self._list(page, size, filters, search)
        return [operator.convert_to_schema() for operator in specialities]

    async def update_operator(self, entity_id: str, schema: OperatorInSchema) -> OperatorSchema:
        operator = await self._update_by_id(schema, entity_id, is_partial=True)
        return operator.convert_to_schema()

    async def delete_operator(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_operator(self, data_in: OperatorInSchema) -> OperatorSchema:
        operator = await self.repository.create(
            OperatorEntity(
                user_id=data_in.user_id,
                name=data_in.name,
                description=data_in.description,
            )
        )
        return operator.convert_to_schema()
