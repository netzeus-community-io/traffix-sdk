from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from loguru import logger
from traffix_sdk.database.async_drivers.sqlmodel.base import CRUDBase
from traffix_sdk.models import (
    TraffixUpdate,
    TraffixUpdateCreate,
    TraffixUpdateUpdate,
)
from traffix_sdk.database.async_drivers import sqlmodel as crud


class CRUDTraffixUpdate(
    CRUDBase[TraffixUpdate, TraffixUpdateCreate, TraffixUpdateUpdate]
):
    async def get_by_name(self, db: AsyncSession, name: str) -> TraffixUpdate | None:
        """Get a Update by name.

        Args:
            db:         SQLModel Session
            name:       Name of Update
        """
        user = await db.execute(select(TraffixUpdate).where(TraffixUpdate.name == name))
        return user.scalar_one_or_none()


traffix_update = CRUDTraffixUpdate(TraffixUpdate)
