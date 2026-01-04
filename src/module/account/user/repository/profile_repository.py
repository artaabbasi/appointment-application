from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from common.lib.base_respository import BaseRepository
from ..entity.profile_entity import ProfileEntity
from database.setup import get_session


class ProfileRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProfileEntity)

    @staticmethod
    async def fetch_by_phone_number(phone_number: str) -> List[ProfileEntity]:
        try:
            async with get_session() as session:
                result = await session.execute(select(ProfileEntity).
                                               filter(ProfileEntity.phone_number == phone_number))
            return result.scalars().all()
        except NoResultFound:
            return []

    @staticmethod
    async def fetch_by_national_code(national_code: str) -> List[ProfileEntity]:
        try:
            async with get_session() as session:
                result = await session.execute(select(ProfileEntity).
                                               filter(ProfileEntity.national_code == national_code))
            return result.scalars().all()
        except NoResultFound:
            return []
