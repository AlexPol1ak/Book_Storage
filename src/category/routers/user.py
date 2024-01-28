# Routes for registered users.

from typing import Annotated, Type

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
