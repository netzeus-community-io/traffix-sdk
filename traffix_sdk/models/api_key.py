from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import uuid4
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from sqlalchemy.sql import func
from pydantic import constr

if TYPE_CHECKING:
    from traffix_sdk.models.user import TraffixAPIUser


class TraffixAPIKeyBase(SQLModel):
    api_key: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    expires_at: Optional[datetime]
    user_id: int


class TraffixAPIKeyCreate(TraffixAPIKeyBase):
    api_key: constr(min_length=36, max_length=36) = Field(default=str(uuid4()))


class TraffixAPIKeyRead(TraffixAPIKeyBase):
    id: int


class TraffixAPIKeyUpdate(TraffixAPIKeyBase):
    user_id: Optional[int]


class TraffixAPIKey(TraffixAPIKeyBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="traffixapiuser.id")
    user: Optional["TraffixAPIUser"] = Relationship(
        back_populates="api_keys", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
