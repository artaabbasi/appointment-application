from typing import Optional
from pydantic import BaseModel


class ProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    national_code: Optional[str] = None
    birth_date: Optional[str] = None
    father_name: Optional[str] = None
    avatar: Optional[str] = None
