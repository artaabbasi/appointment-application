from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseOutputModel(BaseModel):
    id: str

    created_at: datetime
    updated_at: Optional[datetime]