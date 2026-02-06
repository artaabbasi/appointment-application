from typing import Optional

from fastapi import APIRouter, Depends, Body, Path, Query

from common.appointment.schema.appointment_schema import AppointmentSchema
from common.appointment.schema.cart_item_in_schema import CartItemInSchema
from common.appointment.schema.cart_item_schema import CartItemSchema
from common.appointment.schema.cart_schema import CartSchema
from common.appointment.schema.deposit_schema import DepositSchema
from common.appointment.schema.recommended_item_schema import RecommendItemSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseSingleSchema, GenericResponseListSchema
from module.appointment.appointment.entity.cart_item_entity import CartItemEntity
from module.appointment.appointment.service.cart_item_service import CartItemService
from module.appointment.appointment.service.cart_service import CartService
from module.appointment.appointment.service.recommender_service import RecommenderService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

router = APIRouter(prefix='/appointment/cart',
                   tags=['Cart'],
                   responses={
                   }
                   )

@router.get('/get_active_cart',
              response_model=GenericResponseSingleSchema[CartSchema])
async def get_user_active_cart(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.customer_access)),
):
    result = await (CartService().
                    get_user_active_cart(current_user.user_id))
    return GenericResponseSingleSchema[CartSchema].return_response(result)

@router.get('/create_active_cart',
              response_model=GenericResponseSingleSchema[CartSchema])
async def create_user_active_cart(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.customer_access)),
):
    result = await (CartService().
                    get_or_create_user_active_cart(current_user.user_id))
    return GenericResponseSingleSchema[CartSchema].return_response(result)

@router.post('/submit_cart/{cart_id}', response_model=GenericResponseSingleSchema[AppointmentSchema])
async def submit_cart(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        cart_id: str = Path(...),
):
    result = await (CartService().
                    make_appointment_from_cart(cart_id))
    return GenericResponseSingleSchema[AppointmentSchema].return_response(result)

@router.get('/calc_cart_deposit/{cart_id}', response_model=GenericResponseSingleSchema[DepositSchema])
async def calc_cart_deposit(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        cart_id: str = Path(...),
):
    result = await (CartService().
                    calc_cart_deposit(cart_id))
    return GenericResponseSingleSchema[DepositSchema].return_response(result)

@router.get('/cart-item', response_model=GenericResponseListSchema[CartItemSchema])
async def get_cart_items(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),
        cart_id: Optional[str] = Query(None)
):
    filters = {}
    if cart_id is not None:
        filters.update({CartItemEntity.cart_id: cart_id})
    result = await (CartItemService().
                    get_cart_item_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (CartItemService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[CartItemSchema].return_response(result,
                                                                      page=pagination_query.page,
                                                                      size=pagination_query.size,
                                                                      count=count)

@router.post('/cart-item', response_model=GenericResponseSingleSchema[CartItemSchema])
async def create_cart_item(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.customer_access)),
        data_in: CartItemInSchema = Body(...),
):
    result = await (CartItemService().
                    create_cart_item(data_in))
    return GenericResponseSingleSchema[CartItemSchema].return_response(result)

@router.delete('/cart-item/{cart_item_id}', response_model=None, status_code=204)
async def delete_cart_item(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        cart_item_id: str = Path(...),
):
    result = await (CartItemService().
                    delete_cart_item(cart_item_id))
    return None

@router.get('/recommend_service/{cart_id}',
              response_model=GenericResponseListSchema[RecommendItemSchema])
async def get_recommend_services_for_cart(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.customer_access)),
        cart_id: str = Path(...),
):
    result = await (RecommenderService().
                    get_recommended_services_for_cart_id(cart_id))
    return GenericResponseListSchema[RecommendItemSchema].return_response(result)
