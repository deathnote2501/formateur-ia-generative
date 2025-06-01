from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid # Added for potential future use if User ID becomes UUID

class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    # Add other fields that can be updated, making them optional
    # For example, if you add a 'full_name' field to the User model:
    # full_name: Optional[str] = None

class UserRead(UserBase):
    id: int # Assuming User ID is int as per SQLAlchemy model

    class Config:
        orm_mode = True
