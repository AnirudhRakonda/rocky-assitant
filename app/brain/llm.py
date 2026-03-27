"""
Local LLM integration via Ollama.

Handles communication with locally running Ollama instance.
"""

import json
import requests
from typing import Optional

from app.config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT, DEBUG_MODE
from app.utils import logger
from app.brain.prompts import get_system_prompt


class OllamaLLM:
    """Interface to local Ollama LLM."""

    def __init__(self, model: str = OLLAMA_MODEL):
        """
        Initialize Ollama LLM interface.

        Args:
            model: Model name (mistral, llama3, etc.)
        """
        self.model = model
        self.endpoint = f"{OLLAMA_HOST}/api/generate"
        self.system_prompt = get_system_prompt()

        logger.info(f"Initialized OllamaLLM with model: {model}")
        self._verify_connection()

    def _verify_connection(self) -> bool:
        """
        Verify connection to Ollama server.

        Returns:
            True if connection successful

        Raises:
            RuntimeError: If cannot connect to Ollama
        """
        try:
            response = requests.get(
                f"{OLLAMA_HOST}/api/tags",
                timeout=OLLAMA_TIMEOUT
            )
            if response.status_code == 200:
                logger.info("Ollama connection verified")
                return True
            else:
                raise RuntimeError(f"Ollama returned status {response.status_code}")
        except requests.ConnectionError as e:
            logger.error(f"Cannot connect to Ollama at {OLLAMA_HOST}")
            logger.error("Make sure Ollama is running: ollama serve")
            logger.error(f"Then pull a model: ollama pull {self.model}")
            raise RuntimeError(f"Ollama connection failed: {e}")

    def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate response from LLM.

        Args:
            prompt: User input
            context: Optional conversation context
            temperature: Creativity (0.0-1.0, lower = more deterministic)

        Returns:
            Generated text response
        """
        try:
            # Build full prompt with system context
            full_prompt = f"{self.system_prompt}\n\n"
            if context:
                full_prompt += f"Context: {context}\n\n"
            full_prompt += f"User: {prompt}\nRocky:"

            # Request to Ollama
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "temperature": temperature,
                "top_k": 40,
                "top_p": 0.9
            }

            if DEBUG_MODE:
                logger.debug(f"Sending to Ollama: {payload}")

            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=OLLAMA_TIMEOUT
            )

            if response.status_code != 200:
                logger.error(f"Ollama error: {response.status_code}")
                logger.error(response.text)
                return "Error processing request."

            result = response.json()
            generated_text = result.get("response", "").strip()

            logger.info(f"LLM Response: {generated_text[:100]}...")

            return generated_text

        except requests.Timeout:
            logger.error("Ollama request timed out")
            return "Processing timeout."
        except requests.RequestException as e:
            logger.error(f"LLM request failed: {e}")
            return "Connection error."
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Ollama response: {e}")
            return "Response parsing error."

    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.

        Returns:
            Model information dict
        """
        try:
            response = requests.get(
                f"{OLLAMA_HOST}/api/show",
                json={"name": self.model},
                timeout=OLLAMA_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {}


# Singleton instance
_llm_instance: Optional[OllamaLLM] = None


def get_llm() -> OllamaLLM:
    """Get or create the LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = OllamaLLM()
    return _llm_instance
