from typing import Optional

from fastapi import APIRouter, Path, Body, Depends, Request
from fastapi.params import Query

from common.account.schema.api_token_response_schema import ApiTokenResponseSchema
from common.api_manager.schema.api_in_schema import ApiInSchema
from common.api_manager.schema.api_key_access_create_schema import ListCreateApiKeyAccessSchema
from common.api_manager.schema.api_key_schema import ApiKeySchema
from common.api_manager.schema.api_schema import ApiSchema
from common.api_manager.schema.api_tag_in_schema import ApiTagInSchema
from common.api_manager.schema.api_tag_schema import ApiTagSchema
from common.schema.default_schema import DefaultSchema
from common.schema.pagination_schema import PaginationSchema
from common.schema.response_base_schema import GenericResponseSingleSchema, GenericResponseListSchema
from common.settings import get_settings
from module.account.user.service import AdminAuthService
from module.account.user.service.api_key_auth_service import ApiKeyAuthService
from module.api_manager.api_key.service.api_key_service import ApiKeyService
from module.api_manager.api_key.service.api_service import ApiService
from module.api_manager.api_key.service.api_tag_service import ApiTagService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/api-manager',
                   tags=['Api Manager'],
                   responses={
                   }
                   )

@router.get('/api', response_model=GenericResponseListSchema[ApiSchema])
async def get_apis(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        pagination_query: PaginationSchema = Depends(),
        tag: Optional[str] = Query(None),
        search: Optional[str] = Query(None),
):
    filters = {}
    if tag is not None:
        filters.update({"tag":tag})
    result = await (ApiService().
                    get_api_list(page=pagination_query.page, size=pagination_query.size,
                                 filters=filters, search=search))
    count = await (ApiService().get_count(filters=filters, search=search))
    return GenericResponseListSchema[ApiSchema].return_response(result,
                                                                              page=pagination_query.page,
                                                                              size=pagination_query.size,
                                                                              count=count)


@router.post('/api', response_model=GenericResponseSingleSchema[ApiSchema])
async def create_api(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        data_in: ApiInSchema = Body(...),
):
    result = await (ApiService().
                    create_api(data_in))
    return GenericResponseSingleSchema[ApiSchema].return_response(result)


@router.patch('/api/{api_id}',
              response_model=GenericResponseSingleSchema[ApiSchema])
async def update_api(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        api_id: str = Path(...),
        data_in: ApiInSchema = Body(...),
):
    result = await (ApiService().
                    update_api(api_id, data_in))
    return GenericResponseSingleSchema[ApiSchema].return_response(result)


@router.delete('/api/{api_id}', response_model=None, status_code=204)
async def delete_api(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        api_id: str = Path(...),
):
    result = await (ApiService().
                    delete_api(api_id))
    return None

@router.get('/api-tag', response_model=GenericResponseListSchema[ApiTagSchema])
async def get_api_tags(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        pagination_query: PaginationSchema = Depends(),
):
    result = await (ApiTagService().
                    get_api_tag_list(page=pagination_query.page, size=pagination_query.size))
    count = await (ApiTagService().get_count())
    return GenericResponseListSchema[ApiTagSchema].return_response(result,
                                                                   page=pagination_query.page,
                                                                   size=pagination_query.size,
                                                                   count=count)


@router.post('/api-tag', response_model=GenericResponseSingleSchema[ApiTagSchema])
async def create_api_tag(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        data_in: ApiTagInSchema = Body(...),
):
    result = await (ApiTagService().
                    create_api_tag(data_in))
    return GenericResponseSingleSchema[ApiTagSchema].return_response(result)

@router.get('/api-tag/{api_tag_id}',
              response_model=GenericResponseSingleSchema[ApiTagSchema])
async def get_api_tag(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        api_tag_id: str = Path(...)
):
    result = await (ApiTagService().
                    get_api_tag(api_tag_id))
    return GenericResponseSingleSchema[ApiSchema].return_response(result)


@router.patch('/api-tag/{api_tag_id}',
              response_model=GenericResponseSingleSchema[ApiTagSchema])
async def update_api_tag(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        api_tag_id: str = Path(...),
        data_in: ApiTagInSchema = Body(...),
):
    result = await (ApiTagService().
                    update_api_tag(api_tag_id, data_in))
    return GenericResponseSingleSchema[ApiSchema].return_response(result)


@router.delete('/api-tag/{api_tag_id}', response_model=None, status_code=204)
async def delete_api_tag(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        api_tag_id: str = Path(...),
):
    result = await (ApiTagService().
                    delete_api_tag(api_tag_id))
    return None

@router.get('/api-key', response_model=GenericResponseSingleSchema[ApiKeySchema])
async def get_api_key(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        _: DefaultSchema = Depends(),
):
    result = await (ApiKeyService().
                    get_api_key_for_user(current_user.user_id))
    return GenericResponseSingleSchema[ApiKeySchema].return_response(result)

@router.patch('/api-key',
              response_model=GenericResponseSingleSchema[ApiSchema])
async def update_api_key(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.insurance__admins__list)),
        api_access: ListCreateApiKeyAccessSchema = Body(...),
):
    result = await (ApiKeyService().
                    update_api_access(api_access))
    return GenericResponseSingleSchema[ApiSchema].return_response(result)


@router.post('/login', response_model=GenericResponseSingleSchema[ApiTokenResponseSchema])
async def get_api_token(
        request: Request,
        username: str = Body(..., embed=True),
        password: str = Body(..., embed=True)
):
    result = await ApiKeyAuthService().verify_username_password_for_api_token(username, password, request)
    return GenericResponseSingleSchema[ApiTokenResponseSchema].return_response(result)
