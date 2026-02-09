from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, Path

from common.account.enum.user_group_enum import UserGroupEnum
from common.appointment.schema.appointment_item_schema import AppointmentItemSchema
from common.appointment.schema.appointment_schema import AppointmentSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseListSchema
from module.appointment.appointment.entity.appointment_entity import AppointmentEntity
from module.appointment.appointment.entity.appointment_item_entity import AppointmentItemEntity
from module.appointment.appointment.service.appointment_item_service import AppointmentItemService
from module.appointment.appointment.service.appointment_service import AppointmentService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

router = APIRouter(prefix='/appointment/appointment',
                   tags=['Appointment'],
                   responses={
                   }
                   )

@router.get('', response_model=GenericResponseListSchema[AppointmentSchema])
async def get_appointments(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        pagination_query: PaginationSchema = Depends(),
        user_id: Optional[str] = Query(None),
        search: Optional[str] = Query(None),
        created_from: Optional[datetime] = Query(None),
        created_to: Optional[datetime] = Query(None),

):
    filters = {}
    if user_id is not None:
        filters.update({AppointmentEntity.user_id: user_id})
    if current_user.group == UserGroupEnum.customer:
        filters.update({AppointmentEntity.user_id: user_id})
    if created_from is not None:
        filters.update({"created_from": created_from})
    if created_to is not None:
        filters.update({"created_to": created_to})

    result = await (AppointmentService().
                    get_appointment_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (AppointmentService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[AppointmentSchema].return_response(result,
                                                                      page=pagination_query.page,
                                                                      size=pagination_query.size,
                                                                      count=count)

@router.get('/appointment-item', response_model=GenericResponseListSchema[AppointmentItemSchema])
async def get_appointment_items(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),
        operator_id: Optional[str] = Query(None),
        from_datetime: Optional[datetime] = Query(None),
        to_datetime: Optional[datetime] = Query(None),

):
    filters = {}
    if operator_id is not None:
        filters.update({AppointmentItemEntity.operator_id: operator_id})
    if from_datetime is not None:
        filters.update({"from_datetime": from_datetime})
    if to_datetime is not None:
        filters.update({"to_datetime": to_datetime})

    result = await (AppointmentItemService().
                    get_appointment_item_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (AppointmentItemService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[AppointmentItemSchema].return_response(result,
                                                                      page=pagination_query.page,
                                                                      size=pagination_query.size,
                                                                      count=count)

@router.delete('/cancel/{appointment_id}', response_model=None, status_code=204)
async def cancel_appointment(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        appointment_id: str = Path(...),
):
    result = await (AppointmentService().
                    cancel_appointment(current_user.user_id, appointment_id))
    return None
