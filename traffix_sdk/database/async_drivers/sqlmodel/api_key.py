from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from traffix_sdk.database.async_drivers.sqlmodel.base import CRUDBase
from traffix_sdk.models import TraffixAPIKey, TraffixAPIKeyCreate, TraffixAPIKeyUpdate

class CRUDTraffixAPIKey(CRUDBase[TraffixAPIKey, TraffixAPIKeyCreate, TraffixAPIKeyUpdate]):
    async def get_by_api_key(self, db: AsyncSession, api_key: str) -> TraffixAPIKey | None:
        """Get an API Key by api_key.
        
        Args:
            db:         SQLModel Session
            api_key:    API Key to find
        """
        user = await db.execute(select(TraffixAPIKey).where(TraffixAPIKey.api_key == api_key))
        return user.scalar_one_or_none()
    
traffix_api_key = CRUDTraffixAPIKey(TraffixAPIKey)