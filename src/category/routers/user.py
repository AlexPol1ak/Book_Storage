# Routes for registered users.

from typing import Annotated, Type

from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

category_router = APIRouter(tags=['User', 'Category'], prefix='/category')
