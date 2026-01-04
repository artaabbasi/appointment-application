from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from common.form_manager.enum.form_service_type_enum import FormServiceTypeEnum
from common.form_manager.schema.form_field_schema import FormFieldSchema


class FormSchema(BaseModel):
    id: str
    name: str
    service_id: str
    service_type: FormServiceTypeEnum
    fields: List[FormFieldSchema] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
