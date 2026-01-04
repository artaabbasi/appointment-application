from common.api_manager.schema.api_in_schema import ApiInSchema
from common.api_manager.schema.api_schema import ApiSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.api_manager.api_key.entity.api_entity import ApiEntity
from module.api_manager.api_key.repository.api_repository import ApiRepository


class ApiService(BaseCRUDService):
    def __init__(self):
        super().__init__(ApiRepository, ApiEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_api_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[ApiSchema]:
        if not filters:
            filters = {}
        apis = await self.repository.fetch_paginated_list_by_filters(page, size, filters,search)
        return [api.convert_to_schema() for api in apis]

    async def update_api(self, entity_id: str, schema: ApiInSchema) -> ApiSchema:
        api = await self._update_by_id(schema, entity_id, is_partial=True)
        return api.convert_to_schema()

    async def add_api_tag_by_api_id(self, api_id: str, api_tag_id: str) -> ApiSchema:
        api = await self._get(api_id)
        if api_tag_id not in api.tags:
            api.tags.append(api_tag_id)
        api = await self.repository.update(api)
        return api.convert_to_schema()

    async def remove_api_tag_by_api_id(self, api_id: str, api_tag_id: str) -> ApiSchema:
        api = await self._get(api_id)
        if api_tag_id in api.tags:
            api.tags.remove(api_tag_id)
        api = await self.repository.update(api)
        return api.convert_to_schema()

    async def delete_api(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_api(self, data_in: ApiInSchema) -> ApiSchema:
        api = await self.repository.create(
            ApiEntity(
                name=data_in.name,
                url=data_in.url,
                methods=data_in.methods,
                tags=data_in.tags,
            )
        )
        return api.convert_to_schema()

    async def get_api_by_ids(self, api_ids: list[str]) -> list[ApiSchema]:
        apis = await self.repository.fetch_all_by_ids(api_ids)
        return [api.convert_to_schema() for api in apis]

    async def get_apis_by_tag_id(self, api_tag_id: str) -> list[ApiSchema]:
        apis = await self.repository.get_apis_by_tag_id(api_tag_id)
        return [api.convert_to_schema() for api in apis]

