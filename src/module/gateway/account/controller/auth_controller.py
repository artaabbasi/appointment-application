from fastapi import (APIRouter,
                     status,
                     Body,
                     Path, Depends, Header,
                     Request
                     )

from common.account.schema.login_activity_schema import LoginActivitySchema
from common.account.schema.profile_update_schema import ProfileUpdateSchema
from common.schema.default_schema import DefaultSchema
from common.schema.response_base_schema import GenericResponseSingleSchema, GenericResponseListSchema
from common.settings import get_settings
from common.openapi import (generate_openapi_response_dictionary_schema, )
from common.account.schema.login_response_schema import LoginResponseSchema

from common.account.schema.user_registration_request_schema import UserRegistrationRequestSchema
from common.account.schema.user_schema import CustomerUserSchema
from module.account.user.service import CustomerAuthService, CustomerService
from module.account.user.service.login_activity_service import LoginActivityService
from module.gateway.access_management.schema import ActionEnum
from module.gateway.schema.jwt_user_schema import JWTUserSchema
from module.gateway.util.current_user_util import CurrentUserUtil

settings = get_settings()

router = APIRouter(prefix='/auth',
                   tags=['Auth'],
                   responses={
                   }
                   )


@router.get('/profile', response_model=GenericResponseSingleSchema[CustomerUserSchema])
async def get_user_profile(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__user_info)),
        _: DefaultSchema = Depends(),
):
    result = await CustomerAuthService().get_user_profile(current_user.phone_number)
    return GenericResponseSingleSchema[CustomerUserSchema].return_response(result)

@router.patch('/profile', response_model=GenericResponseSingleSchema[CustomerUserSchema])
async def update_user_profile(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__user_info)),
        _: DefaultSchema = Depends(),
        data: ProfileUpdateSchema = Body(...)

):
    result = await CustomerService().update_user(current_user.user_id, data)
    return GenericResponseSingleSchema[CustomerUserSchema].return_response(result)

@router.post('',
             status_code=201,
             responses={
                 **generate_openapi_response_dictionary_schema(
                     status_code=status.HTTP_201_CREATED,
                     description="Success",
                     example_dict={'data': {'detail': 'User registered successfully.'
                                                      ' Please check your phone number for verification instructions.'
                                            }}),

             })
async def register_user(user: UserRegistrationRequestSchema):
    await CustomerAuthService().register_or_login_customer(user)
    return {
        'data': {
            'detail': 'User registered successfully.'
                      ' Please check your entered email for verification instructions.',
        }}


@router.post('/phone-number/verification', response_model=GenericResponseSingleSchema[LoginResponseSchema])
async def verify_phone_number(
        request: Request,
        phone_number: str = Body(..., embed=True),
        code: str = Body(..., embed=True)
):
    result = await CustomerAuthService().verify_code(code, phone_number, request)
    return GenericResponseSingleSchema[LoginResponseSchema].return_response(result)


@router.get('/{phoneNumber}/verification/resend',
            status_code=200,
            responses={
                **generate_openapi_response_dictionary_schema(
                    status_code=status.HTTP_200_OK,
                    description="Success",
                    example_dict={'data': {
                        'detail': "If you've entered a valid phone number, instruction has been sent to you."}}),
            }
            )
async def resend_verification_code(
        phone_number: str = Path(..., alias='phoneNumber')
):
    await CustomerAuthService().resend_verification_code(phone_number)
    return {
        'data': {'detail': "If you've entered a valid phone number, instruction has been sent to you."}}


@router.post('/refresh-token', response_model=GenericResponseSingleSchema[LoginResponseSchema])
async def refresh_user_token(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__auth__refresh_token))):
    """Provide your refresh token at header to gain a new pair of access and refresh tokens."""
    result = await CustomerAuthService().refresh_token(current_user.user_id, current_user.token)
    return GenericResponseSingleSchema[LoginResponseSchema].return_response(result)


@router.post('/logout', response_model=None, status_code=204)
async def logout(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__auth__refresh_token))):
    await LoginActivityService().logout(current_user.user_id, current_user.token)
    return None


@router.post('/login-activity', response_model=GenericResponseListSchema[LoginActivitySchema])
async def get_login_activity_list(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__user_info)),
        refresh_token: str = Body(None, embed=True, alias='refresh_token'),
):
    login_activities = await LoginActivityService().get_login_activities(current_user.user_id,
                                                                         True,
                                                                         refresh_token)
    return GenericResponseListSchema[LoginActivitySchema].return_response(login_activities)


@router.post('/logout-other-activities', response_model=None, status_code=204)
async def logout_other_activities(
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__user_info)),
        refresh_token: str = Body(None, embed=True, alias='refresh_token'),
):
    await LoginActivityService().logout_others_by_refresh_token(current_user.user_id, refresh_token)
    return None


@router.delete('/login-activity/{activity_id}', response_model=None, status_code=204)
async def logout_activity(
        activity_id: str = Path(...),
        current_user: JWTUserSchema = Depends(CurrentUserUtil(action=ActionEnum.account__customers__user_info))
):
    await LoginActivityService().logout_by_activity_id(current_user.user_id, activity_id)
    return None
