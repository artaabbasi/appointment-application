from typing import Optional

from pydantic import BaseModel

from common.form_manager.enum.form_instance_usage_type_enum import FormInstanceUsageTypeEnum


class FormInstanceInSchema(BaseModel):
    name: Optional[str] = None
    form_id: Optional[str] = None
    description: Optional[str] = None
    usage_type: Optional[FormInstanceUsageTypeEnum] = None
