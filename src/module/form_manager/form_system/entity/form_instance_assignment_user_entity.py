from sqlalchemy import Column, String, ARRAY

from common.form_manager.schema.form_instance_assignment_user_schema import FormInstanceAssignmentUserSchema
from common.lib.base_entity import BaseEntity

class FormInstanceAssignmentUserEntity(BaseEntity):
    __tablename__ = "form_instance_assignment_user"

    user_id = Column(String(64), nullable=False)
    form_instance_assignment_id = Column(String(64), nullable=False)
    assigned_from_role_id = Column(String(64), nullable=True)
    user_form_id = Column(String(64), nullable=True)

    def convert_to_schema(self):
        return FormInstanceAssignmentUserSchema(
            id=self.id,
            user_id=self.user_id,
            form_instance_assignment_id=self.form_instance_assignment_id,
            assigned_from_role_id=self.assigned_from_role_id,
            user_form_id=self.user_form_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
