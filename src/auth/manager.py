from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, schemas, exceptions

from auth.models import User
from auth.utils.user import get_user_db
from config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User manager."""
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict['is_verified'] = True
        user_dict['is_superuser'] = False

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


async def get_password_hash(row_password: str) -> str:
    """Returns the password hash."""
    manager = await get_user_manager().__anext__()
    password_hash = manager.password_helper.hash(row_password)
    return password_hash
