from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from loguru import logger
from traffix_sdk.database.async_drivers.sqlmodel.base import CRUDBase
from traffix_sdk.models import (
    TraffixRelease,
    TraffixReleaseCreate,
    TraffixReleaseUpdate,
)
from traffix_sdk.database.async_drivers import sqlmodel as crud


class CRUDTraffixRelease(
    CRUDBase[TraffixRelease, TraffixReleaseCreate, TraffixReleaseUpdate]
):
    async def create(
        self, *, db: AsyncSession, obj_in: TraffixReleaseCreate
    ) -> TraffixRelease:
        """Create an object in the database

        Args:
            db:             SQLModel Session
            obj_in:         SQLModel Object to Create in Database
        """
        db_obj = self.model.from_orm(obj_in)

        categories = []
        for category in obj_in.categories:
            category_exist = await crud.traffix_category.get_by_name(
                db=db, name=category
            )
            if not category_exist:
                continue

            categories.append(category_exist)

        db_obj.categories = categories
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_name(self, db: AsyncSession, name: str) -> TraffixRelease | None:
        """Get a Release by name.

        Args:
            db:         SQLModel Session
            name:       Name of Release
        """
        user = await db.execute(
            select(TraffixRelease).where(TraffixRelease.name == name)
        )
        return user.scalar_one_or_none()


traffix_release = CRUDTraffixRelease(TraffixRelease)
