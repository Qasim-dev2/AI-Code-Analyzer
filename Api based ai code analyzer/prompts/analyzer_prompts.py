"""Prompt helpers for code analysis."""


ANALYSIS_SYSTEM_PROMPT = """You are an expert Python code reviewer.

Respond with valid JSON using this exact shape:
{
  "summary": {
    "quality": "Good|Fair|Poor",
    "readability": 1-10,
    "maintainability": 1-10,
    "summary": "One concise summary sentence"
  },
  "complexity": {
    "time": "O(...)",
    "space": "O(...)",
    "note": "Heuristic estimate based on the visible code"
  },
  "issues": [
    {
      "severity": "Error|Warning|Info",
      "title": "Short title",
      "description": "What is wrong and why it matters",
      "fix": "Concrete fix or improvement"
    }
  ],
  "strengths": ["..."],
  "suggestions": ["..."]
}

Keep the response practical and concise. Return JSON only."""


def build_analysis_prompt(code: str) -> str:
    """Build the analysis request."""
    return f"""Analyze this Python code.

Focus on:
1. Code quality and readability
2. Maintainability
3. Likely bugs or code smells
4. Heuristic time and space complexity
5. Actionable improvements

Code:
```python
{code}
```"""


get_analysis_prompt = build_analysis_prompt
