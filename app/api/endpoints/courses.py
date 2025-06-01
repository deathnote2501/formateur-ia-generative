from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.models import CourseRead, CourseCreate, CourseUpdate, User # Pydantic Schemas & User model
from app.application.services.course_service import CourseService
from app.api.dependencies import get_course_service, current_active_user, current_active_superuser

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_new_course(
    course_data: CourseCreate,
    service: CourseService = Depends(get_course_service),
    # user: User = Depends(current_active_superuser) # Uncomment when superuser logic is fully tested
    # For now, allowing any active user to create, will restrict to superuser later if needed by uncommenting above
    # and potentially removing the default user dependency if not used otherwise in this endpoint.
    # The plan asks for superuser, so let's assume current_active_superuser is the one to use.
    # user_dep: User = Depends(current_active_superuser) # Renaming to avoid conflict if not used
    _ = Depends(current_active_superuser) # Just to enforce superuser check

):
    created_course = await service.create_course(course_data)
    return created_course

@router.get("/{course_id}", response_model=CourseRead)
async def read_course_by_id(
    course_id: int,
    service: CourseService = Depends(get_course_service),
    # user: User = Depends(current_active_user) # Enforce authenticated user
    _ = Depends(current_active_user)
):
    course = await service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.get("/", response_model=List[CourseRead])
async def read_all_courses(
    skip: int = 0,
    limit: int = 100,
    service: CourseService = Depends(get_course_service),
    # user: User = Depends(current_active_user)
    _ = Depends(current_active_user)
):
    courses = await service.get_all_courses(skip=skip, limit=limit)
    return courses

@router.put("/{course_id}", response_model=CourseRead)
async def update_existing_course(
    course_id: int,
    course_data: CourseUpdate,
    service: CourseService = Depends(get_course_service),
    # user: User = Depends(current_active_superuser)
    _ = Depends(current_active_superuser)
):
    updated_course = await service.update_course(course_id, course_data)
    if not updated_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found or no update performed")
    return updated_course

@router.delete("/{course_id}", response_model=CourseRead)
async def delete_existing_course(
    course_id: int,
    service: CourseService = Depends(get_course_service),
    # user: User = Depends(current_active_superuser)
    _ = Depends(current_active_superuser)
):
    deleted_course = await service.delete_course(course_id)
    if not deleted_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return deleted_course
