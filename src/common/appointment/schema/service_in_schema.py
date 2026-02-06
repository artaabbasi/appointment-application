from typing import Optional

from pydantic import BaseModel

from common.appointment.enum.deposit_type_enum import DepositTypeEnum


class ServiceInSchema(BaseModel):
    main_service_id: str
    name: str
    duration: int
    description: Optional[str] = None
    price_as_rial: Optional[int] = None
    deposit_type: Optional[DepositTypeEnum] = None
    deposit_amount: Optional[int] = None
    is_active: Optional[bool] = None