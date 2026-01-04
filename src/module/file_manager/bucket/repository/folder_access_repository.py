from typing import List, Optional

from sqlalchemy import select, and_, Select
from sqlalchemy.exc import NoResultFound

from common.file_manager.enum.folder_access_type import FolderAccessType
from common.lib.base_respository import BaseRepository
from database.setup import get_session
from module.file_manager.bucket.entity.folder_access_entity import FolderAccessEntity


class FolderAccessRepository(BaseRepository):
    def __init__(self):
        super().__init__(FolderAccessEntity,
                         filter_fields=[FolderAccessEntity.folder_id,
                                        FolderAccessEntity.type,
                                        FolderAccessEntity.instance_id])

    async def get_by_folder_id(self, folder_id: str) -> List[FolderAccessEntity]:
        q = select(FolderAccessEntity)
        q = q.filter(and_(FolderAccessEntity.folder_id == folder_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def get_by_instance_id(self, instance_id: str, type: FolderAccessType) -> List[FolderAccessEntity]:
        q = select(FolderAccessEntity)
        q = q.filter(and_(FolderAccessEntity.instance_id == instance_id,
                          FolderAccessEntity.type == type))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def get_by_instance_id_and_folder_id(self, instance_id: str, type: FolderAccessType, folder_id: str) -> FolderAccessEntity:
        q = select(FolderAccessEntity)
        q = q.filter(and_(FolderAccessEntity.instance_id == instance_id,
                          FolderAccessEntity.folder_id == folder_id,
                          FolderAccessEntity.type == type))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound:
            entity = None
        return entity

    async def _get_queryset(self, q: Select, filters: Optional[dict] = None, search: str = None, where: list = None,
                            or_conditions: list = None, is_count: bool = False) -> Select:
        if where is None:
            where = []
        if 'accesses_is_null' in filters:
            if filters['accesses_is_null']:
                where.append(FolderAccessEntity.accesses.is_(None))
            else:
                where.append(FolderAccessEntity.accesses.is_not(None))
        return await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
