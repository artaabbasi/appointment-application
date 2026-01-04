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

    insurance__policy__refresh = auto()
    insurance__policy__list = auto()
    insurance__policy__detail = auto()
    insurance__policy__update = auto()
    insurance__policy__delete = auto()

    insurance__car__croquie__create = auto()
    insurance__life__increase__create = auto()
    insurance__life__print__create = auto()

    financial__admin_wallet__balance = auto()

    financial__wallet__balance = auto()
    financial__wallet__charge = auto()
    financial__order__list = auto()
    financial__admin__order__list = auto()

    insurance__admins__create = auto()
    insurance__admins__detail = auto()
    insurance__admins__list = auto()
    insurance__admins__update = auto()
    insurance__admins__delete = auto()

    insurance__customer__create = auto()

    financial_market__symbol__list = auto()
    financial_market__symbol__update = auto()

    file_manager__upload = auto()

    application_manager__customer__list = auto()
    application_manager__customer__create = auto()

    application_manager__admin__application__detail = auto()
    application_manager__admin__application__delete = auto()
    application_manager__admin__list = auto()
    application_manager__admin__letters__list = auto()
    application_manager__admin__response__create = auto()

    application_manager__admin__user_group__create = auto()
    application_manager__admin__user_group__read = auto()
    application_manager__admin__user_group__update = auto()
    application_manager__admin__user_group__delete = auto()

    survey__admin__manage__create = auto()
    survey__admin__report__create = auto()
    survey__customer__response = auto()

    ins__inquiry__croquie = auto()
    ins__inquiry__vekalat = auto()
    ins__inquiry__amlak_eskan = auto()
    ins__inquiry__car = auto()

    insurance__car__ikco_system__get = auto()

    warehouse__eis__equipment = auto()
    warehouse__eis__equipment_category = auto()

    legal_core__legal_document__get = auto()
    legal_core__legal_document__post = auto()
    legal_core__legal_document_type__get = auto()
    legal_core__legal_document_type__post = auto()

    car__arrears_report__read = auto()

    insurance__third_party__issuance = auto()

    insurance__car_damages__claim__create = auto()
    insurance__car_damages__body_claim__create = auto()
    insurance__car_damages__third_party_claim__create = auto()

    form_manager__form_system__my_requests = auto()
    form_manager__form_system__manage_requests_read = auto()
    form_manager__form_system__manage_requests_create = auto()
    form_manager__form_system__form_read = auto()
    form_manager__form_system__form_create = auto()


    report__admin_dashboard__read = auto()
    report__branch_dashboard__read = auto()
    report__type_dashboard__read = auto()
