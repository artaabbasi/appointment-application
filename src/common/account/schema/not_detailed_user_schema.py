from typing import Optional
from pydantic import BaseModel

from common.account.enum.user_group_enum import UserGroupEnum
from common.settings import get_settings
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.entity.user_entity import UserEntity

settings = get_settings()


class NotDetailedUserSchema(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    en_first_name: Optional[str] = None
    last_name: Optional[str] = None
    en_last_name: Optional[str] = None
    national_code: Optional[str] = None
    birth_date: Optional[str] = None
    group: Optional[UserGroupEnum] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def load_from_entity(user_entity: UserEntity, profile_entity: ProfileEntity) -> 'NotDetailedUserSchema':
        return NotDetailedUserSchema(
            id=user_entity.id,
            username=user_entity.username,
            phone_number=profile_entity.phone_number,
            first_name=profile_entity.first_name,
            en_first_name=profile_entity.en_first_name,
            last_name=profile_entity.last_name,
            en_last_name=profile_entity.en_last_name,
            national_code=profile_entity.national_code,
            birth_date=profile_entity.birth_date,
            group=user_entity.group
        )