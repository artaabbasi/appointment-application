import json
import base64
from datetime import timedelta

from common.account.enum.authentication_error_code_enum import AuthenticationErrorCodeEnum
from common.account.schema.admin_schema import AdminUserSchema
from common.account.schema.api_key_schema import ApiKeyUserSchema
from common.lib.base_service import BaseService
from util.redis_util import RedisUtil
from util.timestamp import DatetimeUtil
from typing import Dict, Union, Tuple
from binascii import Error as BinasciiError

from pydantic import ValidationError as PydanticValidationError, TypeAdapter

from jose import jwt
from jose.constants import ALGORITHMS
from jose import exceptions as jose_exceptions

from common.exceptions import (
    UnauthorizedException,
)
from common.account.schema.authenticated_user_schema import (
    AuthenticatedUserSchema
)
from common.account.schema.user_schema import CustomerUserSchema
from common.account.enum.token_type_enum import TokenTypeEnum
from util.logger import get_custom_logger

logger = get_custom_logger(__name__)


class JwtUtil(BaseService):

    def _encode_token(self, payload: AuthenticatedUserSchema) -> str:
        return jwt.encode(payload.model_dump(), self._get_settings().RSA_PRIVATE_KEY, ALGORITHMS.RS256)

    def _decode_token(self, token: str) -> AuthenticatedUserSchema:
        try:
            data = jwt.decode(token,
                              self._get_settings().RSA_PUBLIC_KEY,
                              algorithms=[ALGORITHMS.RS256, ],
                              options={'require': ['iat', 'exp']})
            return TypeAdapter(AuthenticatedUserSchema).validate_python(data)
        except jose_exceptions.ExpiredSignatureError:
            raise UnauthorizedException(code=AuthenticationErrorCodeEnum.EXPIRED_CREDENTIALS_PROVIDED)
        except jose_exceptions.JWTError as error:
            logger.error(error)
            raise UnauthorizedException(code=AuthenticationErrorCodeEnum.INVALID_CREDENTIALS_PROVIDED)

    @staticmethod
    async def _build_user_payload(user: Union[CustomerUserSchema, AdminUserSchema], token_type: TokenTypeEnum) -> tuple[AuthenticatedUserSchema, int]:
        """
        Generates a dictionary to be used as JWT payload.
        """
        if token_type != TokenTypeEnum.api_key:
            delta = timedelta(minutes=JwtUtil._get_settings().ACCESS_TOKEN_EXPIRATION_TIME_DELTA_MINUTES) \
                if token_type == TokenTypeEnum.access \
                else timedelta(minutes=JwtUtil._get_settings().REFRESH_TOKEN_EXPIRATION_TIME_DELTA_MINUTES)
        else:
            delta = timedelta(minutes=JwtUtil._get_settings().ACCESS_TOKEN_EXPIRATION_TIME_DELTA_MINUTES)

        exp = DatetimeUtil.utc_now_datetime() + delta
        payload = AuthenticatedUserSchema(
            token_type=token_type,
            phone_number=user.phone_number,
            iat=DatetimeUtil.utc_now_datetime() + timedelta(seconds=1),
            exp=exp,
            group=user.group
        )
        if type(user) is AdminUserSchema:
            payload.admin_id = user.id
            payload.roles = [user.role]
            payload.permissions = []
            payload.national_code = user.national_code
            await RedisUtil().set_key(f"user:{user.id}:perms",
                                json.dumps([perm.model_dump() for perm in user.permissions]),
                                ex=timedelta(minutes=JwtUtil._get_settings().REFRESH_TOKEN_EXPIRATION_TIME_DELTA_MINUTES).seconds)

        elif type(user) is ApiKeyUserSchema:
            payload.admin_id = user.id
            payload.user_id = user.id
            payload.roles = []

        else:
            payload.user_id = user.id
            payload.roles = []
            payload.national_code = user.national_code

        return payload, int(exp.timestamp())

    async def create_access_token(self, user: Union[CustomerUserSchema, AdminUserSchema, ApiKeyUserSchema]) -> str:
        payload, exp = await self._build_user_payload(user, TokenTypeEnum.access)
        return self._encode_token(payload)

    async def create_refresh_token(self, user: Union[CustomerUserSchema, AdminUserSchema, ApiKeyUserSchema]) -> tuple[str, int]:
        payload, exp = await self._build_user_payload(user, TokenTypeEnum.refresh)
        return self._encode_token(payload), exp

    async def create_api_token(self, user: Union[AdminUserSchema, ApiKeyUserSchema]) -> tuple[str, int]:
        payload, exp = await self._build_user_payload(user, TokenTypeEnum.api_key)
        return self._encode_token(payload), exp
