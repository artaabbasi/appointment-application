from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.role_schema import RoleSchema
from common.account.schema.user_permission_schema import UserPermissionSchema
from common.settings import get_settings
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.entity.user_entity import UserEntity
from module.account.user.entity.staff_entity import StaffEntity

settings = get_settings()


class ApiKeyUserSchema(BaseModel):
    id: str = None
    phone_number: Optional[str]
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    national_code: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    group: UserGroupEnum
    role: List = []
    last_login_at: Optional[datetime] = None


    @staticmethod
    def load_from_entity(user_entity: UserEntity,
                         profile_entity: ProfileEntity) -> 'ApiKeyUserSchema':

        return ApiKeyUserSchema(
            id=user_entity.id,
            phone_number=profile_entity.phone_number,
            username=user_entity.username,
            email=profile_entity.email,
            first_name=profile_entity.first_name,
            last_name=profile_entity.last_name,
            national_code=profile_entity.national_code,
            avatar=user_entity.avatar,
            is_active=user_entity.is_active if user_entity.is_active is not None else False,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
            group=user_entity.group,
            last_login_at=user_entity.last_login_at,
        )
