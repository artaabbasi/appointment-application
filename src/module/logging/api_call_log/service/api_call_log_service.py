from typing import List

from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from common.logging.schema.api_call_log_in_schema import ApiCallLogInSchema
from common.logging.schema.api_call_log_schema import ApiCallLogSchema
from module.logging.api_call_log.entity.api_call_log_entity import ApiCallLogEntity
from module.logging.api_call_log.repository.api_call_log_repository import ApiCallLogRepository


class ApiCallLogService(BaseCRUDService):
    def __init__(self):
        super().__init__(ApiCallLogRepository, ApiCallLogEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_api_call_log_list(self,
                                    page: int = 1,
                                    size: int = 10,
                                    filters: dict = None,
                                    search: str = "") \
            -> list[ApiCallLogSchema]:
        api_call_logs = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return [api_call_log.convert_to_schema() for api_call_log in api_call_logs]

    async def get_by_id(self, api_call_log_id: str) -> ApiCallLogSchema:
        api_call_log = await self.repository.fetch_by_id(api_call_log_id)
        return api_call_log.convert_to_schema()

    async def get_by_ids(self, api_call_log_ids: List[str]) -> List[ApiCallLogSchema]:
        api_call_logs = await self.repository.fetch_all_by_ids(api_call_log_ids)
        return [api_call_log.convert_to_schema() for api_call_log in api_call_logs]

    async def update_api_call_log(self, entity_id: str, schema: ApiCallLogInSchema) -> ApiCallLogSchema:
        api_call_log = await self._update_by_id(schema, entity_id, is_partial=True)
        return api_call_log.convert_to_schema()

    async def delete_api_call_log(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_api_call_log(self, data_in: ApiCallLogInSchema) -> ApiCallLogSchema:
        api_call_log = await self.repository.create(
            ApiCallLogEntity(
                type=data_in.type,
                description=data_in.description,
                method=data_in.method,
                url=data_in.url,
                headers=data_in.headers,
                payload=data_in.payload,
                status_code=data_in.status_code,
                response_body=data_in.response_body,
                response_headers=data_in.response_headers,
            )
        )
        return api_call_log.convert_to_schema()
