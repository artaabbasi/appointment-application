from typing import Optional
from pydantic import BaseModel

from common.account.enum.auth_action_enum import AuthActionEnum


class PermissionSchema(BaseModel):
    id: str
    title: Optional[str] = None
    module: str
    sub_module: str
    action: AuthActionEnum
