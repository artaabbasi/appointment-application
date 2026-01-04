from datetime import datetime
from typing import Optional

from fastapi import (APIRouter,
                     Depends,
                     Response, Path, Body, Query
                     )

from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.not_detailed_user_schema import NotDetailedUserSchema
from common.account.schema.profile_update_schema import ProfileUpdateSchema
from common.account.schema.user_schema import CustomerUserSchema
from common.config.output_type_enum import OutputTypeEnum
from common.schema.response_base_schema import GenericResponseListSchema, GenericResponseSingleSchema
from common.schema.pagination_schema import PaginationSchema
from common.settings import get_settings
from module.account.user.entity import UserEntity
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.service import CustomerService, CustomerAuthService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/customer',
                   tags=['User'],
                   responses={
                   }
                   )

@router.post('/get_user_by_phone_number', response_model=GenericResponseSingleSchema[CustomerUserSchema])
async def get_customer(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__list)),
        phone_number: str = Body(..., embed=True)
):
    result = await CustomerAuthService().get_or_create_user_schema(phone_number)
    return GenericResponseSingleSchema[CustomerUserSchema].return_response(result)


@router.get('/list', response_model=GenericResponseListSchema[CustomerUserSchema])
async def get_users_list(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__list)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
):
    filters = {UserEntity.group: UserGroupEnum.customer}
    if created_from:
        filters.update({"created_from": created_from})
    if created_to:
        filters.update({"created_to": created_to})

    result = await (CustomerService().
                    get_user_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (CustomerService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[CustomerUserSchema].return_response(result,
                                                                         page=pagination_query.page,
                                                                         size=pagination_query.size,
                                                                         count=count)


@router.patch('/{user_id}', response_model=GenericResponseSingleSchema[CustomerUserSchema])
async def update_customer(
        user_id:  str = Path(...),
        customer: ProfileUpdateSchema = Body(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__update_profile)),
):
    result = await (CustomerService().update_user(user_id, customer))
    return GenericResponseSingleSchema[CustomerUserSchema].return_response(result)


@router.delete('/{user_id}', response_model=None, status_code=204)
async def delete_customer(
        user_id:  str = Path(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__delete)),
):
    await (CustomerService().delete_user(user_id))
    return
