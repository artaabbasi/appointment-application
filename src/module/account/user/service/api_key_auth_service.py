import asyncio
import base64
import io
import math
import os
import random
import string
from datetime import datetime
from typing import List, Optional

from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.api_key_schema import ApiKeyUserSchema
from common.account.schema.api_token_response_schema import ApiTokenResponseSchema
from common.account.schema.login_response_schema import LoginResponseSchema
from common.account.schema.user_change_password_schema import UserChangePasswordSchema
from common.account.util.jwt_util import JwtUtil
from common.exceptions import NotFoundException, ForbiddenException
from common.lib.base_service import BaseService
from module.account.user.config.otp_message import otp_message, verify_message
from module.account.user.config.reset_password_message import reset_password_message
from module.account.user.config.token_config import TokenConfig
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.entity.user_entity import UserEntity
from module.account.user.enum.user_service_error_code_enum import UserServiceErrorCodeEnum
from module.account.user.repository.profile_repository import ProfileRepository
from module.account.user.repository.user_repository import UserRepository
from module.account.user.service.api_key_service import ApiKeyUserService
from module.account.user.service.login_activity_service import LoginActivityService
from module.account.user.util.otp_util import OTPUtil
from module.account.user.util.password_util import verify_password, get_password_hash
from util.captcha_util import CaptchaUtil
from util.dataset_import_util import DatasetImportUtil
from util.sms_util import SmsUtil
from util.string_util import StringUtilService
from util.timestamp import DatetimeUtil
from fastapi import Request


class ApiKeyAuthService(BaseService):
    def __init__(self):
        self.user_repository = UserRepository()
        self.profile_repository = ProfileRepository()

    async def _fetch_admin_and_its_profile(
            self, username: str
    ) -> [UserEntity, ProfileEntity]:

        user = await self.user_repository.fetch_by_group_and_username(
            UserGroupEnum.api_key, username
        )
        if user is None:
            raise NotFoundException(UserServiceErrorCodeEnum.USER_NOT_FOUND)
        return await self._fetch_admin_detailed_entity(user.id)

    async def _fetch_admin_detailed_entity(self, user_id: str) -> \
            [UserEntity, ProfileEntity]:
        user: UserEntity = await self.user_repository.fetch_by_id(user_id)
        if not user:
            raise NotFoundException(UserServiceErrorCodeEnum.USER_NOT_FOUND)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        return [user, profile]

    async def get_user_by_id(self, user_id: str) -> ApiKeyUserSchema:
        [user, profile] = await self._fetch_admin_detailed_entity(user_id)
        return ApiKeyUserSchema.load_from_entity(user, profile)

    async def refresh_token(self, user_id: str, token: str) -> LoginResponseSchema:
        user = await self.get_user_by_id(user_id)
        response, exp = await self._generate_login_response(user)
        await LoginActivityService().refresh_token(user_id, token, response.refresh_token, exp)
        return response

    async def _generate_login_response(self, user: ApiKeyUserSchema) -> tuple[LoginResponseSchema, int]:
        user_record: UserEntity = await self.user_repository.fetch_by_id(user.id)
        user_record.last_login_at = DatetimeUtil.utc_now_datetime()
        await self.user_repository.update(user_record)
        refresh_token, exp = await JwtUtil().create_refresh_token(user)
        return LoginResponseSchema(
            access_token=await JwtUtil().create_access_token(user),
            refresh_token=refresh_token
        ), exp

    async def _generate_api_token_response(self, user: ApiKeyUserSchema) -> tuple[ApiTokenResponseSchema, int]:
        user_record: UserEntity = await self.user_repository.fetch_by_id(user.id)
        user_record.last_login_at = DatetimeUtil.utc_now_datetime()
        await self.user_repository.update(user_record)
        api_token, exp = await JwtUtil().create_api_token(user)
        return ApiTokenResponseSchema(
            token=api_token), exp

    async def verify_username_password_for_api_token(self, username: str, password: str, request: Request) -> ApiTokenResponseSchema:
        [user, profile] = await self._fetch_admin_and_its_profile(username)
        verified, hashed_password = verify_password(password, user.password)
        if not verified:
            raise ForbiddenException(UserServiceErrorCodeEnum.INVALID_CREDENTIAL_PROVIDED)
        if hashed_password is not None:
            user.password = hashed_password
        await self.user_repository.update(user)
        user_schema = ApiKeyUserSchema.load_from_entity(user, profile)
        response, exp = await self._generate_api_token_response(user_schema)
        ip_address = request.client.host
        agent = request.headers.get('User-Agent')
        await LoginActivityService().create_login_activity(user_schema.id, response.token, exp, ip_address,
                                                           agent)
        return response

    async def verify_username_password(self, username: str, password: str,
                                       request: Request) -> LoginResponseSchema:
        [user, profile] = await self._fetch_admin_and_its_profile(username)
        if not user.is_active:
            raise ForbiddenException(UserServiceErrorCodeEnum.USER_NOT_ACTIVE)
        verified, hashed_password = verify_password(password, user.password)
        if not verified:
            raise ForbiddenException(UserServiceErrorCodeEnum.INVALID_CREDENTIAL_PROVIDED)
        if hashed_password is not None:
            user.password = hashed_password
        user.is_verified = True
        await self.user_repository.update(user)
        user_schema = ApiKeyUserSchema.load_from_entity(user, profile)
        response, exp = await self._generate_login_response(user_schema)
        ip_address = request.client.host
        agent = request.headers.get('User-Agent')
        await LoginActivityService().create_login_activity(user_schema.id, response.refresh_token, exp, ip_address,
                                                           agent)
        return response

    async def _send_verification_code(self, user: UserEntity, phone_number: str):
        user.verification_code = StringUtilService().generate_random_verification_code()
        # user.verification_code = "123456"
        user.verification_code_expires_at = (
                DatetimeUtil.utc_now_datetime() + TokenConfig.TOKEN_INTERVAL_IN_MINUTES)
        await self.user_repository.update(user)
        text_message = verify_message
        await SmsUtil().send_sms([phone_number], text_message.format(user.verification_code))

    @staticmethod
    def _check_if_enough_time_is_spent_from_last_token(last_code_expires_at: datetime):
        if DatetimeUtil.utc_now_datetime() < last_code_expires_at:
            delta = last_code_expires_at - DatetimeUtil.utc_now_datetime()
            wait_time = math.ceil(delta.seconds / 60)
            raise ForbiddenException(UserServiceErrorCodeEnum.TOKEN_HAS_BEEN_SENT_ALREADY,
                                     message=f"Token has been sent already."
                                             f" Try again in {wait_time} minute(s).")

    async def send_verification_code(self, user_id: str):
        user = await self.user_repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        if user.verification_code_expires_at is not None:
            self._check_if_enough_time_is_spent_from_last_token(user.verification_code_expires_at)
        return await self._send_verification_code(user, profile.phone_number)

    async def reset_password(self, user_id: str) -> None:
        user = await self.user_repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        characters = string.digits
        random_string = ''.join(random.choice(characters) for _ in range(8))
        user.must_change_password = True
        await self.user_repository.update(user)
        await ApiKeyUserService().change_admin_password(user_id, random_string)
        text_message = reset_password_message
        await SmsUtil().send_sms([profile.phone_number], text_message.format(user.username, random_string))
        return None

    async def change_admin_password(self, user_id: str, data_in: UserChangePasswordSchema) -> None:
        user = await self.user_repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        await OTPUtil().validate_otp(data_in.code, user)
        if data_in.password != data_in.password_repeated:
            raise ForbiddenException(code=UserServiceErrorCodeEnum.PASSWORD_DONT_MATCH)
        user.must_change_password = False
        await self.user_repository.update(user)
        await ApiKeyUserService().change_admin_password(user_id, data_in.password)
        text_message = reset_password_message
        await SmsUtil().send_sms([profile.phone_number], text_message.format(user.username, data_in.password))
        return None
