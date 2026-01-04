from typing import List, Optional

from sqlalchemy import select, and_, Select, or_
from sqlalchemy.exc import NoResultFound

from common.exceptions import NotFoundException
from common.lib.base_respository import BaseRepository
from common.lib.repository_error_code_enum import RepositoryErrorCodeEnum
from database.setup import get_session
from module.file_manager.bucket.entity.folder_entity import FolderEntity


class FolderRepository(BaseRepository):
    def __init__(self):
        super().__init__(FolderEntity,
                         filter_fields=[FolderEntity.parent_folder_id],
                         search_fields=[FolderEntity.name,
                                        FolderEntity.title, ])

    async def fetch_by_names_and_user_id(self, names: List[str], user_id):
        entity = None
        for name in names:
            q = select(self.type)
            q = q.filter(and_(FolderEntity.user_id == user_id,
                              FolderEntity.name == name))
            try:
                async with get_session() as session:
                    result = await session.execute(q)
                    entity = result.scalars().one()
            except NoResultFound:
                entity = await self.create(
                    FolderEntity(
                        name=name,
                        user_id=user_id,
                        parent_folder_id=getattr(entity, 'id', None),
                    )
                )
        return entity

    async def fetch_by_names_and_parent_id(self, names: List[str], parent_id: Optional[str] = None):
        entity = None
        if parent_id is not None:
            entity = self.fetch_by_id(parent_id)
        for name in names:
            q = select(self.type)
            q = q.filter(and_(FolderEntity.parent_folder_id == getattr(entity, 'id', None),
                              FolderEntity.name == name))
            try:
                async with get_session() as session:
                    result = await session.execute(q)
                    entity = result.scalars().one()
            except NoResultFound:
                entity = await self.create(
                    FolderEntity(
                        name=name,
                        parent_folder_id=getattr(entity, 'id', None),
                    )
                )
        return entity

    async def _get_queryset(self, q: Select, filters: Optional[dict] = None, search: str = None, where: list = None,
                            or_conditions: list = None, is_count: bool = False) -> Select:
        if isinstance(filters.get('folder_ids'), list):
            where = [or_(FolderEntity.id.in_(filters['folder_ids']),
                         FolderEntity.parent_folder_id.in_(filters['folder_ids']))]
        q = await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
        return q

    async def get_by_parent_folder_id(self,
                                      parent_folder_id: str,
                                      folder_ids: Optional[List[str]] = None) -> List[FolderEntity]:
        q = select(FolderEntity)
        q = q.filter(and_(FolderEntity.parent_folder_id == parent_folder_id))
        if folder_ids is not None and parent_folder_id not in folder_ids:
            q = q.filter(and_(FolderEntity.id.in_(folder_ids)))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def get_by_user_id(self,
                             user_id: str) -> List[FolderEntity]:
        q = select(FolderEntity)
        q = q.filter(and_(FolderEntity.user_id == user_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities
