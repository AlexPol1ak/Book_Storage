from typing import Annotated

from fastapi import APIRouter, Path, Depends
from fastapi_users import FastAPIUsers

from auth.auth_config import auth_backend, current_user
from auth.manager import get_user_manager
from auth.models import User
from auth.schema import UserRead, UserCreate, UserUpdate, UserUpdateFull
from auth.utils.user import get_user_db

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["auth"],
)


@user_router.put("/user/update/", tags=['user'])
async def user_self_update(data: UserUpdate, user=Depends(current_user)):
    """Updating the user with their data."""

    print(data.username)
    return data



@user_router.put("/user/update/{user_id}", tags=['user'])
async def user_update(user_id: Annotated[int, Path(qe=1)], data: UserUpdateFull):
    """The administrator updates the user data."""
    pass


@user_router.delete("/user/delete/", tags=['user'])
async def user_self_delete():
    """Account deletion by a user."""
    pass


@user_router.delete("/user/delete/{user_id}", tags=['user'])
async def user_delete(user_id: Annotated[int, Path(ge=1)]):
    """Account deletion by admin."""
    pass
