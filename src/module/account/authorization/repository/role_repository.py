from sqlalchemy import select, Select
from sqlalchemy.exc import NoResultFound

from common.lib.base_respository import BaseRepository
from database.setup import get_session
from module.account.authorization.entity.role_entity import RoleEntity


class RoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(RoleEntity,
                         filter_fields=[RoleEntity.show_in_site],
                         search_fields=[RoleEntity.name, RoleEntity.title],
                         order_by=[RoleEntity.title])

    async def fetch_by_name(self, name: str):
        q = select(RoleEntity)
        q = q.filter(RoleEntity.name == name)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def _get_queryset(self, q: Select, filters: dict, search: str = None, where: list = None, or_conditions: list = None, is_count: bool = False) -> Select:
        if filters.get('title_is_null') is not None:
            if filters.get('title_is_null'):
                where = [RoleEntity.title.is_(None)]
            else:
                where = [RoleEntity.title.is_not(None)]
        q = await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
        return q.distinct()
