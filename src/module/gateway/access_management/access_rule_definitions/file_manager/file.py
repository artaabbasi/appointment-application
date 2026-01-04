from common.account.enum.user_group_enum import UserGroupEnum
from ...abstract_rule_definition import AbstractAccessRuleDefinition
from ...schema import ActionEnum


class FileUploadRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.file_manager__upload
    authorized_groups = ['__all__']
    authorized_admin_roles = ['__all__']
    restricted_statuses = []


access_rule_definitions = [
    FileUploadRuleDefinition
]

