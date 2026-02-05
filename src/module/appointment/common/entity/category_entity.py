from sqlalchemy import (Column,
                        String, Text
                        )

from common.appointment.schema.category_schema import CategorySchema
from common.lib.base_entity import BaseEntity


class CategoryEntity(BaseEntity):
    __tablename__ = 'categories'

    name = Column(String(1028), nullable=False)

    def convert_to_schema(self):
        return CategorySchema(
            **self.__dict__
        )