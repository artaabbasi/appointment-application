from datetime import datetime, timedelta
import math
from typing import List, Tuple, Optional
from fastapi import Request, HTTPException
from common.account.enum.user_group_enum import UserGroupEnum
from common.lib.base_service import BaseService

from common.account.schema.login_response_schema import LoginResponseSchema
from common.account.schema.user_schema import CustomerUserSchema
from common.account.schema.user_registration_request_schema import UserRegistrationRequestSchema
from util.sms_util import SmsUtil
from util.string_util import StringUtilService
from util.timestamp import DatetimeUtil
from common.exceptions import (
    ForbiddenException,
    NotFoundException
)
from ._profile_service import ProfileService
from .login_activity_service import LoginActivityService
from ..config.test_phone_numbers_config import TestPhoneNumbersConfig
from ..config.token_config import TokenConfig

from ..repository.user_repository import UserRepository
from ..entity.profile_entity import ProfileEntity
from ..entity.user_entity import UserEntity
from ..enum.user_service_error_code_enum import UserServiceErrorCodeEnum
from ..repository.profile_repository import ProfileRepository
from common.account.util.jwt_util import JwtUtil
from ..util.otp_util import OTPUtil


class CustomerAuthService(BaseService):
    def __init__(self):
        self.user_repository = UserRepository()
        self.profile_repository = ProfileRepository()

    async def _send_verification_code(self, user: UserEntity, phone_number: str):
        if TestPhoneNumbersConfig.is_test_phone_number(phone_number) is False:
            user.verification_code = StringUtilService().generate_random_verification_code()
            user.verification_code_expires_at = (
                    DatetimeUtil.utc_now_datetime() + TokenConfig.TOKEN_INTERVAL_IN_MINUTES)
            await self.user_repository.update(user)
            text_message = ""
            await SmsUtil().send_sms([phone_number], text_message.format(user.verification_code,
                                                                   user.verification_code))
        else:
            user.verification_code = '123456'
            user.verification_code_expires_at = (
                    DatetimeUtil.utc_now_datetime() + TokenConfig.TOKEN_INTERVAL_IN_MINUTES)
            await self.user_repository.update(user)

    async def _add_customer_user(self,
                                 profile_id: str
                                 ):
        user = await self.user_repository.create(
            UserEntity(
                group=UserGroupEnum.customer,
                profile_id=profile_id
            )
        )
        return user

    async def get_customer_profile_from_phone_number(self, phone_number: str) -> Optional[ProfileEntity]:
        profiles = await self.profile_repository.fetch_by_phone_number(phone_number)
        for profile in profiles:
            user = await self.user_repository.fetch_by_group_and_profile_id(
                UserGroupEnum.customer, profile.id
            )
            if user is not None:
                return profile

    async def get_or_create_user_and_profile(self, phone_number: str) -> Tuple[UserEntity, ProfileEntity]:
        profile = await self.get_customer_profile_from_phone_number(phone_number)
        if not profile:
            profile = await ProfileService().add_profile(phone_number)

        user = await self.user_repository.fetch_by_group_and_profile_id(
            UserGroupEnum.customer, profile.id
        )
        if not user:
            user = await self._add_customer_user(profile.id)
        return user, profile

    async def get_or_create_user_schema(self, phone_number: str) -> CustomerUserSchema:
        user, profile = await self.get_or_create_user_and_profile(phone_number)

        return CustomerUserSchema.load_from_entity(user,
                                                   profile)

    async def register_or_login_customer(self, user_request: UserRegistrationRequestSchema) -> None:
        user, profile = await self.get_or_create_user_and_profile(user_request.phone_number)
        await self._send_verification_code(user, profile.phone_number)

    async def _fetch_user_and_its_profile(
            self, phone_number: str
    ) -> [UserEntity, ProfileEntity]:
        profile = await self.get_customer_profile_from_phone_number(phone_number)
        if profile is None:
            raise NotFoundException(code=UserServiceErrorCodeEnum.USER_NOT_FOUND)
        user = await self.user_repository.fetch_by_group_and_profile_id(
            UserGroupEnum.customer, profile.id
        )
        if user is None:
            raise NotFoundException(UserServiceErrorCodeEnum.USER_NOT_FOUND)
        return [user, profile]

    async def verify_code(self, verification_code: str, phone_number: str, request: Request) -> LoginResponseSchema:
        [user, profile] = await self._fetch_user_and_its_profile(phone_number)
        await OTPUtil().validate_otp(verification_code, user)
        user.is_verified = True
        await self.user_repository.update(user)
        user_schema = CustomerUserSchema.load_from_entity(user, profile)
        response, exp = await self._generate_login_response(user_schema)
        return response

    @staticmethod
    def _check_if_enough_time_is_spent_from_last_token(last_code_expires_at: Optional[datetime] = None):
        if last_code_expires_at is None:
            return True
        if DatetimeUtil.utc_now_datetime() < last_code_expires_at:
            delta = last_code_expires_at - DatetimeUtil.utc_now_datetime()
            wait_time = math.ceil(delta.seconds / 60)
            raise ForbiddenException(UserServiceErrorCodeEnum.TOKEN_HAS_BEEN_SENT_ALREADY,
                                     message=f"Token has been sent already."
                                             f" Try again in {wait_time} minute(s).")

    async def resend_verification_code(self, phone_number: str):
        [user, profile] = await self._fetch_user_and_its_profile(phone_number)
        self._check_if_enough_time_is_spent_from_last_token(user.verification_code_expires_at)
        return await self._send_verification_code(user, profile.phone_number)

    async def get_user_profile(self, phone_number: str) -> CustomerUserSchema:
        [user, profile] = await self._fetch_user_and_its_profile(phone_number)
        return CustomerUserSchema.load_from_entity(user,
                                                   profile)

    async def _get_user_detailed_entities(self, user_id: str) -> \
            [UserEntity, ProfileEntity]:
        user: UserEntity = await self.user_repository.fetch_by_id(user_id)
        if not user:
            raise NotFoundException(UserServiceErrorCodeEnum.USER_NOT_FOUND)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        return [user, profile]

    async def get_user_by_id(self, user_id: str) -> CustomerUserSchema:
        [user, profile] = await self._get_user_detailed_entities(user_id)
        return CustomerUserSchema.load_from_entity(user,
                                                   profile)

    async def refresh_token(self, user_id: str, token: str) -> LoginResponseSchema:
        user = await self.get_user_by_id(user_id)
        response, exp = await self._generate_login_response(user)
        await LoginActivityService().refresh_token(user_id, token, response.refresh_token, exp)
        return response

    async def _generate_login_response(self, user: CustomerUserSchema) -> tuple[LoginResponseSchema, int]:
        user_record: UserEntity = await self.user_repository.fetch_by_id(user.id)
        user_record.last_login_at = DatetimeUtil.utc_now_datetime()
        await self.user_repository.update(user_record)
        refresh_token, exp = await JwtUtil().create_refresh_token(user)
        return LoginResponseSchema(
            access_token=await JwtUtil().create_access_token(user),
            refresh_token=refresh_token
        ), exp
