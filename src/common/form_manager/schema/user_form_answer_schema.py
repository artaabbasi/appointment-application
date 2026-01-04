from typing import List, Optional

from pydantic import BaseModel

from common.form_manager.schema.form_field_schema import FormFieldSchema


class UserFormAnswerSchema(BaseModel):
    field: FormFieldSchema
    answer: Optional[str] = None
    attachment_files: List[str] = []
