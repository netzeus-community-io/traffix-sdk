from sqlmodel import SQLModel, Field, Relationship, Column, String, DateTime, text
from sqlalchemy import func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from traffix_sdk.models.api_key import TraffixAPIKey


class TraffixAPIUserBase(SQLModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class TraffixAPIUserCreate(TraffixAPIUserBase):
    email: str
    password: str


class TraffixAPIUserRead(TraffixAPIUserBase):
    id: int


class TraffixAPIUserUpdate(TraffixAPIUserBase):
    password: Optional[str]


class TraffixAPIUser(TraffixAPIUserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: Optional[str]
    api_keys: Optional[List["TraffixAPIKey"]] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
