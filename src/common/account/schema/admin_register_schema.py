from typing import Optional

from pydantic import BaseModel

from common.account.enum.admin_roles_enum import AdminRolesEnum


class AdminRegisterSchema(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    en_first_name: Optional[str] = None
    last_name: Optional[str] = None
    en_last_name: Optional[str] = None
    national_code: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    avatar: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[AdminRolesEnum] = None
    must_change_password: Optional[bool] = None
    has_completed_profile: Optional[bool] = None
    is_active: Optional[bool] = None
