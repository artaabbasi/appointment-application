from common.account.enum.user_group_enum import UserGroupEnum
from ...abstract_rule_definition import AbstractAccessRuleDefinition
from ...schema import ActionEnum


class AllAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.all_access
    authorized_groups = ['__all__']
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


class CustomerAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.customer_access
    authorized_groups = [UserGroupEnum.customer]
    authorized_admin_roles = []
    restricted_statuses = []


class AdminAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.admin_access
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []

access_rule_definitions = [
    AllAccessRuleDefinition,
    CustomerAccessRuleDefinition,
    AdminAccessRuleDefinition,
]
