from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from common.api_manager.schema.api_key_access_schema import ApiKeyAccessSchema


class ApiKeySchema(BaseModel):
    id: str
    user_id: str
    name: str
    accesses: List[ApiKeyAccessSchema]
    created_at: datetime
    updated_at: Optional[datetime] = None
