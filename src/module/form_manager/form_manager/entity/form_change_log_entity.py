from sqlalchemy import Column, String, Integer, Text, Boolean, BigInteger, JSON
from sqlalchemy.dialects.postgresql import ARRAY

from common.form_manager.schema.form_change_log_schema import FormChangeLogSchema
from common.lib.base_entity import BaseEntity


class FormChangeLogEntity(BaseEntity):
    __tablename__ = 'form_change_log'

    user_id = Column(String(64), nullable=False)
    form_id = Column(String(64), nullable=False)
    last_fields = Column(ARRAY(JSON), nullable=True)
    new_fields = Column(ARRAY(JSON), nullable=True)


    def convert_to_schema(self):
        return FormChangeLogSchema(
            **self.__dict__
        )