from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    """A schematic for the user to read."""
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: Optional[str]
    status: str = "STD"
    is_active: bool
    is_admin: bool
    is_superuser: bool
    data_joined: datetime
    rating: float

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    """A schema for user creation."""
    first_name: str
    last_name: str
    username: str
    phone_number: Optional[str]
    is_active: Optional[bool] = Field(exclude=True)
    is_verified: Optional[bool] = Field(exclude=True)
    is_superuser: Optional[bool] = Field(exclude=True)

    # class Config:
    #     exclude = {'is_active', 'is_superuser', 'is_verified'}


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating a user."""
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
