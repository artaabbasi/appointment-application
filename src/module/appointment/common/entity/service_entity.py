from sqlalchemy import (Column,
                        String, Integer,
                        )

from common.appointment.schema.service_schema import ServiceSchema
from common.lib.base_entity import BaseEntity


class ServiceEntity(BaseEntity):
    __tablename__ = 'services'

    main_service_id = Column(String(64), nullable=False)
    name = Column(String(1028), nullable=False)
    duration = Column(Integer, nullable=False)


    def convert_to_schema(self):
        return ServiceSchema(
            **self.__dict__
        )