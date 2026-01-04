from pydantic import BaseModel

from common.account.enum.auth_action_enum import AuthActionEnum


class UserPermissionSchema(BaseModel):
    id: str
    module: str
    sub_module: str
    action: AuthActionEnum
    had_access_to_all: bool
