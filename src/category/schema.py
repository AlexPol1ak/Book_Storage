from datetime import datetime
from typing import Optional
from pydantic import EmailStr, BaseModel, ConfigDict, Field


class CategoryReadScheme(BaseModel):
    """A schema for reading the category."""
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str]


class CategoryReadFullScheme(CategoryReadScheme):
    """A complete schema for reading the category."""

    id: int
    patch: str
    data_joined: datetime
    creator: int


class CategoryCreateScheme(BaseModel):
    """A schema for creating a category."""
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=30)
    description: Optional[str] = Field(min_length=500)
