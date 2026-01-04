from typing import Optional, List

from pydantic import BaseModel

from common.account.schema.role_permission_schema import RolePermissionSchema


class RoleSchema(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    show_in_site: Optional[bool] = None
    permissions: Optional[List[RolePermissionSchema]] = []
    person_count: Optional[int] = 0

