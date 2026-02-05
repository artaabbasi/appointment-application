from common.appointment.schema.cart_in_schema import CartInSchema
from common.appointment.schema.cart_schema import CartSchema
from common.lib.service_action_enum import ServiceActionEnum
from ..entity.cart_entity import CartEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.cart_repository import CartRepository


class CartService(BaseCRUDService):
    def __init__(self):
        super().__init__(CartRepository, CartEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)

    async def get_cart_by_id(self, cart_id: str) -> CartSchema:
        cart = await self.repository.fetch_by_id(cart_id)
        return cart.convert_to_schema()

    async def get_cart_list(self, page: int = 1, size: int = 10, filters: dict = None, search: str = None) \
            -> list[CartSchema]:
        specialities = await self._list(page, size, filters, search)
        return [cart.convert_to_schema() for cart in specialities]

    async def update_cart(self, entity_id: str, schema: CartInSchema) -> CartSchema:
        cart = await self._update_by_id(schema, entity_id, is_partial=True)
        return cart.convert_to_schema()

    async def delete_cart(self, entity_id: str) -> None:
        return await self._delete_by_id(entity_id)

    async def create_cart(self, data_in: CartInSchema) -> CartSchema:
        cart = await self.repository.create(
            CartEntity(
                user_id=data_in.user_id,
                description=data_in.description,
                valid_to=data_in.valid_to,
            )
        )
        return cart.convert_to_schema()
