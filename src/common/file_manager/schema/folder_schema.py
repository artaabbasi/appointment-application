from typing import List, Optional

from pydantic import BaseModel

from common.file_manager.schema.file_info_schema import FileInfoSchema


class FolderSchema(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    folders: List['FolderSchema'] = []
    files: List['FileInfoSchema'] = []
    file_count: Optional[int] = 0
