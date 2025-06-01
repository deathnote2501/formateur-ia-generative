from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update as sql_update, delete as sql_delete

from app.core.models import Slide, SlideCreate, SlideUpdate # SQLAlchemy model and Pydantic schemas
from app.core.ports.slide_repository import SlideRepositoryInterface

class PostgresSlideRepository(SlideRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_slide(self, slide_data: SlideCreate) -> Slide:
        db_slide = Slide(**slide_data.model_dump())
        self.session.add(db_slide)
        await self.session.commit()
        await self.session.refresh(db_slide)
        return db_slide

    async def get_slide_by_id(self, slide_id: int) -> Optional[Slide]:
        try:
            result = await self.session.execute(select(Slide).filter(Slide.id == slide_id))
            return result.scalar_one_or_none()
        except NoResultFound:
             return None

    async def get_slides_by_course_id(self, course_id: int, skip: int = 0, limit: int = 100) -> List[Slide]:
        result = await self.session.execute(
            select(Slide).filter(Slide.course_id == course_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update_slide(self, slide_id: int, slide_data: SlideUpdate) -> Optional[Slide]:
        update_values = slide_data.model_dump(exclude_unset=True)
        if not update_values:
            return await self.get_slide_by_id(slide_id)

        await self.session.execute(
            sql_update(Slide).where(Slide.id == slide_id).values(**update_values)
        )
        await self.session.commit()
        return await self.get_slide_by_id(slide_id)

    async def delete_slide(self, slide_id: int) -> Optional[Slide]:
        slide_to_delete = await self.get_slide_by_id(slide_id)
        if not slide_to_delete:
            return None
        await self.session.execute(sql_delete(Slide).where(Slide.id == slide_id))
        await self.session.commit()
        return slide_to_delete
