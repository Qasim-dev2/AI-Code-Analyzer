"""
AI Coach Prompt Builder

Builds prompts for the AI Coach feature - provides hints and improved solutions
based on code analysis results and user code.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class CoachContext:
    """Context for AI Coach prompts."""
    
    user_code: str
    analysis_data: Optional[dict] = None
    problem_description: Optional[str] = None
    constraints: Optional[str] = None
    test_results: Optional[str] = None


HINT_SYSTEM_PROMPT = """You are an expert Python coding coach. Your role is to help developers improve their code WITHOUT giving away the full solution.

Guidelines:
- Provide helpful hints and nudges in the right direction
- Point out areas that need improvement without fixing them directly
- Ask guiding questions that lead to understanding
- Reference specific line numbers or code sections when helpful
- Be encouraging and supportive
- Focus on teaching concepts, not just fixes

DO NOT:
- Provide complete code solutions
- Rewrite functions entirely
- Give copy-paste ready fixes

Format your response with clear sections using markdown."""


SOLUTION_SYSTEM_PROMPT = """You are an expert Python developer and code reviewer. Your role is to provide an improved version of the user's code with detailed explanations.

Guidelines:
- Provide a complete, improved version of the code
- Explain each significant change you made
- Follow Python best practices (PEP 8, type hints, docstrings)
- Optimize for readability and maintainability
- Address any issues found in the analysis
- Add helpful comments in the code

Format your response with:
1. Brief summary of improvements
2. The improved code in a Python code block
3. Explanation of key changes

Be thorough but concise."""


def build_hint_prompt(context: CoachContext) -> str:
    """
    Build a prompt for getting hints (no full solution).
    
    Args:
        context: The coach context with code and analysis.
    
    Returns:
        Formatted prompt string.
    """
    prompt_parts = [
        "# Code Review Request - Hints Only",
        "",
        "## User's Code",
        "```python",
        context.user_code,
        "```",
        ""
    ]
    
    if context.problem_description:
        prompt_parts.extend([
            "## Problem Description",
            context.problem_description,
            ""
        ])
    
    if context.constraints:
        prompt_parts.extend([
            "## Constraints",
            context.constraints,
            ""
        ])
    
    if context.analysis_data:
        prompt_parts.extend([
            "## Analysis Results",
            _format_analysis_summary(context.analysis_data),
            ""
        ])
    
    if context.test_results:
        prompt_parts.extend([
            "## Test Results",
            context.test_results,
            ""
        ])
    
    prompt_parts.extend([
        "## Your Task",
        "Please provide helpful hints and guidance to improve this code.",
        "- Point out issues without giving the solution",
        "- Ask guiding questions",
        "- Suggest areas to research or concepts to review",
        "- Be encouraging and educational",
        "",
        "Remember: NO complete solutions, just hints!"
    ])
    
    return "\n".join(prompt_parts)


def build_solution_prompt(context: CoachContext) -> str:
    """
    Build a prompt for getting a complete improved solution.
    
    Args:
        context: The coach context with code and analysis.
    
    Returns:
        Formatted prompt string.
    """
    prompt_parts = [
        "# Code Improvement Request - Full Solution",
        "",
        "## User's Original Code",
        "```python",
        context.user_code,
        "```",
        ""
    ]
    
    if context.problem_description:
        prompt_parts.extend([
            "## Problem Description",
            context.problem_description,
            ""
        ])
    
    if context.constraints:
        prompt_parts.extend([
            "## Constraints",
            context.constraints,
            ""
        ])
    
    if context.analysis_data:
        prompt_parts.extend([
            "## Analysis Results",
            _format_analysis_summary(context.analysis_data),
            ""
        ])
    
    if context.test_results:
        prompt_parts.extend([
            "## Test Results",
            context.test_results,
            ""
        ])
    
    prompt_parts.extend([
        "## Your Task",
        "Please provide an improved version of this code with:",
        "1. All issues fixed",
        "2. Best practices applied",
        "3. Proper error handling",
        "4. Clear documentation",
        "5. Optimized performance where possible",
        "",
        "Explain your changes clearly."
    ])
    
    return "\n".join(prompt_parts)


def _format_analysis_summary(data: dict) -> str:
    """Format analysis data for inclusion in prompts."""
    lines = []
    
    # Summary
    summary = data.get("summary", {})
    if summary:
        lines.append(f"- Overall Grade: {summary.get('overall_grade', 'N/A')}")
        lines.append(f"- Readability Score: {summary.get('readability_score', 'N/A')}/10")
        lines.append(f"- Maintainability: {summary.get('maintainability_score', 'N/A')}/100")
        lines.append(f"- Complexity: {summary.get('complexity_level', 'N/A')}")
        lines.append(f"- Documentation: {summary.get('documentation_quality', 'N/A')}")
        lines.append("")
    
    # Issues
    issues = data.get("issues", [])
    if issues:
        lines.append("### Issues Found:")
        for issue in issues[:10]:  # Limit to first 10 issues
            issue_type = issue.get("type", "Info")
            title = issue.get("title", "Unknown")
            location = issue.get("location", "")
            lines.append(f"- [{issue_type}] {title} ({location})")
        lines.append("")
    
    # Improvements
    improvements = data.get("improvements", [])
    if improvements:
        lines.append("### Suggested Improvements:")
        for imp in improvements[:5]:  # Limit to first 5
            lines.append(f"- {imp}")
    
    return "\n".join(lines)


def get_coach_prompts(
    code: str,
    mode: str = "hints",
    analysis_data: Optional[dict] = None,
    problem_description: Optional[str] = None,
    test_results: Optional[str] = None
) -> tuple[str, str]:
    """
    Get system prompt and user prompt for AI Coach.
    
    Args:
        code: The user's code.
        mode: Either "hints" or "solution".
        analysis_data: Optional analysis results.
        problem_description: Optional problem description.
        test_results: Optional test results.
    
    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    context = CoachContext(
        user_code=code,
        analysis_data=analysis_data,
        problem_description=problem_description,
        test_results=test_results
    )
    
    if mode == "hints":
        return HINT_SYSTEM_PROMPT, build_hint_prompt(context)
    else:
        return SOLUTION_SYSTEM_PROMPT, build_solution_prompt(context)
