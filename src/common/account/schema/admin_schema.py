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


class AdminUserSchema(BaseModel):
    id: str = None
    phone_number: Optional[str]
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    en_first_name: Optional[str] = None
    last_name: Optional[str] = None
    en_last_name: Optional[str] = None
    national_code: Optional[str] = None
    avatar: Optional[str] = None
    must_change_password: Optional[bool] = None
    has_completed_profile: Optional[bool] = None
    is_active: Optional[bool] = None
    birth_date: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    group: UserGroupEnum
    role: Optional[AdminRolesEnum] = None
    permissions: Optional[List[UserPermissionSchema]] = []
    user_roles: Optional[List[RoleSchema]] = []
    last_login_at: Optional[datetime] = None

    @staticmethod
    def load_from_entity(user_entity: UserEntity,
                         profile_entity: ProfileEntity,
                         staff_entity: StaffEntity,
                         permissions: Optional[List[List[UserPermissionSchema]]] = None,
                         user_roles: Optional[List[RoleSchema]] = None) -> 'AdminUserSchema':

        return AdminUserSchema(
            id=user_entity.id,
            phone_number=profile_entity.phone_number,
            username=user_entity.username,
            email=profile_entity.email,
            en_first_name=profile_entity.en_first_name,
            first_name=profile_entity.first_name,
            last_name=profile_entity.last_name,
            en_last_name=profile_entity.en_last_name,
            national_code=profile_entity.national_code,
            avatar=user_entity.avatar,
            must_change_password=user_entity.must_change_password if user_entity.must_change_password is not None else True,
            has_completed_profile=user_entity.has_completed_profile if user_entity.has_completed_profile is not None else False,
            is_active=user_entity.is_active if user_entity.is_active is not None else False,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
            group=user_entity.group,
            role=getattr(staff_entity, "role", None),
            permissions=permissions,
            birth_date=profile_entity.birth_date,
            user_roles=user_roles,
            last_login_at=user_entity.last_login_at,
        )
