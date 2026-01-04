from sqlalchemy import Column, String, Text

from common.lib.base_entity import BaseEntity


class UserFormEntity(BaseEntity):
    __tablename__ = 'user_form'

    user_id = Column(String(64), nullable=False)
    form_id = Column(String(64), nullable=False)

    def convert_to_schema(self):
        pass
