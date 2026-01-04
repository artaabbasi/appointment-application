from typing import Optional

from fastapi import (APIRouter,
                     Depends, Path, Body
                     )

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.admin_create_schema import AdminCreateSchema
from common.account.schema.admin_register_schema import AdminRegisterSchema
from common.account.schema.admin_schema import AdminUserSchema
from common.schema.response_base_schema import GenericResponseListSchema, GenericResponseSingleSchema
from common.schema.pagination_schema import PaginationSchema
from common.settings import get_settings
from module.account.user.entity import UserEntity, StaffEntity
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.service import AdminService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/admin',
                   tags=['User'],
                   responses={
                   }
                   )


@router.get('/list', response_model=GenericResponseListSchema[AdminUserSchema])
async def get_users_list(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__list)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = None,
        role: Optional[AdminRolesEnum] = None,
        role_id: Optional[str] = None,
        agent_code: Optional[int] = None,
        branch_code: Optional[int] = None,
        expert_code: Optional[int] = None,
        has_internal_tel: Optional[bool] = None,
):
    filters = {UserEntity.group: UserGroupEnum.admin}
    if role is not None:
        filters.update({StaffEntity.role: role})
    if agent_code is not None:
        filters.update({ProfileEntity.agent_code: agent_code})
    if branch_code is not None:
        filters.update({ProfileEntity.branch_code: branch_code})
    if expert_code is not None:
        filters.update({ProfileEntity.expert_code: expert_code})
    if role_id is not None:
        filters.update({"role_id": role_id})
    if has_internal_tel is not None:
        filters.update({"has_internal_tel": has_internal_tel})
    result = await (AdminService().
                    get_user_list(page=pagination_query.page, size=pagination_query.size, filters=filters,
                                  search=search))
    count = await (AdminService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[AdminUserSchema].return_response(result,
                                                                      page=pagination_query.page,
                                                                      size=pagination_query.size,
                                                                      count=count)


@router.post('/create', response_model=GenericResponseSingleSchema[AdminUserSchema])
async def create_admin(
        admin: AdminCreateSchema,
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__create)),
):
    result = await (AdminService().create_user(admin))
    return GenericResponseSingleSchema[AdminUserSchema].return_response(result)


@router.patch('/{user_id}', response_model=GenericResponseSingleSchema[AdminUserSchema])
async def update_admin(
        user_id:  str = Path(...),
        admin: AdminRegisterSchema = Body(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__update)),
):
    result = await (AdminService().update_user(user_id, admin))
    return GenericResponseSingleSchema[AdminUserSchema].return_response(result)


@router.get('/{user_id}', response_model=GenericResponseSingleSchema[AdminUserSchema])
async def get_admin(
        user_id:  str = Path(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__update)),
):
    result = await (AdminService().get_user_by_id(user_id))
    return GenericResponseSingleSchema[AdminUserSchema].return_response(result)


@router.delete('/{user_id}', response_model=None, status_code=204)
async def delete_admin(
        user_id:  str = Path(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__delete)),
):
    await (AdminService().delete_user(user_id))
    return

