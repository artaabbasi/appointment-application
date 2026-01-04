from typing import Optional

from fastapi import APIRouter, Depends, Body, Path, Query

from common.account.schema.modules_out_schema import ModulesOutSchema
from common.account.schema.permission_in_schema import PermissionInSchema
from common.account.schema.permission_schema import PermissionSchema
from common.account.schema.user_permission_delete_schema import UserPermissionDeleteSchema
from common.account.schema.user_permission_in_schema import UserPermissionInSchema
from common.account.schema.user_permission_schema import UserPermissionSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseListSchema, GenericResponseSingleSchema
from module.account.authorization.service.permission_service import PermissionService
from module.account.authorization.service.user_permission_service import UserPermissionService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

router = APIRouter(prefix='/permission',
                   tags=['Authorization'],
                   responses={
                   }
                   )


@router.get('/list', response_model=GenericResponseListSchema[PermissionSchema])
async def get_permissions_list(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__get)),
        pagination_query: PaginationSchema = Depends()
):
    filters = {}

    result = await (PermissionService().
                    get_permission_list(page=pagination_query.page, size=pagination_query.size, filters=filters))
    count = await (PermissionService().get_count(filters=filters))
    return GenericResponseListSchema[PermissionSchema].return_response(result,
                                                                       page=pagination_query.page,
                                                                       size=pagination_query.size,
                                                                       count=count)


@router.post('/create', response_model=GenericResponseSingleSchema[PermissionSchema])
async def create_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__create)),
        data_in: PermissionInSchema = Body(...)
):
    permission = await PermissionService().create_permission(data_in)
    return GenericResponseSingleSchema[PermissionSchema].return_response(permission)


@router.patch('/detail/{permission_id}', response_model=GenericResponseSingleSchema[PermissionSchema])
async def update_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        permission_id: str = Path(...),
        data_in: PermissionInSchema = Body(...)
):
    permission = await PermissionService().update_permission(permission_id, data_in)
    return GenericResponseSingleSchema[PermissionSchema].return_response(permission)


@router.delete('/detail/{permission_id}')
async def delete_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        permission_id: str = Path(...),
):
    _ = await PermissionService().delete_permission(permission_id)
    return None


@router.get('/user-permission', response_model=GenericResponseListSchema[UserPermissionSchema])
async def get_user_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__get)),
        user_id: Optional[str] = Query(None),
):
    permissions = await UserPermissionService().get_user_permissions(user_id if user_id is not None
                                                                     else current_user.user_id)
    return GenericResponseListSchema[UserPermissionSchema].return_response(permissions)


@router.post('/user-permission')
async def create_user_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__create)),
        data_id: UserPermissionInSchema = Body(...)
):
    _ = await UserPermissionService().create_user_permission(data_id)
    return None


@router.delete('/user-permission')
async def delete_user_permission(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__permissions__detail)),
        data_in: UserPermissionDeleteSchema = Body(...)
):
    _ = await UserPermissionService().delete_user_permission(data_in)
    return None


@router.get('/user-modules', response_model=GenericResponseListSchema[ModulesOutSchema])
async def get_user_permission(
        current_user: JWTUserSchema = Depends(
            CurrentUserUtil(action=ActionEnum.account__admins__permissions__module__get)),
        user_id: Optional[str] = Query(None),
):
    permissions = await UserPermissionService().get_user_permissions_tree(user_id if user_id is not None
                                                                          else current_user.user_id)
    return GenericResponseListSchema[ModulesOutSchema].return_response(permissions)
