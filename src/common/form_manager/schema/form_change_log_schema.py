from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.form_manager.schema.form_field_create_schema import FormFieldCreateSchema
from common.form_manager.schema.form_field_schema import FormFieldSchema

class FormChangeLogSchema(BaseModel):
    user_id: Optional[str] = None
    form_id: Optional[str] = None
    last_fields: Optional[list[FormFieldSchema]] = None
    new_fields: Optional[list[FormFieldCreateSchema]] = None
    created_at: Optional[datetime] = None

    user: Optional[NotDetailedUserSchema] = None
