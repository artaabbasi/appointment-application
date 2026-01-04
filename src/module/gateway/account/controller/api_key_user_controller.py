from typing import Optional

from fastapi import (APIRouter,
                     Depends, Path, Body
                     )

from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.api_key_schema import ApiKeyUserSchema
from common.account.schema.api_key_user_create_schema import ApiKeyUserCreateSchema
from common.schema.response_base_schema import GenericResponseListSchema, GenericResponseSingleSchema
from common.schema.pagination_schema import PaginationSchema
from common.settings import get_settings
from module.account.user.entity import UserEntity
from module.account.user.service.api_key_service import ApiKeyUserService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/api-key-user',
                   tags=['ApiKey User'],
                   responses={
                   }
                   )


@router.get('/list', response_model=GenericResponseListSchema[ApiKeyUserSchema])
async def get_users_list(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__list)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = None,
):
    filters = {UserEntity.group: UserGroupEnum.api_key}

    result = await (ApiKeyUserService().
                    get_user_list(page=pagination_query.page, size=pagination_query.size, filters=filters,
                                  search=search))
    count = await (ApiKeyUserService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[ApiKeyUserSchema].return_response(result,
                                                                      page=pagination_query.page,
                                                                      size=pagination_query.size,
                                                                      count=count)


@router.post('/create', response_model=GenericResponseSingleSchema[ApiKeyUserSchema])
async def create_admin(
        admin: ApiKeyUserCreateSchema = Body(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__create)),
):
    result = await (ApiKeyUserService().create_user(admin))
    return GenericResponseSingleSchema[ApiKeyUserSchema].return_response(result)


@router.patch('/{user_id}', response_model=GenericResponseSingleSchema[ApiKeyUserSchema])
async def update_admin(
        user_id:  str = Path(...),
        admin: ApiKeyUserCreateSchema = Body(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__update)),
):
    result = await (ApiKeyUserService().update_user(user_id, admin))
    return GenericResponseSingleSchema[ApiKeyUserSchema].return_response(result)


@router.get('/{user_id}', response_model=GenericResponseSingleSchema[ApiKeyUserSchema])
async def get_admin(
        user_id:  str = Path(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__update)),
):
    result = await (ApiKeyUserService().get_user_by_id(user_id))
    return GenericResponseSingleSchema[ApiKeyUserSchema].return_response(result)


@router.delete('/{user_id}', response_model=None, status_code=204)
async def delete_admin(
        user_id:  str = Path(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__delete)),
):
    await (ApiKeyUserService().delete_user(user_id))
    return

