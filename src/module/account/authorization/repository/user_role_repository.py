from typing import List

from sqlalchemy import select, and_, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from common.exceptions import NotFoundException, InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.account.authorization.entity.user_role_entity import UserRoleEntity


class UserRoleRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserRoleEntity)

    async def fetch_by_user_id(self, user_id: str):
        q = select(UserRoleEntity)
        q = q.filter(UserRoleEntity.user_id == user_id)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def delete_by_user_id(self, user_id: str):
        q = delete(UserRoleEntity)
        q = q.filter(UserRoleEntity.user_id == user_id)
        try:
            async with get_session() as session:
                await session.execute(q)
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None

    async def delete_by_not_user_ids(self, user_ids: List[str]):
        q = delete(UserRoleEntity)
        q = q.filter(UserRoleEntity.user_id.not_in(user_ids))
        try:
            async with get_session() as session:
                await session.execute(q)
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None

    async def fetch_by_role_id(self, role_id):
        q = select(UserRoleEntity)
        q = q.filter(UserRoleEntity.role_id == role_id)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def fetch_by_role_id_and_user_id(self, role_id, user_id):
        q = select(UserRoleEntity)
        q = q.filter(and_(UserRoleEntity.role_id == role_id,
                          UserRoleEntity.user_id == user_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound:
            entity = None
        return entity
