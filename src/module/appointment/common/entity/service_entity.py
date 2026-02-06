from sqlalchemy import (Column,
                        String, Integer, Text, Boolean,
                        )

from common.appointment.schema.service_schema import ServiceSchema
from common.lib.base_entity import BaseEntity


class ServiceEntity(BaseEntity):
    __tablename__ = 'services'

    main_service_id = Column(String(64), nullable=False)
    name = Column(String(1028), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    price_as_rial = Column(Integer, nullable=True)
    deposit_type = Column(String(64), nullable=True)
    deposit_amount = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False)


    def convert_to_schema(self):
        return ServiceSchema(
            **self.__dict__
        )