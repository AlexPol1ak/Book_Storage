from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, BaseModel, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRead(schemas.BaseUser[int]):
    """A schematic for the user to read."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    email: EmailStr
    phone_number: Optional[PhoneNumber] = Field(default=None, examples=['+375331010101'])
    status_id: int
    is_active: bool
    is_admin: bool
    is_superuser: bool
    data_joined: datetime
    rating: float


class UserCreateScheme(CreateUpdateDictModel):
    """A schema for user creation."""
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    password: str = Field(max_length=30)
    email: EmailStr
    phone_number: Optional[PhoneNumber] = Field(default=None, examples=['+375331010101'])


class UserUpdateScheme(CreateUpdateDictModel):
    """Schema for updating a user."""
    first_name: Optional[str] = Field(default=None, max_length=30)
    last_name: Optional[str] = Field(default=None, max_length=30)
    username: Optional[str] = Field(default=None, max_length=30)
    password: Optional[str] = Field(default=None, max_length=30)
    email: Optional[EmailStr]
    phone_number: Optional[PhoneNumber] = Field(default=None, examples=['+375331010101'])


class UserUpdateFull(UserUpdateScheme):
    """Updates all the user's information."""
    status: Optional[str] = Field(example='STD', default=None)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_superuser: Optional[bool] = None
    rating: Optional[float] = None


class UserDeleteScheme(BaseModel):
    """Deleted user account"""
    email: EmailStr
    password: str = Field(default=None, max_length=30)
