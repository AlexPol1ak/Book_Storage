from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from user.manager import get_user_manager
from user.models import User
from config import SECRET_AUTH, LIFETIME_TOKEN

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Strategy for obtaining the token"""
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=LIFETIME_TOKEN)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
# Текущий пользователь
current_user = fastapi_users.current_user()


async def validate_password(row_password: str, hashed_password: str) -> bool:
    """
    Checks the password against its hash.
    :param row_password: Not an encrypted password.
    :param hashed_password: Password hash.
    :return: True if the password matches the hash, otherwise False.
    """
    manager = await anext(get_user_manager())
    flag, _ = manager.password_helper.verify_and_update(row_password, hashed_password)
    return flag

