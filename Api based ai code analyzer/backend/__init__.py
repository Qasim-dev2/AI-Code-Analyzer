"""
Backend package initialization.
Local AI-powered code analysis using Ollama.
"""

from backend.ollama_client import (
    OllamaClient,
    OllamaConfig,
    check_ollama_status,
    get_ollama_client
)
from backend.code_executor import CodeExecutor, get_executor

__all__ = [
    "OllamaClient",
    "OllamaConfig",
    "check_ollama_status",
    "get_ollama_client",
    "CodeExecutor",
    "get_executor",
]
