from sqlalchemy import Column, String, ARRAY, Integer, Boolean

from common.lib.base_entity import BaseEntity
from common.form_manager.schema.form_field_choice_schema import FormFieldChoiceSchema


class FormFieldChoiceEntity(BaseEntity):
    __tablename__ = "form_field_choice"

    field_id = Column(String(64), nullable=False)
    attachment_files = Column(ARRAY(String(64)), nullable=True)
    description = Column(String(1024), nullable=True)

    def convert_to_schema(self):
        return FormFieldChoiceSchema(
            id=self.id,
            attachment_files=self.attachment_files,
            description=self.description,
        )
