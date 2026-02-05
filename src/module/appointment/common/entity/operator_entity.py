from sqlalchemy import (Column,
                        String, Text,
                        )

from common.appointment.schema.operator_schema import OperatorSchema
from common.lib.base_entity import BaseEntity


class OperatorEntity(BaseEntity):
    __tablename__ = 'operators'

    user_id = Column(String(64), nullable=True)
    name = Column(String(1028), nullable=False)
    description = Column(Text, nullable=True)

    def convert_to_schema(self):
        return OperatorSchema(
            **self.__dict__
        )