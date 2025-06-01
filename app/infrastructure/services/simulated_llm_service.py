from typing import List, Optional, Dict
from app.core.ports.llm_service import LLMServiceInterface
from app.core.models import ChatHistoryItem # Import the Pydantic model

class SimulatedLLMService(LLMServiceInterface):
    async def get_chat_response(
        self,
        user_message: str,
        slide_content: Dict,
        slide_specific_prompt: Optional[str],
        chat_history: Optional[List[ChatHistoryItem]] # Use the Pydantic model
    ) -> str:
        import asyncio # For simulating async behavior

        await asyncio.sleep(0.1) # Simulate a small delay

        slide_title = slide_content.get('title', 'Inconnue')

        response_parts = [
            f"J'ai bien reçu votre message concernant la slide : '{slide_title}'.",
            f"Vous avez dit : '{user_message}'.",
            "Je suis une IA simulée et je ne peux pas vraiment comprendre ou répondre de manière contextuelle pour l'instant."
        ]

        if slide_specific_prompt:
            response_parts.insert(2, f"Le prompt spécifique pour cette slide est : '{slide_specific_prompt}'.")

        if chat_history:
            response_parts.append(f"J'ai noté qu'il y a {len(chat_history)} message(s) précédent(s) dans notre conversation.")

        return " ".join(response_parts)
