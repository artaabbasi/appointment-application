from typing import Optional, List

from pydantic import BaseModel


class FormFieldChoiceCreateSchema(BaseModel):
    id: Optional[str] = None
    attachment_files: Optional[List[str]] = []
    description: Optional[str] = None
