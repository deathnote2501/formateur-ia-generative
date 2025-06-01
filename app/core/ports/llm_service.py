from abc import ABC, abstractmethod
from typing import List, Optional, Dict # For chat_history and slide_content type hints
# Assuming ChatHistoryItem is defined in app.core.models, if not, define a local type or use List[Dict]
from app.core.models import ChatHistoryItem # Import the Pydantic model

class LLMServiceInterface(ABC):
    @abstractmethod
    async def get_chat_response(
        self,
        user_message: str,
        slide_content: Dict, # Assuming parsed JSON content of the slide
        slide_specific_prompt: Optional[str],
        chat_history: Optional[List[ChatHistoryItem]] # Use the Pydantic model
    ) -> str:
        pass
