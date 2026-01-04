from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema


class FileMetaDataSchema(BaseModel):
    code: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    approval_date: Optional[date] = None
    producer_user_id: Optional[str] = None
    controller_user_id: Optional[str] = None
    confirmer_user_id: Optional[str] = None
    approver_user_id: Optional[str] = None
    producer_user: Optional[NotDetailedUserSchema] = None
    controller_user: Optional[NotDetailedUserSchema] = None
    confirmer_user: Optional[NotDetailedUserSchema] = None
    approver_user: Optional[NotDetailedUserSchema] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
