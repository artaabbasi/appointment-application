from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.account.schema.role_schema import RoleSchema


class FormInstanceAssignmentUserSchema(BaseModel):
    id: str

    user_id: str
    form_instance_assignment_id: str
    assigned_from_role_id: Optional[str] = None
    user_form_id: Optional[str] = None

    user: Optional[NotDetailedUserSchema] = None
    assigned_from_role: Optional[RoleSchema] = None

    created_at: datetime
    updated_at: Optional[datetime] = None
