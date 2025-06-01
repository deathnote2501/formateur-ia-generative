from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Path

from app.core.models import SlideRead, SlideCreate, SlideUpdate, User # Pydantic Schemas & User model
from app.application.services.slide_service import SlideService
from app.application.services.course_service import CourseService # For checking course existence
from app.api.dependencies import get_slide_service, get_course_service, current_active_user, current_active_superuser

router = APIRouter(tags=["Slides"]) # No prefix here, as it's handled by path operations

@router.post("/courses/{course_id}/slides/", response_model=SlideRead, status_code=status.HTTP_201_CREATED)
async def create_new_slide_for_course(
    course_id: int,
    slide_data: SlideCreate,
    slide_service: SlideService = Depends(get_slide_service),
    course_service: CourseService = Depends(get_course_service), # To check if course exists
    # user: User = Depends(current_active_superuser)
    _ = Depends(current_active_superuser)
):
    # Check if course exists before creating slide for it
    course = await course_service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {course_id} not found")

    # Ensure the slide_data is for the correct course_id from the path
    if slide_data.course_id != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Slide's course_id ({slide_data.course_id}) in request body does not match course_id in path ({course_id})."
        )

    created_slide = await slide_service.create_slide(slide_data)
    return created_slide

@router.get("/slides/{slide_id}", response_model=SlideRead)
async def read_slide_by_id(
    slide_id: int,
    service: SlideService = Depends(get_slide_service),
    # user: User = Depends(current_active_user)
    _ = Depends(current_active_user)
):
    slide = await service.get_slide(slide_id)
    if not slide:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slide not found")
    return slide

@router.get("/courses/{course_id}/slides/", response_model=List[SlideRead])
async def read_all_slides_for_course(
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    service: SlideService = Depends(get_slide_service),
    # user: User = Depends(current_active_user)
    _ = Depends(current_active_user)
):
    # Optionally, check if course exists first, though not strictly necessary if it just returns an empty list
    slides = await service.get_slides_by_course(course_id, skip=skip, limit=limit)
    return slides

@router.put("/slides/{slide_id}", response_model=SlideRead)
async def update_existing_slide(
    slide_id: int,
    slide_data: SlideUpdate,
    service: SlideService = Depends(get_slide_service),
    # user: User = Depends(current_active_superuser)
    _ = Depends(current_active_superuser)
):
    updated_slide = await service.update_slide(slide_id, slide_data)
    if not updated_slide:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slide not found or no update performed")
    return updated_slide

@router.delete("/slides/{slide_id}", response_model=SlideRead)
async def delete_existing_slide(
    slide_id: int,
    service: SlideService = Depends(get_slide_service),
    # user: User = Depends(current_active_superuser)
    _ = Depends(current_active_superuser)
):
    deleted_slide = await service.delete_slide(slide_id)
    if not deleted_slide:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slide not found")
    return deleted_slide
