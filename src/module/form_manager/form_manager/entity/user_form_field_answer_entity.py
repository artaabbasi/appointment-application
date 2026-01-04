from sqlalchemy import Column, String, Text, ARRAY

from common.lib.base_entity import BaseEntity


class UserFormFieldAnswerEntity(BaseEntity):
    __tablename__ = 'user_form_field_answer'

    user_form_id = Column(String(64), nullable=False)
    form_field_id = Column(String(64), nullable=False)
    answer = Column(Text, nullable=True)
    attachment_files = Column(ARRAY(String(64)), nullable=True)

    def convert_to_schema(self):
        pass
