from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from auth.auth_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schema import UserRead, UserCreate

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"]
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt/register",
    tags=["auth"],
)
