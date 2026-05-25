"""
AI Code Analyzer Backend Module

Core module for AI-driven code analysis using Google Gemini.
Handles API communication, prompt building, response validation, and error handling.
"""

import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from backend.ai_client import (
    AIClient,
    AIClientError,
    ConfigurationError,
    ProviderError,
    validate_configuration
)
from config import ANALYSIS_DEPTHS
from config.settings import AnalysisConfig
from utils.prompt_builder import build_messages, AnalysisDepth


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Container for analysis results."""
    
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    raw_response: Optional[str] = None
    processing_time: float = 0.0


class AIAnalyzer:
    """
    AI-powered code analyzer using Google Gemini for semantic code analysis.
    
    This class handles:
    - API communication via the Gemini AIClient
    - Dynamic prompt construction based on analysis depth
    - Strict JSON response validation
    - Graceful error handling
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Analyzer.
        
        Args:
            api_key: Optional Google API key override (used for runtime key entry).
                     If provided, sets GOOGLE_API_KEY in environment.
        """
        self.analysis_config = AnalysisConfig()
        self._client: Optional[AIClient] = None
        
        # If API key provided at runtime, set it in environment
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
    
    def _get_client(self) -> AIClient:
        """
        Get or create the AI client.
        
        Returns:
            AIClient instance.
        
        Raises:
            ConfigurationError: If configuration is invalid.
        """
        if self._client is None:
            self._client = AIClient()
        return self._client
    
    def analyze(
        self,
        code: str,
        depth: AnalysisDepth = "Detailed"
    ) -> AnalysisResult:
        """
        Analyze Python code using the AI model.
        
        Args:
            code: Python source code to analyze.
            depth: Analysis depth - "Quick" or "Detailed".
        
        Returns:
            AnalysisResult containing the analysis data or error information.
        """
        start_time = time.time()
        
        # Validate input code
        validation_error = self._validate_code(code)
        if validation_error:
            return AnalysisResult(
                success=False,
                error=validation_error,
                processing_time=time.time() - start_time
            )
        
        # Validate configuration before proceeding
        is_valid, config_error = validate_configuration()
        if not is_valid:
            return AnalysisResult(
                success=False,
                error=config_error,
                processing_time=time.time() - start_time
            )
        
        # Build messages for the AI
        messages = build_messages(code, depth)
        max_tokens = ANALYSIS_DEPTHS[depth]["max_tokens"]
        
        try:
            # Get the AI client
            client = self._get_client()
            
            # Make the API call to Gemini
            logger.info(f"Starting {depth} analysis with Gemini...")
            raw_response = client.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=0  # Deterministic output
            )
            
            # Parse and validate the response
            result = self._parse_response(raw_response)
            result.processing_time = time.time() - start_time
            
            if result.success:
                logger.info(f"Analysis completed successfully in {result.processing_time:.2f}s")
            else:
                logger.warning(f"Analysis completed with errors: {result.error}")
            
            return result
            
        except ConfigurationError as e:
            logger.error(f"Configuration error: {e}")
            return AnalysisResult(
                success=False,
                error=e.user_message,
                processing_time=time.time() - start_time
            )
            
        except ProviderError as e:
            logger.error(f"Provider error: {e}")
            return AnalysisResult(
                success=False,
                error=e.user_message,
                processing_time=time.time() - start_time
            )
            
        except AIClientError as e:
            logger.error(f"AI client error: {e}")
            return AnalysisResult(
                success=False,
                error=e.user_message,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.exception(f"Unexpected error during analysis: {e}")
            return AnalysisResult(
                success=False,
                error="An unexpected error occurred. Please try again.",
                processing_time=time.time() - start_time
            )
    
    def _validate_code(self, code: str) -> Optional[str]:
        """
        Validate the input code.
        
        Args:
            code: Code to validate.
        
        Returns:
            Error message if invalid, None if valid.
        """
        if not code or not code.strip():
            return "No code provided for analysis."
        
        if len(code) < self.analysis_config.MIN_CODE_LENGTH:
            return "Code is too short for meaningful analysis."
        
        if len(code) > self.analysis_config.MAX_CODE_LENGTH:
            return f"Code exceeds maximum length of {self.analysis_config.MAX_CODE_LENGTH} characters."
        
        return None
    
    def _parse_response(self, raw_response: str) -> AnalysisResult:
        """
        Parse and validate the AI response.
        
        Args:
            raw_response: Raw response string from the API.
        
        Returns:
            AnalysisResult with parsed data or error.
        """
        try:
            # Clean the response (remove potential markdown formatting)
            cleaned = self._clean_json_response(raw_response)
            
            # Parse JSON
            data = json.loads(cleaned)
            
            # Validate structure
            validation_error = self._validate_response_structure(data)
            if validation_error:
                return AnalysisResult(
                    success=False,
                    error=f"Invalid AI response format: {validation_error}",
                    raw_response=raw_response
                )
            
            # Normalize data
            data = self._normalize_response(data)
            
            return AnalysisResult(
                success=True,
                data=data,
                raw_response=raw_response
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.debug(f"Raw response: {raw_response[:500]}...")
            return AnalysisResult(
                success=False,
                error="The AI returned an invalid response. Please try again.",
                raw_response=raw_response
            )
    
    def _clean_json_response(self, response: str) -> str:
        """
        Clean potential formatting issues from the response.
        
        Args:
            response: Raw response string.
        
        Returns:
            Cleaned JSON string.
        """
        response = response.strip()
        
        # Remove ```json ... ``` wrapper if present
        if response.startswith("```"):
            lines = response.split("\n")
            lines = lines[1:]  # Remove first line (```json or ```)
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response = "\n".join(lines)
        
        return response.strip()
    
    def _validate_response_structure(self, data: dict) -> Optional[str]:
        """
        Validate that the response has the required structure.
        
        Args:
            data: Parsed JSON data.
        
        Returns:
            Error message if invalid, None if valid.
        """
        required_keys = ["summary", "metrics", "issues", "strengths", "improvements"]
        
        for key in required_keys:
            if key not in data:
                return f"Missing required field: {key}"
        
        # Validate summary structure
        summary_keys = ["overall_grade", "readability_score", "maintainability_score", 
                       "complexity_level", "documentation_quality"]
        for key in summary_keys:
            if key not in data.get("summary", {}):
                return f"Missing summary field: {key}"
        
        # Validate metrics structure
        metrics_keys = ["estimated_cyclomatic_complexity", "functions_count", 
                       "classes_count", "average_function_length", "lines_of_code"]
        for key in metrics_keys:
            if key not in data.get("metrics", {}):
                return f"Missing metrics field: {key}"
        
        return None
    
    def _normalize_response(self, data: dict) -> dict:
        """
        Normalize and clean response data.
        
        Args:
            data: Parsed response data.
        
        Returns:
            Normalized data dictionary.
        """
        # Ensure grade is valid
        valid_grades = ["A", "B", "C", "D"]
        if data["summary"].get("overall_grade") not in valid_grades:
            data["summary"]["overall_grade"] = "C"
        
        # Ensure scores are in valid ranges
        try:
            data["summary"]["readability_score"] = max(1, min(10, 
                int(data["summary"]["readability_score"])))
        except (ValueError, TypeError):
            data["summary"]["readability_score"] = 5
            
        try:
            data["summary"]["maintainability_score"] = max(0, min(100,
                int(data["summary"]["maintainability_score"])))
        except (ValueError, TypeError):
            data["summary"]["maintainability_score"] = 50
        
        # Ensure complexity level is valid
        valid_complexity = ["Low", "Medium", "High"]
        if data["summary"].get("complexity_level") not in valid_complexity:
            data["summary"]["complexity_level"] = "Medium"
        
        # Ensure documentation quality is valid
        valid_doc = ["Poor", "Average", "Good", "Excellent"]
        if data["summary"].get("documentation_quality") not in valid_doc:
            data["summary"]["documentation_quality"] = "Average"
        
        # Ensure issues have valid types
        valid_types = ["Error", "Warning", "Info"]
        for issue in data.get("issues", []):
            if issue.get("type") not in valid_types:
                issue["type"] = "Info"
        
        # Ensure lists exist
        data["issues"] = data.get("issues", [])
        data["strengths"] = data.get("strengths", [])
        data["improvements"] = data.get("improvements", [])
        
        return data


def create_analyzer(api_key: Optional[str] = None) -> AIAnalyzer:
    """
    Factory function to create an AIAnalyzer instance.
    
    Args:
        api_key: Optional API key. If provided, overrides environment config.
    
    Returns:
        Configured AIAnalyzer instance.
    """
    return AIAnalyzer(api_key=api_key)
