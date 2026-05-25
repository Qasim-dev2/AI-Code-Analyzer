# 🤖 AI Code Analyzer

<div align="center">

### A Powerful Local-First AI Code Assistant Powered by Ollama

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Qasim--dev2%2FAI--Code--Analyzer-black.svg)](https://github.com/Qasim-dev2/AI-Code-Analyzer)

</div>

---

## 📋 Project Overview

**AI Code Analyzer** is an intelligent, local-first code analysis and learning platform powered by **Ollama AI**. It provides real-time code analysis, practice problem generation, interactive coaching, and comprehensive learning tools—**all running locally without requiring internet connectivity or API costs**.

Built with **Streamlit** for the UI and **Ollama** for local LLM inference, this tool combines code analysis, practice problem generation, coaching, hints, code execution, and side-by-side comparison in one powerful interface.

### ✨ Key Features

- **🎯 100% Local & Free** - No API costs, no cloud dependencies
- **🔒 Privacy-First** - All data stays on your machine  
- **⚡ Real-time AI** - Streaming responses for instant feedback
- **📚 7 Powerful Tabs** - Complete coding learning ecosystem
- **🤖 Multi-Model Support** - Choose from 7+ AI models
- **💻 Cross-Platform** - Windows, macOS, and Linux compatible

---

## 🎯 What You Can Do

### 🔍 **Analyze Code**
Paste any Python code and get instant AI-powered analysis:
- Complexity assessment (Time/Space)
- Code quality scoring
- Vulnerability detection
- Best practices recommendations
- Improvement suggestions

### 🎯 **Practice Problems**
Learn by solving AI-generated coding challenges:
- 18 programming topics
- 3 difficulty levels
- Timer-based challenges
- Real-time code execution
- Automated test validation

### 💬 **Chat with Coach**
Get help from an interactive AI assistant:
- Natural conversation interface
- Context-aware responses
- Quick reference questions
- Chat history persistence

### 💡 **Get Hints**
Learn without spoilers:
- Conceptual guidance
- Socratic teaching approach
- Step-by-step hints
- Encouraging feedback

### 🛠️ **Full Solutions**
Complete code assistance:
- Bug fixes
- Code optimization
- Concept explanations
- Refactoring suggestions

### ⚖️ **Compare Code**
Side-by-side analysis:
- Performance comparison
- Best practices evaluation
- Code quality assessment

### 📚 **Quick Reference**
Essential programming resources:
- Big O complexity charts
- Data structure reference
- Algorithm templates
- Python tips & tricks

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed ([download here](https://ollama.com/download))
- At least one AI model

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Qasim-dev2/AI-Code-Analyzer.git
cd "Api based ai code analyzer"

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Ollama (in another terminal)
ollama serve

# 5. Pull an AI model
ollama pull codellama:7b

# 6. Run the application
streamlit run main_app.py
```

App opens at: **http://localhost:8501**

---

## 🏗️ Architecture

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

## 📁 Project Structure

```
.
├── README.md                           # This file
├── Api based ai code analyzer/         # Main application folder
│   ├── main_app.py                    # ⭐ Current entry point
│   ├── requirements.txt               # Python dependencies
│   ├── PROJECT_DOCUMENTATION.md       # Detailed documentation
│   ├── backend/
│   │   ├── ollama_client.py          # Ollama AI integration
│   │   ├── code_executor.py          # Code execution engine
│   │   └── ...
│   ├── config/
│   │   └── settings.py               # Configuration
│   ├── prompts/
│   │   ├── analyzer_prompts.py
│   │   ├── practice_prompts.py
│   │   └── coach_prompts.py
│   ├── utils/
│   │   ├── session_manager.py
│   │   ├── sample_loader.py
│   │   └── ...
│   └── public/
│       └── Screenshots & images
└── .venv/                             # Virtual environment
```

---

## 🛠️ Technology Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Core language | 3.8+ |
| **Streamlit** | Web UI framework | 1.28.0+ |
| **Ollama** | Local AI inference | Latest |
| **CodeLlama** | Primary AI model | 7B/13B |

### Supported AI Models

- **CodeLlama 7B** - Best for general coding (recommended)
- **CodeLlama 13B** - Advanced coding tasks
- **Mistral 7B** - Fast, all-purpose
- **LLaMA 3.2 3B** - Quick responses
- **DeepSeek Coder 6.7B** - Best for complex code
- **Qwen2.5 Coder 7B** - State-of-the-art

---

## 📋 System Requirements

- **OS**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5-15GB for AI models
- **Internet**: Required for initial setup, works offline after

---

## 🔒 Security & Privacy

✅ **100% Local** - No data sent to cloud  
✅ **No API Keys** - No external service dependencies  
✅ **Offline Ready** - Works without internet  
✅ **Code Safety** - Sandboxed subprocess execution  
✅ **GDPR Compliant** - Full data privacy

---

## 🎓 Use Cases

👨‍🎓 **Students**
- Practice data structures & algorithms
- Learn Python fundamentals
- Prepare for technical interviews

👨‍💼 **Professionals**
- Code review & optimization
- Quick reference lookup
- Learn new patterns & best practices

🧑‍🏫 **Educators**
- Generate practice problems
- Provide personalized feedback
- Supplement teaching materials

---

## 📚 Documentation

For **detailed documentation**, including:
- Complete feature guide
- Advanced configuration
- Contributing guidelines
- Troubleshooting

See: [`Api based ai code analyzer/README.md`](Api%20based%20ai%20code%20analyzer/README.md)

---

## 🚀 Getting Started

1. **Setup**: Follow the [Quick Start](#-quick-start) section above
2. **Launch**: Run `streamlit run main_app.py`
3. **Choose Model**: Select an AI model from the sidebar
4. **Start Analyzing**: Pick a tab and begin!

---

## 📝 License

MIT License - feel free to use this project freely

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit pull requests
- Report bugs and issues
- Suggest new features
- Improve documentation

---

## 👨‍💻 Author

**Qasim-dev2** | [GitHub Profile](https://github.com/Qasim-dev2)

---

<div align="center">

**⭐ If you find this project helpful, please give it a star on GitHub!**

[View on GitHub](https://github.com/Qasim-dev2/AI-Code-Analyzer) | [Report Issues](https://github.com/Qasim-dev2/AI-Code-Analyzer/issues)

</div> 
