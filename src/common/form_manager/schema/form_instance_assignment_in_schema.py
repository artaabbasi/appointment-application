from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel



class FormInstanceAssignmentInSchema(BaseModel):
    name: Optional[str] = None
    form_instance_id: Optional[str] = None
    release_at: Optional[datetime] = None
    deadline: Optional[datetime] = None

    assign_to_user_ids: Optional[List[str]] = []
    assign_to_role_ids: Optional[List[str]] = []
