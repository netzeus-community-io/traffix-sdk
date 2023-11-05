from typing import Annotated
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from sqlmodel.ext.asyncio.session import AsyncSession
from redis import Redis

from traffix_sdk.config import settings
from traffix_sdk.dependencies.database import get_db
from traffix_sdk.dependencies.redis import get_redis

DatabaseDep = Annotated[AsyncSession, Depends(get_db)]
RedisDep = Annotated[Redis, Depends(get_redis)]
ApiKeyDep = Annotated[
    str, Depends(APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False))
]
