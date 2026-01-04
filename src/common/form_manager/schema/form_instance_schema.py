from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.form_manager.enum.form_instance_usage_type_enum import FormInstanceUsageTypeEnum


class FormInstanceSchema(BaseModel):
    id: str

    name: str
    user_id: str
    form_id: Optional[str] = None
    description: Optional[str] = None
    usage_type: FormInstanceUsageTypeEnum

    created_at: datetime
    updated_at: Optional[datetime] = None
