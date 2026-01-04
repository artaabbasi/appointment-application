from fastapi import (APIRouter,
                     status,
                     Body,
                     Path, Depends, Header, Request
                     )
from fastapi.responses import StreamingResponse

from common.account.schema.api_key_schema import ApiKeyUserSchema
from common.account.schema.api_token_response_schema import ApiTokenResponseSchema
from common.account.schema.user_change_password_schema import UserChangePasswordSchema
from common.schema.response_base_schema import GenericResponseSingleSchema
from common.settings import get_settings
from common.account.schema.login_response_schema import LoginResponseSchema
from module.account.user.service.api_key_auth_service import ApiKeyAuthService
from module.account.user.service.api_key_service import ApiKeyUserService

from module.account.user.service.login_activity_service import LoginActivityService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/api-key-auth',
                   tags=['ApiKey Auth'],
                   responses={
                   }
                   )


@router.get('/profile', response_model=GenericResponseSingleSchema[ApiKeyUserSchema])
async def get_user_profile(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__user_info))

):
    result = await ApiKeyAuthService().get_user_by_id(current_user.admin_id)
    return GenericResponseSingleSchema[ApiKeyUserSchema].return_response(result)


@router.post('/login', response_model=GenericResponseSingleSchema[LoginResponseSchema])
async def verify_phone_number(
        request: Request,
        username: str = Body(..., embed=True),
        password: str = Body(..., embed=True),
):
    result = await ApiKeyAuthService().verify_username_password(username, password, request)
    return GenericResponseSingleSchema[LoginResponseSchema].return_response(result)


@router.post('/refresh-token', response_model=GenericResponseSingleSchema[LoginResponseSchema])
async def refresh_token(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__auth__refresh_token))):
    """Provide your refresh token at header to gain a new pair of access and refresh tokens."""
    result = await ApiKeyAuthService().refresh_token(current_user.admin_id, current_user.token)
    return GenericResponseSingleSchema[LoginResponseSchema].return_response(result)


@router.get('/reset_password/{admin_id}')
async def reset_user_password(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__update)),
        admin_id: str = Path(...)
):
    result = await ApiKeyAuthService().reset_password(admin_id)
    return None


@router.get('/send_otp')
async def send_otp_user(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__user_info)),
):
    result = await ApiKeyAuthService().send_verification_code(current_user.user_id)
    return None


@router.post('/change_password')
async def change_user_password(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__user_info)),
        data_in: UserChangePasswordSchema = Body(...)
):
    result = await ApiKeyAuthService().change_admin_password(current_user.user_id, data_in)
    return None
