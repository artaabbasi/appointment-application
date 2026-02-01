from typing import Optional

from pydantic import BaseModel


class OperatorInSchema(BaseModel):
    user_id: Optional[str] = None
    name: str
    description: Optional[str] = None