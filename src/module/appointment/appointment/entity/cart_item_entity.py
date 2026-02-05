from sqlalchemy import (Column,
                        String, Text, DateTime
                        )

from common.appointment.schema.cart_item_schema import CartItemSchema
from common.lib.base_entity import BaseEntity


class CartItemEntity(BaseEntity):
    __tablename__ = 'cart_items'

    cart_id = Column(String(64), nullable=False)
    service_id = Column(String(64), nullable=False)
    operator_id = Column(String(64), nullable=False)
    from_datetime = Column(DateTime(timezone=True), nullable=False)
    to_datetime = Column(DateTime(timezone=True), nullable=False)


    def convert_to_schema(self):
        return CartItemSchema(
            **self.__dict__
        )