from sqlalchemy import (Column,
                        String, Text, DateTime,
                        )

from common.appointment.schema.cart_schema import CartSchema
from common.lib.base_entity import BaseEntity


class CartEntity(BaseEntity):
    __tablename__ = 'carts'

    user_id = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    valid_to = Column(DateTime(timezone=True), nullable=False)


    def convert_to_schema(self):
        return CartSchema(
            **self.__dict__
        )