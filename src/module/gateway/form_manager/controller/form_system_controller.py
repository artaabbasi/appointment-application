from typing import Optional, List

from fastapi import APIRouter, Depends, Body, Path, Query, Response

from common.account.schema.role_schema import RoleSchema
from common.form_manager.enum.form_instance_usage_type_enum import FormInstanceUsageTypeEnum
from common.form_manager.schema.form_instance_assignment_in_schema import FormInstanceAssignmentInSchema
from common.form_manager.schema.form_instance_assignment_schema import FormInstanceAssignmentSchema
from common.form_manager.schema.form_instance_assignment_user_in_schema import FormInstanceAssignmentUserInSchema
from common.form_manager.schema.form_instance_assignment_user_schema import FormInstanceAssignmentUserSchema
from common.form_manager.schema.form_instance_in_schema import FormInstanceInSchema
from common.form_manager.schema.form_instance_schema import FormInstanceSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseSingleSchema, GenericResponseListSchema
from module.form_manager.form_system.entity.form_instance_assignment_entity import FormInstanceAssignmentEntity
from module.form_manager.form_system.entity.form_instance_assignment_user_entity import FormInstanceAssignmentUserEntity
from module.form_manager.form_system.entity.form_instance_entity import FormInstanceEntity
from module.form_manager.form_system.service.form_instance_assignment_service import FormInstanceAssignmentService
from module.form_manager.form_system.service.form_instance_assignment_user_service import \
    FormInstanceAssignmentUserService
from module.form_manager.form_system.service.form_instance_service import FormInstanceService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

router = APIRouter(prefix='/form-system',
                   tags=['Form System'],
                   responses={
                   }
                   )


@router.get('/form-instance', response_model=GenericResponseListSchema[FormInstanceSchema])
async def get_form_instances(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__form_read)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),
        form_id : Optional[str] = Query(None),
        usage_type : Optional[FormInstanceUsageTypeEnum] = Query(None),
):
    filters = {}
    if form_id is not None:
        filters.update({FormInstanceEntity.form_id: form_id})
    if usage_type is not None:
        filters.update({FormInstanceEntity.usage_type: usage_type})

    result = await FormInstanceService().get_form_instance_list(
        page=pagination_query.page, size=pagination_query.size, filters=filters, search=search)
    count = await FormInstanceService().get_count(filters=filters, search=search)
    return GenericResponseListSchema[FormInstanceSchema].return_response(result,
                                                                          page=pagination_query.page,
                                                                          size=pagination_query.size,
                                                                          count=count)

@router.post('/form-instance', response_model=GenericResponseSingleSchema[FormInstanceSchema])
async def create_form_instance(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__form_create)),
        data: FormInstanceInSchema = Body(...)
):
    result = await FormInstanceService().create_form_instance(current_user.user_id, data)
    return GenericResponseSingleSchema[FormInstanceSchema].return_response(result)


@router.get('/form-instance/assignment', response_model=GenericResponseListSchema[FormInstanceAssignmentSchema])
async def get_form_instance_assignments(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),
        form_instance_id: Optional[str] = Query(None),
):
    filters = {}
    if form_instance_id is not None:
        filters.update({FormInstanceAssignmentEntity.form_instance_id: form_instance_id})

    result = await FormInstanceAssignmentService().get_form_instance_assignment_list(
        page=pagination_query.page, size=pagination_query.size, filters=filters, search=search)
    count = await FormInstanceAssignmentService().get_count(filters=filters, search=search)
    return GenericResponseListSchema[FormInstanceAssignmentSchema].return_response(result,
                                                                          page=pagination_query.page,
                                                                          size=pagination_query.size,
                                                                          count=count)

@router.post('/form-instance/assignment', response_model=GenericResponseSingleSchema[FormInstanceAssignmentSchema])
async def create_form_instance_assignment(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        data: FormInstanceAssignmentInSchema = Body(...)
):
    result = await FormInstanceAssignmentService().create_form_instance_assignment(current_user.user_id, data)
    return GenericResponseSingleSchema[FormInstanceAssignmentSchema].return_response(result)


@router.get('/form-instance/{form_instance_id}', response_model=GenericResponseSingleSchema[FormInstanceSchema])
async def get_form_instance(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__form_create)),
        form_instance_id: str = Path(...)
):
    result = await FormInstanceService().get_by_id(form_instance_id)
    return GenericResponseSingleSchema[FormInstanceSchema].return_response(result)

@router.patch('/form-instance/{form_instance_id}', response_model=None)
async def update_form_instance(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__form_create)),
        form_instance_id: str = Path(...),
        data: FormInstanceInSchema = Body(...)
):
    result = await FormInstanceService().update_form_instance(form_instance_id, data)
    return None

@router.delete('/form-instance/{form_instance_id}', response_model=None)
async def delete_form_instance(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__form_create)),
        form_instance_id: str = Path(...)
):
    result = await FormInstanceService().delete_form_instance(form_instance_id)
    return None

@router.get('/form-instance/assignment/user', response_model=GenericResponseListSchema[FormInstanceAssignmentUserSchema])
async def get_form_instance_assignment_users(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_read)),
        pagination_query: PaginationSchema = Depends(),
        form_instance_assignment_id: Optional[str] = Query(None),
        user_id: Optional[str] = Query(None),
        assigned_from_role_id: Optional[str] = Query(None),
        user_form_id_is_null: Optional[bool] = Query(None),
):
    filters = {}
    if form_instance_assignment_id is not None:
        filters.update({FormInstanceAssignmentUserEntity.form_instance_assignment_id: form_instance_assignment_id})
    if user_id is not None:
        filters.update({FormInstanceAssignmentUserEntity.user_id: user_id})
    if assigned_from_role_id is not None:
        filters.update({FormInstanceAssignmentUserEntity.assigned_from_role_id: assigned_from_role_id})
    if user_form_id_is_null is not None:
        filters.update({"user_form_id_is_null": user_form_id_is_null})

    result = await FormInstanceAssignmentUserService().get_form_instance_assignment_user_list(
        page=pagination_query.page, size=pagination_query.size, filters=filters)
    count = await FormInstanceAssignmentUserService().get_count(filters=filters)
    return GenericResponseListSchema[FormInstanceAssignmentUserSchema].return_response(result,
                                                                          page=pagination_query.page,
                                                                          size=pagination_query.size,
                                                                          count=count)

@router.get('/form-instance/assignment/user_excel_export/{form_instance_assignment_id}')
async def get_form_instance_assignment_users(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_read)),
        form_instance_assignment_id: Optional[str] = Path(...),
        user_id: Optional[str] = Query(None),
        assigned_from_role_id: Optional[str] = Query(None),
):
    filters = {}
    if user_id is not None:
        filters.update({FormInstanceAssignmentUserEntity.user_id: user_id})
    if assigned_from_role_id is not None:
        filters.update({FormInstanceAssignmentUserEntity.assigned_from_role_id: assigned_from_role_id})
    output_stream = await FormInstanceAssignmentUserService().form_instance_assignment_user_list_excel_export(form_instance_assignment_id, filters=filters)
    response = Response(content=output_stream.read(),
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = f"attachment; filename=form_answers_{form_instance_assignment_id}.xlsx"
    return response

@router.get('/form-instance/assignment/user_assign_roles/{form_instance_assignment_id}', response_model=GenericResponseListSchema[RoleSchema])
async def get_form_instance_assignment_users(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_read)),
        form_instance_assignment_id: str = Path(...)

):
    result = await FormInstanceAssignmentUserService().get_assigned_roles_by_form_instance_assignment_id(form_instance_assignment_id)
    return GenericResponseListSchema[RoleSchema].return_response(result)

@router.post('/form-instance/assignment/user', response_model=GenericResponseSingleSchema[FormInstanceAssignmentUserSchema])
async def create_form_instance_assignment_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_create)),
        form_instance_assignment_id: str = Body(...),
        assign_to_user_ids: List[str] = Body(None),
        assign_to_role_ids: List[str] = Body(None),
):
    result = await FormInstanceAssignmentUserService().create_multi_form_instance_assignment_users(
        form_instance_assignment_id=form_instance_assignment_id,
        assign_to_user_ids=assign_to_user_ids,
        assign_to_role_ids=assign_to_role_ids,
    )
    return GenericResponseSingleSchema[FormInstanceAssignmentUserSchema].return_response(result)

@router.get('/form-instance/assignment/{form_instance_assignment_id}', response_model=GenericResponseSingleSchema[FormInstanceAssignmentSchema])
async def get_form_instance_assignment(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_create)),
        form_instance_assignment_id: str = Path(...)
):
    result = await FormInstanceAssignmentService().get_by_id(form_instance_assignment_id)
    return GenericResponseSingleSchema[FormInstanceAssignmentSchema].return_response(result)

@router.patch('/form-instance/assignment/{form_instance_assignment_id}', response_model=None)
async def update_form_instance_assignment(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_create)),
        form_instance_assignment_id: str = Path(...),
        data: FormInstanceAssignmentInSchema = Body(...)
):
    result = await FormInstanceAssignmentService().update_form_instance_assignment(form_instance_assignment_id, data)
    return None

@router.delete('/form-instance/assignment/{form_instance_assignment_id}', response_model=None)
async def delete_form_instance_assignment(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_create)),
        form_instance_assignment_id: str = Path(...)
):
    result = await FormInstanceAssignmentService().delete_form_instance_assignment(form_instance_assignment_id)
    return None

@router.get('/form-instance/assignment/user/{form_instance_assignment_user_id}', response_model=GenericResponseSingleSchema[FormInstanceAssignmentUserSchema])
async def get_form_instance_assignment_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_create)),
        form_instance_assignment_user_id: str = Path(...)
):
    result = await FormInstanceAssignmentUserService().get_by_id(form_instance_assignment_user_id)
    return GenericResponseSingleSchema[FormInstanceAssignmentUserSchema].return_response(result)

@router.delete('/form-instance/assignment/user/{form_instance_assignment_user_id}', response_model=None)
async def delete_form_instance_assignment_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__manage_requests_create)),
        form_instance_assignment_user_id: str = Path(...)
):
    result = await FormInstanceAssignmentUserService().delete_form_instance_assignment_user(form_instance_assignment_user_id)
    return None
