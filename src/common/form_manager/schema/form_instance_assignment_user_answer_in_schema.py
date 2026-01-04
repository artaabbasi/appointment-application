from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FormInstanceAssignmentUserAnswerInSchema(BaseModel):
    user_form_id: Optional[str] = None
