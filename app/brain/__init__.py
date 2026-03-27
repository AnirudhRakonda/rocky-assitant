"""Rocky Assistant Brain Module.

Handles LLM integration and conversation logic.
"""

from app.brain.llm import get_llm, OllamaLLM
from app.brain.prompts import get_system_prompt, get_emotion_prompt

__all__ = ['get_llm', 'OllamaLLM', 'get_system_prompt', 'get_emotion_prompt']
