from abc import ABC, abstractmethod
from typing import List, Optional

from app.core.models import Slide, SlideCreate, SlideUpdate # SQLAlchemy model and Pydantic schemas

class SlideRepositoryInterface(ABC):
    @abstractmethod
    async def create_slide(self, slide_data: SlideCreate) -> Slide:
        pass

    @abstractmethod
    async def get_slide_by_id(self, slide_id: int) -> Optional[Slide]:
        pass

    @abstractmethod
    async def get_slides_by_course_id(self, course_id: int, skip: int = 0, limit: int = 100) -> List[Slide]:
        pass

    @abstractmethod
    async def update_slide(self, slide_id: int, slide_data: SlideUpdate) -> Optional[Slide]:
        pass

    @abstractmethod
    async def delete_slide(self, slide_id: int) -> Optional[Slide]:
        pass
