# Routes for privileged users.


from typing import Annotated, Type

from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category import crud
from category.schema import CategoryCreateScheme, CategoryReadScheme
from config import STORAGE
from database import get_async_session
from user.auth_config import current_user

p_category_router = APIRouter(tags=['Admin and superuser', 'Category'], prefix='/category')


@p_category_router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_category(
        data: CategoryCreateScheme,
        auth_user=Depends(current_user),
        session: AsyncSession = Depends(get_async_session)) -> CategoryReadScheme:
    """Creates a new category and returns information about it."""

    if auth_user.is_superuser or auth_user.is_admin:
        try:
            category_path = await STORAGE.add_category(data.name)
            category_obj = await crud.create_category(session, data.name, data.description, category_path, auth_user.id)
            return CategoryReadScheme.model_validate(category_obj)
        except (FileExistsError, ValueError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Category {data.name} exists")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not enough authority.")