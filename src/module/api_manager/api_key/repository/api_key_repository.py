from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from typing_extensions import Optional
from common.lib.base_respository import BaseRepository
from database.setup import get_session
from module.api_manager.api_key.entity.api_key_entity import ApiKeyEntity


class ApiKeyRepository(BaseRepository):
    def __init__(self):
        super().__init__(ApiKeyEntity)

    async def get_by_user_id(self, user_id: str) -> Optional[ApiKeyEntity]:
        q = select(ApiKeyEntity)
        q = q.filter(ApiKeyEntity.user_id == user_id)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            entity = None
        return entity
