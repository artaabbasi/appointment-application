from datetime import timedelta

from common.lib.base_service import BaseService
from util.redis_util import RedisUtil


class RedisJwtUtil(BaseService):
    def __init__(self):
        self.redis = RedisUtil()

    @staticmethod
    def _create_key(token: str):
        return f"jwt:blacklist:{token}"

    async def is_token_blacklisted(self, token: str) -> bool:
        return await self.redis.get_key(self._create_key(token)) is not None

    async def blacklist_token(self, token: str) -> None:
        await self.redis.set_key(self._create_key(token), "blacklist",
                                 int(timedelta(minutes=self._get_settings().REFRESH_TOKEN_EXPIRATION_TIME_DELTA_MINUTES).total_seconds()))

