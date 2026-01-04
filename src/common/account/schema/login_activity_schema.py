from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class LoginActivitySchema(BaseModel):
    id: str
    user_id: str
    expire_timestamp: int
    agent: Optional[str] = None
    is_current: Optional[bool] = False
    created_at: datetime
