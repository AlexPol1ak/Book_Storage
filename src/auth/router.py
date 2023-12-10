from typing import Annotated

from fastapi import APIRouter, Path, Depends, HTTPException, status
from fastapi_users import FastAPIUsers
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import auth_backend, current_user
from auth.manager import get_user_manager
from auth.models import User
from auth.schema import UserRead, UserCreate, UserUpdate, UserUpdateFull
from database import get_async_session
from . import crud

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
async def user_self_update(data: UserUpdate,
                           auth_user=Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """Updating the user with their data."""

    user_db = await crud.update_user(session, data, auth_user.id)
    return UserRead.model_validate(user_db)


@user_router.put("/user/update/{user_id}", tags=['user'])
async def user_update(user_id: Annotated[int, Path(qe=1)],
                      data: UserUpdateFull,
                      auth_user=Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)) :
    """The administrator updates the user data."""
    if not auth_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={"message": "Not enough rights to perform the operation."})

    user_db = await crud.update_user(session, data, user_id)
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"User id: {user_id} not found"})

    return UserRead.model_validate(user_db)


@user_router.delete("/user/delete/", tags=['user'])
async def user_self_delete():
    """Account deletion by a user."""
    pass


@user_router.delete("/user/delete/{user_id}", tags=['user'])
async def user_delete(user_id: Annotated[int, Path(ge=1)]):
    """Account deletion by admin."""
    pass
