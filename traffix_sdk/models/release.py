from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import constr
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy import BigInteger
from traffix_sdk.config import settings
from traffix_sdk.models.link_tables import ReleaseCategoryLink, ReleasePlatformLink
from traffix_sdk.models.category import TraffixCategory, TraffixCategoryName

if TYPE_CHECKING:
    from traffix_sdk.models.platforms import TraffixPlatform
    from traffix_sdk.models.update import TraffixUpdate


class TraffixReleaseBase(SQLModel):
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


class TraffixReleaseCreate(TraffixReleaseBase):
    name: str
    estimated_size: int
    categories: Optional[List[str]] = []


class TraffixReleaseRead(TraffixReleaseBase):
    categories: Optional[List[TraffixCategoryName]] = []


class TraffixReleaseUpdate(TraffixReleaseBase):
    categories: Optional[List[str]]


class TraffixRelease(TraffixReleaseBase, table=True):
    id: int = Field(default=None, primary_key=True)
    categories: List[TraffixCategory] = Relationship(
        back_populates="releases",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ReleaseCategoryLink,
    )
    updates: Optional[List["TraffixUpdate"]] = Relationship(
        back_populates="release", sa_relationship_kwargs={"lazy": "selectin"}
    )
    platforms: Optional[List["TraffixPlatform"]] = Relationship(
        back_populates="releases",
        sa_relationship_kwargs={"lazy": "selectin"},
        link_model=ReleasePlatformLink,
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
