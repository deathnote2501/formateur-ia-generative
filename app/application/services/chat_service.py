from typing import Optional # Added for type hint Optional[Slide]
from fastapi import HTTPException, status # For error handling

from app.core.models import ChatMessageInput, ChatMessageOutput, Slide # Pydantic and SQLAlchemy
from app.core.ports.llm_service import LLMServiceInterface
from app.core.ports.slide_repository import SlideRepositoryInterface

class ChatService:
    def __init__(
        self,
        llm_service: LLMServiceInterface,
        slide_repository: SlideRepositoryInterface
    ):
        self.llm_service = llm_service
        self.slide_repository = slide_repository

    async def process_chat_message(self, chat_input: ChatMessageInput) -> ChatMessageOutput:
        slide: Optional[Slide] = await self.slide_repository.get_slide_by_id(chat_input.slide_id)

        if not slide:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Slide with ID {chat_input.slide_id} not found."
            )

        # Ensure slide.content_json is a dict, default to empty if None or not a dict
        slide_content_data = slide.content_json if isinstance(slide.content_json, dict) else {}

        llm_reply = await self.llm_service.get_chat_response(
            user_message=chat_input.message,
            slide_content=slide_content_data, # Pass the JSON content of the slide
            slide_specific_prompt=slide.specific_prompt,
            chat_history=chat_input.history
        )

        suggested_messages = []
        if isinstance(slide.suggested_messages_json, list):
            suggested_messages = [str(msg) for msg in slide.suggested_messages_json if isinstance(msg, str)]


        return ChatMessageOutput(
            reply=llm_reply,
            suggested_messages=suggested_messages # Use suggested messages from the slide
        )
