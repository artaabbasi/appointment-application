from typing import Optional, List
from sqlalchemy import select, and_, Select
from sqlalchemy.exc import NoResultFound
from common.lib.base_respository import BaseRepository
from database.setup import get_session
from module.api_manager.api_key.entity.api_entity import ApiEntity


class ApiRepository(BaseRepository):
    def __init__(self):
        super().__init__(ApiEntity,
                         search_fields=[ApiEntity.name, ApiEntity.url])

    async def get_api_by_url(self, url: str) -> Optional[ApiEntity]:
        q = select(ApiEntity)
        q = q.filter(and_(ApiEntity.url == url))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            entity = None
        return entity

    async def get_apis_by_tag_id(self, tag_id: str) -> List[ApiEntity]:
        q = select(ApiEntity)
        q = q.filter(and_(ApiEntity.tags.any(tag_id)))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound as error:
            entities = []
        return entities

    async def _get_queryset(self, q: Select, filters: Optional[dict] = None, search: str = None,
                            where: list = None, or_conditions: list = None, is_count: bool = False) -> Select:
        if filters.get('tag'):
            tag = filters.get('tag', None)
            where = [ApiEntity.tags.any(tag)]
        q = await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
        return q