from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from common.lib.base_respository import BaseRepository
from database.setup import get_session
from ..entity.staff_entity import StaffEntity


class StaffRepository(BaseRepository):
    def __init__(self):
        super().__init__(StaffEntity)

    @staticmethod
    async def fetch_by_user_id(user_id: str) -> Optional[StaffEntity]:
        try:
            async with get_session() as session:
                result = await session.execute(select(StaffEntity).
                                               filter(StaffEntity.user_id == user_id)
                                               )
            return result.scalars().one()
        except NoResultFound:
            return None
