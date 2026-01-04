from sqlalchemy import Column, String, ARRAY

from common.file_manager.schema.folder_access_schema import FolderAccessSchema
from common.lib.base_entity import BaseEntity


class FolderAccessEntity(BaseEntity):
    __tablename__ = 'folder_access'
    type = Column(String(64), nullable=False)
    folder_id = Column(String(64), nullable=False)
    instance_id = Column(String(64), nullable=False)
    accesses = Column(ARRAY(String(64)), nullable=True)
    user_id = Column(String(64), nullable=True)

    def convert_to_schema(self):
        return FolderAccessSchema(
            id=self.id,
            type=self.type,
            folder_id=self.folder_id,
            instance_id=self.instance_id,
            user_id=self.user_id,
            accesses=self.accesses,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
