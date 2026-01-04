from contextlib import asynccontextmanager

from redis.asyncio import Redis

from common.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def get_redis_session() -> Redis:
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
    )
    try:
        yield redis
    finally:
        await redis.close()
