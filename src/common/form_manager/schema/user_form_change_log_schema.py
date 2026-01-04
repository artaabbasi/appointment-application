from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.form_manager.schema.user_form_answer_schema import UserFormAnswerSchema

class UserFormChangeLogSchema(BaseModel):
    user_id: Optional[str] = None
    user_form_id: Optional[str] = None
    last_answers: Optional[list[UserFormAnswerSchema]] = None
    new_answers: Optional[list[UserFormAnswerSchema]] = None
    created_at: Optional[datetime] = None

    user: Optional[NotDetailedUserSchema] = None
