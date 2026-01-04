from typing import Optional, Union, List
from pydantic import BaseModel

from common.file_manager.enum.file_access_type_enum import FileAccessTypeEnum


class FileUploadSchema(BaseModel):
    file_name: Optional[str] = None
    folder_names: Optional[str] = None
    folder_id: Optional[str] = None
    access_type: Optional[FileAccessTypeEnum] = FileAccessTypeEnum.LOCAL
    reduce_quality: Optional[bool] = True
