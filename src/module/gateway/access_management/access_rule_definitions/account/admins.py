from common.account.enum.user_group_enum import UserGroupEnum
from ...abstract_rule_definition import AbstractAccessRuleDefinition
from ...schema import ActionEnum
from common.account.enum.admin_roles_enum import AdminRolesEnum


class CreateAdminAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__create
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.owner_admin, AdminRolesEnum.admin]
    restricted_statuses = []


class GetAdminAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__detail
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.owner_admin, AdminRolesEnum.admin]
    restricted_statuses = []


class ListAdminAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__list
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


class UpdateAdminAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__update
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.owner_admin, AdminRolesEnum.admin]
    restricted_statuses = []


class DeleteAdminAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__delete
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.owner_admin, AdminRolesEnum.admin]
    restricted_statuses = []


class GetPermissionAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__permissions__get
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.owner_admin, AdminRolesEnum.admin]
    restricted_statuses = []


class CreatePermissionAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__permissions__create
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.owner_admin, AdminRolesEnum.admin]
    restricted_statuses = []


class DetailPermissionAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__permissions__detail
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = [AdminRolesEnum.owner_admin, AdminRolesEnum.admin]
    restricted_statuses = []


class AdminModulesAccessRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__permissions__module__get
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


class AdminUserInfoRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.account__admins__user_info
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


access_rule_definitions = [
    CreateAdminAccessRuleDefinition,
    GetAdminAccessRuleDefinition,
    ListAdminAccessRuleDefinition,
    UpdateAdminAccessRuleDefinition,
    DeleteAdminAccessRuleDefinition,
    AdminUserInfoRuleDefinition,
    GetPermissionAccessRuleDefinition,
    CreatePermissionAccessRuleDefinition,
    DetailPermissionAccessRuleDefinition,
    AdminModulesAccessRuleDefinition,
]
