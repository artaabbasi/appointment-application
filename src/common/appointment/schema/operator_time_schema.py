from datetime import datetime
from typing import Optional
from common.lib.base_output_model import BaseOutputModel


class OperatorTimeSchema(BaseOutputModel):
    operator_id: Optional[str] = None
    from_datetime: datetime = None
    to_datetime: datetime = None