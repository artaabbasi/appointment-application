from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FormInstanceAssignmentUserInSchema(BaseModel):
    user_id: str
    form_instance_assignment_id: str
    assigned_from_role_id: Optional[str] = None
    user_form_id: Optional[str] = None
