from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, BaseModel, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRead(schemas.BaseUser[int]):
    """A schematic for the user to read."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: Optional[PhoneNumber] = None
    status_id: int
    is_active: bool
    is_admin: bool
    is_superuser: bool
    data_joined: datetime
    rating: float


class UserCreate(CreateUpdateDictModel):
    """A schema for user creation."""
    first_name: str
    last_name: str
    username: str
    password: str
    email: EmailStr
    phone_number: Optional[PhoneNumber] = None


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneNumber] = None


class UserUpdateFull(UserUpdate):
    """Updates all the user's information."""
    status_id: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_superuser: Optional[bool] = None
    data_joined: Optional[bool] = None
    rating: Optional[float] = None
