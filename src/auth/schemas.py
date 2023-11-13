from datetime import datetime, timedelta
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr


class UserView(BaseModel):
    email: EmailStr


class UserAuth(UserView):
    email: EmailStr
    password: str


class User(UserAuth):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    id: UUID
    is_active: bool
    is_superuser: bool
    is_verified: bool


class TokenView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
