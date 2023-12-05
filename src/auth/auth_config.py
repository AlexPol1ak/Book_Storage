from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

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
