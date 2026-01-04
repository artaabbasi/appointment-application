from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from common.config.http_method_enum import HTTPMethodEnum
from common.logging.enum.api_call_log_type_enum import ApiCalLogTypeEnum
from common.logging.enum.request_log_type_enum import RequestLogTypeEnum
from common.logging.schema.api_call_log_schema import ApiCallLogSchema
from common.logging.schema.request_log_schema import RequestLogSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseListSchema
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil
from module.logging.api_call_log.entity.api_call_log_entity import ApiCallLogEntity
from module.logging.api_call_log.service.api_call_log_service import ApiCallLogService
from module.logging.request_log.entity.request_log_entity import RequestLogEntity
from module.logging.request_log.service.request_log_service import RequestLogService

router = APIRouter(prefix='/logs',
                   tags=['Logs'],
                   responses={
                   }
                   )


@router.get('/api-call-log', response_model=GenericResponseListSchema[ApiCallLogSchema])
async def get_api_call_logs(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        pagination_query: PaginationSchema = Depends(),
        type: Optional[ApiCalLogTypeEnum] = Query(None),
        method: Optional[HTTPMethodEnum] = Query(None),
        url: Optional[str] = Query(None),
        description: Optional[str] = Query(None),
        status_code: Optional[int] = Query(None),
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        search: Optional[str] = Query(None),
):
    filters = {}
    if type is not None:
        filters.update({ApiCallLogEntity.type: type})
    if method is not None:
        filters.update({ApiCallLogEntity.method: method})
    if url is not None:
        filters.update({ApiCallLogEntity.url: url})
    if description is not None:
        filters.update({ApiCallLogEntity.description: description})
    if status_code is not None:
        filters.update({ApiCallLogEntity.status_code: status_code})
    if created_from:
        filters.update({"created_from": created_from})
    if created_to:
        filters.update({"created_to": created_to})

    result = await (ApiCallLogService().
                    get_api_call_log_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (ApiCallLogService().get_count(filters, search))
    return GenericResponseListSchema[ApiCallLogSchema].return_response(result,
                                                                              page=pagination_query.page,
                                                                              size=pagination_query.size,
                                                                              count=count)

@router.get('/request-log', response_model=GenericResponseListSchema[RequestLogSchema])
async def get_request_logs(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        pagination_query: PaginationSchema = Depends(),
        type: Optional[RequestLogTypeEnum] = Query(None),
        method: Optional[HTTPMethodEnum] = Query(None),
        url: Optional[str] = Query(None),
        response_status_code: Optional[int] = Query(None),
        client: Optional[str] = Query(None),
        search: Optional[str] = Query(None),
):
    filters = {}
    if type is not None:
        filters.update({RequestLogEntity.type: type})
    if method is not None:
        filters.update({RequestLogEntity.method: method})
    if url is not None:
        filters.update({RequestLogEntity.url: url})
    if response_status_code is not None:
        filters.update({RequestLogEntity.response_status_code: response_status_code})
    if client is not None:
        filters.update({RequestLogEntity.client: client})

    result = await (RequestLogService().
                    get_request_log_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (RequestLogService().get_count(filters, search))
    return GenericResponseListSchema[RequestLogSchema].return_response(result,
                                                                              page=pagination_query.page,
                                                                              size=pagination_query.size,
                                                                              count=count)
