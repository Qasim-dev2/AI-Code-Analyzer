"""Configuration exports for the active application."""

from .settings import (
    AnalysisConfig,
    AppConfig,
    DIFFICULTIES,
    PRACTICE_TIMES,
    RECOMMENDED_MODELS,
    REFERENCE_CONTENT,
    SAMPLE_CODES,
    TOPICS,
)


APP_NAME = AppConfig.APP_NAME
APP_VERSION = AppConfig.APP_VERSION
APP_DESCRIPTION = AppConfig.APP_DESCRIPTION

ANALYSIS_DEPTHS = {
    "Quick": {
        "description": "Fast analysis focused on obvious issues and code quality.",
        "max_tokens": AnalysisConfig.QUICK_MAX_TOKENS,
    },
    "Detailed": {
        "description": "More thorough analysis with deeper recommendations.",
        "max_tokens": AnalysisConfig.DETAILED_MAX_TOKENS,
    },
}

GRADE_DESCRIPTIONS = {
    "A": "Excellent - production-ready code with strong practices",
    "B": "Good - solid code with minor improvements available",
    "C": "Average - works, but there are visible quality gaps",
    "D": "Needs improvement - several important issues need attention",
}

SEVERITY_COLORS = {
    "Error": "#FF4B4B",
    "Warning": "#FFA500",
    "Info": "#1E88E5",
}

REPORT_FORMATS = ["Text", "HTML", "JSON"]

__all__ = [
    "AnalysisConfig",
    "AppConfig",
    "APP_NAME",
    "APP_VERSION",
    "APP_DESCRIPTION",
    "ANALYSIS_DEPTHS",
    "GRADE_DESCRIPTIONS",
    "SEVERITY_COLORS",
    "REPORT_FORMATS",
    "TOPICS",
    "DIFFICULTIES",
    "PRACTICE_TIMES",
    "RECOMMENDED_MODELS",
    "SAMPLE_CODES",
    "REFERENCE_CONTENT",
]
