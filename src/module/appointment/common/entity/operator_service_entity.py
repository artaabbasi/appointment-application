from sqlalchemy import (Column,
                        String, Text
                        )

from common.appointment.schema.operator_service_schema import OperatorServiceSchema
from common.lib.base_entity import BaseEntity


class OperatorServiceEntity(BaseEntity):
    __tablename__ = 'operator_services'

    operator_id = Column(String(64), nullable=True)
    service_id = Column(String(64), nullable=True)


    def convert_to_schema(self):
        return OperatorServiceSchema(
            **self.__dict__
        )