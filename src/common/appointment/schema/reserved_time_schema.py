from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReservedTimeSchema(BaseModel):
    from_datetime: Optional[datetime] = None
    to_datetime: Optional[datetime] = None
