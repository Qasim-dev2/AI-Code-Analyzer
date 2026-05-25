# AI Code Analyzer

<div align="center">

![AI Code Analyzer](public/AI%20Code%20Analyzer%20Thumbnill.png)

### 🚀 A Powerful Local-First AI Code Assistant

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Screenshots](#-screenshots) • [Architecture](#-architecture) • [Technologies](#-technologies)

</div>

---

## 📋 Overview

**AI Code Analyzer** is an intelligent, local-first code analysis and learning platform powered by **Ollama AI**. It provides real-time code analysis, practice problem generation, interactive coaching, and comprehensive learning tools—**all running locally without requiring internet connectivity or API costs**.

### ✨ Key Highlights

- **🎯 100% Local & Free** - No API costs, no cloud dependencies
- **🔒 Privacy-First** - All data stays on your machine
- **⚡ Real-time AI** - Streaming responses for instant feedback
- **🎨 7 Powerful Features** - Complete coding learning ecosystem
- **🤖 Multi-Model Support** - Choose from 7+ AI models (CodeLlama, Mistral, LLaMA, DeepSeek, etc.)
- **💻 Cross-Platform** - Works on Windows, macOS, and Linux

---

## 🎯 Features

### **🔍 Tab 1: Analyze**
Real-time code analysis with AI-powered insights
- Line and character metrics
- Complexity analysis (Time/Space)
- Code quality scoring
- Identification of strengths & weaknesses
- Actionable improvement suggestions

### **🎯 Tab 2: Practice**
Learn by doing with AI-generated coding challenges
- 18 programming topics (Arrays, Trees, DP, Graphs, etc.)
- 3 difficulty levels (Easy, Medium, Hard)
- Timer-based challenges
- Code execution & test validation
- Hint system for guidance
- Reset and try again functionality

### **💬 Tab 3: Chat with Coach**
Interactive AI coding assistant
- Natural conversation interface
- Context-aware responses
- 6-message conversation history
- Quick question buttons
- Chat history persistence

### **💡 Tab 4: Hints**
Get guidance without spoiling the solution
- Import code from other tabs
- Ask specific questions
- Receive hints, not answers
- Socratic teaching approach

### **🛠️ Tab 5: Full Help**
Complete solutions and detailed explanations
- Fix bugs automatically
- Optimize code for performance
- Explain complex concepts
- Refactor code structure
- Code block formatting with syntax highlighting

### **⚖️ Tab 6: Compare**
Side-by-side code comparison & analysis
- Dual code editors
- Comparative performance analysis
- Best practices evaluation
- Recommendation system

### **📚 Tab 7: Reference**
Quick programming reference guide
- Big O complexity charts
- Data structures reference
- Algorithm templates
- Python tips & tricks
- Copy-paste code examples

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    STREAMLIT UI                         │
│              (Frontend Framework)                       │
├─────────────────────────────────────────────────────────┤
│     7 Interactive Tabs (Analyze, Practice, Chat, etc)  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│              PYTHON BACKEND                             │
│  • Session Management   • Code Execution                │
│  • Prompt Engineering   • Response Parsing              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│              OLLAMA AI ENGINE                           │
│  • Local AI Models      • Streaming API                 │
│  • CodeLlama, Mistral, LLaMA 3.2, DeepSeek, etc.      │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed locally
- At least one AI model pulled

### 1️⃣ Clone & Setup
```bash
git clone https://github.com/Qasim-dev2/AI-Code-Analyzer.git
cd "Api based ai code analyzer"
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2️⃣ Start Ollama
```bash
ollama serve
```

### 3️⃣ Pull a Model
```bash
ollama pull codellama:7b
```

### 4️⃣ Run the App
```bash
streamlit run main_app.py
```

App will open at: `http://localhost:8501`

---

## 📥 Installation

### Step 1: Install Ollama
- **Windows/macOS/Linux**: Download from [ollama.com](https://ollama.com/download)
- **Verify**: Run `ollama serve` in a terminal

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download AI Models
```bash
# Recommended primary model
ollama pull codellama:7b

# Optional models for comparison
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull deepseek-coder:6.7b
ollama pull qwen2.5-coder:7b
```

### Step 4: Launch Application
```bash
streamlit run main_app.py
```

---

## 📸 Screenshots

### Analyze Tab - Code Analysis
![Analyze Feature](public/Screenshot%202026-05-12%20183115.png)

### Practice Tab - Problem Generation
![Practice Feature](public/Screenshot%202026-05-12%20183144.png)

### Chat Tab - AI Coach
![Chat Feature](public/Screenshot%202026-05-12%20183202.png)

### Full Help Tab - Complete Solutions
![Help Feature](public/Screenshot%202026-05-12%20183933.png)

---

## 🛠️ Technology Stack

### **Frontend**
- **Streamlit** 1.28+ - Interactive Python web framework
- **Python** 3.8+ - Core application language

### **Backend**
- **Ollama** - Local AI model inference engine
- **Subprocess** - Isolated Python code execution
- **Streamlit Session State** - Cross-tab data persistence

### **AI Models**
| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| CodeLlama 7B | 3.8GB | General coding | Medium |
| CodeLlama 13B | 7.3GB | Complex problems | Slower |
| Mistral 7B | 4.1GB | Fast responses | Fast |
| LLaMA 3.2 3B | 2GB | Quick questions | Very Fast |
| DeepSeek Coder 6.7B | 3.8GB | Best coding | Medium |
| Qwen2.5 Coder 7B | 4.7GB | State-of-the-art | Medium |

---

## 📁 Project Structure

```
Api based ai code analyzer/
├── main_app.py                 # ⭐ Current main application
├── app.py                      # Legacy Gemini implementation
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── PROJECT_DOCUMENTATION.md    # Detailed documentation
│
├── backend/
│   ├── __init__.py
│   ├── ollama_client.py       # Ollama AI integration
│   ├── code_executor.py       # Safe Python code execution
│   ├── ai_analyzer.py         # Code analysis logic
│   └── ai_client.py           # Legacy AI client
│
├── config/
│   ├── __init__.py
│   └── settings.py            # App configuration & constants
│
├── prompts/
│   ├── __init__.py
│   ├── analyzer_prompts.py    # Code analysis prompts
│   ├── practice_prompts.py    # Problem generation prompts
│   └── coach_prompts.py       # Coaching prompts
│
├── utils/
│   ├── __init__.py
│   ├── session_manager.py     # State management
│   ├── sample_loader.py       # Sample code library
│   ├── report_generator.py    # Report formatting
│   ├── prompt_builder.py      # Prompt construction
│   └── coach_prompts.py       # Coach-specific prompts
│
└── public/
    ├── AI Code Analyzer Thumbnill.png
    └── Screenshot *.png       # Application screenshots
```

---

## 🔧 Main Components

### **main_app.py** (Current Entry Point)
- User interface with 7 tabs
- Prompt orchestration
- Session state management
- Streaming output rendering
- Response parsing (JSON extraction)

### **backend/ollama_client.py** (AI Bridge)
- Connects to local Ollama server
- Handles model listing
- Streams tokens in real-time
- Manages timeouts & errors

### **backend/code_executor.py** (Code Execution)
- Runs user code in isolated subprocess
- Captures stdout/stderr
- Enforces execution timeout (30 sec)
- Validates against test cases

### **config/settings.py** (Configuration)
- Application constants
- 18 programming topics
- Difficulty levels
- Sample code library

---

## 🔒 Security & Privacy

- **No Cloud Uploads**: All code stays locally
- **No API Keys**: No external dependencies
- **Offline Capable**: Works without internet
- **Subprocess Isolation**: Code runs safely in separate process
- **Timeout Protection**: 30-second execution limit
- **Error Handling**: Graceful failure management

---

## ⚡ Performance Optimizations

- **Caching**: Efficient module & data caching
- **Lazy Loading**: Load only what's needed
- **Streaming**: Token-by-token rendering
- **Session State**: Persistent data across tab switches

---

## 🎓 Use Cases

### 👨‍🎓 Students
- Practice data structures and algorithms
- Learn Python fundamentals
- Interview preparation

### 👨‍💼 Professionals
- Code review and optimization
- Quick reference lookup
- Learning new patterns

### 🧑‍🏫 Educators
- Supplement teaching materials
- Generate practice problems
- Provide personalized feedback

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 5-15GB for AI models
- **OS**: Windows 10/11, macOS, Linux
- **Internet**: Optional (only for initial model download)

---

## 🚦 Current Status

- ✅ **Active Development** - Maintained and updated
- ✅ **Production Ready** - Fully functional
- 📝 **Documentation** - Comprehensive
- 🧪 **Tested** - Regular usage validation

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Active runtime flows

### Code analysis flow

1. User pastes or loads code in the Analyze tab.
2. `main_app.py` builds an analysis prompt.
3. `get_client()` creates an `OllamaClient`.
4. The app streams tokens from Ollama.
5. `parse_json()` attempts to recover structured JSON from the model output.
6. Parsed results are saved in `st.session_state.analysis`.
7. `show_analysis()` renders quality, complexity, issues, strengths, and suggestions.

### Practice flow

1. User chooses topic and difficulty.
2. The app asks Ollama to generate a practice problem in JSON.
3. The result is stored in `st.session_state.practice_q`.
4. The user writes a solution in the editor.
5. `run_code()` or `run_tests()` calls `backend/code_executor.py`.
6. Execution results are stored in session state and rendered back in the tab.

### Chat / hints / full help flow

1. The user provides code or a question.
2. `main_app.py` selects the appropriate system prompt.
3. `stream_response()` renders the answer token by token.
4. For chat, the last messages are reused as conversational context.

### Compare flow

1. The user enters two versions of code.
2. The app builds a comparison prompt.
3. Ollama returns a streamed explanation of which version is better and why.

## Project structure

```text
Api based ai code analyzer/
|-- main_app.py
|-- app.py
|-- README.md
|-- PROJECT_DOCUMENTATION.md
|-- requirements.txt
|-- config.py
|-- backend/
|   |-- ollama_client.py
|   |-- code_executor.py
|   |-- ai_analyzer.py
|   `-- ai_client.py
|-- config/
|   |-- __init__.py
|   `-- settings.py
|-- prompts/
|   |-- analyzer_prompts.py
|   |-- practice_prompts.py
|   `-- coach_prompts.py
`-- utils/
    |-- session_manager.py
    |-- sample_loader.py
    |-- report_generator.py
    |-- prompt_builder.py
    `-- coach_prompts.py
```

## Which files matter most

- `main_app.py`: current UI, orchestration, active prompts, state
- `backend/ollama_client.py`: local LLM integration
- `backend/code_executor.py`: safe-ish subprocess execution
- `config/settings.py`: constants, topics, defaults
- `utils/sample_loader.py`: richer sample library used by the older app

## Active vs legacy files

The repository contains two generations of the product.

### Active local-Ollama path

- `main_app.py`
- `backend/ollama_client.py`
- `backend/code_executor.py`
- `config/settings.py`

This is the path supported by `requirements.txt`.

### Legacy Gemini path

- `app.py`
- `backend/ai_analyzer.py`
- `backend/ai_client.py`
- `utils/report_generator.py`
- `utils/prompt_builder.py`
- `prompts/*`
- `utils/coach_prompts.py`

Notes:

- `app.py` expects Google Gemini configuration
- `backend/ai_client.py` imports `google.generativeai`
- that dependency is not listed in the current `requirements.txt`
- several docs in the repo still describe this older architecture

## Setup

### Prerequisites

- Python 3.9+
- Ollama installed locally
- At least one local model, such as `codellama:7b`

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Start Ollama

```bash
ollama serve
```

### Pull a model

```bash
ollama pull codellama:7b
```

Optional models shown in the UI include:

- `codellama:13b`
- `llama3.2:3b`
- `llama3.2:1b`
- `mistral:7b`
- `deepseek-coder:6.7b`
- `qwen2.5-coder:7b`

### Run the app

```bash
streamlit run main_app.py
```

## Requirements file status

Current `requirements.txt` is enough for the active local app:

- `streamlit`
- `requests`
- `python-dotenv`

It is not enough for the legacy Gemini app, because `app.py` also needs Google Gemini SDK dependencies.

## Design observations

- The current app is intentionally compact and puts most orchestration in one file.
- The backend is thin and mostly focused on I/O boundaries: Ollama HTTP calls and subprocess execution.
- Prompt engineering is duplicated across generations of the app.
- The repo would be easier to maintain if the active prompt definitions and config were moved out of `main_app.py` into dedicated modules.

## Security notes

- User code is executed locally in a subprocess.
- Timeouts and output caps reduce risk, but this is not a secure sandbox.
- For untrusted code in a real production environment, use stronger isolation such as containers or VM-based execution.

## Suggested cleanup if you continue developing it

1. Remove or archive the legacy Gemini path if it is no longer needed.
2. Move active prompt strings out of `main_app.py` into `prompts/`.
3. Unify session state helpers so there is one state model.
4. Align documentation files so `README.md` stays authoritative.
5. Add tests around JSON parsing and code execution behavior.

## Summary

This project is best understood as a local AI coding workspace built around Streamlit, Ollama, and a lightweight Python execution layer. The active architecture is simple:

- `main_app.py` orchestrates the UI and workflows
- `backend/ollama_client.py` talks to the local model server
- `backend/code_executor.py` runs user code safely enough for local practice
- session state and caches hold everything together across reruns

If you are extending the project, start from `main_app.py` and treat the Gemini-based files as a previous generation unless you intend to revive that path.
 