from fastapi import APIRouter, Depends, Body, Path

from common.form_manager.schema.form_change_log_schema import FormChangeLogSchema
from common.form_manager.schema.form_create_schema import FormCreateSchema
from common.form_manager.schema.form_schema import FormSchema
from common.form_manager.schema.user_form_answer_create_schema import UserFormAnswerCreateSchema
from common.form_manager.schema.user_form_change_log_schema import UserFormChangeLogSchema
from common.form_manager.schema.user_form_schema import UserFormSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseSingleSchema, GenericResponseListSchema
from module.form_manager.form_manager.service.form_service import FormService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

router = APIRouter(prefix='/form-manager',
                   tags=['Form Manager'],
                   responses={
                   }
                   )


@router.post('/form', response_model=GenericResponseSingleSchema[FormSchema])
async def create_form(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        data: FormCreateSchema = Body(...)
):
    result = await FormService().import_form(current_user.user_id, data)
    return GenericResponseSingleSchema[FormSchema].return_response(result)


@router.get('/form/{form_id}', response_model=GenericResponseSingleSchema[FormSchema])
async def get_form(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        form_id: str = Path(...)
):
    result = await FormService().get_form(form_id)
    return GenericResponseSingleSchema[FormSchema].return_response(result)

@router.delete('/form/{form_id}', response_model=None)
async def delete_form(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        form_id: str = Path(...)
):
    result = await FormService().delete_form(form_id)
    return None


@router.post('/form/user-form', response_model=GenericResponseSingleSchema[UserFormSchema])
async def create_user_form(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        data: UserFormAnswerCreateSchema = Body(...)
):
    result = await FormService().create_form_answer(current_user.user_id, data)
    return GenericResponseSingleSchema[UserFormSchema].return_response(result)


@router.get('/form/user-form/{user_form_id}', response_model=GenericResponseSingleSchema[UserFormSchema])
async def get_user_form(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        user_form_id: str = Path(...)
):
    result = await FormService().get_user_form_by_id(user_form_id)
    return GenericResponseSingleSchema[UserFormSchema].return_response(result)

@router.delete('/form/user-form/{user_form_id}', response_model=GenericResponseSingleSchema[UserFormSchema])
async def delete_user_form(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        user_form_id: str = Path(...)
):
    result = await FormService().delete_user_form_by_id(user_form_id)
    return GenericResponseSingleSchema[UserFormSchema].return_response(result)

@router.get('/form/logs/{form_id}', response_model=GenericResponseListSchema[FormChangeLogSchema])
async def get_form_change_logs(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        form_id: str = Path(...)
):
    result = await FormService().get_form_changes_by_form_id(form_id)
    return GenericResponseListSchema[FormChangeLogSchema].return_response(result)

@router.get('/form/user-form/logs/{user_form_id}', response_model=GenericResponseListSchema[UserFormChangeLogSchema])
async def get_user_form_change_logs(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        user_form_id: str = Path(...)
):
    result = await FormService().get_user_form_changes_by_user_form_id(user_form_id)
    return GenericResponseListSchema[UserFormChangeLogSchema].return_response(result)
