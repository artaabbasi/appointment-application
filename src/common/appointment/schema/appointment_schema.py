from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.lib.base_output_model import BaseOutputModel


class AppointmentSchema(BaseOutputModel):
    user_id: str
    description: Optional[str] = None
    is_cancelled: Optional[bool] = False
    cancelled_at: Optional[datetime] = None
    cancelled_by_id: Optional[str] = None
