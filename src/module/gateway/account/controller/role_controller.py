from typing import Optional, List

from fastapi import APIRouter, Depends, Body, Path, Query

from common.account.schema.role_in_schema import RoleInSchema
from common.account.schema.role_permission_delete_schema import RolePermissionDeleteSchema
from common.account.schema.role_permission_in_schema import RolePermissionInSchema
from common.account.schema.role_permission_schema import RolePermissionSchema
from common.account.schema.role_schema import RoleSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseListSchema, GenericResponseSingleSchema
from module.account.authorization.entity.role_entity import RoleEntity
from module.account.authorization.service.role_service import RoleService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

router = APIRouter(prefix='/role',
                   tags=['Authorization'],
                   responses={
                   }
                   )


@router.get('/list', response_model=GenericResponseListSchema[RoleSchema])
async def get_roles_list(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__list)),
        search: Optional[str] = None,
        title_is_null: Optional[bool] = None,
        show_in_site: Optional[bool] = None,
        pagination_query: PaginationSchema = Depends()
):
    filters = {}
    if title_is_null is not None:
        filters['title_is_null'] = title_is_null
    if show_in_site is not None:
        filters[RoleEntity.show_in_site] = show_in_site

    result = await (RoleService().
                    get_role_list(page=pagination_query.page, size=pagination_query.size, filters=filters,
                                  search=search))
    count = await (RoleService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[RoleSchema].return_response(result,
                                                                 page=pagination_query.page,
                                                                 size=pagination_query.size,
                                                                 count=count)


@router.post('/create', response_model=GenericResponseSingleSchema[RoleSchema])
async def create_role(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__create)),
        data_in: RoleInSchema = Body(...)
):
    role = await RoleService().create_role(data_in)
    return GenericResponseSingleSchema[RoleSchema].return_response(role)


@router.get('/detail/{role_id}', response_model=GenericResponseSingleSchema[RoleSchema])
async def get_role(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        role_id: str = Path(...)
):
    role = await RoleService().get_by_id(role_id)
    return GenericResponseSingleSchema[RoleSchema].return_response(role)


@router.patch('/detail/{role_id}', response_model=GenericResponseSingleSchema[RoleSchema])
async def update_role(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        role_id: str = Path(...),
        data_in: RoleInSchema = Body(...)
):
    role = await RoleService().update_role(role_id, data_in)
    return GenericResponseSingleSchema[RoleSchema].return_response(role)


@router.delete('/detail/{role_id}')
async def delete_role(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        role_id: str = Path(...),
):
    _ = await RoleService().delete_role(role_id)
    return None


@router.get('/user-role', response_model=GenericResponseListSchema[RoleSchema])
async def get_user_roles(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__get)),
        user_id: Optional[str] = Query(None),
):
    using_user_id = user_id if user_id is not None else current_user.user_id
    roles = await RoleService().get_user_roles(using_user_id)
    return GenericResponseListSchema[RoleSchema].return_response(roles)


@router.post('/user-role')
async def create_user_role(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__create)),
        user_ids: list[str] = Body(..., embed=True),
        role_ids: list[str] = Body(..., embed=True)
):
    _ = await RoleService().create_roles_for_users(user_ids, role_ids)
    return None

@router.post('/user-role/add')
async def create_role_for_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__create)),
        user_ids: list[str] = Body(..., embed=True),
        role_ids: list[str] = Body(..., embed=True)
):
    _ = await RoleService().add_roles_to_users(user_ids, role_ids)
    return None

@router.patch('/user-role')
async def delete_user_role(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        user_ids: list[str] = Body(..., embed=True),
        role_ids: list[str] = Body(..., embed=True)
):
    _ = await RoleService().delete_roles_for_users(user_ids, role_ids)
    return None


@router.get('/role-permission/{role_id}', response_model=GenericResponseListSchema[RolePermissionSchema])
async def get_role_permissions(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__get)),
        role_id: str = Path(...)
):
    permissions = await RoleService().get_role_permissions(role_id)
    return GenericResponseListSchema[RolePermissionSchema].return_response(permissions)


@router.post('/role-permission')
async def create_role_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__create)),
        data_in: RolePermissionInSchema = Body(...)
):
    _ = await RoleService().create_role_permission(data_in)
    return None


@router.delete('/role-permission')
async def delete_role_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        data_in: RolePermissionDeleteSchema = Body(...)
):
    _ = await RoleService().delete_role_permission(data_in)
    return None
