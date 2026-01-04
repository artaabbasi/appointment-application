from common.account.schema.permission_in_schema import PermissionInSchema
from common.account.schema.modules_out_schema import ModulesOutSchema, SubModulesOutSchema
from common.account.schema.permission_schema import PermissionSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.account.authorization.entity.permission_entity import PermissionEntity
from module.account.authorization.repository.permission_repository import PermissionRepository
from module.account.authorization.service.user_permission_service import UserPermissionService


class PermissionService(BaseCRUDService):

    def __init__(self):
        super().__init__(PermissionRepository, PermissionEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.user_permission_service = UserPermissionService()

    async def get_permission_list(self, page: int = 1, size: int = 10, filters: dict = None) \
            -> list[PermissionSchema]:
        if not filters:
            filters = {}
        permissions = await self.repository.fetch_paginated_list_by_filters(page, size, filters)
        return [permission.convert_to_schema() for permission in permissions]

    async def update_permission(self, entity_id: str, schema: PermissionInSchema) -> PermissionSchema:
        permission = await self._update_by_id(schema, entity_id, is_partial=True)
        return permission.convert_to_schema()

    async def delete_permission(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_permission(self, data_in: PermissionInSchema) -> PermissionSchema:
        permission = await self.repository.create(
            PermissionEntity(
                title=data_in.title,
                module=data_in.module,
                sub_module=data_in.sub_module,
                action=data_in.action
            )
        )
        return permission.convert_to_schema()



    async def get_permission_by_ids(self, permission_ids: list[str]) -> list[PermissionSchema]:
        permissions = await self.repository.fetch_all_by_ids(permission_ids)
        return [permission.convert_to_schema() for permission in permissions]
