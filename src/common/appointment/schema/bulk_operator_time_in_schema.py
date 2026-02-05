from datetime import datetime, date, time
from typing import Optional, List

from pydantic import BaseModel


class BulkOperatorTimeInSchema(BaseModel):
    operator_id: str
    dates: List[date]
    from_time: time
    to_time: time