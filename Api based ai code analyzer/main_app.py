"""Streamlit entry point for the active Ollama-based application."""

from __future__ import annotations

import json
import re
from typing import Any

import streamlit as st

from config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    AppConfig,
    DIFFICULTIES,
    PRACTICE_TIMES,
    RECOMMENDED_MODELS,
    REFERENCE_CONTENT,
    SAMPLE_CODES,
    TOPICS,
)
from prompts import (
    ANALYSIS_SYSTEM_PROMPT,
    CHAT_SYSTEM_PROMPT,
    FULL_GUIDANCE_SYSTEM_PROMPT,
    HINTS_SYSTEM_PROMPT,
    PRACTICE_SYSTEM_PROMPT,
    build_analysis_prompt,
    build_full_guidance_prompt,
    build_hints_prompt,
    build_practice_prompt,
)
from utils.session_manager import (
    format_time,
    get_remaining_time,
    init_session_state,
    reset_analysis,
    start_practice,
)


st.set_page_config(
    page_title=APP_NAME,
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_ollama_module():
    """Cache Ollama imports."""
    from backend.ollama_client import OllamaClient, OllamaConfig, check_ollama_status

    return OllamaClient, OllamaConfig, check_ollama_status


@st.cache_resource
def get_executor_factory():
    """Cache code executor import."""
    from backend.code_executor import get_executor

    return get_executor


@st.cache_data(ttl=60)
def get_cached_models() -> list[str]:
    """Return installed Ollama models."""
    ollama_client, ollama_config, _ = get_ollama_module()
    try:
        client = ollama_client(ollama_config())
        return client.list_models()
    except Exception:
        return []


@st.cache_data(ttl=10)
def get_connection_status() -> tuple[bool, str]:
    """Return cached Ollama connection status."""
    _, _, check_ollama_status = get_ollama_module()
    return check_ollama_status()


def render_styles() -> None:
    """Render lightweight app styles."""
    st.markdown(
        """
        <style>
        .app-header {
            padding: 1.25rem 1.5rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #102542, #1f4e79);
            color: white;
            margin-bottom: 1rem;
        }
        .app-header h1 {
            margin: 0;
            font-size: 2rem;
        }
        .app-header p {
            margin: 0.35rem 0 0;
            opacity: 0.9;
        }
        .timer-box {
            padding: 0.9rem;
            border-radius: 10px;
            text-align: center;
            font-family: Consolas, monospace;
            font-size: 1.8rem;
            font-weight: 700;
            background: #102542;
            color: white;
        }
        .section-note {
            padding: 0.85rem 1rem;
            border-radius: 10px;
            background: #f4f7fb;
            border: 1px solid #d9e2ec;
            margin-bottom: 1rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_client():
    """Build a configured Ollama client from current state."""
    ollama_client, ollama_config, _ = get_ollama_module()
    return ollama_client(
        ollama_config(
            model=st.session_state.model,
            temperature=st.session_state.temperature,
            timeout=AppConfig.REQUEST_TIMEOUT,
        )
    )


def parse_json_response(text: str) -> dict[str, Any] | None:
    """Parse JSON from a raw model response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if block_match:
        try:
            return json.loads(block_match.group(1))
        except json.JSONDecodeError:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None

    return None


def normalize_practice_question(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize practice question data into one stable schema."""
    statement = payload.get("statement") or payload.get("problem_statement") or ""
    starter_code = payload.get("starter_code") or payload.get("starter") or "def solution():\n    pass"

    examples = [item for item in payload.get("examples", []) if isinstance(item, dict)]
    constraints = [str(item) for item in payload.get("constraints", [])]
    hints = [str(item) for item in payload.get("hints", [])]

    raw_tests = payload.get("test_cases") or payload.get("tests") or []
    test_cases = []
    for item in raw_tests:
        if not isinstance(item, dict):
            continue
        test_cases.append(
            {
                "input": str(item.get("input", item.get("stdin", ""))),
                "expected_output": str(
                    item.get(
                        "expected_output",
                        item.get("output", item.get("expected", "")),
                    )
                ),
            }
        )

    return {
        "title": payload.get("title", "Practice Problem"),
        "difficulty": payload.get("difficulty", "Medium"),
        "topic": payload.get("topic", "General"),
        "statement": statement,
        "constraints": constraints,
        "examples": examples,
        "starter_code": starter_code,
        "test_cases": test_cases,
        "hints": hints,
    }


def stream_response(container: Any, prompt: str, system_prompt: str) -> str:
    """Stream an AI response into a placeholder container."""
    placeholder = container.empty() if hasattr(container, "empty") else st.empty()
    chunks: list[str] = []

    for index, token in enumerate(get_client().stream_generate(prompt, system_prompt), start=1):
        chunks.append(token)
        if index % 4 == 0 or token.endswith((".", "!", "?", "\n")):
            placeholder.markdown("".join(chunks) + "|")

    full_response = "".join(chunks)
    placeholder.markdown(full_response)
    return full_response


def render_sidebar() -> bool:
    """Render the sidebar and return whether AI features are available."""
    with st.sidebar:
        st.header("Settings")

        connected, status = get_connection_status()
        if connected:
            st.success(status)
        else:
            st.error(status)
            st.code("ollama serve", language="bash")
            return False

        models = get_cached_models()
        if not models:
            st.warning("Ollama is running but no local models were found.")
            st.code("ollama pull codellama:7b", language="bash")
            return False

        with st.expander("Recommended models", expanded=False):
            for model_name, description in RECOMMENDED_MODELS.items():
                installed = "installed" if model_name in models else "not installed"
                st.caption(f"{model_name}: {description} ({installed})")

        if st.session_state.model not in models:
            st.session_state.model = models[0]

        st.session_state.model = st.selectbox(
            "Model",
            options=models,
            index=models.index(st.session_state.model),
        )
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=float(st.session_state.temperature),
            step=0.1,
        )

        st.caption(f"App version: {APP_VERSION}")
        st.caption(f"Active model: {st.session_state.model}")

    return True


def run_analysis(code: str) -> None:
    """Run analysis and store the result."""
    with st.spinner("Running analysis..."):
        raw_response = get_client().generate(build_analysis_prompt(code), ANALYSIS_SYSTEM_PROMPT)

    parsed = parse_json_response(raw_response)
    if parsed is None:
        st.warning("The model returned output that could not be parsed as structured JSON.")
        with st.expander("Raw response", expanded=False):
            st.markdown(raw_response)
        return

    st.session_state.analysis = parsed


def show_analysis(data: dict[str, Any]) -> None:
    """Render structured analysis results."""
    summary = data.get("summary", {})
    complexity = data.get("complexity", {})
    issues = [item for item in data.get("issues", []) if isinstance(item, dict)]

    st.divider()
    st.subheader("Analysis Results")

    metric_columns = st.columns(4)
    metric_columns[0].metric("Quality", summary.get("quality", "N/A"))
    metric_columns[1].metric("Readability", summary.get("readability", "N/A"))
    metric_columns[2].metric("Maintainability", summary.get("maintainability", "N/A"))
    metric_columns[3].metric("Issues", len(issues))

    if summary.get("summary"):
        st.markdown(summary["summary"])

    complexity_columns = st.columns(2)
    complexity_columns[0].metric("Time complexity", complexity.get("time", "N/A"))
    complexity_columns[1].metric("Space complexity", complexity.get("space", "N/A"))
    if complexity.get("note"):
        st.caption(complexity["note"])

    if issues:
        st.markdown("#### Issues")
        grouped = {
            "Error": [item for item in issues if item.get("severity") == "Error"],
            "Warning": [item for item in issues if item.get("severity") == "Warning"],
            "Info": [item for item in issues if item.get("severity") == "Info"],
        }
        for severity, entries in grouped.items():
            if not entries:
                continue
            for issue in entries:
                title = issue.get("title", "Issue")
                with st.expander(f"{severity}: {title}", expanded=severity == "Error"):
                    st.markdown(issue.get("description", ""))
                    if issue.get("fix"):
                        st.info(issue["fix"])
    else:
        st.success("No structured issues were reported.")

    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("#### Strengths")
        strengths = data.get("strengths", [])
        if strengths:
            for item in strengths:
                st.markdown(f"- {item}")
        else:
            st.caption("No specific strengths were listed.")

    with right_col:
        st.markdown("#### Suggestions")
        suggestions = data.get("suggestions", [])
        if suggestions:
            for item in suggestions:
                st.markdown(f"- {item}")
        else:
            st.caption("No specific suggestions were listed.")


def render_analyze_tab() -> None:
    """Render the analysis tab."""
    st.subheader("Analyze Python Code")

    sample_name = st.selectbox(
        "Load sample code",
        options=[""] + list(SAMPLE_CODES.keys()),
        format_func=lambda value: "Select a sample..." if not value else value,
    )
    if sample_name and st.session_state.analyze_code != SAMPLE_CODES[sample_name]:
        st.session_state.analyze_code = SAMPLE_CODES[sample_name]

    code = st.text_area(
        "Code",
        key="analyze_code",
        height=320,
        placeholder="Paste Python code here...",
    )

    control_col, clear_col, stats_col = st.columns([1, 1, 2])
    with control_col:
        run_clicked = st.button("Analyze", type="primary", use_container_width=True, disabled=not code)
    with clear_col:
        clear_clicked = st.button("Clear", use_container_width=True)
    with stats_col:
        if code:
            st.markdown(
                f'<div class="section-note">Lines: {code.count(chr(10)) + 1} | Characters: {len(code)}</div>',
                unsafe_allow_html=True,
            )

    if clear_clicked:
        st.session_state.analyze_code = ""
        reset_analysis()
        st.rerun()

    if run_clicked and code:
        run_analysis(code)

    if st.session_state.analysis:
        show_analysis(st.session_state.analysis)


def generate_practice_question(topic: str, difficulty: str) -> None:
    """Generate and store a practice question."""
    with st.spinner("Generating practice question..."):
        raw_response = get_client().generate(
            build_practice_prompt(topic, difficulty),
            PRACTICE_SYSTEM_PROMPT,
        )

    parsed = parse_json_response(raw_response)
    if parsed is None:
        st.warning("The model response could not be parsed as a practice question.")
        with st.expander("Raw response", expanded=False):
            st.markdown(raw_response)
        return

    normalized = normalize_practice_question(parsed)
    st.session_state.practice_question = normalized
    st.session_state.practice_solution = normalized["starter_code"]
    st.session_state.practice_started = False
    st.session_state.practice_start_time = None
    st.session_state.practice_time_limit = PRACTICE_TIMES.get(difficulty, PRACTICE_TIMES["Medium"])
    st.session_state.run_output = None


def run_code(code: str) -> None:
    """Run arbitrary code with the configured executor."""
    executor = get_executor_factory()(AppConfig.EXECUTION_TIMEOUT)
    result = executor.execute(code)
    st.session_state.run_output = {"type": "run", "data": result.__dict__}


def run_tests(code: str, test_cases: list[dict[str, str]]) -> None:
    """Run code against generated test cases."""
    if not test_cases:
        st.warning("No test cases are available for this question.")
        return

    executor = get_executor_factory()(AppConfig.EXECUTION_TIMEOUT)
    results, passed, total = executor.run_with_tests(code, test_cases)
    st.session_state.run_output = {
        "type": "tests",
        "results": results,
        "passed": passed,
        "total": total,
    }


def show_run_output(output: dict[str, Any]) -> None:
    """Render execution or test output."""
    st.markdown("#### Output")

    if output["type"] == "run":
        data = output["data"]
        if data.get("success"):
            st.success("Code executed successfully.")
            st.code(data.get("stdout", "") or "No output")
        else:
            st.error("Code execution failed.")
            st.code(data.get("stderr", "") or data.get("error_message", "Unknown error"))
        return

    passed = output["passed"]
    total = output["total"]
    if passed == total:
        st.success(f"All tests passed ({passed}/{total}).")
    else:
        st.warning(f"{passed}/{total} tests passed.")

    for result in output["results"]:
        title = f"Test {result['test_num']} - {'pass' if result['passed'] else 'fail'}"
        with st.expander(title, expanded=not result["passed"]):
            st.markdown(f"Input: `{result['input']}`")
            st.markdown(f"Expected: `{result['expected']}`")
            st.markdown(f"Actual: `{result['actual']}`")
            if result.get("error"):
                st.code(result["error"])


def show_practice_question(question: dict[str, Any]) -> None:
    """Render the active practice question."""
    st.divider()

    left_col, right_col = st.columns([4, 1])
    with left_col:
        st.subheader(question.get("title", "Practice Problem"))
        st.caption(f"{question.get('difficulty', 'Medium')} | {question.get('topic', 'General')}")
    with right_col:
        if not st.session_state.practice_started:
            if st.button("Start timer", type="primary", use_container_width=True):
                start_practice(st.session_state.practice_time_limit)
                st.rerun()
        else:
            remaining = get_remaining_time()
            if remaining is not None:
                st.markdown(
                    f'<div class="timer-box">{format_time(remaining)}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown(question.get("statement", ""))

    example_col, constraint_col = st.columns(2)
    with example_col:
        examples = question.get("examples", [])
        if examples:
            st.markdown("**Examples**")
            for index, example in enumerate(examples[:3], start=1):
                with st.expander(f"Example {index}", expanded=index == 1):
                    st.code(
                        "\n".join(
                            [
                                f"Input: {example.get('input', '')}",
                                f"Output: {example.get('output', '')}",
                                f"Explanation: {example.get('explanation', '')}",
                            ]
                        )
                    )
    with constraint_col:
        constraints = question.get("constraints", [])
        if constraints:
            st.markdown("**Constraints**")
            for item in constraints:
                st.markdown(f"- {item}")

    hints = question.get("hints", [])
    if hints:
        with st.expander("Hints", expanded=False):
            for index, item in enumerate(hints, start=1):
                st.markdown(f"{index}. {item}")

    st.divider()
    code = st.text_area(
        "Solution",
        key="practice_solution",
        height=260,
        placeholder="Write your solution here...",
    )

    run_col, test_col, reset_col = st.columns(3)
    with run_col:
        if st.button("Run code", type="primary", use_container_width=True):
            run_code(code)
            st.rerun()
    with test_col:
        if st.button("Run tests", use_container_width=True):
            run_tests(code, question.get("test_cases", []))
            st.rerun()
    with reset_col:
        if st.button("Reset solution", use_container_width=True):
            st.session_state.practice_solution = question.get("starter_code", "")
            st.session_state.run_output = None
            st.rerun()

    if st.session_state.run_output:
        show_run_output(st.session_state.run_output)


def render_practice_tab() -> None:
    """Render the practice tab."""
    st.subheader("Practice Mode")

    topic_col, difficulty_col, time_col = st.columns(3)
    with topic_col:
        topic = st.selectbox("Topic", TOPICS)
    with difficulty_col:
        difficulty = st.selectbox("Difficulty", DIFFICULTIES)
    with time_col:
        st.metric("Recommended time", format_time(PRACTICE_TIMES[difficulty]))

    if st.button("Generate question", type="primary", use_container_width=True):
        generate_practice_question(topic, difficulty)
        st.rerun()

    question = st.session_state.practice_question
    if question:
        show_practice_question(question)


def render_chat_tab() -> None:
    """Render the chat tab."""
    st.subheader("Chat with the Coach")

    control_col, _ = st.columns([1, 5])
    with control_col:
        if st.button("Clear chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    quick_message = ""
    quick_prompts = [
        "How do I reason about Big O notation?",
        "When should I use recursion?",
        "What is the difference between a list and a tuple?",
        "How do hash maps work in Python?",
    ]
    quick_columns = st.columns(len(quick_prompts))
    for column, prompt in zip(quick_columns, quick_prompts):
        with column:
            if st.button(prompt, use_container_width=True):
                quick_message = prompt

    for message in st.session_state.chat_history:
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(message["content"])

    chat_input = st.chat_input("Ask about Python, debugging, or algorithms")
    user_message = chat_input or quick_message
    if not user_message:
        return

    st.session_state.chat_history.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    history_window = st.session_state.chat_history[-6:]
    history_lines = []
    for item in history_window:
        role = "User" if item["role"] == "user" else "Assistant"
        history_lines.append(f"{role}: {item['content']}")
    prompt = "\n".join(history_lines) + "\n\nRespond helpfully."

    with st.chat_message("assistant"):
        response = stream_response(st, prompt, CHAT_SYSTEM_PROMPT)

    st.session_state.chat_history.append({"role": "assistant", "content": response})


def render_hints_tab() -> None:
    """Render the hints tab."""
    st.subheader("Hints Only")
    st.markdown(
        '<div class="section-note">This mode gives guidance without full solutions.</div>',
        unsafe_allow_html=True,
    )

    copy_analyze_col, copy_practice_col = st.columns(2)
    with copy_analyze_col:
        if st.button("Use code from Analyze", use_container_width=True, key="hints_from_analyze") and st.session_state.analyze_code:
            st.session_state.hints_code = st.session_state.analyze_code
            st.rerun()
    with copy_practice_col:
        if st.button("Use code from Practice", use_container_width=True, key="hints_from_practice") and st.session_state.practice_solution:
            st.session_state.hints_code = st.session_state.practice_solution
            st.rerun()

    code = st.text_area("Code", key="hints_code", height=220)
    question = st.text_input("What are you stuck on?", key="hints_question")

    if st.button("Get hints", type="primary", disabled=not code):
        prompt = build_hints_prompt(code=code, specific_question=question)
        st.markdown("#### Hints")
        stream_response(st.container(), prompt, HINTS_SYSTEM_PROMPT)


def render_full_help_tab() -> None:
    """Render the full-help tab."""
    st.subheader("Full Help")

    copy_analyze_col, copy_practice_col = st.columns(2)
    with copy_analyze_col:
        if st.button("Use code from Analyze", use_container_width=True, key="full_from_analyze") and st.session_state.analyze_code:
            st.session_state.full_code = st.session_state.analyze_code
            st.rerun()
    with copy_practice_col:
        if st.button("Use code from Practice", use_container_width=True, key="full_from_practice") and st.session_state.practice_solution:
            st.session_state.full_code = st.session_state.practice_solution
            st.rerun()

    code = st.text_area("Code", key="full_code", height=220)

    action_columns = st.columns(4)
    suggested_action = ""
    actions = ["Fix bugs", "Optimize", "Explain", "Refactor"]
    for column, action in zip(action_columns, actions):
        with column:
            if st.button(action, use_container_width=True):
                suggested_action = action

    if suggested_action:
        st.session_state.full_request = suggested_action

    request_text = st.text_input(
        "What do you want help with?",
        key="full_request",
        placeholder="Example: optimize this loop or explain why this fails",
    )

    if st.button("Get full help", type="primary", disabled=not code):
        prompt = build_full_guidance_prompt(
            code=code,
            specific_question=request_text,
            analysis_result=st.session_state.analysis,
        )
        st.markdown("#### Response")
        stream_response(st.container(), prompt, FULL_GUIDANCE_SYSTEM_PROMPT)


def render_compare_tab() -> None:
    """Render the compare tab."""
    st.subheader("Compare Two Versions")

    left_col, right_col = st.columns(2)
    with left_col:
        st.text_area("Version 1", key="compare_code1", height=240)
    with right_col:
        st.text_area("Version 2", key="compare_code2", height=240)

    code_one = st.session_state.compare_code1
    code_two = st.session_state.compare_code2

    if st.button("Compare", type="primary", disabled=not (code_one and code_two)):
        prompt = (
            "Compare these two Python implementations.\n\n"
            f"Version 1:\n```python\n{code_one}\n```\n\n"
            f"Version 2:\n```python\n{code_two}\n```\n\n"
            "Explain which version is stronger and why. Comment on readability, correctness, "
            "maintainability, and likely performance."
        )
        st.markdown("#### Comparison")
        stream_response(st.container(), prompt, FULL_GUIDANCE_SYSTEM_PROMPT)


def render_reference_tab() -> None:
    """Render the reference tab."""
    st.subheader("Quick Reference")
    topic = st.selectbox("Reference topic", list(REFERENCE_CONTENT.keys()))
    st.markdown(REFERENCE_CONTENT[topic])


def main() -> None:
    """Main application entry point."""
    init_session_state()
    render_styles()

    st.markdown(
        f"""
        <div class="app-header">
            <h1>{APP_NAME}</h1>
            <p>{APP_DESCRIPTION}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ai_ready = render_sidebar()
    if not ai_ready:
        st.info("The UI is ready, but Ollama must be available before AI features can run.")
        return

    tabs = st.tabs(
        [
            "Analyze",
            "Practice",
            "Chat",
            "Hints",
            "Full Help",
            "Compare",
            "Reference",
        ]
    )

    with tabs[0]:
        render_analyze_tab()
    with tabs[1]:
        render_practice_tab()
    with tabs[2]:
        render_chat_tab()
    with tabs[3]:
        render_hints_tab()
    with tabs[4]:
        render_full_help_tab()
    with tabs[5]:
        render_compare_tab()
    with tabs[6]:
        render_reference_tab()


if __name__ == "__main__":
    main()
