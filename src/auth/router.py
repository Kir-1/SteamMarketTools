import time
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from src.auth import view, controller
from src.auth.schemas import User, UserAuth, TokenView, UserView
from src.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_cache.decorator import cache

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[UserView])
async def get_users(
    user: UserAuth = Depends(view.get_current_user),
    session: AsyncSession = Depends(database.get_async_session),
):
    return await view.get_users(session=session)


@router.get("/me", response_model=UserView)
async def get_user_by_id(
    user: UserAuth = Depends(view.get_current_user),
    session: AsyncSession = Depends(database.get_async_session),
):
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/", response_model=User, status_code=201)
async def create_user(
    user: UserAuth, session: AsyncSession = Depends(database.get_async_session)
):
    return await controller.create_user(session=session, user=user)


@router.post("/token", response_model=TokenView)
@cache(expire=3600)
async def auth_for_token(
    user: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(database.get_async_session),
):
    return await controller.auth_user(
        session=session, user=UserAuth(email=user.username, password=user.password)
    )
