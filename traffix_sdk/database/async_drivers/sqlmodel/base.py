from typing import TypeVar, Generic, Type, Union, Dict, Any, List

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """CRUD Object with default methods to Create, Read, Update and Delete (CRUD).
        Args:
            model:  SQLModel
        """
        self.model = model

    async def get(self, *, db: AsyncSession, id: int) -> ModelType | None:
        """Get a single object from the database and load into the ModelType

        Args:
            db:             SQLModel Session
            id:             Database ID
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, *, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Gets multiple objects from the database that match the filter query

        Args:
            db:             SQLModel Session
            skip:           Skip entries in database
            limit:          Limit database results
        """
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """Create an object in the database

        Args:
            db:             SQLModel Session
            obj_in:         SQLModel Object to Create in Database
        """
        db_obj = self.model.from_orm(obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Updates an existing object in the database

        Args:
            db:             SQLModel Session
            db_obj:         SQLModel Object from the Database
            obj_in:         SQLModel with changes to update db_obj
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        """Removes an existing object from the database

        Args:
            db:             SQLModel Session
            id:             ID of the database row
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one()
        await db.delete(obj)
        await db.commit()
        return obj
