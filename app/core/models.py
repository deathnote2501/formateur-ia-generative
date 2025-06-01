from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB # Import JSONB

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    slides = relationship("Slide", back_populates="course")

class Slide(Base):
    __tablename__ = "slides"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    template_type = Column(String, nullable=False)
    content_json = Column(JSONB, nullable=False)  # Use JSONB
    specific_prompt = Column(String, nullable=True)
    suggested_messages_json = Column(JSONB, nullable=True)  # Use JSONB

    course = relationship("Course", back_populates="slides")

# Add imports for fastapi-users and pydantic schemas (assuming they will be in app.core.schemas)
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

# Placeholder for Pydantic schemas - these will need to be created
# For now, let's assume they will be available from app.core.schemas
# If app.core.schemas does not exist or is empty, these lines will cause issues later
# but are needed for the FastAPIUsers generic types.
# We will create these schemas in the next step.
from app.core.schemas import UserRead, UserCreate

# This will be defined properly in app/infrastructure/db/session.py
# For now, we need a placeholder for type hinting in SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.session import get_async_session # This will be created later

# Placeholder for get_async_session dependency
# This is just to allow the file to be written without errors.
# The actual dependency will be created in a later step.


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

SECRET_KEY = "YOUR_SUPER_SECRET_KEY_CHANGE_ME" # TODO: Load from environment variables

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# Note: UserManager requires Pydantic schemas that might not exist yet.
# We are using imported schemas UserRead and UserCreate from app.core.schemas.
# These will need to be properly defined in app.core.schemas.
# fastapi_users = FastAPIUsers[User, UserCreate, UserRead]( # This line should be User.id, not User
fastapi_users = FastAPIUsers[User, int, UserRead, UserCreate, UserRead]( # Corrected: User.id is int
    get_user_db,
    [auth_backend],
)

# Placeholder for UserManager, will be properly initialized in main.py or a similar setup file
# current_user = fastapi_users.current_user()
