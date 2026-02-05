from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class OperatorServiceInSchema(BaseModel):
    operator_id: Optional[str] = None
    service_id: Optional[str] = None