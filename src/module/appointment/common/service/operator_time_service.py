from datetime import datetime

from common.appointment.schema.bulk_operator_time_in_schema import BulkOperatorTimeInSchema
from common.appointment.schema.operator_time_in_schema import OperatorTimeInSchema
from common.appointment.schema.operator_time_schema import OperatorTimeSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.operator_time_entity import OperatorTimeEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.operator_time_repository import OperatorTimeRepository


class OperatorTimeService(BaseCRUDService):
    def __init__(self):
        super().__init__(OperatorTimeRepository, OperatorTimeEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_operator_time_by_id(self, operator_time_id: str) -> OperatorTimeSchema:
        operator_time = await self.repository.fetch_by_id(operator_time_id)
        return operator_time.convert_to_schema()

    async def get_operator_time_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[OperatorTimeSchema]:
        operator_times = await self._list(page, size, filters, search)
        return [operator_time.convert_to_schema() for operator_time in operator_times]

    async def update_operator_time(self, entity_id: str, schema: OperatorTimeInSchema) -> OperatorTimeSchema:
        operator_time = await self._update_by_id(schema, entity_id, is_partial=True)
        return operator_time.convert_to_schema()

    async def delete_operator_time(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_operator_time(self, data_in: OperatorTimeInSchema) -> OperatorTimeSchema:
        operator_time = await self.repository.create(
            OperatorTimeEntity(
                operator_id=data_in.operator_id,
                from_datetime=data_in.from_datetime,
                to_datetime=data_in.to_datetime,
            )
        )
        return operator_time.convert_to_schema()

    async def create_bulk_operator_time(self, data_in: BulkOperatorTimeInSchema) -> list[OperatorTimeSchema]:
        operator_times = []
        for date in data_in.dates:
            operator_times.append(await self.create_operator_time(
                OperatorTimeInSchema(
                    operator_id=data_in.operator_id,
                    from_datetime=datetime.combine(date, data_in.from_time),
                    to_datetime=datetime.combine(date, data_in.from_time),
                )
            ))
        return operator_times
