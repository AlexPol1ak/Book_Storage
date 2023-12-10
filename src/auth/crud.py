from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.manager import get_user_manager
from auth.models import User
from auth.schema import UserUpdateFull, UserUpdate


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    """Get user database"""
    user = await session.get(User, user_id)
    return user


async def update_user(session: AsyncSession, model_data: UserUpdate, user_id: int) -> User:
    """Update user."""

    data_dict = model_data.model_dump(exclude_none=True)
    if 'password' in data_dict:
        manager = await get_user_manager().__anext__()
        data_dict['hashed_password'] = manager.password_helper.hash(data_dict['password'])
        data_dict.pop("password")

    stmt = (update(User).where(User.id == user_id).
            values(**data_dict).returning(User))
    result = await session.scalar(stmt)
    await session.commit()
    return result
