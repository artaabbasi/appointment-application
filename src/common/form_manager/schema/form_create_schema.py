from typing import Optional, List

from pydantic import BaseModel

from common.form_manager.enum.form_service_type_enum import FormServiceTypeEnum
from common.form_manager.schema.form_field_create_schema import FormFieldCreateSchema


class FormCreateSchema(BaseModel):
    name: str
    service_id: str
    service_type: FormServiceTypeEnum
    fields: List[FormFieldCreateSchema]
