import asyncio
from typing import Union, Optional
from util.logger import get_custom_logger
from database.redis_setup import get_redis_session

logger = get_custom_logger(__name__)


class RedisUtil:
    @staticmethod
    async def health_check():
        try:
            async with get_redis_session() as session:
                response = await session.ping()
                return response is True
        except Exception as e:
            logger.warning(f"Redis health check failed: {e}")
            return False

    async def get_key(self, key: str) -> Optional[bytes]:
        if not await self.health_check():
            return None
        try:
            async with get_redis_session() as session:
                value = await session.get(key)
                logger.info(f'Successfully getting redis key: ', extra={"key": key, "value": value})

        except Exception as e:
            value = None
            logger.error(f'Error getting redis key: {e}', extra={"key": key})
        return value

    async def set_key(self, key: str, value: Union[int, str, float, bytes], ex: int):
        if not await self.health_check():
            return None
        try:
            async with get_redis_session() as session:
                await session.set(key, value, ex=int(ex))
                logger.info(f'Successfully setting redis key: ', extra={"key": key, "value": value, "ex": ex})

        except Exception as e:
            logger.error(f'Error setting redis key: {e}', extra={"key": key, "value": value})
            pass
        return None
