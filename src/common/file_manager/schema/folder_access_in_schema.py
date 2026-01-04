from typing import Union, Optional, List

from pydantic import BaseModel

from common.file_manager.enum.folder_access_type import FolderAccessType
from common.file_manager.enum.folder_accesses_enum import FolderAccessesEnum


class FolderAccessInSchema(BaseModel):
    type: FolderAccessType
    folder_id: str
    instance_id: str
    accesses: Optional[List[FolderAccessesEnum]] = None


class FolderAccessInListSchema(BaseModel):
    data: List[FolderAccessInSchema]
