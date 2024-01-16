from datetime import datetime
from typing import Optional
from pydantic import EmailStr, BaseModel, ConfigDict, Field


class CategoryReadScheme(BaseModel):
    """A schema for reading the category."""
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str]
    data_joined: datetime


class CategoryReadFullScheme(CategoryReadScheme):
    """A complete schema for reading the category."""

    id: int
    patch: str
    creator: int


class CategoryCreateScheme(BaseModel):
    """A schema for creating a category."""
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=3 ,max_length=30, example='CategoryName.')
    description: Optional[str] = Field(min_length=3, max_length=500,
                                       example="Category description up to 500 characters.")
