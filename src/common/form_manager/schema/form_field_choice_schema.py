from typing import Optional, List

from pydantic import BaseModel


class FormFieldChoiceSchema(BaseModel):
    id: str
    attachment_files: Optional[List[str]] = []
    description: Optional[str] = None
