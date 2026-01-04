from datetime import datetime

from pydantic import BaseModel, Field
from typing_extensions import TypeAlias
from typing import Union, List, Optional
from pydantic import EmailStr

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.account.enum.token_type_enum import TokenTypeEnum
from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.user_permission_schema import UserPermissionSchema


class AuthenticatedUserSchema(BaseModel):
    admin_id: Optional[str] = None
    user_id: Optional[str] = None
    token_type: TokenTypeEnum
    phone_number: str
    iat: datetime = None
    exp: datetime = None
    roles: List[Union[AdminRolesEnum]] = []
    permissions: Optional[List[UserPermissionSchema]] = []
    permission: Optional[UserPermissionSchema] = None
    group: UserGroupEnum
    customer_code: Optional[int] = None
    national_code: Optional[str] = None
    token: Optional[str] = None


