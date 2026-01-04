from sqlalchemy import Column, String, ARRAY, Text

from common.form_manager.schema.form_instance_schema import FormInstanceSchema
from common.lib.base_entity import BaseEntity

class FormInstanceEntity(BaseEntity):
    __tablename__ = "form_instance"

    name = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(String(64), nullable=False)
    form_id = Column(String(64), nullable=True)
    usage_type = Column(String(64), nullable=False)

    def convert_to_schema(self):
        return FormInstanceSchema(
            id=self.id,
            name=self.name,
            description=self.description,
            user_id=self.user_id,
            form_id=self.form_id,
            usage_type=self.usage_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )