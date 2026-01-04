from sqlalchemy import Column, String, ARRAY, DateTime

from common.form_manager.schema.form_instance_assignment_schema import FormInstanceAssignmentSchema
from common.lib.base_entity import BaseEntity
from util.timestamp import DatetimeUtil


class FormInstanceAssignmentEntity(BaseEntity):
    __tablename__ = "form_instance_assignment"

    name = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=False)
    form_instance_id = Column(String(64), nullable=False)
    release_at = Column(DateTime(timezone=True), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)

    def convert_to_schema(self):
        return FormInstanceAssignmentSchema(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            form_instance_id=self.form_instance_id,
            release_at=self.release_at,
            deadline=self.deadline,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )