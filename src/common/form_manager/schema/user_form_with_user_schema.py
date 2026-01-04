from typing import List

from pydantic import BaseModel

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.form_manager.schema.user_form_answer_schema import UserFormAnswerSchema


class UserFormWithUserSchema(BaseModel):
    user: NotDetailedUserSchema
    field_answers: List[UserFormAnswerSchema] = []
