"""Centralized Streamlit session state helpers for the active app."""

from __future__ import annotations

import time
from typing import Any

import streamlit as st

from config import AppConfig


STATE_DEFAULTS = {
    "model": AppConfig.DEFAULT_MODEL,
    "temperature": AppConfig.DEFAULT_TEMPERATURE,
    "analyze_code": "",
    "analysis": None,
    "practice_question": None,
    "practice_solution": "",
    "practice_started": False,
    "practice_start_time": None,
    "practice_time_limit": 1800,
    "run_output": None,
    "chat_history": [],
    "hints_code": "",
    "hints_question": "",
    "full_code": "",
    "full_request": "",
    "compare_code1": "",
    "compare_code2": "",
}


def init_session_state() -> None:
    """Initialize session state for the active app."""
    for key, value in STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_state(key: str, default: Any = None) -> Any:
    """Read a session state value."""
    return st.session_state.get(key, default)


def set_state(key: str, value: Any) -> None:
    """Write a session state value."""
    st.session_state[key] = value


def reset_analysis() -> None:
    """Clear analysis-related state."""
    st.session_state.analysis = None


def reset_practice() -> None:
    """Clear the active practice session."""
    st.session_state.practice_question = None
    st.session_state.practice_solution = ""
    st.session_state.practice_started = False
    st.session_state.practice_start_time = None
    st.session_state.practice_time_limit = 1800
    st.session_state.run_output = None


def start_practice(duration_seconds: int) -> None:
    """Start the practice timer."""
    st.session_state.practice_started = True
    st.session_state.practice_start_time = time.time()
    st.session_state.practice_time_limit = duration_seconds
    st.session_state.run_output = None


def get_remaining_time() -> int | None:
    """Return remaining practice time in seconds."""
    start_time = st.session_state.get("practice_start_time")
    if not st.session_state.get("practice_started") or start_time is None:
        return None

    elapsed = int(time.time() - start_time)
    remaining = st.session_state.practice_time_limit - elapsed
    return max(0, remaining)


def format_time(seconds: int) -> str:
    """Format seconds as MM:SS."""
    minutes, seconds = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{seconds:02d}"
