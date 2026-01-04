from typing import Optional, List
from sqlalchemy import select, and_, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from common.exceptions import InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.api_manager.api_key.entity.api_key_access_entity import ApiKeyAccessEntity


class ApiKeyAccessRepository(BaseRepository):
    def __init__(self):
        super().__init__(ApiKeyAccessEntity)

    async def get_by_api_id_and_api_key_id(self, api_id: str, api_key_id: str) -> Optional[ApiKeyAccessEntity]:
        q = select(ApiKeyAccessEntity)
        q = q.filter(and_(ApiKeyAccessEntity.api_id == api_id,
                          ApiKeyAccessEntity.api_key_id == api_key_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            entity = None
        return entity

    async def get_by_api_tag_id_and_api_key_id(self, api_tag_id: str, api_key_id: str) -> Optional[ApiKeyAccessEntity]:
        q = select(ApiKeyAccessEntity)
        q = q.filter(and_(ApiKeyAccessEntity.api_tag_id == api_tag_id,
                          ApiKeyAccessEntity.api_key_id == api_key_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound as error:
            entity = None
        return entity

    async def get_by_api_key_id_and_tag_not_null(self, api_key_id: str) -> List[ApiKeyAccessEntity]:
        q = select(ApiKeyAccessEntity)
        q = q.filter(and_(ApiKeyAccessEntity.api_tag_id.is_not(None),
                          ApiKeyAccessEntity.api_key_id == api_key_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound as error:
            entities = []
        return entities

    async def get_all_by_api_key_id(self, api_key_id: str) -> List[ApiKeyAccessEntity]:
        q = select(ApiKeyAccessEntity)
        q = q.filter(and_(ApiKeyAccessEntity.api_key_id == api_key_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound as error:
            entities = []
        return entities

    async def delete_all_by_api_key_id(self, api_key_id: str):
        q = delete(ApiKeyAccessEntity)
        q = q.filter(and_(ApiKeyAccessEntity.api_key_id == api_key_id))
        try:
            async with get_session() as session:
                await session.execute(q)
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None
