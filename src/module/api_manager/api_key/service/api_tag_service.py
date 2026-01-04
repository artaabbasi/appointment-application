import asyncio
from typing import Union
from common.api_manager.schema.api_tag_in_schema import ApiTagInSchema
from common.api_manager.schema.api_tag_schema import ApiTagSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.api_manager.api_key.entity.api_tag_entity import ApiTagEntity
from module.api_manager.api_key.repository.api_tag_repository import ApiTagRepository
from module.api_manager.api_key.service.api_service import ApiService


class ApiTagService(BaseCRUDService):
    def __init__(self):
        super().__init__(ApiTagRepository, ApiTagEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.api_service = ApiService()

    async def _aggregate_schema(self, schema: Union[ApiTagSchema, list[ApiTagSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_schema(item) for item in schema
                ]
            )
        else:
            apis = await self.api_service.get_apis_by_tag_id(schema.id)
            schema.apis = apis
        return schema

    async def get_api_tag_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None,) \
            -> list[ApiTagSchema]:
        if not filters:
            filters = {}
        api_tags = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return [api_tag.convert_to_schema() for api_tag in api_tags]

    async def update_api_tag(self, entity_id: str, schema: ApiTagInSchema) -> ApiTagSchema:
        api_tag = await self._update_by_id(schema, entity_id, is_partial=True)
        apis = await self.api_service.get_apis_by_tag_id(api_tag.id)
        await asyncio.gather(
            *[self.api_service.remove_api_tag_by_api_id(api.id, api_tag.id) for api in apis]
        )
        await asyncio.gather(
            *[self.api_service.add_api_tag_by_api_id(api_id, api_tag.id) for api_id in schema.apis]
        )
        return api_tag.convert_to_schema()

    async def delete_api_tag(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def get_api_tag(self, entity_id: str) -> ApiTagSchema:
        api_tag = await self._get(entity_id)
        return await self._aggregate_schema(api_tag.convert_to_schema())

    async def create_api_tag(self, data_in: ApiTagInSchema) -> ApiTagSchema:
        api_tag = await self.repository.create(
            ApiTagEntity(
                name=data_in.name,
            )
        )
        await asyncio.gather(
            *[self.api_service.add_api_tag_by_api_id(api, api_tag.id) for api in data_in.apis]
        )
        return api_tag.convert_to_schema()

    async def get_api_tag_by_ids(self, api_tag_ids: list[str]) -> list[ApiTagSchema]:
        api_tags = await self.repository.fetch_all_by_ids(api_tag_ids)
        return [api_tag.convert_to_schema() for api_tag in api_tags]

