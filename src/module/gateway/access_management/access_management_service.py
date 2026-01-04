from typing import Type, List, Union, Optional, Literal

from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.permission_schema import PermissionSchema
from common.account.schema.user_permission_schema import UserPermissionSchema
from .abstract_rule_definition import AbstractAccessRuleDefinition
from .abstract_registry import AbstractAccessRuleRegistry
from .registry import access_rule_definition_registry
from .schema import ActionEnum
from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.exceptions import (ForbiddenException)
from ..enum.error_code_enum import ErrorCodeEnum


class AccessManagementService:
    def __init__(self):
        self.registry: Type[AbstractAccessRuleRegistry] = access_rule_definition_registry

    def get_access_role_definition_by_action(self, action: ActionEnum) -> AbstractAccessRuleDefinition:
        return self.registry.get_access_rule_definition_by_action(action)

    def get_authorized_groups_for_action(self, action: ActionEnum) -> list[UserGroupEnum | Literal['__all__']]:
        res = self.get_access_role_definition_by_action(action)
        return res.authorized_groups

    def get_authorized_roles_for_action(self, action: ActionEnum) -> List[Union[str, AdminRolesEnum]]:
        roles = self.get_access_role_definition_by_action(action).authorized_admin_roles
        if '__all__' in roles:
            return [
                AdminRolesEnum.owner_admin,
                AdminRolesEnum.admin,
                AdminRolesEnum.full_read,
                AdminRolesEnum.supporter
            ]
        return roles

    def bulk_authorized_groups_in_order(self, actions: List[ActionEnum]) -> (
            list)[list[UserGroupEnum | Literal['__all__']]]:
        return [self.get_authorized_groups_for_action(action) for action in actions]

    def bulk_authorized_roles_in_order(self, actions: List[ActionEnum]) -> List[List[Union[str, AdminRolesEnum]]]:
        return [self.get_authorized_roles_for_action(action) for action in actions]

    def get_access_rules_for_action(self, action: ActionEnum) -> AbstractAccessRuleDefinition:
        rules = self.registry.get_access_rule_definition_by_action(action)
        assert rules, f'There was no access rule for action: {str(action)}'
        if '__all__' in rules.authorized_groups:
            rules.authorized_groups = [UserGroupEnum.admin, UserGroupEnum.customer, UserGroupEnum.api_key]
        if '__all__' in rules.authorized_admin_roles:
            rules.authorized_admin_roles = [
                AdminRolesEnum.owner_admin,
                AdminRolesEnum.admin,
                AdminRolesEnum.full_read,
                AdminRolesEnum.supporter
            ]
        return rules

    async def check_if_user_has_access_to_action(self,
                                                 current_user_id: str,
                                                 action: ActionEnum,
                                                 user_group: UserGroupEnum,
                                                 user_roles: Optional[List[Union[AdminRolesEnum]]],
                                                 permissions: Optional[List[UserPermissionSchema]]) -> Optional[UserPermissionSchema]:
        access_rule = self.get_access_rules_for_action(action)
        if user_group not in access_rule.authorized_groups:
            raise ForbiddenException(code=ErrorCodeEnum.ACCESS_DENIED)
        if (user_group == UserGroupEnum.admin and
                any(role not in access_rule.authorized_admin_roles for role in user_roles)):
            raise ForbiddenException(code=ErrorCodeEnum.ACCESS_DENIED)
        action_permission = None
        if (AdminRolesEnum.supporter in user_roles or AdminRolesEnum.full_read in user_roles) and type(access_rule.module) is str:
            has_access = False
            for permission in permissions:
                if permission.module == access_rule.module and permission.sub_module == access_rule.sub_module:
                    has_access = access_rule.auth_action == permission.action or has_access
                if has_access:
                    action_permission = permission
                    break
            if not has_access:
                raise ForbiddenException(code=ErrorCodeEnum.ACCESS_DENIED)
        return action_permission
        # if user_group != UserGroupEnum.admin:
        #     await self.check_user_restrictions(action, current_user_id)
