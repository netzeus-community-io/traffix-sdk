from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from sqlalchemy.sql import func
from traffix_sdk.models.link_tables import ReleasePlatformLink

if TYPE_CHECKING:
    from traffix_sdk.models.release import TraffixRelease


class TraffixPlatformBase(SQLModel):
    name: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TraffixPlatformCreate(TraffixPlatformBase):
    name: str


class TraffixPlatformRead(TraffixPlatformBase):
    id: int


class TraffixPlatformUpdate(TraffixPlatformBase):
    pass


class TraffixPlatform(TraffixPlatformBase, table=True):
    id: int = Field(default=None, primary_key=True)
    releases: Optional[List["TraffixRelease"]] = Relationship(
        back_populates="platforms", link_model=ReleasePlatformLink
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
