from loguru import logger
from redis import asyncio as aioredis
from traffix_sdk.config import settings


async def get_redis() -> aioredis.Redis:
    """Returns instance of redis for caching purposes."""
    try:
        client = await aioredis.from_url(
            str(settings.REDIS_URI), encoding="utf8", decode_responses=True
        )

        logger.success(f"Connected to redis - {settings.REDIS_URI}")
        return client

    except ConnectionError as e:
        logger.error(f"Redis ConnectionError occured: {e}")

    except Exception as e:
        logger.error(f"Redis Generic Exception occured: {e}")
