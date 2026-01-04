from typing import Optional

from pydantic import BaseModel

from common.account.enum.admin_roles_enum import AdminRolesEnum


class ApiKeyUserCreateSchema(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    avatar: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    national_code: Optional[str] = None
    is_active: Optional[bool] = None
