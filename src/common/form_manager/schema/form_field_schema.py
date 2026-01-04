from typing import Optional, List

from pydantic import BaseModel

from common.form_manager.enum.form_field_type_enum import FormFieldTypeEnum
from common.form_manager.schema.form_field_choice_schema import FormFieldChoiceSchema


class FormFieldSchema(BaseModel):
    id: str
    field_type: Optional[FormFieldTypeEnum] = None
    title: Optional[str] = None
    description: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    is_required: bool = False
    attachment_files: Optional[List[str]] = []
    choices: List[FormFieldChoiceSchema] = []
