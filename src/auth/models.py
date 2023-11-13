from datetime import timedelta
from typing import List

from src.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    token: Mapped[List["Token"]] = relationship(back_populates="user")


class Token(Base):
    access_token: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    time_live: Mapped[timedelta] = mapped_column(
        nullable=False, default=timedelta(minutes=60)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="token")
