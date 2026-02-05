from sqlalchemy import (Column,
                        String,
                        )

from common.appointment.schema.main_service_schema import MainServiceSchema
from common.lib.base_entity import BaseEntity


class MainServiceEntity(BaseEntity):
    __tablename__ = 'main_services'

    name = Column(String(1028), nullable=False)

    def convert_to_schema(self):
        return MainServiceSchema(
            **self.__dict__
        )