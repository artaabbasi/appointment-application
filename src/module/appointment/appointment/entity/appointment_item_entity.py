from sqlalchemy import (Column,
                        String, Text, DateTime, Boolean
                        )

from common.appointment.schema.appointment_item_schema import AppointmentItemSchema
from common.lib.base_entity import BaseEntity


class AppointmentItemEntity(BaseEntity):
    __tablename__ = 'appointment_items'

    appointment_id = Column(String(64), nullable=False)
    service_id = Column(String(64), nullable=False)
    operator_id = Column(String(64), nullable=False)
    from_datetime = Column(DateTime(timezone=True), nullable=False)
    to_datetime = Column(DateTime(timezone=True), nullable=False)
    is_cancelled = Column(Boolean, nullable=True, default=False)

    def convert_to_schema(self):
        return AppointmentItemSchema(
            **self.__dict__
        )