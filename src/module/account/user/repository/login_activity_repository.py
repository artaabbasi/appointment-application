from typing import Optional, List

from sqlalchemy import and_, select, Select
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.account.user.entity.login_activity_entity import LoginActivityEntity
from util.timestamp import DatetimeUtil


class LoginActivityRepository(BaseRepository):
    def __init__(self):
        super().__init__(LoginActivityEntity,
                         filter_fields=[LoginActivityEntity.user_id])

    @staticmethod
    async def fetch_by_user_id_and_token(user_id: str, token: str) -> Optional[LoginActivityEntity]:
        q = select(LoginActivityEntity)
        q = q.filter(and_(LoginActivityEntity.user_id == user_id, LoginActivityEntity.refresh_token == token, ))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound:
            raise NotFoundException(RepositoryErrorCodeEnum.ENTITY_NOT_FOUND)
        return entity

    @staticmethod
    async def fetch_all_by_user_id_and_token(user_id: str, token: str) -> List[LoginActivityEntity]:
        q = select(LoginActivityEntity)
        q = q.filter(and_(LoginActivityEntity.user_id == user_id, LoginActivityEntity.refresh_token == token, ))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            entities = []
        return entities

    @staticmethod
    async def exclude_by_user_id_and_token(user_id: str, token: str) -> List[LoginActivityEntity]:
        q = select(LoginActivityEntity)
        q = q.filter(and_(LoginActivityEntity.user_id == user_id, LoginActivityEntity.refresh_token != token, ))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def fetch_by_id_and_user_id(
            self,
            entity_id: str,
            user_id: str,
    ) -> LoginActivityEntity:
        q = select(LoginActivityEntity)
        q = q.filter(and_(LoginActivityEntity.id == entity_id, LoginActivityEntity.user_id == user_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound:
            raise NotFoundException(RepositoryErrorCodeEnum.ENTITY_NOT_FOUND, entity_id)
        return entity

    async def _get_queryset(self, q: Select, filters: dict, search: str = None, where: list = None,
                            or_conditions: list = None, is_count: bool = False) -> Select:
        if filters.get('is_active'):
            where = [LoginActivityEntity.expire_timestamp > DatetimeUtil.utc_now_timestamp()]
        q = await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
        return q
