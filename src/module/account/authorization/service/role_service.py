import asyncio
from typing import List, Union

from common.account.schema._permission_schema import _PermissionSchema
from common.account.schema.permission_schema import PermissionSchema
from common.account.schema.role_in_schema import RoleInSchema
from common.account.schema.role_permission_delete_schema import RolePermissionDeleteSchema
from common.account.schema.role_permission_in_schema import RolePermissionInSchema
from common.account.schema.role_permission_schema import RolePermissionSchema
from common.account.schema.role_schema import RoleSchema
from common.account.schema.user_permission_delete_schema import UserPermissionDeleteSchema
from common.account.schema.user_permission_in_schema import UserPermissionInSchema
from common.lib.base_crud_service import BaseCRUDService
from common.lib.service_action_enum import ServiceActionEnum
from module.account.authorization.entity.role_entity import RoleEntity
from module.account.authorization.entity.role_permission_entity import RolePermissionEntity
from module.account.authorization.entity.user_role_entity import UserRoleEntity
from module.account.authorization.repository.role_permission_repository import RolePermissionRepository
from module.account.authorization.repository.role_repository import RoleRepository
from module.account.authorization.repository.user_role_repository import UserRoleRepository
from module.account.authorization.service.permission_service import PermissionService
from module.account.authorization.service.user_permission_service import UserPermissionService


class RoleService(BaseCRUDService):
    def __init__(self):
        super().__init__(RoleRepository, RoleEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.user_role_repository = UserRoleRepository()
        self.role_permission_repository = RolePermissionRepository()
        self.user_permission_service = UserPermissionService()
        self.permission_service = PermissionService()

    async def _aggregate_schema(self, schema: Union[RoleSchema, list[RoleSchema], any]):
        if not schema:
            return schema
        if isinstance(schema, list):
            schema = await asyncio.gather(
                *[
                    self._aggregate_schema(item) for item in schema
                ]
            )
        else:
            permissions = await self.get_role_permissions(schema.id)
            schema.permissions = permissions
            users = await self.get_user_ids_by_role_id(schema.id)
            schema.person_count = len(users)
        return schema

    async def get_role_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None,) \
            -> list[RoleSchema]:
        if not filters:
            filters = {}
        roles = await self.repository.fetch_paginated_list_by_filters(page, size, filters, search)
        return await self._aggregate_schema([role.convert_to_schema() for role in roles])

    async def get_by_id(self, role_id: str) -> RoleSchema:
        role = await self.repository.fetch_by_id(role_id)
        return await self._aggregate_schema(role.convert_to_schema())

    async def get_not_detailed_by_id(self, role_id: str) -> RoleSchema:
        role = await self.repository.fetch_by_id(role_id)
        return role.convert_to_schema()

    async def get_by_ids(self, role_ids: List[str]) -> List[RoleSchema]:
        roles = await self.repository.fetch_all_by_ids(role_ids)
        return [role.convert_to_schema() for role in roles]

    async def get_roles_by_name(self, name: str) -> List[RoleSchema]:
        roles = await self.repository.fetch_by_name(name)
        return [role.convert_to_schema() for role in roles]

    async def update_role(self, entity_id: str, schema: RoleInSchema) -> RoleSchema:
        role = await self._update_by_id(schema, entity_id, is_partial=True)
        return role.convert_to_schema()

    async def delete_role(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_role(self, data_in: RoleInSchema) -> RoleSchema:
        role = await self.repository.create(
            RoleEntity(
                name=data_in.name,
                title=data_in.title,
                show_in_site=data_in.show_in_site
            )
        )
        return role.convert_to_schema()

    async def get_user_roles(self, user_id: str) -> list[RoleSchema]:
        user_roles = await self.user_role_repository.fetch_by_user_id(user_id)
        roles = await self.repository.fetch_all_by_ids([user_role.role_id for user_role in user_roles])
        return [role.convert_to_schema() for role in roles]

    async def get_user_ids_by_role_id(self, role_id: str) -> list[str]:
        user_roles = await self.user_role_repository.fetch_by_role_id(role_id)
        return [user_role.user_id for user_role in user_roles]

    async def create_role_for_user(self, user_id: str, role_id: str) -> None:
        user_role = await self.user_role_repository.fetch_by_role_id_and_user_id(role_id, user_id)
        if user_role is None:
            await self.user_role_repository.create(
                UserRoleEntity(
                    user_id=user_id,
                    role_id=role_id
                )
            )
            permissions = await self.get_role_permissions(role_id)
            await asyncio.gather(
                *[self.user_permission_service.create_user_permission(
                    UserPermissionInSchema(
                        users=[user_id],
                        permissions=[
                            _PermissionSchema(id=permission.id, had_access_to_all=permission.had_access_to_all) for permission in permissions
                        ],
                        reset=False
                    )
                )]
            )
        return None

    async def create_roles_for_users(self, user_ids: list[str], role_ids: list[str]) -> None:
        for user_id in user_ids:
            await self.user_role_repository.delete_by_user_id(user_id)
            for role_id in role_ids:
                await self.create_role_for_user(user_id, role_id)

    async def add_roles_to_users(self, user_ids: list[str], role_ids: list[str]) -> None:
        for user_id in user_ids:
            for role_id in role_ids:
                await self.create_role_for_user(user_id, role_id)

    async def delete_role_for_user(self, user_id: str, role_id: str) -> None:
        user_role = await self.user_role_repository.fetch_by_role_id_and_user_id(role_id, user_id)
        permissions = await self.get_role_permissions(role_id)
        await asyncio.gather(
            *[self.user_permission_service.delete_user_permission(
                UserPermissionDeleteSchema(
                    users=[user_id],
                    permissions=[permission.id for permission in permissions]
                )
            )]
        )
        await self.user_role_repository.delete(user_role)
        return None

    async def delete_roles_for_users(self, user_ids: list[str], role_ids: list[str]) -> None:
        for user_id in user_ids:
            for role_id in role_ids:
                await self.delete_role_for_user(user_id, role_id)

    async def get_role_permissions(self, role_id: str) -> list[RolePermissionSchema]:
        role_permissions = await self.role_permission_repository.fetch_by_role_id(role_id)
        permissions = await self.permission_service.get_permission_by_ids(
            [role_permission.permission_id for role_permission in role_permissions])
        role_permission_result = []
        for role_permission in role_permissions:
            for permission in permissions:
                if permission.id == role_permission.permission_id:
                    break
            else:
                continue
            role_permission_result.append(
                RolePermissionSchema(
                    id=permission.id,
                    module=permission.module,
                    sub_module=permission.sub_module,
                    action=permission.action,
                    had_access_to_all=role_permission.had_access_to_all,
                )
            )
        return role_permission_result

    async def create_role_permission(self,  data_in: RolePermissionInSchema) -> None:
        for role in set(data_in.roles):
            role_permissions = await self.role_permission_repository.fetch_by_role_id(role)
            await self.delete_role_permission(
                RolePermissionDeleteSchema(
                    roles=[role],
                    permissions=[role_perm.permission_id
                                 for role_perm in role_permissions if role_perm.permission_id not in data_in.permissions],
                    add_to_users=data_in.add_to_users
                )
            )

        for permission in data_in.permissions:
            for role in data_in.roles:
                await self.role_permission_repository.create(
                    RolePermissionEntity(
                        role_id=role,
                        permission_id=permission.id,
                        had_access_to_all=permission.had_access_to_all,
                    )
                )
        if data_in.add_to_users:
            user_ids = []
            for role in data_in.roles:
                user_ids.extend([user.user_id for user in await self.user_role_repository.fetch_by_role_id(role)])
            await asyncio.gather(
                *[self.user_permission_service.create_user_permission(
                    UserPermissionInSchema(
                        users=user_ids,
                        permissions=data_in.permissions,
                        reset=False
                    )
                )]
            )
        return

    async def delete_role_permission(self,  data_in: RolePermissionDeleteSchema) -> None:
        entities = await asyncio.gather(*[
            self.role_permission_repository.fetch_by_role_id_and_permission_id(role_id, permission_id)
            for permission_id in data_in.permissions for role_id in data_in.roles
        ])
        await asyncio.gather(*[self.role_permission_repository.delete(entity) for entity in entities])
        if data_in.add_to_users:
            users = []
            for role in data_in.roles:
                users.extend(await self.user_role_repository.fetch_by_role_id(role))
            await asyncio.gather(
                *[self.user_permission_service.delete_user_permission(
                    UserPermissionDeleteSchema(
                        users=[user.user_id for user in users],
                        permissions=data_in.permissions
                    )
                )]
            )
        return

    async def delete_user_roles_by_not_user_ids(self, user_ids: List[str]) -> None:
        await self.user_role_repository.delete_by_not_user_ids(user_ids)
