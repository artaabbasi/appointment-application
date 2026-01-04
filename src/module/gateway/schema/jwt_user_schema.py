from typing import Optional, List, Union

from pydantic import BaseModel, Field

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.user_permission_schema import UserPermissionSchema


class JWTUserSchema(BaseModel):
    raw_jwt: str
    user_id: str = None
    admin_id: str = None
    group: UserGroupEnum
    roles: List[Union[AdminRolesEnum]] = []
    phone_number: str
    national_code: Optional[str] = None
    customer_code: Optional[int] = None
    expert_code: Optional[int] = None
    marketer_code: Optional[int] = None
    agent_code: Optional[int] = None
    branch_code: Optional[int] = None
    token: Optional[str] = None
    permission: Optional[UserPermissionSchema] = None

    def is_admin(self):
        if self.group == UserGroupEnum.admin:
            return True
        return False
