"""
Ollama Streaming Client

A streaming client for local Ollama models.
Provides token-by-token streaming for real-time AI responses.
"""

import requests
import json
import logging
from typing import Iterator, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class OllamaConfig:
    """Configuration for Ollama client."""
    
    base_url: str = "http://localhost:11434"
    model: str = "codellama:7b"
    temperature: float = 0.7
    timeout: int = 120


class OllamaClient:
    """
    Streaming client for Ollama local models.
    
    Provides token-by-token streaming for real-time AI responses.
    """
    
    def __init__(self, config: Optional[OllamaConfig] = None):
        """
        Initialize the Ollama client.
        
        Args:
            config: Optional configuration. Uses defaults if None.
        """
        self.config = config or OllamaConfig()
        self._verify_connection()
    
    def _verify_connection(self) -> bool:
        """Verify Ollama server is running."""
        try:
            response = requests.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            logger.warning("Ollama server not running at %s", self.config.base_url)
            return False
    
    def is_available(self) -> bool:
        """Check if Ollama is available and has models."""
        try:
            response = requests.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json().get("models", [])
                return len(models) > 0
            return False
        except Exception:
            return False
    
    def list_models(self) -> list[str]:
        """Get list of available models."""
        try:
            response = requests.get(
                f"{self.config.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [m["name"] for m in models]
            return []
        except Exception:
            return []
    
    def stream_generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None
    ) -> Iterator[str]:
        """
        Stream tokens from Ollama.
        
        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt for context.
        
        Yields:
            Individual tokens as they're generated.
        """
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.config.temperature,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            with requests.post(
                f"{self.config.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=self.config.timeout
            ) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            token = data.get("response", "")
                            if token:
                                yield token
                            
                            # Check if generation is done
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.ConnectionError:
            yield "❌ Error: Ollama server is not running. Please start Ollama first."
        except requests.exceptions.Timeout:
            yield "❌ Error: Request timed out. The model may be too slow or overloaded."
        except Exception as e:
            yield f"❌ Error: {str(e)}"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a complete response (non-streaming).
        
        Args:
            prompt: The user prompt.
            system_prompt: Optional system prompt.
        
        Returns:
            The complete generated text.
        """
        tokens = list(self.stream_generate(prompt, system_prompt))
        return "".join(tokens)


def get_ollama_client(model: str = "codellama:7b") -> OllamaClient:
    """
    Factory function to create an Ollama client.
    
    Args:
        model: The model to use.
    
    Returns:
        Configured OllamaClient instance.
    """
    config = OllamaConfig(model=model)
    return OllamaClient(config)


def check_ollama_status() -> tuple[bool, str]:
    """
    Check if Ollama is available and return status message.
    
    Returns:
        Tuple of (is_available, status_message)
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                model_names = [m["name"] for m in models]
                return True, f"✅ Ollama running with models: {', '.join(model_names)}"
            else:
                return False, "⚠️ Ollama running but no models installed. Run: ollama pull codellama:7b"
        return False, "❌ Ollama server returned an error"
    except requests.exceptions.ConnectionError:
        return False, "❌ Ollama not running. Start it with: ollama serve"
    except Exception as e:
        return False, f"❌ Error checking Ollama: {str(e)}"
