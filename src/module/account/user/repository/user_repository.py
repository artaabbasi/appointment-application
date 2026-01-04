from typing import Optional

from sqlalchemy import select, Select, or_, cast, String, and_, func
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.date_filter_enum import DateFilterEnum
from ..entity.user_entity import UserEntity

from database.setup import get_session
from common.account.enum.user_group_enum import UserGroupEnum
from ..enum.user_service_error_code_enum import UserServiceErrorCodeEnum


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserEntity,
                         filter_fields=[UserEntity.group],
                         date_filters={
                                "created_from": (DateFilterEnum.FROM, UserEntity.created_at),
                                "created_to": (DateFilterEnum.TO, UserEntity.created_at),
                            },
                         order_by=[UserEntity.created_at.desc()]
                         )

    @staticmethod
    async def fetch_by_group_and_profile_id(group: UserGroupEnum, profile_id: str) -> Optional[UserEntity]:
        try:
            async with get_session() as session:
                result = await session.execute(select(UserEntity).
                                               filter(UserEntity.group == group).
                                               filter(UserEntity.profile_id == profile_id)
                                               )
            return result.scalars().one()
        except NoResultFound:
            return None

    @staticmethod
    async def fetch_by_group_and_username(group: UserGroupEnum, username: str) -> UserEntity:
        try:
            async with get_session() as session:
                result = await session.execute(select(UserEntity).
                                               filter(UserEntity.group == group).
                                               filter(UserEntity.username == username)
                                               )
            return result.scalars().one()
        except NoResultFound:
            raise NotFoundException(code=UserServiceErrorCodeEnum.USER_NOT_FOUND)
