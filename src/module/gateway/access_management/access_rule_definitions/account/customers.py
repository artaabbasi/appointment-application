from common.account.enum.user_group_enum import UserGroupEnum
from ...abstract_rule_definition import AbstractAccessRuleDefinition
from ...schema import ActionEnum
from common.account.enum.admin_roles_enum import AdminRolesEnum


class GetCustomerListAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__customers__list
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


class GetCustomerDetailAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__customers__detail
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


class DeleteCustomerAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__customers__delete
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.admin,
                              AdminRolesEnum.owner_admin]
    restricted_statuses = []


class UpdateCustomerProfileAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__customers__update_profile
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.admin,
                              AdminRolesEnum.owner_admin]
    restricted_statuses = []


access_rule_definitions = [
    GetCustomerListAccessRuleDefinition,
    GetCustomerDetailAccessRuleDefinition,
    DeleteCustomerAccessRuleDefinition,
    UpdateCustomerProfileAccessRuleDefinition,
]
