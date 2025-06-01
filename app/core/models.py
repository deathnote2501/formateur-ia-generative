from typing import Optional, List
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.declarative import declarative_base
# We won't define SQLAlchemy models yet, but we need Base for Alembic

Base = declarative_base()

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
    template_type: str  # (ex: 'title', 'menu', 'content')
    content_json: dict
    specific_prompt: Optional[str] = None
    suggested_messages_json: Optional[List[str]] = None

class SlideCreate(SlideBase):
    pass

class SlideRead(SlideBase):
    id: int

    class Config:
        orm_mode = True
