from common.appointment.schema.cart_item_in_schema import CartItemInSchema
from common.appointment.schema.cart_item_schema import CartItemSchema
from common.exceptions import BadRequestException
from common.lib.service_action_enum import ServiceActionEnum
from module.gateway.enum.error_code_enum import ErrorCodeEnum
from .appointment_item_service import AppointmentItemService
from ..entity.appointment_item_entity import AppointmentItemEntity
from ..entity.cart_item_entity import CartItemEntity
from common.lib.base_crud_service import BaseCRUDService
from ..repository.cart_item_repository import CartItemRepository


class CartItemService(BaseCRUDService):
    def __init__(self):
        super().__init__(CartItemRepository, CartItemEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.appointment_item_service = AppointmentItemService()

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
        this_cart_items = await self.get_cart_item_list(page=1, size=-1, filters={CartItemEntity.id: data_in.cart_id})
        for cart_item in this_cart_items:
            if cart_item.from_datetime >= data_in.from_datetime and cart_item.to_datetime <= data_in.to_datetime:
                raise BadRequestException(ErrorCodeEnum.CONFLICT_WITH_CART)
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
