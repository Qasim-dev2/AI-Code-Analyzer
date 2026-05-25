"""Prompt helpers for practice question generation."""


PRACTICE_SYSTEM_PROMPT = """You generate original Python practice problems.

Respond with valid JSON using this exact shape:
{
  "title": "Problem title",
  "difficulty": "Easy|Medium|Hard",
  "topic": "Topic name",
  "statement": "Clear problem statement",
  "constraints": ["Constraint 1", "Constraint 2"],
  "examples": [
    {
      "input": "...",
      "output": "...",
      "explanation": "..."
    }
  ],
  "starter_code": "def solution(...):\\n    pass",
  "test_cases": [
    {
      "input": "...",
      "expected_output": "..."
    }
  ],
  "hints": ["Hint 1", "Hint 2"]
}

Rules:
- Create an original educational problem.
- Make it solvable in Python.
- Include 2-4 useful test cases.
- Keep hints helpful but not revealing.
- Return JSON only."""


def build_practice_prompt(topic: str, difficulty: str) -> str:
    """Build the practice generation request."""
    guidance = {
        "Easy": "Use one core idea and keep the implementation direct.",
        "Medium": "Require some reasoning or a standard pattern.",
        "Hard": "Require stronger problem solving or a more advanced pattern.",
    }

    return f"""Create a {difficulty} Python coding problem about {topic}.

Difficulty guidance: {guidance.get(difficulty, guidance["Medium"])}

Make the examples realistic and the test cases easy to run from stdin/stdout when possible."""


get_practice_prompt = build_practice_prompt
