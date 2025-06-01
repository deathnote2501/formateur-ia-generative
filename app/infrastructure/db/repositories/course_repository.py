from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update as sql_update, delete as sql_delete

from app.core.models import Course, CourseCreate, CourseUpdate # SQLAlchemy model and Pydantic schemas
from app.core.ports.course_repository import CourseRepositoryInterface

class PostgresCourseRepository(CourseRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_course(self, course_data: CourseCreate) -> Course:
        db_course = Course(**course_data.model_dump())
        self.session.add(db_course)
        await self.session.commit()
        await self.session.refresh(db_course)
        return db_course

    async def get_course_by_id(self, course_id: int) -> Optional[Course]:
        try:
            result = await self.session.execute(select(Course).filter(Course.id == course_id))
            return result.scalar_one_or_none() # Changed from scalar_one to handle not found
        except NoResultFound: # Should not be strictly necessary with scalar_one_or_none
            return None

    async def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        result = await self.session.execute(select(Course).offset(skip).limit(limit))
        return result.scalars().all()

    async def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]:
        # Filter out None values from course_data to only update provided fields
        update_values = course_data.model_dump(exclude_unset=True)
        if not update_values: # No actual data provided for update
            # Optionally, fetch and return the course without changes, or handle as an error/noop
            return await self.get_course_by_id(course_id)

        await self.session.execute(
            sql_update(Course).where(Course.id == course_id).values(**update_values)
        )
        await self.session.commit()
        # Fetch the updated course to return it
        return await self.get_course_by_id(course_id) # Re-fetch to get updated state

    async def delete_course(self, course_id: int) -> Optional[Course]:
        course_to_delete = await self.get_course_by_id(course_id)
        if not course_to_delete:
            return None
        await self.session.execute(sql_delete(Course).where(Course.id == course_id))
        await self.session.commit()
        return course_to_delete
