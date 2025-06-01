from fastapi import APIRouter, Depends, HTTPException, status

from app.core.models import ChatMessageInput, ChatMessageOutput, User # Pydantic Schemas & User model
from app.application.services.chat_service import ChatService
from app.api.dependencies import get_chat_service, current_active_user # User dependency

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatMessageOutput, status_code=status.HTTP_200_OK)
async def handle_chat_message(
    chat_data: ChatMessageInput,
    chat_service: ChatService = Depends(get_chat_service),
    user: User = Depends(current_active_user) # Enforce user authentication
):
    # Docstring for OpenAPI
    """
    Processes a user's chat message related to a specific slide and returns the AI's response.

    - **chat_data**: Input message, slide ID, and optional chat history.
    - Requires authentication.
    """
    try:
        response = await chat_service.process_chat_message(chat_data)
        return response
    except HTTPException as e:
        # Re-raise HTTPException directly if ChatService raised it (e.g., slide not found)
        raise e
    except Exception as e:
        # Catch any other unexpected errors during chat processing
        # Log the error e for debugging
        print(f"Unexpected error in chat endpoint: {e}") # Basic logging
        # Consider more robust logging in a real application
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the chat message."
        )
