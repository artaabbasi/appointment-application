from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        Boolean,
                        DateTime,
                        Index,
                        and_, Integer
                        )

from common.file_manager.schema.file_info_schema import FileInfoSchema
from common.lib.base_entity import BaseEntity
from common.settings import get_settings

settings = get_settings()


class FileEntity(BaseEntity):
    __tablename__ = 'files'
    folder_id = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=True)
    access_type = Column(String(64), nullable=False)
    name = Column(String(1024), nullable=False)
    file_path = Column(String(1024), nullable=False)
    size = Column(Integer, nullable=False)
    mime_type = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<File(id={self.id})>"

    def get_info_schema(self) -> FileInfoSchema:
        return FileInfoSchema(
            id=self.id,
            file_name=self.name,
            access_type=self.access_type,
            size=self.size,
            mime_type=self.mime_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )