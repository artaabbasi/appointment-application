from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from common.account.enum.user_group_enum import UserGroupEnum
from common.settings import get_settings
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.entity.user_entity import UserEntity

settings = get_settings()


class CustomerUserSchema(BaseModel):
    id: str = None
    phone_number: Optional[str]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    national_code: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    group: UserGroupEnum
    last_login_at: Optional[datetime] = None
    birth_date: Optional[str] = None
    avatar: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name if self.first_name is not None else ''} {self.last_name if self.last_name is not None  else ''}" \
            if self.last_name and self.first_name else '-'

    @staticmethod
    def load_from_entity(user_entity: UserEntity, profile_entity: ProfileEntity):
        return CustomerUserSchema(
            id=user_entity.id,
            phone_number=profile_entity.phone_number,
            first_name=profile_entity.first_name,
            last_name=profile_entity.last_name,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
            group=user_entity.group,
            avatar=user_entity.avatar,
            last_login_at=user_entity.last_login_at,
            national_code=profile_entity.national_code,
            birth_date=profile_entity.birth_date,
        )
