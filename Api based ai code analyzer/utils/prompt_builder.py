"""
Prompt Builder Module

Constructs system and user prompts for AI-driven code analysis.
Enforces JSON-only output rules and configurable analysis depth.
"""

from typing import Literal


AnalysisDepth = Literal["Quick", "Detailed"]


def build_system_prompt(depth: AnalysisDepth = "Detailed") -> str:
    """
    Build the system prompt that defines AI behavior and output format.
    
    Args:
        depth: Analysis depth - "Quick" for fast overview, "Detailed" for comprehensive analysis.
    
    Returns:
        System prompt string for the AI model.
    """
    depth_instruction = _get_depth_instruction(depth)
    
    return f"""You are an expert Python code analyzer with deep expertise in software engineering, 
code quality assessment, and best practices. Your role is to analyze Python source code 
and provide professional, actionable insights.

ANALYSIS DEPTH: {depth}
{depth_instruction}

CRITICAL OUTPUT RULES:
1. You MUST respond with ONLY valid JSON - no markdown, no explanations, no text before or after
2. Do NOT wrap the JSON in code blocks or backticks
3. Do NOT include any text outside the JSON structure
4. Ensure all JSON strings are properly escaped
5. Use double quotes for all JSON keys and string values

ANALYSIS GUIDELINES:
- Reason semantically about code quality, logic flow, and maintainability
- Detect code smells, poor design patterns, unclear naming, and over-complex logic
- Evaluate documentation quality based on docstrings and inline comments
- Estimate complexity based on logical reasoning, not mathematical formulas
- Consider readability, maintainability, and professional standards
- Be constructive and provide actionable recommendations

REQUIRED JSON RESPONSE FORMAT:
{{
  "summary": {{
    "overall_grade": "A|B|C|D",
    "readability_score": <1-10>,
    "maintainability_score": <0-100>,
    "complexity_level": "Low|Medium|High",
    "documentation_quality": "Poor|Average|Good|Excellent"
  }},
  "metrics": {{
    "estimated_cyclomatic_complexity": <number>,
    "functions_count": <number>,
    "classes_count": <number>,
    "average_function_length": <number>,
    "lines_of_code": <number>
  }},
  "issues": [
    {{
      "type": "Error|Warning|Info",
      "title": "Short issue title",
      "description": "Clear explanation of the problem",
      "location": "Function name, class name, or line range",
      "recommendation": "Concrete and actionable fix suggestion"
    }}
  ],
  "strengths": [
    "Positive aspects of the code"
  ],
  "improvements": [
    "High-level architectural or design improvements"
  ]
}}

GRADING CRITERIA:
- Grade A: Excellent code following best practices, minimal issues
- Grade B: Good code with minor improvements possible
- Grade C: Functional code with notable areas for improvement
- Grade D: Code with significant issues requiring attention

SCORING GUIDELINES:
- readability_score (1-10): How easy is the code to read and understand
- maintainability_score (0-100): How easy is the code to maintain and extend
- complexity_level: Based on logical complexity, nesting, and cognitive load
- documentation_quality: Based on presence and quality of docstrings/comments"""


def _get_depth_instruction(depth: AnalysisDepth) -> str:
    """Get depth-specific analysis instructions."""
    if depth == "Quick":
        return """QUICK ANALYSIS MODE:
- Focus on the most critical issues and overall code quality
- Identify major code smells and design problems
- Provide a high-level summary with key recommendations
- Limit issues to the 5 most important findings
- Keep recommendations concise and actionable"""
    else:
        return """DETAILED ANALYSIS MODE:
- Perform comprehensive analysis of all aspects
- Identify all code smells, design issues, and improvement opportunities
- Provide detailed explanations and recommendations
- Include both critical issues and minor suggestions
- Analyze documentation, naming conventions, and code structure thoroughly"""


def build_user_prompt(code: str, depth: AnalysisDepth = "Detailed") -> str:
    """
    Build the user prompt containing the code to analyze.
    
    Args:
        code: Python source code to analyze.
        depth: Analysis depth setting.
    
    Returns:
        User prompt string with the code.
    """
    return f"""Analyze the following Python code and provide your assessment in the exact JSON format specified.

ANALYSIS DEPTH: {depth}

PYTHON CODE TO ANALYZE:
```python
{code}
```

Remember: Respond with ONLY valid JSON, no additional text or formatting."""


def build_messages(code: str, depth: AnalysisDepth = "Detailed") -> list[dict]:
    """
    Build the complete message list for the AI API call.
    
    Args:
        code: Python source code to analyze.
        depth: Analysis depth setting.
    
    Returns:
        List of message dictionaries for the API.
    """
    return [
        {"role": "system", "content": build_system_prompt(depth)},
        {"role": "user", "content": build_user_prompt(code, depth)}
    ]
