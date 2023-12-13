from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, Response
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from user import crud
from user.auth_config import auth_backend, current_user, validate_password
from user.manager import get_user_manager
from user.models import User
from user.schema import UserReadScheme, UserCreateScheme, UserUpdateScheme, UserDeleteScheme, UserReadFullScheme

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
    fastapi_users.get_register_router(UserReadScheme, UserCreateScheme),
    prefix="/auth",
)

router: APIRouter = fastapi_users.get_users_router(UserReadScheme, UserUpdateScheme)

# Remove APIRoute(path='/{id}', name='users:patch_user', methods=['PATCH']),
#        APIRoute(path='/{id}', name='users:delete_user', methods=['DELETE'])
router.routes = list(filter(lambda r: r.name != 'users:patch_user' and r.name != 'users:delete_user', router.routes))

user_router.include_router(router, prefix='/users')


@user_router.delete('/delete/me', status_code=status.HTTP_200_OK)
async def user_self_delete(
        data: UserDeleteScheme,
        response: Response,
        auth_user=Depends(current_user),
        session: AsyncSession = Depends(get_async_session),

):
    """A user deleting their page."""
    user_db = await crud.get_user(session, auth_user.id)
    if user_db.email == data.email and await validate_password(data.password, user_db.hashed_password):
        flag = await crud.delete_user(session, user_db)
        response.delete_cookie('Authorization')
        return {'deleted': flag}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect login password")


@user_router.get('/user/info/{id_or_username}', tags=['User'])
async def user_info(id_or_username: int | str,
                    auth_user=Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)) -> UserReadScheme | UserReadFullScheme:
    """Returns information about the user based on the user's permissions."""
    try:
        user = abs(int(id_or_username))
    except ValueError:
        user = id_or_username

    user_db = await crud.get_user(session, user)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    if auth_user.is_admin or auth_user.is_superuser:
        return UserReadFullScheme.model_validate(user_db)
    else:
        return UserReadScheme.model_validate(user_db)
