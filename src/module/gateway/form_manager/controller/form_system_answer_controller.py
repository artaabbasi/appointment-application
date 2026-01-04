from typing import Optional

from fastapi import APIRouter, Depends, Body, Path, Query

from common.form_manager.schema.form_instance_assignment_schema import FormInstanceAssignmentSchema
from common.form_manager.schema.form_instance_assignment_user_answer_in_schema import \
    FormInstanceAssignmentUserAnswerInSchema
from common.form_manager.schema.form_instance_assignment_user_schema import FormInstanceAssignmentUserSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseSingleSchema, GenericResponseListSchema
from module.form_manager.form_system.entity.form_instance_assignment_entity import FormInstanceAssignmentEntity
from module.form_manager.form_system.entity.form_instance_assignment_user_entity import FormInstanceAssignmentUserEntity
from module.form_manager.form_system.entity.form_instance_entity import FormInstanceEntity
from module.form_manager.form_system.service.form_instance_assignment_service import FormInstanceAssignmentService
from module.form_manager.form_system.service.form_instance_assignment_user_service import \
    FormInstanceAssignmentUserService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil
from util.timestamp import DatetimeUtil

router = APIRouter(prefix='/form-system-answer',
                   tags=['Form System'],
                   responses={
                   }
                   )

@router.get('/assignment', response_model=GenericResponseListSchema[FormInstanceAssignmentSchema])
async def get_form_instance_assignments_for_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__my_requests)),
        pagination_query: PaginationSchema = Depends(),
):
    filters = {
        "release_to":DatetimeUtil.utc_now_datetime(),
        "deadline_from":DatetimeUtil.utc_now_datetime()
    }
    result = await FormInstanceAssignmentService().get_form_instance_assignment_list_for_user(
        user_id=current_user.user_id, page=pagination_query.page, size=pagination_query.size, filters=filters)
    count = await FormInstanceAssignmentService().get_count(filters=filters)
    return GenericResponseListSchema[FormInstanceAssignmentSchema].return_response(result,
                                                                          page=pagination_query.page,
                                                                          size=pagination_query.size,
                                                                          count=count)

@router.get('/assignment_answer/{form_instance_assignment_id}', response_model=GenericResponseSingleSchema[FormInstanceAssignmentUserSchema])
async def get_form_instance_assignment_user_for_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__my_requests)),
        form_instance_assignment_id: str = Path(...),
):
    result = await FormInstanceAssignmentUserService().get_by_user_id_and_form_instance_assignment_id(current_user.user_id,
                                                                                                      form_instance_assignment_id)
    return GenericResponseSingleSchema[FormInstanceAssignmentUserSchema].return_response(result)

@router.patch('/assignment_answer/{form_instance_assignment_id}', response_model=None)
async def update_form_instance_assignment_user_for_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.form_manager__form_system__my_requests)),
        form_instance_assignment_id: str = Path(...),
        data: FormInstanceAssignmentUserAnswerInSchema = Body(...)
):
    result = await FormInstanceAssignmentUserService().update_by_user_id_and_form_instance_assignment_id(current_user.user_id,
                                                                                                         form_instance_assignment_id,
                                                                                                         data)
    return None
