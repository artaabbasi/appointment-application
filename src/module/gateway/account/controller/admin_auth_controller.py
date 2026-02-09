from fastapi import (APIRouter,
                     status,
                     Body,
                     Path, Depends, Header, Request
                     )
from fastapi.responses import StreamingResponse

from common.account.schema.admin_change_profile_schema import AdminChangeProfileSchema
from common.account.schema.user_change_password_schema import UserChangePasswordSchema
from common.schema.response_base_schema import GenericResponseSingleSchema
from common.settings import get_settings
from common.account.schema.login_response_schema import LoginResponseSchema

from common.account.schema.admin_schema import AdminUserSchema
from module.account.user.service import AdminAuthService, AdminService
from module.account.user.service.login_activity_service import LoginActivityService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/admin-auth',
                   tags=['Auth'],
                   responses={
                   }
                   )


@router.get('/profile', response_model=GenericResponseSingleSchema[AdminUserSchema])
async def get_user_profile(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__user_info))

):
    result = await AdminAuthService().get_user_by_id(current_user.admin_id)
    return GenericResponseSingleSchema[AdminUserSchema].return_response(result)


@router.get('/get-captcha', response_class=StreamingResponse)
async def get_captcha():
    captcha = await AdminAuthService().get_captcha()
    return StreamingResponse(captcha, media_type="image/png")


@router.post('/login', response_model=GenericResponseSingleSchema[LoginResponseSchema])
async def verify_phone_number(
        request: Request,
        username: str = Body(..., embed=True),
        password: str = Body(..., embed=True),
        captcha: str = Body(..., embed=True),
):
    result = await AdminAuthService().verify_username_password(username, password, captcha, request)
    return GenericResponseSingleSchema[LoginResponseSchema].return_response(result)


@router.post('/refresh-token', response_model=GenericResponseSingleSchema[LoginResponseSchema])
async def refresh_token(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__auth__refresh_token))):
    """Provide your refresh token at header to gain a new pair of access and refresh tokens."""
    result = await AdminAuthService().refresh_token(current_user.admin_id, current_user.token)
    return GenericResponseSingleSchema[LoginResponseSchema].return_response(result)


@router.post('/reset_password')
async def reset_user_password(
        username: str = Body(..., embed=True),
        code: str = Body(..., embed=True),
        captcha: str = Body(..., embed=True),
):
    result = await AdminAuthService().reset_password_by_username(username, code, captcha)
    return None


@router.get('/reset_password/{admin_id}')
async def reset_user_password(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__update)),
        admin_id: str = Path(...)
):
    result = await AdminAuthService().reset_password(admin_id)
    return None


@router.post('/change_password')
async def change_user_password(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__user_info)),
        data_in: UserChangePasswordSchema = Body(...)
):
    result = await AdminAuthService().change_admin_password(current_user.user_id, data_in)
    return None


@router.patch('/profile', response_model=GenericResponseSingleSchema[AdminUserSchema])
async def update_admin(
        admin: AdminChangeProfileSchema = Body(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__admins__user_info)),
):
    result = await (AdminService().update_user(current_user.admin_id, admin))
    return GenericResponseSingleSchema[AdminUserSchema].return_response(result)

