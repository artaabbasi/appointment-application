from datetime import datetime
from typing import Optional
from common.lib.base_output_model import BaseOutputModel


class OperatorServiceSchema(BaseOutputModel):
    operator_id: Optional[str] = None
    service_id: Optional[str] = None