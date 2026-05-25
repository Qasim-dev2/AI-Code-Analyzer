"""Prompt helpers for coaching and explanation flows."""


HINTS_SYSTEM_PROMPT = """You are a Python coach.

Rules:
- Do not provide a complete solution.
- Give hints, checks, and small nudges.
- Point out likely mistakes and edge cases.
- Ask guiding questions when useful.
- Keep the answer concise and practical."""

FULL_GUIDANCE_SYSTEM_PROMPT = """You are an expert Python developer.

Provide direct help:
- fix bugs
- explain code
- refactor
- optimize when justified

Use markdown and code blocks when useful. Explain the important changes, not every tiny detail."""

CHAT_SYSTEM_PROMPT = """You are a concise Python learning assistant.

Answer clearly, stay on topic, and optimize for practical understanding."""


def build_hints_prompt(
    code: str,
    problem_context: str = "",
    specific_question: str = "",
) -> str:
    """Build a hints-only request."""
    parts = []

    if problem_context:
        parts.append(f"Problem context:\n{problem_context}")

    parts.append(f"Current code:\n```python\n{code}\n```")

    if specific_question:
        parts.append(f"Question:\n{specific_question}")

    parts.append(
        "Give hints only. Identify what is promising, where the logic may be off, "
        "and what to check next."
    )
    return "\n\n".join(parts)


def build_full_guidance_prompt(
    code: str,
    problem_context: str = "",
    specific_question: str = "",
    analysis_result: dict | None = None,
) -> str:
    """Build a full-help request."""
    parts = []

    if problem_context:
        parts.append(f"Problem context:\n{problem_context}")

    parts.append(f"Code:\n```python\n{code}\n```")

    if specific_question:
        parts.append(f"Request:\n{specific_question}")

    if analysis_result:
        summary = analysis_result.get("summary", {})
        issues = analysis_result.get("issues", [])
        summary_text = summary.get("summary")
        if summary_text:
            parts.append(f"Previous analysis summary:\n{summary_text}")
        if issues:
            issue_lines = []
            for issue in issues[:5]:
                issue_lines.append(f"- {issue.get('severity', 'Info')}: {issue.get('title', 'Issue')}")
            parts.append("Previous issues:\n" + "\n".join(issue_lines))

    parts.append(
        "Provide complete help. If you change code, explain the most important fixes and tradeoffs."
    )
    return "\n\n".join(parts)


get_hints_prompt = build_hints_prompt
get_full_guidance_prompt = build_full_guidance_prompt
