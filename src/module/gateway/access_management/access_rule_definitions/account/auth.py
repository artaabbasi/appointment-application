from common.account.enum.user_group_enum import UserGroupEnum
from ...abstract_rule_definition import AbstractAccessRuleDefinition
from ...schema import ActionEnum


class RefreshTokenAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__auth__refresh_token
    authorized_groups = ['__all__']
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


class UpdateProfileAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__customers__verify_profile
    authorized_groups = [UserGroupEnum.customer]
    authorized_admin_roles = []
    restricted_statuses = []


class GetCurrentUserInfoAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__customers__user_info
    authorized_groups = [UserGroupEnum.customer, UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


access_rule_definitions = [
    RefreshTokenAccessRuleDefinition,
    UpdateProfileAccessRuleDefinition,
    GetCurrentUserInfoAccessRuleDefinition,
]
