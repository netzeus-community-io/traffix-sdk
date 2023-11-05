from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from traffix_sdk.database.async_drivers.sqlmodel.base import CRUDBase
from traffix_sdk.models.user import TraffixAPIUser, TraffixAPIUserCreate, TraffixAPIUserUpdate
from traffix_sdk.security.auth import get_password_hash, verify_password

class CRUDTraffixUser(CRUDBase[TraffixAPIUser, TraffixAPIUserCreate, TraffixAPIUserUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str) -> TraffixAPIUser | None:
        """Get a user by email address.
        
        Args:
            db:     SQLModel Session
            email:  Email address
        """
        user = await db.execute(select(TraffixAPIUser).where(TraffixAPIUser.email == email))
        return user.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, obj_in: TraffixAPIUserCreate) -> TraffixAPIUser:
        """Creates a user and hashes the password.
        
        Args:
            db:     SQLModel Session
            obj_in: TraffixAPIUserCreate Object
        """
        db_obj = TraffixAPIUser.from_orm(obj_in)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, db_obj: TraffixAPIUser, obj_in: TraffixAPIUserUpdate) -> TraffixAPIUser:
        """Updates a user.
        
        Args:
            db:     SQLModel Session
            db_obj: Current TraffixAPIUser Object in the database
            obj_in: TraffixAPIUserCreate Object
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True, exclude_none=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if obj_in.password:
            db_obj.hashed_password = get_password_hash(password=obj_in.password)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def authenticate(self, db: AsyncSession, email: str, password: str) -> TraffixAPIUser | None:
        """Attempts to authenticate a user.
        
        Args:
            db:         SQLModel Session
            email:      Users email address
            password:   Users password
        """
        user = await self.get_by_email(db=db, email=email)
        if not user or not user.is_active:
            return None
        
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        
        return user
    
traffix_user = CRUDTraffixUser(TraffixAPIUser)