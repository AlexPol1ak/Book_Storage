from typing import Annotated

from fastapi import APIRouter, Path, Depends, HTTPException, status, Body
from fastapi_users import FastAPIUsers
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


@user_router.get("/user/info/me", tags=['user'])
async def user_info_me(auth_user=Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """Returns information about the registered user."""
    user: User = await crud.get_user(session, auth_user.id)
    return UserRead.model_validate(user)


@user_router.get("/user/info/{id_or_username}", tags=['user'])
async def user_info(id_or_username: str | int,
                    auth_user=Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """Returns information about a user by their id or username."""
    ind: str | int
    user_db: User | None
    try:
        ind = int(id_or_username)
    except ValueError:
        ind = id_or_username

    user_db = await crud.get_user(session, ind)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"User not found"})

    return UserRead.model_validate(user_db)


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
                      session: AsyncSession = Depends(get_async_session)):
    """The administrator updates the user data."""
    if not auth_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={"message": "Not enough rights to perform the operation."})

    if data.status is not None:
        user_statuses: list[str] = await crud.collection_statuses(session, view='list')
        if data.status not in user_statuses:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail={
                                    "message": f"The status of {data.status} is not available. "
                                               f"Available statuses: {', '.join(user_statuses)}.",
                                    'statuses': user_statuses,
                                })

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
