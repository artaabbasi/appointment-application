from sqlalchemy import (Column,
                        String, Text
                        )

from common.appointment.schema.service_category_schema import ServiceCategorySchema
from common.lib.base_entity import BaseEntity


class ServiceCategoryEntity(BaseEntity):
    __tablename__ = 'service_categories'

    category_id = Column(String(64), nullable=True)
    service_id = Column(String(64), nullable=True)


    def convert_to_schema(self):
        return ServiceCategorySchema(
            **self.__dict__
        )