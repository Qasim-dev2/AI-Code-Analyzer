"""
AI Client Module - Google Gemini Only

A dedicated AI API client for Google Gemini (Google AI Studio).
All configuration is read from environment variables.
"""

import os
import logging
from typing import Optional
from dataclasses import dataclass

# Load environment variables (safety measure in case not loaded elsewhere)
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from google.api_core import exceptions as google_exceptions


# Configure logging
logger = logging.getLogger(__name__)


class AIClientError(Exception):
    """Base exception for AI client errors."""
    
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        self.user_message = user_message or message


class ConfigurationError(AIClientError):
    """Raised when configuration is missing or invalid."""
    pass


class ProviderError(AIClientError):
    """Raised when the AI provider returns an error."""
    pass


@dataclass
class AIClientConfig:
    """Configuration for AI client."""
    
    api_key: str
    model_name: str
    temperature: float = 0.0
    max_retries: int = 3
    timeout: int = 60


def load_config() -> AIClientConfig:
    """
    Load and validate configuration from environment variables.
    
    Returns:
        Validated AIClientConfig for Gemini.
    
    Raises:
        ConfigurationError: If required variables are missing.
    """
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    
    if not api_key:
        raise ConfigurationError(
            "GOOGLE_API_KEY not set",
            "Please set GOOGLE_API_KEY environment variable with your Google AI Studio API key."
        )
    
    model_name = os.getenv("AI_MODEL_NAME", "gemini-2.0-flash").strip()
    
    return AIClientConfig(
        api_key=api_key,
        model_name=model_name,
        temperature=float(os.getenv("AI_TEMPERATURE", "0")),
        max_retries=int(os.getenv("AI_MAX_RETRIES", "3")),
        timeout=int(os.getenv("AI_TIMEOUT", "60"))
    )


class AIClient:
    """
    AI client for Google Gemini.
    
    Uses the official google-generativeai SDK for API communication.
    All configuration is read from environment variables.
    """
    
    def __init__(self, config: Optional[AIClientConfig] = None):
        """
        Initialize the AI client.
        
        Args:
            config: Optional pre-built configuration. If None, loads from environment.
        
        Raises:
            ConfigurationError: If configuration is invalid.
        """
        self.config = config or load_config()
        self._configure_client()
        self._model = self._create_model()
    
    def _configure_client(self) -> None:
        """Configure the Gemini client with API key."""
        genai.configure(api_key=self.config.api_key)
    
    def _create_model(self) -> genai.GenerativeModel:
        """
        Create the Gemini model instance.
        
        Returns:
            Configured GenerativeModel instance.
        """
        logger.info(f"[DEBUG] Creating Gemini model: {self.config.model_name}")
        return genai.GenerativeModel(
            model_name=self.config.model_name,
            generation_config=GenerationConfig(
                temperature=self.config.temperature
            )
        )
    
    def chat_completion(
        self,
        messages: list[dict],
        max_tokens: int = 4000,
        temperature: Optional[float] = None
    ) -> str:
        """
        Send a chat completion request to Gemini.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            max_tokens: Maximum tokens in the response.
            temperature: Override default temperature (0 for deterministic).
        
        Returns:
            The model's response content as a string.
        
        Raises:
            ProviderError: If the API call fails.
        """
        try:
            # Convert messages to Gemini format
            prompt = self._convert_messages_to_prompt(messages)
            
            # Create generation config with overrides
            gen_config = GenerationConfig(
                temperature=temperature if temperature is not None else self.config.temperature,
                max_output_tokens=max_tokens
            )
            
            logger.info(f"[DEBUG] Sending request to Gemini model: {self.config.model_name}")
            logger.info(f"[DEBUG] Prompt length: {len(prompt)} characters")
            
            # Make the API call
            response = self._model.generate_content(
                prompt,
                generation_config=gen_config
            )
            
            logger.info(f"[DEBUG] Response received from Gemini")
            
            # Check if response was blocked
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                raise ProviderError(
                    f"Response blocked: {response.prompt_feedback.block_reason}",
                    "The AI model blocked this request. Please modify your input and try again."
                )
            
            # Check for candidates
            if not response.candidates:
                raise ProviderError(
                    "No candidates in response",
                    "The AI model returned no response. Please try again."
                )
            
            # Try to get text content
            try:
                response_text = response.text
            except ValueError as e:
                # response.text raises ValueError if no text parts
                logger.error(f"No text in response: {e}")
                # Try to get from parts directly
                if response.candidates[0].content.parts:
                    response_text = response.candidates[0].content.parts[0].text
                else:
                    raise ProviderError(
                        "No text content in response",
                        "The AI model returned an invalid response. Please try again."
                    )
            
            if not response_text or not response_text.strip():
                raise ProviderError(
                    "Empty response from Gemini",
                    "The AI model returned an empty response. Please try again."
                )
            
            logger.info(f"[DEBUG] Response length: {len(response_text)} characters")
            return response_text
            
        except google_exceptions.InvalidArgument as e:
            logger.error(f"Invalid argument: {e}")
            raise ProviderError(
                f"Invalid request: {e}",
                "Invalid request to AI service. Please check your input."
            )
            
        except google_exceptions.PermissionDenied as e:
            logger.error(f"Permission denied: {e}")
            raise ProviderError(
                f"Permission denied: {e}",
                "Invalid API key. Please check your GOOGLE_API_KEY."
            )
            
        except google_exceptions.ResourceExhausted as e:
            logger.error(f"Resource exhausted: {e}")
            raise ProviderError(
                f"Rate limit exceeded: {e}",
                "API rate limit exceeded. Please wait a moment and try again."
            )
            
        except google_exceptions.ServiceUnavailable as e:
            logger.error(f"Service unavailable: {e}")
            raise ProviderError(
                f"Service unavailable: {e}",
                "AI service is temporarily unavailable. Please try again later."
            )
            
        except google_exceptions.GoogleAPIError as e:
            logger.error(f"Google API error: {e}")
            raise ProviderError(
                f"API error: {e}",
                f"AI service error: {str(e)}"
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error during API call: {e}")
            raise ProviderError(
                f"Unexpected error: {e}",
                "An unexpected error occurred. Please try again later."
            )
    
    def _convert_messages_to_prompt(self, messages: list[dict]) -> str:
        """
        Convert chat-style messages to a single prompt for Gemini.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
        
        Returns:
            Combined prompt string.
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"Instructions:\n{content}\n")
            elif role == "user":
                prompt_parts.append(f"{content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Previous response:\n{content}\n")
        
        return "\n".join(prompt_parts)


def create_client() -> AIClient:
    """
    Factory function to create an AI client.
    
    Returns:
        Configured AIClient instance.
    
    Raises:
        ConfigurationError: If configuration is invalid.
    """
    return AIClient()


def validate_configuration() -> tuple[bool, Optional[str]]:
    """
    Validate the current configuration without creating a client.
    
    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        load_config()
        return True, None
    except ConfigurationError as e:
        return False, e.user_message
