from common.account.enum.auth_action_enum import AuthActionEnum
from common.account.enum.user_group_enum import UserGroupEnum
from ...abstract_rule_definition import AbstractAccessRuleDefinition
from ...schema import ActionEnum


class MyRequestsRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.form_manager__form_system__my_requests
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []
    # module = "aml"
    # sub_module = "myRequests"
    # auth_action = AuthActionEnum.READ

class ManageRequestReadRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.form_manager__form_system__manage_requests_read
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []
    # module = "aml"
    # sub_module = "manageRequests"
    # auth_action = AuthActionEnum.READ

class ManageRequestCreateRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.form_manager__form_system__manage_requests_create
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []
    # module = "aml"
    # sub_module = "manageRequests"
    # auth_action = AuthActionEnum.CREATE

class FormReadRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.form_manager__form_system__form_read
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []
    # module = "aml"
    # sub_module = "formsList"
    # auth_action = AuthActionEnum.READ

class FormCreateRuleDefinition(AbstractAccessRuleDefinition):
    action = ActionEnum.form_manager__form_system__form_create
    authorized_groups = [UserGroupEnum.admin]
    authorized_admin_roles = ['__all__']
    restricted_statuses = []
    # module = "aml"
    # sub_module = "formList"
    # auth_action = AuthActionEnum.CREATE


access_rule_definitions = [
    MyRequestsRuleDefinition,
    ManageRequestReadRuleDefinition,
    ManageRequestCreateRuleDefinition,
    FormReadRuleDefinition,
    FormCreateRuleDefinition,
]
