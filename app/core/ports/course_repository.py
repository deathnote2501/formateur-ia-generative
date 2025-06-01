from abc import ABC, abstractmethod
from typing import List, Optional

from app.core.models import Course, CourseCreate, CourseUpdate # SQLAlchemy model and Pydantic schemas

class CourseRepositoryInterface(ABC):
    @abstractmethod
    async def create_course(self, course_data: CourseCreate) -> Course:
        pass

    @abstractmethod
    async def get_course_by_id(self, course_id: int) -> Optional[Course]:
        pass

    @abstractmethod
    async def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        pass

    @abstractmethod
    async def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]:
        pass

    @abstractmethod
    async def delete_course(self, course_id: int) -> Optional[Course]:
        pass
