from datetime import datetime
from typing import Optional, Union
from fastapi import UploadFile, File
from pydantic import BaseModel

from common.file_manager.enum.file_access_type_enum import FileAccessTypeEnum
from common.file_manager.schema.file_meta_data_schema import FileMetaDataSchema


class FileInfoSchema(BaseModel):
    id: str
    file_name: Optional[str] = None
    access_type: Optional[FileAccessTypeEnum] = FileAccessTypeEnum.LOCAL
    size: Optional[int] = None
    mime_type: Optional[str] = None
    meta_data: Optional[FileMetaDataSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
