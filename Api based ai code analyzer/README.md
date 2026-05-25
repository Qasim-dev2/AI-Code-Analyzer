# AI Code Analyzer

Local Streamlit app for Python code analysis, practice problems, coaching, and code comparison using Ollama.

## Active App

The supported entrypoint is:

```powershell
streamlit run main_app.py
```

On Windows you can also use:

```powershell
.\run_app.ps1
```

## Project Layout

```text
Api based ai code analyzer/
|-- main_app.py              # Active Streamlit UI
|-- run_app.ps1             # Windows launcher
|-- requirements.txt
|-- README.md
|-- PROJECT_DOCUMENTATION.md
|-- backend/
|   |-- ollama_client.py    # Ollama HTTP client
|   `-- code_executor.py    # Local Python runner
|-- config/
|   `-- settings.py         # Shared app settings/content
|-- prompts/
|   |-- analyzer_prompts.py
|   |-- practice_prompts.py
|   `-- coach_prompts.py
`-- utils/
    `-- session_manager.py  # Shared Streamlit session helpers
```

## Legacy Files

These files are still in the repo for reference, but they are not the active runtime path:

- `app.py`
- `backend/ai_client.py`
- `backend/ai_analyzer.py`
- `utils/report_generator.py`
- `utils/prompt_builder.py`

## Prerequisites

- Python 3.9+
- Ollama installed locally
- At least one local model, for example `codellama:7b`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
ollama serve
ollama pull codellama:7b
```

## Run

```powershell
streamlit run main_app.py
```

The app will usually open at `http://localhost:8501`.

## Notes

- The code runner uses a subprocess with a timeout. It is isolated from the app process, but it is not a hardened sandbox.
- Practice generation now uses the same test-case schema as the test runner, so generated questions can be executed without manual key fixes.
