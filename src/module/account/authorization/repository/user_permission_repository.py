from sqlalchemy import select, and_, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from common.exceptions import NotFoundException, InternalServerErrorException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.account.authorization.entity.user_permission_entity import UserPermissionEntity


class UserPermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserPermissionEntity)

    async def fetch_by_user_id(self, user_id):
        q = select(UserPermissionEntity)
        q = q.filter(UserPermissionEntity.user_id == user_id)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def fetch_by_permission_id(self, permission_id):
        q = select(UserPermissionEntity)
        q = q.filter(UserPermissionEntity.permission_id == permission_id)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def fetch_by_user_id_and_permission_id(self, user_id, permission_id):
        q = select(UserPermissionEntity)
        q = q.filter(and_(UserPermissionEntity.user_id == user_id,
                          UserPermissionEntity.permission_id == permission_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound:
            entity = None
        return entity

    async def delete_by_user_id_and_permission_id(self, user_id, permission_id):
        q = delete(UserPermissionEntity)
        q = q.filter(and_(UserPermissionEntity.user_id == user_id,
                          UserPermissionEntity.permission_id == permission_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                await session.commit()
        except IntegrityError as error:
            raise InternalServerErrorException(RepositoryErrorCodeEnum.ERROR_ON_DELETING_ENTITY, error)
        return None
