from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class ReleaseCategoryLink(SQLModel, table=True):
    release_id: Optional[int] = Field(
        default=None, foreign_key="traffixrelease.id", primary_key=True
    )
    category_id: Optional[int] = Field(
        default=None, foreign_key="traffixcategory.id", primary_key=True
    )


class ReleasePlatformLink(SQLModel, table=True):
    release_id: Optional[int] = Field(
        default=None, foreign_key="traffixrelease.id", primary_key=True
    )
    platform_id: Optional[int] = Field(
        default=None, foreign_key="traffixplatform.id", primary_key=True
    )
