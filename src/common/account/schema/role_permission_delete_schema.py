from typing import List, Optional

from pydantic import BaseModel


class RolePermissionDeleteSchema(BaseModel):
    roles: List[str]
    permissions: List[str]
    add_to_users: Optional[bool] = False
