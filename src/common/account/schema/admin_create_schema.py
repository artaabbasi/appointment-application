from typing import Optional

from pydantic import BaseModel

from common.account.enum.admin_roles_enum import AdminRolesEnum


class AdminCreateSchema(BaseModel):
    phone_number: str
    first_name: Optional[str] = None
    en_first_name: Optional[str] = None
    last_name: Optional[str] = None
    en_last_name: Optional[str] = None
    national_code: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    avatar: Optional[str] = None
    username: str
    password: str
    role: AdminRolesEnum
    must_change_password: Optional[bool] = True
    has_completed_profile: Optional[bool] = False
    is_active: Optional[bool] = False

