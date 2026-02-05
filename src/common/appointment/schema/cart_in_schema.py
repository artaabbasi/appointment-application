from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CartInSchema(BaseModel):
    user_id: Optional[str] = None
    description: Optional[str] = None
    valid_to: Optional[datetime] = None
