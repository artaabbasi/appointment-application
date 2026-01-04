from typing import Optional

from common.api_manager.schema.api_key_access_schema import ApiKeyAccessSchema
from common.api_manager.schema.api_key_schema import ApiKeySchema
from common.api_manager.schema.api_key_access_create_schema import ListCreateApiKeyAccessSchema
from common.config.http_method_enum import HTTPMethodEnum
from common.exceptions import NotFoundException
from common.lib.base_service import BaseService
from module.api_manager.api_key.entity.api_key_access_entity import ApiKeyAccessEntity
from module.api_manager.api_key.entity.api_key_entity import ApiKeyEntity
from module.api_manager.api_key.repository.api_key_access_repository import ApiKeyAccessRepository
from module.api_manager.api_key.repository.api_key_repository import ApiKeyRepository
from module.api_manager.api_key.repository.api_repository import ApiRepository
from module.api_manager.api_key.repository.api_tag_repository import ApiTagRepository


class ApiKeyService(BaseService):
    def __init__(self):
        self.api_key_access_repository = ApiKeyAccessRepository()
        self.api_key_repository = ApiKeyRepository()
        self.api_repository = ApiRepository()
        self.api_tag_repository = ApiTagRepository()

    async def _aggregate_api_key_schema(self, api_key: ApiKeySchema) -> ApiKeySchema:
        accesses = await self.api_key_access_repository.get_all_by_api_key_id(api_key.id)
        apis = await self.api_repository.fetch_all_by_ids([access.api_id for access in accesses if access.api_id is not None])
        api_tags = await self.api_tag_repository.fetch_all_by_ids([access.api_tag_id for access in accesses if access.api_tag_id is not None])
        accesses_result = []
        for access in accesses:
            if access.api_tag_id is not None:
                for tag in api_tags:
                    if tag.id == access.api_tag_id:
                        accesses_result.append(
                            ApiKeyAccessSchema(
                                api_tag_id=tag.id,
                                api_name=tag.name
                            )
                        )
                        break
            if access.api_id is not None:
                for api in apis:
                    if api.id == access.api_id:
                        accesses_result.append(
                            ApiKeyAccessSchema(
                                api_id=api.id,
                                api_name=api.name,
                                api_url=api.url,
                                api_tags=api.tags,
                                api_methods=api.methods,
                                access_methods=access.methods,
                            )
                        )
                        break
        api_key.accesses = accesses_result
        return api_key

    async def get_api_key_for_user(self, user_id: str) -> ApiKeySchema:
        api_key = await self._get_or_create_api_key(user_id)
        return await self._aggregate_api_key_schema(api_key)

    async def _get_or_create_api_key(self, user_id: str) -> ApiKeySchema:
        api_key = await self.api_key_repository.get_by_user_id(user_id)
        if api_key is None:
            api_key = await self.api_key_repository.create(
                ApiKeyEntity(
                    user_id=user_id,
                    name=user_id,
                )
            )
        return api_key.convert_to_schema()

    async def create_api_accesses(self, data_in: ListCreateApiKeyAccessSchema) -> ApiKeySchema:
        api_key = await self._get_or_create_api_key(data_in.user_id)
        for api in data_in.apis:
            api_key_access = await self.api_key_access_repository.get_by_api_id_and_api_key_id(
                api.api_id, api_key.id
            )
            if api_key_access is None:
                api_key_access = await self.api_key_access_repository.create(
                    ApiKeyAccessEntity(
                        api_key_id=api_key.id,
                        api_id=api.api_id,
                        methods=[],
                    )
                )
            for method in api.methods:
                if method not in api_key_access.methods:
                    api_key_access.methods.append(method)
        for tag in data_in.tags:
            api_key_access = await self.api_key_access_repository.get_by_api_tag_id_and_api_key_id(
                tag.api_tag_id, api_key.id
            )
            if api_key_access is None:
                api_key_access = await self.api_key_access_repository.create(
                    ApiKeyAccessEntity(
                        api_key_id=api_key.id,
                        api_tag_id=tag.api_tag_id,
                        methods=[],
                    )
                )
            await self.api_key_access_repository.update(api_key_access)
        return await self._aggregate_api_key_schema(api_key)

    async def api_key_has_access(self, url: str, method: HTTPMethodEnum, user_id: str) -> bool:
        api = await self.api_repository.get_api_by_url(url)
        if api is None:
            api = await self.api_repository.get_api_by_url("/".join(url.split("/")[:-1]))
        api_key = await self.api_key_repository.get_by_user_id(user_id)
        if api is None or api_key is None:
            return False

        api_key_access = await self.api_key_access_repository.get_by_api_id_and_api_key_id(
            api.id, api_key.id
        )
        if api_key_access is None:
            api_key_accesses = await self.api_key_access_repository.get_by_api_key_id_and_tag_not_null(api_key.id)
            for api_key_access in api_key_accesses:
                if api_key_access.api_tag_id in api.tags:
                    return True
            return False

        return method.value in api_key_access.methods or api_key_access.api_tag_id in api.tags

    async def update_api_access(self, data_in: ListCreateApiKeyAccessSchema) -> None:
        api_key = await self._get_or_create_api_key(data_in.user_id)
        await self.api_key_access_repository.delete_all_by_api_key_id(api_key.id)
        await self.create_api_accesses(data_in)
        return None

