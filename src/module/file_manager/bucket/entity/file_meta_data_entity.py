from __future__ import annotations
from sqlalchemy import (Column,
                        String,
                        Boolean,
                        Index,
                        and_, Integer, Text, Date
                        )

from common.file_manager.schema.file_meta_data_schema import FileMetaDataSchema
from common.lib.base_entity import BaseEntity
from common.settings import get_settings

settings = get_settings()


class FileMetaDataEntity(BaseEntity):
    __tablename__ = 'file_meta_data'
    file_id = Column(String(64), nullable=False, index=True, unique=True)
    code = Column(Integer, nullable=True)
    name = Column(String(1024), nullable=True)
    description = Column(Text, nullable=True)
    approval_date = Column(Date, nullable=True)
    producer_user_id = Column(String(64), nullable=True)
    controller_user_id = Column(String(64), nullable=True)
    confirmer_user_id = Column(String(64), nullable=True)
    approver_user_id = Column(String(64), nullable=True)

    def convert_to_schema(self):
        return FileMetaDataSchema(
            id=self.id,
            file_id=self.file_id,
            code=self.code,
            name=self.name,
            description=self.description,
            approval_date=self.approval_date,
            producer_user_id=self.producer_user_id,
            controller_user_id=self.controller_user_id,
            confirmer_user_id=self.confirmer_user_id,
            approver_user_id=self.approver_user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
