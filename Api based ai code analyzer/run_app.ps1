$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    $python = "python"
}

& $python -m streamlit run (Join-Path $PSScriptRoot "main_app.py")
