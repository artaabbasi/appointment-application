from common.appointment.schema.cart_item_in_schema import CartItemInSchema
from common.appointment.schema.cart_item_schema import CartItemSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.cart_item_entity import CartItemEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.cart_item_repository import CartItemRepository


class CartItemService(BaseCRUDService):
    def __init__(self):
        super().__init__(CartItemRepository, CartItemEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_cart_item_by_id(self, cart_item_id: str) -> CartItemSchema:
        cart_item = await self.repository.fetch_by_id(cart_item_id)
        return cart_item.convert_to_schema()

    async def get_cart_item_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[CartItemSchema]:
        specialities = await self._list(page, size, filters, search)
        return [cart_item.convert_to_schema() for cart_item in specialities]

    async def update_cart_item(self, entity_id: str, schema: CartItemInSchema) -> CartItemSchema:
        cart_item = await self._update_by_id(schema, entity_id, is_partial=True)
        return cart_item.convert_to_schema()

    async def delete_cart_item(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_cart_item(self, data_in: CartItemInSchema) -> CartItemSchema:
        cart_item = await self.repository.create(
            CartItemEntity(
                cart_id=data_in.cart_id,
                service_id=data_in.service_id,
                operator_id=data_in.operator_id,
                from_datetime=data_in.from_datetime,
                to_datetime=data_in.to_datetime,
            )
        )
        return cart_item.convert_to_schema()
