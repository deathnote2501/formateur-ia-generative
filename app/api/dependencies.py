from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_async_session
from app.core.ports.course_repository import CourseRepositoryInterface
from app.infrastructure.db.repositories.course_repository import PostgresCourseRepository
from app.application.services.course_service import CourseService

from app.core.ports.slide_repository import SlideRepositoryInterface
from app.infrastructure.db.repositories.slide_repository import PostgresSlideRepository
from app.application.services.slide_service import SlideService

# New imports for LLM and Chat services
from app.core.ports.llm_service import LLMServiceInterface
from app.infrastructure.services.simulated_llm_service import SimulatedLLMService
from app.application.services.chat_service import ChatService

# User related dependencies ( leveraging fastapi-users )
from app.core.models import User # SQLAlchemy User model
from app.core.db_users import fastapi_users # The FastAPIUsers instance

# Dependency for an active user
current_active_user = fastapi_users.current_user(active=True)

# Dependency for an active superuser
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)


# Repository and Service Dependencies
def get_course_repository(
    session: AsyncSession = Depends(get_async_session)
) -> CourseRepositoryInterface:
    return PostgresCourseRepository(session)

def get_course_service(
    repo: CourseRepositoryInterface = Depends(get_course_repository)
) -> CourseService:
    return CourseService(repo)

def get_slide_repository(
    session: AsyncSession = Depends(get_async_session)
) -> SlideRepositoryInterface:
    return PostgresSlideRepository(session)

def get_slide_service(
    repo: SlideRepositoryInterface = Depends(get_slide_repository)
) -> SlideService:
    return SlideService(repo)

# New dependency providers for LLM and Chat services
def get_llm_service() -> LLMServiceInterface:
    # This is where you might switch to a real LLM service based on config/env vars
    return SimulatedLLMService()

def get_chat_service(
    llm_service: LLMServiceInterface = Depends(get_llm_service),
    slide_repo: SlideRepositoryInterface = Depends(get_slide_repository) # Uses existing dependency
) -> ChatService:
    return ChatService(llm_service=llm_service, slide_repository=slide_repo)
