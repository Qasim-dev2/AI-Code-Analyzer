"""Prompt exports for the active application."""

from .analyzer_prompts import ANALYSIS_SYSTEM_PROMPT, build_analysis_prompt, get_analysis_prompt
from .coach_prompts import (
    CHAT_SYSTEM_PROMPT,
    FULL_GUIDANCE_SYSTEM_PROMPT,
    HINTS_SYSTEM_PROMPT,
    build_full_guidance_prompt,
    build_hints_prompt,
    get_full_guidance_prompt,
    get_hints_prompt,
)
from .practice_prompts import PRACTICE_SYSTEM_PROMPT, build_practice_prompt, get_practice_prompt

__all__ = [
    "ANALYSIS_SYSTEM_PROMPT",
    "PRACTICE_SYSTEM_PROMPT",
    "HINTS_SYSTEM_PROMPT",
    "FULL_GUIDANCE_SYSTEM_PROMPT",
    "CHAT_SYSTEM_PROMPT",
    "build_analysis_prompt",
    "build_practice_prompt",
    "build_hints_prompt",
    "build_full_guidance_prompt",
    "get_analysis_prompt",
    "get_practice_prompt",
    "get_hints_prompt",
    "get_full_guidance_prompt",
]
