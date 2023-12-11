from typing import Annotated

from fastapi import APIRouter, Path, Depends, HTTPException, status, Body
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from user.auth_config import auth_backend, current_user
from user.manager import get_user_manager
from user.models import User
from user.schema import UserRead, UserCreateScheme, UserUpdateScheme, UserUpdateFull, UserDeleteScheme
from database import get_async_session
from . import crud

