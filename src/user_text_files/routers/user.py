# A router to handle user files.

from typing import Annotated, Type, List

from asyncstdlib import any_iter
from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category.manager import category_manager
from database import get_async_session
from user.auth_config import current_user

text_files_router = APIRouter(tags=['User', 'Files'], prefix='/file')