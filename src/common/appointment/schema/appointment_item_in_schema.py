from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AppointmentItemInSchema(BaseModel):
    appointment_id: Optional[str] = None
    service_id: Optional[str] = None
    operator_id: Optional[str] = None
    from_datetime: Optional[datetime] = None
    to_datetime: Optional[datetime] = None
