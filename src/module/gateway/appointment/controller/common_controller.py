from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Path, Body, Query

from common.appointment.schema.bulk_operator_time_in_schema import BulkOperatorTimeInSchema
from common.appointment.schema.main_service_in_schema import MainServiceInSchema
from common.appointment.schema.main_service_schema import MainServiceSchema
from common.appointment.schema.operator_in_schema import OperatorInSchema
from common.appointment.schema.operator_schema import OperatorSchema
from common.appointment.schema.operator_time_in_schema import OperatorTimeInSchema
from common.appointment.schema.operator_time_schema import OperatorTimeSchema
from common.appointment.schema.service_in_schema import ServiceInSchema
from common.appointment.schema.service_schema import ServiceSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseListSchema, GenericResponseSingleSchema
from module.appointment.common.entity.operator_time_entity import OperatorTimeEntity
from module.appointment.common.entity.service_entity import ServiceEntity
from module.appointment.common.service.main_service_service import MainServiceService
from module.appointment.common.service.operator_service import OperatorService
from module.appointment.common.service.operator_time_service import OperatorTimeService
from module.appointment.common.service.service_service import ServiceService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

router = APIRouter(prefix='/appointment/common',
                   tags=['Common'],
                   responses={
                   }
                   )


@router.get('/operator', response_model=GenericResponseListSchema[OperatorSchema])
async def get_operators(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),
):
    filters = {}

    result = await (OperatorService().
                    get_operator_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (OperatorService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[OperatorSchema].return_response(result,
                                                                      page=pagination_query.page,
                                                                      size=pagination_query.size,
                                                                      count=count)

@router.post('/operator', response_model=GenericResponseSingleSchema[OperatorSchema])
async def create_operator(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        data_in: OperatorInSchema = Body(...),
):
    result = await (OperatorService().
                    create_operator(data_in))
    return GenericResponseSingleSchema[OperatorSchema].return_response(result)


@router.get('/operator/{operator_id}',
              response_model=GenericResponseSingleSchema[OperatorSchema])
async def get_operator(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        operator_id: str = Path(...),
):
    result = await (OperatorService().
                    get_operator_by_id(operator_id))
    return GenericResponseSingleSchema[OperatorSchema].return_response(result)

@router.patch('/operator/{operator_id}',
              response_model=GenericResponseSingleSchema[OperatorSchema])
async def update_operator(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        operator_id: str = Path(...),
        data_in: OperatorInSchema = Body(...),
):
    result = await (OperatorService().
                    update_operator(operator_id, data_in))
    return GenericResponseSingleSchema[OperatorSchema].return_response(result)


@router.delete('/operator/{operator_id}', response_model=None, status_code=204)
async def delete_operator(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        operator_id: str = Path(...),
):
    result = await (OperatorService().
                    delete_operator(operator_id))
    return None

@router.get('/operator-time', response_model=GenericResponseListSchema[OperatorTimeSchema])
async def get_operator_times(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),
        operator_id: Optional[str] = Query(None),
        from_datetime: Optional[datetime] = Query(None),
        to_datetime: Optional[datetime] = Query(None),
):
    filters = {}
    if operator_id is not None:
        filters.update({OperatorTimeEntity.operator_id: operator_id})
    if from_datetime is not None:
        filters.update({"from_datetime": from_datetime})
    if to_datetime is not None:
        filters.update({"to_datetime": to_datetime})
    result = await (OperatorTimeService().
                    get_operator_time_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (OperatorTimeService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[OperatorTimeSchema].return_response(result,
                                                                              page=pagination_query.page,
                                                                              size=pagination_query.size,
                                                                              count=count)

@router.post('/operator-time', response_model=GenericResponseSingleSchema[OperatorTimeSchema])
async def create_operator_time(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        data_in: OperatorTimeInSchema = Body(...),
):
    result = await (OperatorTimeService().
                    create_operator_time(data_in))
    return GenericResponseSingleSchema[OperatorTimeSchema].return_response(result)

@router.post('/operator-time/bulk_create', response_model=GenericResponseListSchema[OperatorTimeSchema])
async def bulk_create_operator_time(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        data_in: BulkOperatorTimeInSchema = Body(...),
):
    result = await (OperatorTimeService().
                    create_bulk_operator_time(data_in))
    return GenericResponseListSchema[OperatorTimeSchema].return_response(result)


@router.get('/operator-time/{operator_id}',
              response_model=GenericResponseSingleSchema[OperatorTimeSchema])
async def get_operator_time(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        operator_id: str = Path(...),
):
    result = await (OperatorTimeService().
                    get_operator_time_by_id(operator_id))
    return GenericResponseSingleSchema[OperatorTimeSchema].return_response(result)

@router.patch('/operator-time/{operator_id}',
              response_model=GenericResponseSingleSchema[OperatorTimeSchema])
async def update_operator_time(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        operator_id: str = Path(...),
        data_in: OperatorTimeInSchema = Body(...),
):
    result = await (OperatorTimeService().
                    update_operator_time(operator_id, data_in))
    return GenericResponseSingleSchema[OperatorTimeSchema].return_response(result)


@router.delete('/operator-time/{operator_id}', response_model=None, status_code=204)
async def delete_operator_time(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        operator_id: str = Path(...),
):
    result = await (OperatorTimeService().
                    delete_operator_time(operator_id))
    return None

@router.get('/main-service', response_model=GenericResponseListSchema[MainServiceSchema])
async def get_main_services(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),

):
    filters = {}

    result = await (MainServiceService().
                    get_main_service_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (MainServiceService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[MainServiceSchema].return_response(result,
                                                                              page=pagination_query.page,
                                                                              size=pagination_query.size,
                                                                              count=count)

@router.post('/main-service', response_model=GenericResponseSingleSchema[MainServiceSchema])
async def create_main_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        data_in: MainServiceInSchema = Body(...),
):
    result = await (MainServiceService().
                    create_main_service(data_in))
    return GenericResponseSingleSchema[MainServiceSchema].return_response(result)


@router.get('/main-service/{main_service_id}',
              response_model=GenericResponseSingleSchema[MainServiceSchema])
async def get_main_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        main_service_id: str = Path(...),
):
    result = await (MainServiceService().
                    get_main_service_by_id(main_service_id))
    return GenericResponseSingleSchema[MainServiceSchema].return_response(result)

@router.patch('/main-service/{main_service_id}',
              response_model=GenericResponseSingleSchema[MainServiceSchema])
async def update_main_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        main_service_id: str = Path(...),
        data_in: MainServiceInSchema = Body(...),
):
    result = await (MainServiceService().
                    update_main_service(main_service_id, data_in))
    return GenericResponseSingleSchema[MainServiceSchema].return_response(result)


@router.delete('/main-service/{main_service_id}', response_model=None, status_code=204)
async def delete_main_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        main_service_id: str = Path(...),
):
    result = await (MainServiceService().
                    delete_main_service(main_service_id))
    return None

@router.get('/service', response_model=GenericResponseListSchema[ServiceSchema])
async def get_services(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        pagination_query: PaginationSchema = Depends(),
        search: Optional[str] = Query(None),
        main_service_id: Optional[str] = Query(None),
):
    filters = {}
    if main_service_id is not None:
        filters.update({ServiceEntity.main_service_id: main_service_id})
    result = await (ServiceService().
                    get_service_list(page=pagination_query.page, size=pagination_query.size, filters=filters, search=search))
    count = await (ServiceService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[ServiceSchema].return_response(result,
                                                                              page=pagination_query.page,
                                                                              size=pagination_query.size,
                                                                              count=count)

@router.post('/service', response_model=GenericResponseSingleSchema[ServiceSchema])
async def create_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        data_in: ServiceInSchema = Body(...),
):
    result = await (ServiceService().
                    create_service(data_in))
    return GenericResponseSingleSchema[ServiceSchema].return_response(result)


@router.get('/service/{service_id}',
              response_model=GenericResponseSingleSchema[ServiceSchema])
async def get_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        service_id: str = Path(...),
):
    result = await (ServiceService().
                    get_service_by_id(service_id))
    return GenericResponseSingleSchema[ServiceSchema].return_response(result)

@router.patch('/service/{service_id}',
              response_model=GenericResponseSingleSchema[ServiceSchema])
async def update_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        service_id: str = Path(...),
        data_in: ServiceInSchema = Body(...),
):
    result = await (ServiceService().
                    update_service(service_id, data_in))
    return GenericResponseSingleSchema[ServiceSchema].return_response(result)


@router.delete('/service/{service_id}', response_model=None, status_code=204)
async def delete_service(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.admin_access)),
        service_id: str = Path(...),
):
    result = await (ServiceService().
                    delete_service(service_id))
    return None
