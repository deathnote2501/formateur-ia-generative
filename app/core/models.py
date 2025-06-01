from typing import List, Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text  # Assuming Text for content_json and specific_prompt

Base = declarative_base()

# Pydantic Models
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

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

class SlideBase(BaseModel):
    course_id: int
    order_index: int
    template_type: str  # ex: 'title', 'menu', 'content'
    content_json: dict  # For flexibility, using dict. Could be pydantic model too.
    specific_prompt: Optional[str] = None
    suggested_messages_json: Optional[List[str]] = None # Storing as list of strings

class SlideCreate(SlideBase):
    pass

class SlideRead(SlideBase):
    id: int

    class Config:
        orm_mode = True

# SQLAlchemy Models (Example structure, will need to be defined if using Alembic for these)
# For now, only Base is critical for Alembic configuration in env.py
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)
#     is_superuser = Column(Boolean, default=False)

# class Course(Base):
#     __tablename__ = "courses"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True, nullable=False)
#     description = Column(String, nullable=True)

# class Slide(Base):
#     __tablename__ = "slides"
#     id = Column(Integer, primary_key=True, index=True)
#     course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
#     order_index = Column(Integer, nullable=False)
#     template_type = Column(String, nullable=False)
#     content_json = Column(Text, nullable=False) # Using Text to store JSON string
#     specific_prompt = Column(Text, nullable=True)
#     suggested_messages_json = Column(Text, nullable=True) # Using Text to store JSON string of list
