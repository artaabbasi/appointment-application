from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.account.authorization.entity.role_permission_entity import RolePermissionEntity


class RolePermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(RolePermissionEntity)

    async def fetch_by_role_id(self, role_id):
        q = select(RolePermissionEntity)
        q = q.filter(RolePermissionEntity.role_id == role_id)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def fetch_by_role_id_and_permission_id(self, role_id, permission_id):
        q = select(RolePermissionEntity)
        q = q.filter(and_(RolePermissionEntity.role_id == role_id,
                          RolePermissionEntity.permission_id == permission_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound:
            entity = None
        return entity
