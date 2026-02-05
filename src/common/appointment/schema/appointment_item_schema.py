from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.lib.base_output_model import BaseOutputModel


class AppointmentItemSchema(BaseOutputModel):
    appointment_id: str
    service_id: str
    operator_id: str
    from_datetime: datetime
    to_datetime: datetime
