from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from user import crud
from user.auth_config import auth_backend, current_user
from user.manager import get_user_manager
from user.models import User
from user.schema import UserRead, UserCreateScheme, UserUpdateScheme, UserDeleteScheme

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

user_router = APIRouter(tags=['User'])

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
)

user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreateScheme),
    prefix="/auth/jwt",
)


@user_router.get("/user/info/me")
async def user_info_me(auth_user=Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """Returns information about the registered user."""
    user: User = await crud.get_user(session, auth_user.id)
    return UserRead.model_validate(user)


@user_router.get("/user/info/{id_or_username}")
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


@user_router.put("/user/update/")
async def user_self_update(data: UserUpdateScheme,
                           auth_user=Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """Updating the user with their data."""

    user_db = await crud.update_user(session, data, auth_user.id)
    return UserRead.model_validate(user_db)


@user_router.delete("/user/delete/")
async def user_self_delete(data: UserDeleteScheme,
                           auth_user=Depends(current_user),
                           session: AsyncSession = Depends(get_async_session),
                           ):
    """Account deletion by a user."""
    pass
