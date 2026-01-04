from typing import List, Optional

from pydantic import BaseModel

from common.form_manager.schema.user_form_field_answer_create_schema import UserFormFieldAnswerCreateSchema


class UserFormAnswerCreateSchema(BaseModel):
    form_id: str
    user_form_id: Optional[str] = None
    answers: List[UserFormFieldAnswerCreateSchema]
