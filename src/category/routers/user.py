# Routes for registered users.

from typing import Annotated, Type, List

from asyncstdlib import any_iter
from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category.manager import category_manager
from category.schema import CategoryInfoScheme
from database import get_async_session
from user.auth_config import current_user

category_router = APIRouter(tags=['User', 'Category'], prefix='/category')


@category_router.get('/info/{category_name_or_id}')
async def category_info(
        category_name_or_id: Annotated[str, Path(min_length=2)],
        auth_user=Depends(current_user),
        session: AsyncSession = Depends(get_async_session)) -> CategoryInfoScheme:
    try:
        category_dict = await category_manager.get_category(session, category_name_or_id)
        return CategoryInfoScheme(name=category_dict.get('name'),
                                  description=category_dict.get('description'),
                                  date_joined=category_dict.get('date_joined'),
                                  count_files=category_dict.get('count_files')
                                  )
    except NotADirectoryError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category {category_name_or_id} not found.")


@category_router.get('/all')
async def all_categories(session: AsyncSession = Depends(get_async_session)) -> List[CategoryInfoScheme]:
    """Returns a list with information about all categories."""
    try:
        categories = await category_manager.all_categories(session)
        result: List[CategoryInfoScheme] = []

        categories = any_iter(categories)  # Get async iterator

        async for cat in categories:
            obj = CategoryInfoScheme(name=cat.get('name'),
                                     description=cat.get('description'),
                                     date_joined=cat.get('date_joined'),
                                     count_files=cat.get('count_files')
                                     )
            result.append(obj)

        return result

    except NotADirectoryError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categories not found.")
