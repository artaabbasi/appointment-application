import base64
import io

import random
import string
from typing import List, Optional

from common.account.enum.admin_roles_enum import AdminRolesEnum
from common.account.enum.user_group_enum import UserGroupEnum
from common.account.schema.admin_schema import AdminUserSchema
from common.account.schema.api_token_response_schema import ApiTokenResponseSchema
from common.account.schema.login_response_schema import LoginResponseSchema
from common.account.schema.user_change_password_schema import UserChangePasswordSchema
from common.account.schema.user_permission_schema import UserPermissionSchema
from common.account.util.jwt_util import JwtUtil
from common.exceptions import NotFoundException, ForbiddenException
from common.lib.base_service import BaseService
from common.settings import EnvironmentEnum
from module.account.authorization.service.role_service import RoleService
from module.account.authorization.service.user_permission_service import UserPermissionService
from module.account.user.config.reset_password_message import reset_password_message
from module.account.user.entity.profile_entity import ProfileEntity
from module.account.user.entity.staff_entity import StaffEntity
from module.account.user.entity.user_entity import UserEntity
from module.account.user.enum.user_service_error_code_enum import UserServiceErrorCodeEnum
from module.account.user.repository.profile_repository import ProfileRepository
from module.account.user.repository.staff_repository import StaffRepository
from module.account.user.repository.user_repository import UserRepository
from module.account.user.service.admin_service import AdminService
from module.account.user.service.login_activity_service import LoginActivityService
from module.account.user.util.otp_util import OTPUtil
from module.account.user.util.password_util import verify_password, get_password_hash
from util.captcha_util import CaptchaUtil
from util.sms_util import SmsUtil
from util.timestamp import DatetimeUtil
from fastapi import Request


class AdminAuthService(BaseService):
    def __init__(self):
        self.user_repository = UserRepository()
        self.profile_repository = ProfileRepository()
        self.staff_repository = StaffRepository()

    async def _fetch_admin_and_its_profile(
            self, username: str
    ) -> [UserEntity, ProfileEntity, StaffEntity, List[UserPermissionSchema]]:

        user = await self.user_repository.fetch_by_group_and_username(
            UserGroupEnum.admin, username
        )
        if user is None:
            raise NotFoundException(UserServiceErrorCodeEnum.USER_NOT_FOUND)
        return await self._fetch_admin_detailed_entity(user.id)

    async def _fetch_admin_detailed_entity(self, user_id: str) -> \
            [UserEntity, ProfileEntity, StaffEntity, List[UserPermissionSchema]]:
        user: UserEntity = await self.user_repository.fetch_by_id(user_id)
        if not user:
            raise NotFoundException(UserServiceErrorCodeEnum.USER_NOT_FOUND)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        staff = await self.staff_repository.fetch_by_user_id(user.id)
        permissions = await UserPermissionService().get_user_permissions(user.id)
        return [user, profile, staff, permissions]

    async def get_user_by_id(self, user_id: str) -> AdminUserSchema:
        [user, profile, staff, permissions] = await self._fetch_admin_detailed_entity(user_id)
        user_roles = await RoleService().get_user_roles(user.id)
        return AdminUserSchema.load_from_entity(user, profile, staff, permissions, user_roles)

    async def refresh_token(self, user_id: str, token: str) -> LoginResponseSchema:
        user = await self.get_user_by_id(user_id)
        response, exp = await self._generate_login_response(user)
        await LoginActivityService().refresh_token(user_id, token, response.refresh_token, exp)
        return response

    async def _generate_login_response(self, user: AdminUserSchema) -> tuple[LoginResponseSchema, int]:
        user_record: UserEntity = await self.user_repository.fetch_by_id(user.id)
        user_record.last_login_at = DatetimeUtil.utc_now_datetime()
        await self.user_repository.update(user_record)
        refresh_token, exp = await JwtUtil().create_refresh_token(user)
        return LoginResponseSchema(
            access_token=await JwtUtil().create_access_token(user),
            refresh_token=refresh_token
        ), exp

    async def _generate_api_token_response(self, user: AdminUserSchema) -> tuple[ApiTokenResponseSchema, int]:
        user_record: UserEntity = await self.user_repository.fetch_by_id(user.id)
        user_record.last_login_at = DatetimeUtil.utc_now_datetime()
        await self.user_repository.update(user_record)
        api_token, exp = await JwtUtil().create_api_token(user)
        return ApiTokenResponseSchema(
            token=api_token), exp

    async def verify_username_password_for_api_token(self, username: str, password: str, request: Request) -> ApiTokenResponseSchema:
        [user, profile, staff, _] = await self._fetch_admin_and_its_profile(username)
        verified, hashed_password = verify_password(password, user.password)
        if not verified:
            raise ForbiddenException(UserServiceErrorCodeEnum.INVALID_CREDENTIAL_PROVIDED)
        if hashed_password is not None:
            user.password = hashed_password
        await self.user_repository.update(user)
        user_schema = AdminUserSchema.load_from_entity(user, profile, staff)
        response, exp = await self._generate_api_token_response(user_schema)
        ip_address = request.client.host
        agent = request.headers.get('User-Agent')
        await LoginActivityService().create_login_activity(user_schema.id, response.token, exp, ip_address,
                                                           agent)
        return response

    async def verify_username_password(self, username: str, password: str, captcha: str,
                                       request: Request) -> LoginResponseSchema:
        [user, profile, staff, permissions] = await self._fetch_admin_and_its_profile(username)
        if self._get_settings().ENV != EnvironmentEnum.DEVELOPMENT:
            if not await CaptchaUtil().verify_captcha(captcha):
                raise ForbiddenException(UserServiceErrorCodeEnum.INVALID_CAPTCHA_PROVIDED)
        if not user.is_active and staff.role != AdminRolesEnum.owner_admin:
            raise ForbiddenException(UserServiceErrorCodeEnum.USER_NOT_ACTIVE)
        verified, hashed_password = verify_password(password, user.password)
        if not verified:
            raise ForbiddenException(UserServiceErrorCodeEnum.INVALID_CREDENTIAL_PROVIDED)
        if hashed_password is not None:
            user.password = hashed_password
        user.is_verified = True
        await self.user_repository.update(user)
        user_schema = AdminUserSchema.load_from_entity(user, profile, staff, permissions)
        response, exp = await self._generate_login_response(user_schema)
        ip_address = request.client.host
        agent = request.headers.get('User-Agent')
        await LoginActivityService().create_login_activity(user_schema.id, response.refresh_token, exp, ip_address,
                                                           agent)
        return response

    async def get_user_and_profile_with_username(self, username: str) -> Optional[AdminUserSchema]:
        default_admin_user = await self.user_repository.fetch_by_group_and_username(
            UserGroupEnum.admin, username
        )
        [user, profile, staff, permissions] = await self._fetch_admin_detailed_entity(default_admin_user.id)
        return AdminUserSchema.load_from_entity(user, profile, staff, permissions)

    async def get_captcha(self) -> io.BytesIO:
        captcha, code = await CaptchaUtil().generate_captcha()
        captcha_image = captcha.decode("utf-8")
        return io.BytesIO(base64.b64decode(captcha_image))

    async def create_default_admin_user(self) -> AdminUserSchema:
        return await self.create_default_user(
            self._get_settings().DEFAULT_USERNAME,
            self._get_settings().DEFAULT_PHONE,
            self._get_settings().DEFAULT_PASSWORD,
            AdminRolesEnum.owner_admin
        )

    async def create_default_user(self,
                                  username: str,
                                  phone_number: str,
                                  password: str,
                                  role: AdminRolesEnum,
                                  email: Optional[str] = None,
                                  national_code: Optional[str] = None,
                                  first_name: Optional[str] = None,
                                  last_name: Optional[str] = None,
                                  en_first_name: Optional[str] = None,
                                  en_last_name: Optional[str] = None,
                                  ) -> AdminUserSchema:
        user = None
        profile = None
        staff = None
        permissions = None
        try:
            default_admin_user = await self.user_repository.fetch_by_group_and_username(
                UserGroupEnum.admin, username
            )
            [user, profile, staff, permissions] = await self._fetch_admin_detailed_entity(default_admin_user.id)
            print(f"User exist with id: {user.id}")
        except NotFoundException:
            pass
        if profile is not None:
            profile = await self.profile_repository.update(
                ProfileEntity(
                    id=profile.id,
                    phone_number=phone_number if phone_number is not None else profile.phone_number,
                    email=email if email is not None else profile.email,
                    first_name=first_name if first_name is not None else profile.first_name,
                    last_name=last_name if last_name is not None else profile.last_name,
                    national_code=national_code if national_code is not None else profile.national_code,
                    en_first_name=en_first_name if en_first_name is not None else profile.en_first_name,
                    en_last_name=en_last_name if en_last_name is not None else profile.en_last_name,

                )
            )
        else:
            profile = await self.profile_repository.create(
                ProfileEntity(
                    phone_number=phone_number,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    national_code=national_code,
                    en_first_name=en_first_name,
                    en_last_name=en_last_name,
                )
            )
        if user is not None:
            user = await self.user_repository.update(
                UserEntity(
                    id=user.id,
                    username=username if username is not None else user.username,
                    password=get_password_hash(password) if password is not None else user.password,
                    group=UserGroupEnum.admin,
                    is_verified=True,
                    profile_id=profile.id,
                    is_active=True
                )
            )
        else:
            user = await self.user_repository.create(
                UserEntity(
                    username=username,
                    password=get_password_hash(password),
                    group=UserGroupEnum.admin,
                    is_verified=True,
                    profile_id=profile.id,
                    is_active=True
                )
            )
        if staff is None:
            staff = await self.staff_repository.create(
                StaffEntity(
                    user_id=user.id,
                    is_active=True,
                    role=role
                )
            )
        print(f"User created/updated with id: {user.id}")
        return AdminUserSchema.load_from_entity(user, profile, staff, permissions)

    async def _reset_password(self, user: UserEntity):
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        characters = string.digits
        random_string = ''.join(random.choice(characters) for _ in range(8))
        user.must_change_password = True
        await self.user_repository.update(user)
        await AdminService().change_admin_password(user.id, random_string)
        text_message = reset_password_message
        await SmsUtil().send_sms([profile.phone_number], text_message.format(user.username, random_string))
        return None

    async def reset_password_by_username(self, username: str, code: str, captcha: str) -> None:
        if self._get_settings().ENV != EnvironmentEnum.DEVELOPMENT:
            if not await CaptchaUtil().verify_captcha(captcha):
                raise ForbiddenException(UserServiceErrorCodeEnum.INVALID_CAPTCHA_PROVIDED)
        user = await self.user_repository.fetch_by_group_and_username(UserGroupEnum.admin, username)
        await OTPUtil().validate_otp(code, user)
        await self._reset_password(user)

    async def reset_password(self, user_id: str) -> None:
        user = await self.user_repository.fetch_by_id(user_id)
        await self._reset_password(user)

    async def change_admin_password(self, user_id: str, data_in: UserChangePasswordSchema) -> None:
        user = await self.user_repository.fetch_by_id(user_id)
        profile = await self.profile_repository.fetch_by_id(user.profile_id)
        if data_in.password != data_in.password_repeated:
            raise ForbiddenException(code=UserServiceErrorCodeEnum.PASSWORD_DONT_MATCH)
        user.must_change_password = False
        await self.user_repository.update(user)
        await AdminService().change_admin_password(user_id, data_in.password)
        return None
