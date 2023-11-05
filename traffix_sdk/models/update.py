from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import constr
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy import BigInteger
from traffix_sdk.config import settings
from traffix_sdk.models.category import TraffixCategory, TraffixCategoryName
from traffix_sdk.models.release import TraffixRelease


class TraffixUpdateBase(SQLModel):
    name: Optional[str]
    description: Optional[str]
    estimated_size: Optional[int] = Field(sa_column=Column(BigInteger()))
    size: Optional[int] = Field(sa_column=Column(BigInteger()))
    release_date: Optional[datetime]
    image_url: Optional[constr(max_length=settings.MAX_IMAGE_URL_LENGTH)]
    verified: Optional[bool] = False
    verified_date: Optional[datetime]
    verified_by: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TraffixUpdateCreate(TraffixUpdateBase):
    name: str
    estimated_size: int
    release_id: int


class TraffixUpdateRead(TraffixUpdateBase):
    release: Optional[TraffixRelease] = None


class TraffixUpdateUpdate(TraffixUpdateBase):
    release_id: Optional[int]


class TraffixUpdate(TraffixUpdateBase, table=True):
    id: int = Field(default=None, primary_key=True)
    release_id: Optional[int] = Field(default=None, foreign_key="traffixrelease.id")
    release: Optional["TraffixRelease"] = Relationship(
        back_populates="updates", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
