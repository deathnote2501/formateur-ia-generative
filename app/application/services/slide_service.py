from typing import List, Optional
from app.core.models import Slide, SlideCreate, SlideRead, SlideUpdate # Pydantic and SQLAlchemy
from app.core.ports.slide_repository import SlideRepositoryInterface

class SlideService:
    def __init__(self, slide_repo: SlideRepositoryInterface):
        self.slide_repo = slide_repo

    async def create_slide(self, slide_data: SlideCreate) -> Slide:
        return await self.slide_repo.create_slide(slide_data)

    async def get_slide(self, slide_id: int) -> Optional[Slide]:
        return await self.slide_repo.get_slide_by_id(slide_id)

    async def get_slides_by_course(self, course_id: int, skip: int = 0, limit: int = 100) -> List[Slide]:
        return await self.slide_repo.get_slides_by_course_id(course_id, skip=skip, limit=limit)

    async def update_slide(self, slide_id: int, slide_data: SlideUpdate) -> Optional[Slide]:
        return await self.slide_repo.update_slide(slide_id, slide_data)

    async def delete_slide(self, slide_id: int) -> Optional[Slide]:
        return await self.slide_repo.delete_slide(slide_id)
