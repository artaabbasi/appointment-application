from importlib.metadata import files
from typing import List, Optional

from sqlalchemy import and_, select, Select, func
from sqlalchemy.exc import NoResultFound

from common.lib.base_respository import BaseRepository
from database.setup import get_session
from module.file_manager.bucket.entity.file_entity import FileEntity
from module.file_manager.bucket.repository.file_meta_data_repository import FileMetaDataRepository


class FileRepository(BaseRepository):
    def __init__(self):
        super().__init__(FileEntity,
                         filter_fields=[FileEntity.folder_id])

    async def get_by_folder_id(self,
                               folder_id: str,
                               meta_data_is_null: Optional[bool] = None) -> List[FileEntity]:
        q = select(self.type)
        filters = {FileEntity.folder_id: folder_id}
        if meta_data_is_null is not None:
            filters['meta_data_is_null'] = meta_data_is_null
        q = await self._get_queryset(q, filters)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities

    async def get_count_by_folder_id(self,
                                     folder_id: str,
                                     meta_data_is_null: Optional[bool] = None) -> int:
        q = select(func.count()).select_from(self.type)
        filters = {FileEntity.folder_id: folder_id}
        if meta_data_is_null is not None:
            filters['meta_data_is_null'] = meta_data_is_null
        q = await self._get_queryset(q, filters)
        try:
            async with get_session() as session:
                result = await session.execute(q)
                count = result.one()[0]
        except NoResultFound:
            return 0
        return count

    async def _get_queryset(self, q: Select, filters: dict, search: str = None, where: list = None,
                            or_conditions: list = None, is_count: bool = False) -> Select:
        if where is None:
            where = []
        if 'meta_data_is_null' in filters:
            file_ids = await FileMetaDataRepository().get_file_ids()
            if filters['meta_data_is_null']:
                where.append(FileEntity.id.not_in(file_ids))
            else:
                where.append(FileEntity.id.in_(file_ids))
        return await super()._get_queryset(q, filters, search, where, or_conditions, is_count)
