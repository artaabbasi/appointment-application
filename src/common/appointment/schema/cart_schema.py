from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.lib.base_output_model import BaseOutputModel


class CartSchema(BaseOutputModel):
    user_id: str
    description: Optional[str] = None
    valid_to: datetime
