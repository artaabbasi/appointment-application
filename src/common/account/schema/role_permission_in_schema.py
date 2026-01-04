from typing import List, Optional

from pydantic import BaseModel

from common.account.schema._permission_schema import _PermissionSchema


class RolePermissionInSchema(BaseModel):
    roles: List[str]
    permissions: List[_PermissionSchema]
    add_to_users: Optional[bool] = False
