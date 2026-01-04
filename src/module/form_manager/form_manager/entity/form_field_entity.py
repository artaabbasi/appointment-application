from sqlalchemy import Column, String, ARRAY, Integer, Boolean

from common.form_manager.schema.form_field_schema import FormFieldSchema
from common.lib.base_entity import BaseEntity


class FormFieldEntity(BaseEntity):
    __tablename__ = "form_field"

    form_id = Column(String(64), nullable=False)
    field_type = Column(String(64), nullable=False)
    attachment_files = Column(ARRAY(String(64)), nullable=True)
    title = Column(String(1024), nullable=False)
    description = Column(String(1024), nullable=True)
    min_length = Column(Integer, nullable=True)
    max_length = Column(Integer, nullable=True)
    is_required = Column(Boolean, nullable=False, default=False)

    def convert_to_schema(self):
        return FormFieldSchema(
            id=self.id,
            field_type=self.field_type,
            attachment_files=self.attachment_files,
            title=self.title,
            description=self.description,
            min_length=self.min_length,
            max_length=self.max_length,
            is_required=self.is_required,
        )
