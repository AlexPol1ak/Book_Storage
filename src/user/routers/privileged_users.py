from enum import Enum
from typing import Annotated, Type

from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from user import crud
from user.auth_config import current_user
from user.schema import UserUpdateFullScheme, UserReadFullScheme

admin_router = APIRouter(tags=['Admin and superuser'])


@admin_router.patch("/user/update/{user_id}")
async def user_update(user_id: Annotated[int, Path(qe=1)],
                      data: UserUpdateFullScheme,
                      auth_user=Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    """The administrator updates the user data."""
    if not auth_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={"message": "Not enough rights to perform the operation."})

    if data.status is not None:
        user_statuses: list[str] = await crud.collection_statuses(session, view='list')
        if data.status not in user_statuses:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail={
                                    "message": f"The status of {data.status} is not available. "
                                               f"Available statuses: {', '.join(user_statuses)}.",
                                    'statuses': user_statuses,
                                })
    try:
        user_db = await crud.update_user(session, data, user_id)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"{ex}"})

    return UserReadFullScheme.model_validate(user_db)


@admin_router.delete("/user/delete/{user_id}")
async def user_delete(user_id: Annotated[int, Path(ge=1)],
                      auth_user=Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)
                      ):
    """
    Account deletion by admin.
    Returns true if the deletion was successful. False if the user is not found or deleted.
    """

    if not auth_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={"message": "Not enough rights to perform the operation."})
    else:
        flag = await crud.delete_user(session, user_id)
        return {"result": flag}


@admin_router.get('/user/edit-status/{user_id}/{new_status}')
async def edit_status_user(user_id: Annotated[int, Path(ge=1)],
                           new_status: str,
                           auth_user=Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)
                           ):
    if not auth_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={"message": "Not enough rights to perform the operation."})

    statuses: list = await crud.collection_statuses(session, view='list')
    if new_status not in statuses:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={
                                "message": f"The status of {new_status} is not available. "
                                           f"Available statuses: {', '.join(statuses)}.",
                                'statuses': statuses,
                            })

    update_scheme = UserUpdateFullScheme(status=new_status)
    try:
        user_db = await crud.update_user(session, update_scheme, user_id)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": f"{ex}"})

    return UserReadFullScheme.model_validate(user_db)
