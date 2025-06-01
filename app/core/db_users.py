import uuid # Keep uuid for now, though IntegerIDMixin won't use it directly for user ID.
from typing import Optional

from fastapi import Depends # Keep Depends
from fastapi_users import BaseUserManager, IntegerIDMixin, models, schemas # Replaced UUIDIDMixin with IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession # Keep for type hint in get_user_db

from app.core.models import User, UserCreate, UserRead, UserUpdate # Pydantic and SQLAlchemy User model
from app.infrastructure.db.session import get_async_session


SECRET_KEY = "YOUR_SUPER_SECRET_KEY_CHANGE_ME" # Replace with env var later

class UserManager(IntegerIDMixin, BaseUserManager[User, int]): # Changed to IntegerIDMixin and User, int
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[str] = None): # Changed models.UP to User
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[str] = None # Changed models.UP to User
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[str] = None # Changed models.UP to User
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Schemas for FastAPI Users routes (already imported via fastapi_users.schemas)
# These are often re-exported or aliased for clarity if needed, but direct use of schemas.xxx is also common.
# Example: UserReadSchema = schemas.UserRead[int] # If you need to explicitly type hint the ID type
# Example: UserCreateSchema = schemas.UserCreate
# Example: UserUpdateSchema = schemas.UserUpdate

# We are using our own Pydantic models (UserCreate, UserRead, UserUpdate) which should be compatible
# as long as they meet the field requirements of fastapi-users.
# fastapi-users v11+ uses models.ID for the id type in its schemas by default.
# Our UserRead has 'id: int', UserCreate does not have 'id', UserUpdate is optional. This aligns.
