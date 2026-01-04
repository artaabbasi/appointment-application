from sqlalchemy import Column, String, ARRAY

from common.lib.base_entity import BaseEntity
from common.form_manager.schema.form_schema import FormSchema


class FormEntity(BaseEntity):
    __tablename__ = "form"

    name = Column(String(64), nullable=False)
    service_id = Column(String(64), nullable=False)
    service_type = Column(String(64), nullable=False)

    def convert_to_schema(self):
        return FormSchema(
            id=self.id,
            name=self.name,
            service_id=self.service_id,
            service_type=self.service_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )