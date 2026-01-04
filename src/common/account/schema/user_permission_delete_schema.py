from typing import List, Optional

from pydantic import BaseModel


class UserPermissionDeleteSchema(BaseModel):
    users: List[str]
    permissions: List[str]
