from typing import Optional

from pydantic import BaseModel

from common.lib.base_output_model import BaseOutputModel


class OperatorSchema(BaseOutputModel):
    user_id: Optional[str] = None
    name: str
    description: Optional[str] = None
