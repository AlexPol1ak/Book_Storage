from typing import Literal

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from user.manager import get_user_manager, get_password_hash
from user.models import User, Status
from user.schema import UserUpdateScheme
from database import get_async_session


async def get_user(session: AsyncSession, user: int | str) -> User | None:
    """
    Get user database.
    :param session: instance AsyncSession
    :param user: id: int or username: str
    :return: An instance of the user table or None if none is found.
    """
    result: User | None = None

    if isinstance(user, int):
        result = await session.get(User, user)
    elif isinstance(user, str):
        stmt = select(User).where(User.username == user)
        result = await session.scalar(stmt)
    return result


async def update_user(session: AsyncSession, model_data: UserUpdateScheme, user_id: int) -> User:
    """Update user."""

    data_dict = model_data.model_dump(exclude_none=True)

    if 'password' in data_dict:
        data_dict['hashed_password'] = await get_password_hash(data_dict['password'])
        data_dict.pop("password")

    # Replacing the string representation of a status with its id. If it exists.
    if 'status' in data_dict:
        status = data_dict['status']
        statuses_dict: dict[str, Status] = await collection_statuses(session, view='dict')
        if status in statuses_dict:
            data_dict['status_id'] = statuses_dict[status].id

        data_dict.pop('status')

    stmt = (update(User).where(User.id == user_id).
            values(**data_dict).returning(User))
    result = await session.scalar(stmt)

    await session.commit()
    return result


async def delete_user(session: AsyncSession, user: int | str) -> bool:
    """
    Get user database.
    :param session: instance AsyncSession
    :param user: id: int or username: str
    :return: True if the user is deleted. False if not deleted (e.g. not found).
    """
    result: User | None = None

    if isinstance(user, int):
        result = await session.get(User, user)
    elif isinstance(user, str):
        stmt = select(User).where(User.username == user)
        result = await session.scalar(stmt)

    if result is not None:
        await session.delete(result)
        await session.commit()
        return True
    else:
        return False


async def get_all_statuses(session: AsyncSession) -> list[Status]:
    """Returns all available statuses."""
    stmt = select(Status)
    result = await session.scalars(stmt)
    statuses: list[Status] = list(result.all())
    return statuses


async def collection_statuses(session: AsyncSession,
                              view: Literal['list', 'dict'] = 'list') -> dict[str, Status] | list[str]:
    """
    Returns a collection of statuses.
    :param session: AsyncSession/
    :param view: Literal 'list' return a collection of names all statuses.
                 Literal 'dict' will return a dictionary in which the key is the name of the status
                 and the value is an instance of the status.
    """
    statuses = await get_all_statuses(session)

    result_dict = {}
    for status in statuses:
        result_dict[str(status.name)] = status

    if view == 'dict':
        return result_dict
    elif view == 'list':
        return list(result_dict.keys())
    else:
        raise ValueError(f"Argument view={view} incorrect.")
