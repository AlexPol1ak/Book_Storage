# A router to handle user files. For privileged users.

from typing import Annotated, Type, Optional
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category.manager import category_manager
from database import get_async_session
from user.user_dependencies import is_superuser_or_admin

p_text_files_router = APIRouter(tags=['Admin and superuser', 'Files'], prefix='/file')