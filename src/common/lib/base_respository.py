import uuid
from uuid import uuid4
from typing import TypeVar, List, Generic, Type, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import update, select, Column, func, Select, asc, desc, or_, delete

from common.exceptions import BadRequestException, InternalServerErrorException, NotFoundException
from common.lib.base_entity import BaseEntity
from common.lib.date_filter_enum import DateFilterEnum
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from util.logger import get_custom_logger
from util.timestamp import DatetimeUtil

T = TypeVar('T', bound=BaseEntity)
logger = get_custom_logger(__name__)


class BaseRepository(Generic[T]):
    _filter_fields: List[Column] = []
    _order_by: List[Column] = []
    _search_fields: List[Column] = []
    _date_filters: dict[str, tuple[DateFilterEnum, Column]] = {}

    def __init__(self, entity_type: Type[T],
                 filter_fields=None,
                 date_filters=None,
                 search_fields=None,
                 order_by=None,
                 ):
        if filter_fields is not None:
            self._filter_fields = filter_fields
        if search_fields is not None:
            self._search_fields = search_fields
        if date_filters is not None:
            self._date_filters = date_filters
        if order_by is not None:
            self._order_by = order_by
        self.type = entity_type

    async def delete(self, entity: T):
        if entity is None:
            return None
        try:
            async with get_session() as session:
                await session.delete(entity)
                await session.commit()
        except IntegrityError as error:
            logger.error(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None

    async def delete_all(self):
        try:
            async with get_session() as session:
                await session.execute(
                    delete(self.type)
                )
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None

    async def create(self, entity: T) -> T:
        if entity.id is None:
            entity.id = str(uuid4())
        entity.created_at = DatetimeUtil.utc_now_datetime()
        async with get_session() as session:
            session.add(entity)
            try:
                await session.commit()
            except IntegrityError as error:
                logger.error(RepositoryErrorCodeEnum.ENTITY_ALREADY_EXISTS, error)
                raise BadRequestException(RepositoryErrorCodeEnum.ENTITY_ALREADY_EXISTS, error)
        return entity

    async def update(self, entity: T) -> T:
        entity.updated_at = DatetimeUtil.utc_now_datetime()
        update_need_dict = {key: value for key, value in entity.to_dict().items()}
        q = update(self.type).values(**update_need_dict).where(
            self.type.id == entity.id)
        q.execution_options(synchronize_session="fetch")
        try:
            async with get_session() as session:
                await session.execute(q)
                await session.commit()
        except IntegrityError as error:
            logger.error(RepositoryErrorCodeEnum.ERROR_ON_UPDATING_ENTITY, error)
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_UPDATING_ENTITY, error)
        return entity

    async def fetch_by_id(
            self,
            entity_id: str,
    ) -> T:
        q = select(self.type)
        q = q.filter(self.type.id == entity_id)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            raise NotFoundException(RepositoryErrorCodeEnum.ENTITY_NOT_FOUND, entity_id)
        return entity

    async def batch_update(self, entities: List[T]) -> List[T]:
        for entity in entities:
            await self.update(entity)  # TODO, find a way to batch update
        return entities

    @staticmethod
    async def batch_create(entities: List[T]) -> List[T]:
        for entity in entities:
            if entity.id is None:
                entity.id = str(uuid4())
            entity.created_at = DatetimeUtil.utc_now_datetime()
        async with get_session() as session:
            session.add_all(entities)
            try:
                await session.commit()
            except IntegrityError as error:
                logger.error(RepositoryErrorCodeEnum.ERROR_ON_BATCH_INSERT, error)
                raise BadRequestException(
                    RepositoryErrorCodeEnum.ERROR_ON_BATCH_INSERT,
                    {'entity': T, 'error': error}
                )
        return entities

    async def fetch_all_by_ids(self, entity_ids: List[str]) -> List[T]:
        q = select(self.type)
        q = q.filter(self.type.id.in_(entity_ids))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    @staticmethod
    async def _get_pagination_parameters(page: int, size: int) -> tuple[int, int]:
        skip = (page - 1) * size
        limit = size
        return skip, limit

    async def _get_queryset(self, q: Select, filters: Optional[dict] = None, search: str = None, where: list = None, or_conditions: list = None, is_count: bool = False) -> Select:
        if where is None:
            where = []
        if or_conditions is None:
            or_conditions = []
        if filters is None:
            filters = {}
        for field in self._filter_fields:
            if field in filters.keys():
                value = filters.get(field)
                where.append(field == value)

        for name, filter_data in self._date_filters.items():
            if name in filters.keys():
                value = filters.get(name)
                if filter_data[0] == DateFilterEnum.FROM:
                    where.append(filter_data[1] >= value)
                elif filter_data[0] == DateFilterEnum.TO:
                    where.append(filter_data[1] <= value)
                else:
                    where.append(filter_data[1] == value)

        if search:
            for field in self._search_fields:
                new_search = search.replace("ی", "ي")
                new_search = new_search.replace("ک", "ك")
                or_conditions.append(field.like(f"%{search}%"))
                or_conditions.append(field.like(f"%{new_search}%"))
        where.append(or_(*or_conditions))

        q = q.filter(*where)

        if self._order_by is not None and not is_count:
            q = q.order_by(*self._order_by)
        elif self._order_by is None:
            q = q.order_by(*self.type.created_at.asc())

        return q

    async def fetch_paginated_list_by_filters(self,
                                              page: int,
                                              size: int,
                                              filters: dict,
                                              search: str = None,
                                              *, where_condition: Optional[list] = None
                                              ) -> List[T]:

        q = select(self.type)
        get_q_kwargs: Dict[str, Any] = {
            "q": q,
            "filters": filters,
            "search": search,
        }
        if where_condition is not None:
            get_q_kwargs["where"] = where_condition

        q = await self._get_queryset(**get_q_kwargs)

        if size >= 0:
            skip, limit = await self._get_pagination_parameters(page=page, size=size)
            q = q.offset(skip).limit(limit)

        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def count(self, filters: dict, search: str = None) -> int:
        where = []
        q = select(func.count()).select_from(self.type)

        q = await self._get_queryset(q, filters, search, is_count=True)

        q = q.filter(*where)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                count = result.one()[0]
        except NoResultFound:
            return 0
        return count
