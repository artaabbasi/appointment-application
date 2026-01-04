import asyncio

from common.account.schema.modules_out_schema import ModulesOutSchema, SubModulesOutSchema
from common.account.schema.user_permission_delete_schema import UserPermissionDeleteSchema
from common.account.schema.user_permission_in_schema import UserPermissionInSchema
from common.account.schema.user_permission_schema import UserPermissionSchema
from common.lib.base_service import BaseService
from module.account.authorization.entity.user_permission_entity import UserPermissionEntity
from module.account.authorization.repository.permission_repository import PermissionRepository
from module.account.authorization.repository.user_permission_repository import UserPermissionRepository


class UserPermissionService(BaseService):

    def __init__(self):
        self.repository = UserPermissionRepository()
        self.permission_repository = PermissionRepository()

    async def get_permission_ids_by_user(self, user_id: str) -> list[str]:
        user_permissions = await self.repository.fetch_by_user_id(user_id)
        return [user_permission.permission_id for user_permission in user_permissions]

    async def delete_user_permission(self, data_in: UserPermissionDeleteSchema) -> None:
        entities = []
        for user in data_in.users:
            entities.extend(await asyncio.gather(*[
                self.repository.delete_by_user_id_and_permission_id(user, permission_id)
                for permission_id in data_in.permissions
            ]))
        return

    async def create_user_permission(self, data_in: UserPermissionInSchema) -> None:
        if data_in.reset:
            for user in set(data_in.users):
                user_permissions = await self.repository.fetch_by_user_id(user)
                await asyncio.gather(*[self.repository.delete(entity) for entity in user_permissions])
        user_permissions = []
        for permission in data_in.permissions:
            for user in data_in.users:
                user_permissions.append(UserPermissionEntity(
                        user_id=user,
                        permission_id=permission.id,
                        had_access_to_all=permission.had_access_to_all,
                    ))
        await self.repository.batch_create(user_permissions)
        return

    async def get_user_ids_by_permission_id(self, permission_id: str) -> list[str]:
        user_permissions = await self.repository.fetch_by_permission_id(permission_id)
        return [user_permission.user_id for user_permission in user_permissions]

    async def has_all_access(self, user_id: str, permission_id: str) -> bool:
        user_permission = await self.repository.fetch_by_user_id_and_permission_id(user_id, permission_id)
        return user_permission.had_access_to_all

    async def get_user_permissions(self, user_id: str) -> list[UserPermissionSchema]:
        user_permissions = await self.repository.fetch_by_user_id(user_id)
        permissions = await self.permission_repository.fetch_all_by_ids(
            [user_permission.permission_id for user_permission in user_permissions])
        user_permission_result = []
        for user_permission in user_permissions:
            for permission in permissions:
                if permission.id == user_permission.permission_id:
                    break
            else:
                continue
            user_permission_result.append(
                UserPermissionSchema(
                    id=permission.id,
                    module=permission.module,
                    sub_module=permission.sub_module,
                    action=permission.action,
                    had_access_to_all=user_permission.had_access_to_all,
                )
            )
        return user_permission_result

    async def get_user_permissions_tree(self, user_id: str) -> list[ModulesOutSchema]:
        permissions = await self.get_user_permissions(user_id)
        base_tree = dict()
        for permission in permissions:
            module_node = base_tree.get(permission.module, dict())
            if permission.sub_module is not None:
                sub_sub_module_name = None
                sub_module_names = permission.sub_module.split('-')
                sub_module_name = sub_module_names[0]
                try:
                    sub_sub_module_name = sub_module_names[1]
                except IndexError:
                    pass
                sub_module_node = module_node.get(sub_module_name, dict())
                if sub_sub_module_name is not None:
                    sub_sub_module_list = sub_module_node.get('sub_sub_module_list', set())
                    sub_sub_module_list.add(sub_sub_module_name)
                    sub_module_node['sub_sub_module_list'] = sub_sub_module_list
                module_node[sub_module_name] = sub_module_node

            base_tree[permission.module] = module_node
        modules = []
        for name, node in base_tree.items():
            module = ModulesOutSchema(name=name, sub_modules=[])
            for name_, sub_node in node.items():
                sub_module = SubModulesOutSchema(name=name_, sub_modules=sub_node.get('sub_sub_module_list', []))
                module.sub_modules.append(sub_module)
            modules.append(module)
        return modules
