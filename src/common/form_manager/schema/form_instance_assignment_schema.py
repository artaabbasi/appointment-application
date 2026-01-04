from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.form_manager.schema.form_instance_schema import FormInstanceSchema


class FormInstanceAssignmentSchema(BaseModel):
    id: str

    name: str
    user_id: str
    form_instance_id: str
    release_at: Optional[datetime] = None
    deadline: Optional[datetime] = None

    form_instance: Optional[FormInstanceSchema] = None
    user_has_answer: Optional[bool] = None
    users_count: Optional[int] = None
    answered_users_count: Optional[int] = None
    not_answered_users_count: Optional[int] = None

    created_at: datetime
    updated_at: Optional[datetime] = None
