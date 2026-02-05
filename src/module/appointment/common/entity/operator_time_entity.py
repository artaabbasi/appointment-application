from sqlalchemy import (Column,
                        String, Text, DateTime,
                        )

from common.appointment.schema.operator_time_schema import OperatorTimeSchema
from common.lib.base_entity import BaseEntity


class OperatorTimeEntity(BaseEntity):
    __tablename__ = 'operator_times'

    operator_id = Column(String(64), nullable=True)
    from_datetime = Column(DateTime(timezone=True), nullable=False)
    to_datetime = Column(DateTime(timezone=True), nullable=False)


    def convert_to_schema(self):
        return OperatorTimeSchema(
            **self.__dict__
        )