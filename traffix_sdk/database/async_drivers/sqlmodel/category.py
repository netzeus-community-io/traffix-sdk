from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from traffix_sdk.database.async_drivers.sqlmodel.base import CRUDBase
from traffix_sdk.models import (
    TraffixCategory,
    TraffixCategoryCreate,
    TraffixCategoryUpdate,
)


class CRUDTraffixCategory(
    CRUDBase[TraffixCategory, TraffixCategoryCreate, TraffixCategoryUpdate]
):
    async def get_by_name(self, db: AsyncSession, name: str) -> TraffixCategory | None:
        """Get a Category by name.

        Args:
            db:         SQLModel Session
            name:       Name of Category
        """
        user = await db.execute(
            select(TraffixCategory).where(TraffixCategory.name == name)
        )
        return user.scalar_one_or_none()


traffix_category = CRUDTraffixCategory(TraffixCategory)
