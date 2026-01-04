from typing import List, Optional

from pydantic import BaseModel

from common.account.schema._permission_schema import _PermissionSchema


class UserPermissionInSchema(BaseModel):
    users: List[str]
    permissions: List[_PermissionSchema]
    reset: Optional[bool] = True
