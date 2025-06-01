from typing import List, Optional
from app.core.models import Course, CourseCreate, CourseRead, CourseUpdate # Pydantic and SQLAlchemy
from app.core.ports.course_repository import CourseRepositoryInterface

class CourseService:
    def __init__(self, course_repo: CourseRepositoryInterface):
        self.course_repo = course_repo

    async def create_course(self, course_data: CourseCreate) -> Course: # Returns SQLAlchemy model
        # In a real app, you might have more business logic here
        return await self.course_repo.create_course(course_data)

    async def get_course(self, course_id: int) -> Optional[Course]: # Returns SQLAlchemy model
        return await self.course_repo.get_course_by_id(course_id)

    async def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[Course]: # Returns list of SQLAlchemy models
        return await self.course_repo.get_all_courses(skip=skip, limit=limit)

    async def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]: # Returns SQLAlchemy model
        return await self.course_repo.update_course(course_id, course_data)

    async def delete_course(self, course_id: int) -> Optional[Course]: # Returns SQLAlchemy model
        return await self.course_repo.delete_course(course_id)
