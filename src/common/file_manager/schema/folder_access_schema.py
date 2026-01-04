from datetime import datetime
from typing import Union, Optional, List

from pydantic import BaseModel

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.account.schema.role_schema import RoleSchema
from common.file_manager.enum.folder_access_type import FolderAccessType
from common.file_manager.enum.folder_accesses_enum import FolderAccessesEnum


class FolderAccessSchema(BaseModel):
    id: Optional[str] = None
    type: Optional[FolderAccessType] = None
    folder_id: Optional[str] = None
    instance_id: Optional[str] = None
    user_id: Optional[str] = None
    instance: Union[NotDetailedUserSchema, RoleSchema, None] = None
    user: Optional[NotDetailedUserSchema] = None
    accesses: Optional[List[FolderAccessesEnum]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
