from sqlalchemy import (Column,
                        String, Text,
                        )

from common.appointment.schema.appointment_schema import AppointmentSchema
from common.lib.base_entity import BaseEntity


class AppointmentEntity(BaseEntity):
    __tablename__ = 'appointments'

    user_id = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)

    def convert_to_schema(self):
        return AppointmentSchema(
            **self.__dict__
        )