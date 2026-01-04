from common.exceptions import ForbiddenException
from common.lib.base_service import BaseService
from module.account.user.config.token_config import TokenConfig
from module.account.user.entity import UserEntity
from module.account.user.enum.user_service_error_code_enum import UserServiceErrorCodeEnum
from module.account.user.repository.user_repository import UserRepository
from util.redis_util import RedisUtil
from util.timestamp import DatetimeUtil


class OTPUtil(BaseService):
    def __init__(self):
        self.redis = RedisUtil()

    @staticmethod
    def _create_key(user_id: str):
        return f"otp:count:{user_id}"

    async def validate_otp(self,
                           code: str,
                           user: UserEntity):
        count = await self.redis.get_key(OTPUtil._create_key(user.id))
        if count is not None:
            if count.isdigit() and int(count) > 2:
                raise ForbiddenException(code=UserServiceErrorCodeEnum.EXPIRED_VERIFICATION_CODE_PROVIDED)
        if user.verification_code != code:
            if count is not None:
                new_count = str(int(count) + 1)
            else:
                new_count = str(1)
            await self.redis.set_key(OTPUtil._create_key(user.id), new_count, TokenConfig.TOKEN_INTERVAL_IN_MINUTES.seconds)
            raise ForbiddenException(code=UserServiceErrorCodeEnum.INVALID_VERIFICATION_CODE_PROVIDED)
        if user.verification_code_expires_at is None:
            raise ForbiddenException(code=UserServiceErrorCodeEnum.EXPIRED_VERIFICATION_CODE_PROVIDED)
        if user.verification_code_expires_at < DatetimeUtil.utc_now_datetime():
            raise ForbiddenException(code=UserServiceErrorCodeEnum.EXPIRED_VERIFICATION_CODE_PROVIDED)
        user.verification_code_expires_at = None
        await UserRepository().update(user)
