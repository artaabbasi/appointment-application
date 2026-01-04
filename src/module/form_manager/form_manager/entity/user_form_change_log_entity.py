from sqlalchemy import Column, String, Integer, Text, Boolean, BigInteger, JSON
from sqlalchemy.dialects.postgresql import ARRAY

from common.form_manager.schema.user_form_change_log_schema import UserFormChangeLogSchema
from common.lib.base_entity import BaseEntity


class UserFormChangeLogEntity(BaseEntity):
    __tablename__ = 'user_form_change_log'

    user_id = Column(String(64), nullable=False)
    user_form_id = Column(String(64), nullable=False)
    last_answers = Column(ARRAY(JSON), nullable=True)
    new_answers = Column(ARRAY(JSON), nullable=True)


    def convert_to_schema(self):
        return UserFormChangeLogSchema(
            **self.__dict__
        )