from typing import Optional

from pydantic import BaseModel


class AppointmentInSchema(BaseModel):
    user_id: Optional[str] = None
    description: Optional[str] = None
