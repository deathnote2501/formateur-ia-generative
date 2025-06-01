from typing import Optional, List
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON # Added JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB # For PostgreSQL specific JSON type
# We won't define SQLAlchemy models yet, but we need Base for Alembic

Base = declarative_base()

# Pydantic models
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True # Renamed from from_attributes for Pydantic v2

class UserUpdate(UserBase): # UserUpdate was already here
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: int

    class Config:
        orm_mode = True

class CourseUpdate(CourseBase):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class SlideBase(BaseModel):
    course_id: int
    order_index: int
    template_type: str
    content_json: dict
    specific_prompt: Optional[str] = None
    suggested_messages_json: Optional[List[str]] = None

class SlideCreate(SlideBase):
    pass

class SlideRead(SlideBase):
    id: int

    class Config:
        orm_mode = True

class SlideUpdate(SlideBase):
    course_id: Optional[int] = None
    order_index: Optional[int] = None
    template_type: Optional[str] = None
    content_json: Optional[dict] = None
    specific_prompt: Optional[str] = None
    suggested_messages_json: Optional[List[str]] = None

    class Config:
        orm_mode = True

# Chat Schemas (New)
class ChatHistoryItem(BaseModel):
    role: str # Typically "user" or "model" (or "assistant")
    content: str

class ChatMessageInput(BaseModel):
    message: str
    slide_id: int # To associate chat with a specific slide context
    history: Optional[List[ChatHistoryItem]] = None

class ChatMessageOutput(BaseModel):
    reply: str
    suggested_messages: Optional[List[str]] = None


# SQLAlchemy models
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
    content_json = Column(JSONB, nullable=False)
    specific_prompt = Column(String, nullable=True)
    suggested_messages_json = Column(JSONB, nullable=True)

    course = relationship("Course", back_populates="slides")
