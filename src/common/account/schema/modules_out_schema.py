from typing import Optional, List

from pydantic import BaseModel

from common.account.enum.auth_action_enum import AuthActionEnum


class ModulesOutSchema(BaseModel):
    name: str
    sub_modules: List['SubModulesOutSchema']


class SubModulesOutSchema(BaseModel):
    name: str
    sub_modules: List[str]
