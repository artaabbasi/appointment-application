from datetime import timedelta
from math import ceil

from common.appointment.enum.deposit_type_enum import DepositTypeEnum
from common.appointment.schema.appointment_in_schema import AppointmentInSchema
from common.appointment.schema.appointment_item_in_schema import AppointmentItemInSchema
from common.appointment.schema.appointment_schema import AppointmentSchema
from common.appointment.schema.cart_in_schema import CartInSchema
from common.appointment.schema.cart_schema import CartSchema
from common.appointment.schema.deposit_schema import DepositSchema
from common.exceptions import NotFoundException, BadRequestException
from common.lib.service_action_enum import ServiceActionEnum
from module.gateway.enum.error_code_enum import ErrorCodeEnum
from util.timestamp import DatetimeUtil
from .appointment_item_service import AppointmentItemService
from .appointment_service import AppointmentService
from .cart_item_service import CartItemService
from ..entity.cart_entity import CartEntity
from common.lib.base_crud_service import BaseCRUDService
from ..entity.cart_item_entity import CartItemEntity
from ..repository.cart_repository import CartRepository
from ...common.service.service_service import ServiceService


class CartService(BaseCRUDService):
    def __init__(self):
        super().__init__(CartRepository, CartEntity,
                         ServiceActionEnum.FROM_IMPLEMENTED_REPOSITORY)
        self.appointment_service = AppointmentService()
        self.appointment_item_service = AppointmentItemService()
        self.cart_item_service = CartItemService()
        self.service_service = ServiceService()

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

    async def get_user_active_cart(self, user_id: str) -> CartSchema:
        cart = await self.repository.fetch_active_by_user_id(user_id)
        return cart.convert_to_schema()

    async def get_or_create_user_active_cart(self, user_id: str) -> CartSchema:
        try:
            cart = await self.get_user_active_cart(user_id)
        except NotFoundException:
            cart = await self.create_cart(CartInSchema(user_id=user_id,
                                                       valid_to=DatetimeUtil.utc_now_datetime() + timedelta(seconds=self._get_settings().CART_VALID_SECS)))
        return cart

    async def make_appointment_from_cart(self, cart_id: str) -> AppointmentSchema:
        cart = await self.repository.fetch_by_id(cart_id)
        if not cart.valid_to >= DatetimeUtil.utc_now_datetime() :
            raise BadRequestException(ErrorCodeEnum.INVALID_CART)

        cart_items = await self.cart_item_service.get_cart_item_list(page=1, size=-1, filters={CartItemEntity.cart_id: cart_id})
        appointment = await self.appointment_service.create_appointment(AppointmentInSchema(
            user_id=cart.user_id,
            description=cart.description,
        ))
        for cart_item in cart_items:
            await self.appointment_item_service.create_appointment_item(
                AppointmentItemInSchema(
                    appointment_id=appointment.id,
                    service_id=cart_item.service_id,
                    operator_id=cart_item.operator_id,
                    from_datetime=cart_item.from_datetime,
                    to_datetime=cart_item.to_datetime,
                )
            )
        cart.valid_to = appointment.created_at
        await self.repository.update(cart)
        return appointment

    async def calc_cart_deposit(self, cart_id: str) -> DepositSchema:
        cart = await self.repository.fetch_by_id(cart_id)
        if not cart.valid_to >= DatetimeUtil.utc_now_datetime() :
            raise BadRequestException(ErrorCodeEnum.INVALID_CART)

        cart_items = await self.cart_item_service.get_cart_item_list(page=1, size=-1, filters={CartItemEntity.cart_id: cart_id})
        price = 0
        for cart_item in cart_items:
            service = await self.service_service.get_service_by_id(cart_item.service_id)
            if not (service.deposit_amount and service.price_as_rial):
                continue
            if service.deposit_type == DepositTypeEnum.ABSOLUTE:
                price += service.deposit_amount
            else:
                price += ceil((service.deposit_amount * service.price_as_rial) / 100)
        return DepositSchema(
            amount=price
        )
