from typing import Optional, List

from pydantic import BaseModel

from common.file_manager.enum.folder_accesses_enum import FolderAccessesEnum


class FolderAccessAccessesSchema(BaseModel):
    folder_id: Optional[str] = None
    accesses: Optional[List[FolderAccessesEnum]] = []
