from enum import Enum, auto


class RestrictionEnum(str, Enum):
    blocked_user = 'blocked_user'  # TODO, we should check if we want to have block service or not!


class ActionEnum(str, Enum):
    """
    List of all available actions in the system, This will be used by the access_management_service

    Stick to the naming convention `module_name__service_name__action_name`
    """
    # Account actions
    # account__auth__customer_login = auto()
    # account__auth__admin_login = auto()
    account__auth__refresh_token = auto()

    account__customers__verify_profile = auto()
    account__customers__user_info = auto()

    account__customers__list = auto()
    account__customers__detail = auto()
    account__customers__delete = auto()
    account__customers__update_profile = auto()
    account__customers__change_email = auto()
    account__customers__remove_unverified_email = auto()
    account__customers__send_reset_password = auto()
    account__customers__suspend = auto()
    account__customers__unsuspend = auto()
    account__customers__activate = auto()
    account__customers__deactivate = auto()
    account__customers__add_note = auto()

    account__admins__create = auto()
    account__admins__detail = auto()
    account__admins__list = auto()
    account__admins__update = auto()
    account__admins__delete = auto()
    account__admins__user_info = auto()

    account__admins__permissions__get = auto()
    account__admins__permissions__create = auto()
    account__admins__permissions__detail = auto()
    account__admins__permissions__module__get = auto()

    file_manager__upload = auto()


    all_access = auto()
    customer_access = auto()
    admin_access = auto()
