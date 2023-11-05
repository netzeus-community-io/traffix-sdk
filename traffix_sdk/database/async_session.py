from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from traffix_sdk.config import settings

# echo = Enables log output for async engine
# future = Allows seamless shift to sqlalchemy v2.0 when released
engine = create_async_engine(settings.CORE_DATABASE_URI, echo=False, future=True)

# Fixed configuration for the base database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # https://github.com/sqlalchemy/sqlalchemy/discussions/6165#discussioncomment-550636
)
