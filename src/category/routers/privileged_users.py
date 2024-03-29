# Routes for privileged users.

from typing import Annotated, Type, Optional
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category.manager import category_manager
from category.schema import CategoryCreateScheme, CategoryReadScheme, CategoryUpdateScheme
from config import STORAGE
from database import get_async_session
from user.user_dependencies import is_superuser_or_admin

p_category_router = APIRouter(tags=['Admin and superuser', 'Category'], prefix='/category')


@p_category_router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_category(
        data: CategoryCreateScheme,
        auth_user=Depends(is_superuser_or_admin),
        session: AsyncSession = Depends(get_async_session)) -> CategoryReadScheme:
    """Creates a new category and returns information about it."""

    try:
        category_dict = await category_manager.create(session, data.name, data.description, auth_user.id)
        return CategoryReadScheme(name=category_dict.get('name'),
                                  description=category_dict.get('description'),
                                  data_joined=category_dict.get('date_joined'),
                                  )
    except (FileExistsError, ValueError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Category {data.name} exists")


@p_category_router.patch('/update/{category_name_or_id}')
async def update_category(category_name_or_id: str | int,
                          data: CategoryUpdateScheme,
                          auth_user=Depends(is_superuser_or_admin),
                          session: AsyncSession = Depends(get_async_session)) -> CategoryReadScheme:
    """Updates the category name or description and returns information about the category."""
    try:
        category_dict = await category_manager.update(session, category_name_or_id,
                                                      new_name=data.name, new_description=data.description)
        return CategoryReadScheme(name=category_dict.get('name'),
                                  description=category_dict.get('description'),
                                  data_joined=category_dict.get('date_joined'),
                                  )
    except NotADirectoryError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category {category_name_or_id} not found.")
    except IsADirectoryError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Category {category_name_or_id} is not empty.")



@p_category_router.delete('/delete/{category_name_or_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_name_or_id: str | int,
                          auth_user=Depends(is_superuser_or_admin),
                          session: AsyncSession = Depends(get_async_session)
                          ):
    """Deletes a category if it is not empty."""

    try:
        await category_manager.delete(session, category_name_or_id)
    except NotADirectoryError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category {category_name_or_id} not found.")
    except IsADirectoryError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Category {category_name_or_id} is not empty.")
