from typing import List

from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from common.logging.schema.request_log_in_schema import RequestLogInSchema
from common.logging.schema.request_log_schema import RequestLogSchema
from module.logging.request_log.entity.request_log_entity import RequestLogEntity
from module.logging.request_log.repository.request_log_repository import RequestLogRepository


class RequestLogService(BaseCRUDService):
    def __init__(self):
        super().__init__(RequestLogRepository, RequestLogEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_request_log_list(self,
                                    page: int = 1,
                                    size: int = 10,
                                    filters: dict = None,
                                    search: str = "") \
            -> list[RequestLogSchema]:
        request_logs = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return [request_log.convert_to_schema() for request_log in request_logs]

    async def get_by_id(self, request_log_id: str) -> RequestLogSchema:
        request_log = await self.repository.fetch_by_id(request_log_id)
        return request_log.convert_to_schema()

    async def get_by_ids(self, request_log_ids: List[str]) -> List[RequestLogSchema]:
        request_logs = await self.repository.fetch_all_by_ids(request_log_ids)
        return [request_log.convert_to_schema() for request_log in request_logs]

    async def update_request_log(self, entity_id: str, schema: RequestLogInSchema) -> RequestLogSchema:
        request_log = await self._update_by_id(schema, entity_id, is_partial=True)
        return request_log.convert_to_schema()

    async def delete_request_log(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_request_log(self, data_in: RequestLogInSchema) -> RequestLogSchema:
        request_log = await self.repository.create(
            RequestLogEntity(
                type=data_in.type,
                url=data_in.url,
                method=data_in.method,
                client=data_in.client,
                request_headers=data_in.request_headers,
                request_payload=data_in.request_payload,
                response_status_code=data_in.response_status_code,
                response_body=data_in.response_body,
                response_headers=data_in.response_headers,
            )
        )
        return request_log.convert_to_schema()
