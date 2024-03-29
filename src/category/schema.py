from datetime import datetime
from typing import Optional, List
from pydantic import EmailStr, BaseModel, ConfigDict, Field


class CategoryReadScheme(BaseModel):
    """A schema for reading the category."""
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str]
    date_joined: datetime


class CategoryInfoScheme(CategoryReadScheme):
    """A schema for reading the category."""
    count_files: int = Field(ge=0, description='Number of files')


class CategoryReadFullScheme(CategoryReadScheme):
    """A complete schema for reading the category."""

    id: int
    patch: str
    creator: int


class CategoryCreateScheme(BaseModel):
    """A schema for creating a category."""
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=3, max_length=30, example='CategoryName.')
    description: Optional[str] = Field(min_length=3, max_length=500,
                                       example="Category description up to 500 characters.", default=None)


class CategoryUpdateScheme(BaseModel):
    """A schema for updating a category."""

    name: Optional[str] = Field(max_length=30, example='New name', default=None)
    description: Optional[str] = Field(min_length=3, max_length=500,
                                       example="Category new description. Up to 500 characters.", default=None)
