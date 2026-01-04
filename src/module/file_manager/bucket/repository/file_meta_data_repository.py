from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound

from common.lib.base_respository import BaseRepository
from database.setup import get_session
from module.file_manager.bucket.entity.file_meta_data_entity import FileMetaDataEntity


class FileMetaDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(FileMetaDataEntity)

    async def get_by_file_id(self, file_id: str) -> Optional[FileMetaDataEntity]:
        q = select(FileMetaDataEntity)
        q = q.filter(and_(FileMetaDataEntity.file_id == file_id))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entity = result.scalars().one()
        except NoResultFound:
            return None
        return entity

    async def get_file_ids(self) -> List[str]:
        q = select(FileMetaDataEntity.file_id)
        q = q.filter(and_(FileMetaDataEntity.file_id.is_not(None)))
        try:
            async with get_session() as session:
                result = await session.execute(q)
                entities = result.scalars().all()
        except NoResultFound:
            return []
        return entities
