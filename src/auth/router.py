from typing import Annotated

from fastapi import APIRouter, Path, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import auth_backend, current_user
from auth.manager import get_user_manager
from auth.models import User
from auth.schema import UserRead, UserCreate, UserUpdate, UserUpdateFull
from database import get_async_session

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
                           session: AsyncSession = Depends(get_async_session)):
    """Updating the user with their data."""
    data_dict = data.model_dump(exclude_none=True)
    if 'password' in data_dict:
        manager = await get_user_manager().__anext__()
        data_dict['hashed_password'] = manager.password_helper.hash(data_dict['password'])
        data_dict.pop("password")

    stmt = (update(User).where(User.id == auth_user.id).
            values(**data_dict).returning(User))
    result = await session.scalar(stmt)
    await session.commit()

    result_model = UserRead.model_validate(result, from_attributes=True)
    return result_model


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
