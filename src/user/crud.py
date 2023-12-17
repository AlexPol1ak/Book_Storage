from typing import Literal, Type, Any, Coroutine

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from user.manager import get_user_manager
from user.models import User, Status
from user.schema import UserUpdateFullScheme


async def get_user(session: AsyncSession, user: int | str) -> User | None:
    """
    Get user database.
    :param session: instance AsyncSession
    :param user: id: int or username: str
    :return: An instance of the user table or None if none is found.
    """
    result: User | None = None

    if isinstance(user, int):
        result = await session.get(User, abs(user))
    elif isinstance(user, str):
        stmt = select(User).where(User.username == user)
        result = await session.scalar(stmt)
    return result


async def update_user(session: AsyncSession, model_data: UserUpdateFullScheme, user_id: int) \
        -> Coroutine[Any, Any, User | None] | None:
    """Update user."""
    data_dict = model_data.model_dump(exclude_none=True)
    if len(data_dict) == 0:
        raise ValueError("Empty data.")
    updated_user: User | None = None

    if 'status' in data_dict:
        user = await get_user(session, user_id)
        if not user:
            raise ValueError(f"User id {user_id} not found")
        statuses: dict[str, Status] = await collection_statuses(session, view='dict')
        if data_dict['status'] in statuses:
            status: Status = statuses[data_dict['status']]
            user.status = status
            session.add(user)
            updated_user = user
            data_dict.pop('status')
        else:
            raise ValueError(f"Status '{data_dict['status']}' not found")

    if 'password' in data_dict:
        manager = await anext(get_user_manager())
        hashed_password = manager.password_helper.hash(data_dict['password'])
        data_dict['hashed_password'] = hashed_password
        data_dict.pop('password')

    if len(data_dict) > 0:
        stmt = update(User).where(User.id == user_id).values(**data_dict).returning(User)
        updated_user = await session.scalar(stmt)

    await session.commit()

    return updated_user


async def delete_user(session: AsyncSession, user: int | str | User) -> bool:
    """
    Get user database.
    :param session: instance AsyncSession
    :param user: id: int or username: str
    :return: True if the user is deleted. False if not deleted (e.g. not found).
    """
    result: User | None | Type[User] = None

    if isinstance(user, int):
        result = await session.get(User, user)
    elif isinstance(user, str):
        stmt = select(User).where(User.username == user)
        result = await session.scalar(stmt)
    elif isinstance(user, User):
        result = user

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
