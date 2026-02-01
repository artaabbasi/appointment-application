from fastapi import APIRouter, Depends, Path, Body

from common.appointment.schema.main_service_in_schema import MainServiceInSchema
from common.appointment.schema.main_service_schema import MainServiceSchema
from common.appointment.schema.operator_in_schema import OperatorInSchema
from common.appointment.schema.operator_schema import OperatorSchema
from common.appointment.schema.service_in_schema import ServiceInSchema
from common.appointment.schema.service_schema import ServiceSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseListSchema, GenericResponseSingleSchema
from module.appointment.common.service.main_service_service import MainServiceService
from module.appointment.common.service.operator_service import OperatorService
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
):
    result = await (OperatorService().
                    get_operator_list(page=pagination_query.page, size=pagination_query.size))
    count = await (OperatorService().get_count())
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

@router.get('/main-service', response_model=GenericResponseListSchema[MainServiceSchema])
async def get_main_services(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.all_access)),
        pagination_query: PaginationSchema = Depends(),
):
    result = await (MainServiceService().
                    get_main_service_list(page=pagination_query.page, size=pagination_query.size))
    count = await (MainServiceService().get_count())
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
):
    result = await (ServiceService().
                    get_service_list(page=pagination_query.page, size=pagination_query.size))
    count = await (ServiceService().get_count())
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
