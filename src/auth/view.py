from typing import Annotated
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User

from fastapi import Depends, HTTPException, status
from src.config import settings
import jwt


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.created_at.desc())
    result: Result = await session.execute(stmt)
    product = result.scalars().all()
    return list(product)


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    return await session.get(User, user_id)


async def get_current_user(token: str = Depends(settings.OAUTH2_BEARER)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("email")
        id = payload.get("id")
        if email is None or id is None:
            raise jwt.PyJWTError
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(email=email, id=id, is_active=True)
