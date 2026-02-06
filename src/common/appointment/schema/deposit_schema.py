from typing import Optional

from pydantic import BaseModel

from common.appointment.enum.deposit_type_enum import DepositTypeEnum
from common.lib.base_output_model import BaseOutputModel


class DepositSchema(BaseModel):
    amount: Optional[int] = None