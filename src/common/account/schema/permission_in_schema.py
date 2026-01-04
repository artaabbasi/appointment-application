from typing import Optional

from pydantic import BaseModel

from common.account.enum.auth_action_enum import AuthActionEnum


class PermissionInSchema(BaseModel):
    title: Optional[str] = None
    module: Optional[str] = None
    sub_module: Optional[str] = None
    action: Optional[AuthActionEnum] = None
