import uuid
from datetime import timedelta, datetime

import jwt
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserAuth
from fastapi import HTTPException, status
from src.config import settings
from src.auth.schemas import TokenView


async def create_user(session: AsyncSession, user: UserAuth) -> User:
    if await session.scalar(select(User).where(User.email == user.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    user = User(**user.model_dump())
    user.password = settings.PWD_CONTEXT.hash(user.password)
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def auth_user(session: AsyncSession, user: UserAuth) -> TokenView:
    user_db: User = await session.scalar(
        select(User).where(User.email == user.email).where(User.is_active == True)
    )
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User doesn't exists",
        )

    if not settings.PWD_CONTEXT.verify(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password or email",
        )
    encode = {
        "email": user_db.email,
        "id": str(user_db.id),
        "exp": datetime.utcnow() + timedelta(minutes=60),
    }
    # expires = datetime.utcnow() + timedelta(minutes=60)
    # encode.update({"exp": expires.timestamp()})

    token: TokenView = TokenView(
        access_token=jwt.encode(
            encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
    )
    return token
