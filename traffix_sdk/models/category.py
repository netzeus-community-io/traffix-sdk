from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from sqlalchemy.sql import func
from traffix_sdk.models.link_tables import ReleaseCategoryLink

if TYPE_CHECKING:
    from traffix_sdk.models.release import TraffixRelease


class TraffixCategoryBase(SQLModel):
    name: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TraffixCategoryCreate(TraffixCategoryBase):
    name: str


class TraffixCategoryRead(TraffixCategoryBase):
    id: int


class TraffixCategoryUpdate(TraffixCategoryBase):
    pass


class TraffixCategoryName(SQLModel):
    name: str


class TraffixCategory(TraffixCategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    releases: Optional[List["TraffixRelease"]] = Relationship(
        back_populates="categories", link_model=ReleaseCategoryLink
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
