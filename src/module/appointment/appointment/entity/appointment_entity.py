from sqlalchemy import (Column,
                        String, Text, Boolean, DateTime,
                        )

from common.appointment.schema.appointment_schema import AppointmentSchema
from common.lib.base_entity import BaseEntity


class AppointmentEntity(BaseEntity):
    __tablename__ = 'appointments'

    user_id = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    is_cancelled = Column(Boolean, nullable=True, default=False)
    cancelled_at = Column(DateTime, nullable=True)
    cancelled_by_id = Column(String(64), nullable=True)

    def convert_to_schema(self):
        return AppointmentSchema(
            **self.__dict__
        )