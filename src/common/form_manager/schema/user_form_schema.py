from typing import List

from pydantic import BaseModel

from common.form_manager.schema.user_form_answer_schema import UserFormAnswerSchema


class UserFormSchema(BaseModel):
    user_form_id: str
    field_answers: List[UserFormAnswerSchema] = []
