from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        Boolean,
                        DateTime,
                        Index,
                        and_, Integer
                        )

from common.file_manager.schema.folder_schema import FolderSchema
from common.lib.base_entity import BaseEntity
from common.settings import get_settings

settings = get_settings()


class FolderEntity(BaseEntity):
    __tablename__ = 'folders'
    parent_folder_id = Column(String(64), nullable=True)
    user_id = Column(String(64), nullable=True)
    name = Column(String(1024), nullable=False)
    title = Column(String(1024), nullable=True)

    def __repr__(self):
        return f"<Folder(id={self.id})>"

    def convert_to_schema(self):
        return FolderSchema(
            id=self.id,
            name=self.name,
            title=self.title,
        )
