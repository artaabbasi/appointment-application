from typing import List, Optional

from pydantic import BaseModel


class UserFormFieldAnswerCreateSchema(BaseModel):
    field_id: str
    answer: Optional[str] = None
    attachment_files: List[str] = []
