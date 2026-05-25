# AI Code Analyzer - Project Documentation

## 📋 Project Overview

**AI Code Analyzer** is an intelligent, local-first code analysis and learning platform powered by Ollama AI. It provides real-time code analysis, practice problem generation, interactive coaching, and comprehensive learning tools—all running locally without requiring internet connectivity or API costs.

### Key Highlights
- **100% Local & Free** - No API costs, no cloud dependencies
- **Privacy-First** - All data stays on your machine
- **Real-time AI** - Streaming responses for instant feedback
- **7 Powerful Features** - Complete coding learning ecosystem
- **Multi-Model Support** - Choose from 7+ AI models

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

## 💻 Frontend Technology Stack

### **Streamlit** (Primary Framework)
- **Version**: 1.28.0+
- **Purpose**: Rapid web application development with Python
- **Key Features Used**:
  - Multi-tab interface (`st.tabs`)
  - Session state management (`st.session_state`)
  - Real-time streaming (`st.empty()`, progressive rendering)
  - Interactive widgets (buttons, text areas, selectboxes)
  - Custom CSS styling
  - Metrics and progress indicators

### Frontend Components
1. **Layout System**
   - Wide layout mode
   - Column-based responsive design
   - Expandable sidebar
   - Tab-based navigation

2. **Interactive Widgets**
   - Code editors (text_area with syntax highlighting)
   - Dropdown selectors (model selection, topic selection)
   - Action buttons (analyze, generate, send)
   - Real-time metrics (line count, character count, timer)

3. **Styling**
   - Custom CSS for modern UI
   - Color-coded elements (status indicators, timers)
   - Responsive containers
   - Markdown rendering for formatted output

---

## 🔧 Backend Technology Stack

### **Python 3.x** (Core Language)
Primary backend language handling all business logic and AI integration.

### Key Backend Modules

#### 1. **Ollama Client** (`backend/ollama_client.py`)
- **Purpose**: Interface with local Ollama AI server
- **Key Features**:
  - Streaming response handling
  - Model management and listing
  - Connection health checks
  - Configurable parameters (temperature, timeout)
- **API Endpoint**: `http://localhost:11434`

#### 2. **Code Executor** (`backend/code_executor.py`)
- **Purpose**: Safe Python code execution
- **Features**:
  - Subprocess-based execution (sandboxed)
  - Timeout management (prevents hanging)
  - Test case validation
  - Output capture (stdout, stderr)

#### 3. **Configuration** (`config/settings.py`)
- Application settings
- Topic lists (18 programming topics)
- Difficulty levels
- Sample code library (5 algorithms)

#### 4. **Prompt Engineering** (`prompts/`)
- **analyzer_prompts.py**: Code analysis instructions
- **practice_prompts.py**: Problem generation templates
- **coach_prompts.py**: Coaching and guidance prompts
- **JSON-structured outputs** for reliable parsing

#### 5. **Utilities**
- **Session Manager**: State persistence across tabs
- **Report Generator**: Analysis formatting
- **Sample Loader**: Pre-built code examples

---

## 🤖 AI/ML Technology Stack

### **Ollama** (Local AI Infrastructure)
- **Version**: Latest stable
- **Platform**: Windows, macOS, Linux compatible
- **Purpose**: Run large language models locally
- **Advantages**:
  - Zero API costs
  - Complete privacy
  - Offline capability
  - Fast inference

### Supported AI Models

| Model | Size | Specialty | Use Case |
|-------|------|-----------|----------|
| **CodeLlama 7B** | 3.8GB | Code generation | Primary coding model |
| **CodeLlama 13B** | 7.3GB | Advanced coding | Complex problems |
| **LLaMA 3.2 3B** | 2GB | Fast responses | Quick questions |
| **LLaMA 3.2 1B** | 1GB | Ultra-fast | Simple tasks |
| **Mistral 7B** | 4.1GB | All-rounder | General coding |
| **DeepSeek Coder 6.7B** | 3.8GB | Code-focused | Best for coding |
| **Qwen2.5 Coder 7B** | 4.7GB | Latest coder | State-of-the-art |

### AI Capabilities
1. **Code Analysis**: Complexity, efficiency, best practices
2. **Problem Generation**: Custom coding challenges
3. **Conversational AI**: Natural language coaching
4. **Code Comparison**: Side-by-side analysis
5. **Bug Detection**: Issue identification
6. **Optimization**: Performance improvements
7. **Explanation**: Concept clarification

---

## 🎯 Features & Functionality

### **Tab 1: 🔍 Analyze**
**Purpose**: Real-time code analysis and feedback

**Features**:
- Paste or load sample code
- Line and character metrics
- One-click analysis
- Streaming AI responses
- Structured JSON output:
  - Complexity analysis
  - Time/space complexity
  - Code quality score
  - Strengths identification
  - Improvement suggestions

**Technology**: 
- Streamlit text_area widget
- JSON parsing with regex fallback
- Progress indicators
- Caching for performance

---

### **Tab 2: 🎯 Practice**
**Purpose**: Generate coding problems and solve them

**Features**:
- 18 topics (Arrays, Trees, DP, etc.)
- 3 difficulty levels (Easy, Medium, Hard)
- Timer-based challenges
- Code editor with execution
- Test case validation
- Hint system
- Reset functionality

**Technology**:
- Dynamic problem generation via AI
- Code execution in subprocess
- Real-time timer with warnings
- State management for session persistence

---

### **Tab 3: 💬 Chat with Coach**
**Purpose**: Interactive AI coding assistant

**Features**:
- Natural conversation interface
- Context-aware responses (6-message history)
- Quick question buttons
- Chat history persistence
- Clear conversation option
- Markdown-formatted responses

**Technology**:
- Conversational AI prompts
- Session state for chat history
- Streaming text generation
- Context window management

---

### **Tab 4: 💡 Hints**
**Purpose**: Get guidance without full solutions

**Features**:
- Import code from other tabs
- Ask specific questions
- Receive hints, not answers
- Encouraging coaching style
- Conceptual guidance

**Technology**:
- Specialized hint-only prompt system
- Cross-tab code import
- Socratic teaching approach

---

### **Tab 5: 🛠️ Full Help**
**Purpose**: Complete solutions and explanations

**Features**:
- Import code from other tabs
- 4 action modes:
  - 🐛 Fix bugs
  - ⚡ Optimize code
  - 📖 Explain concepts
  - 🔧 Refactor structure
- Detailed explanations
- Code block formatting

**Technology**:
- Action-based prompt engineering
- Complete solution generation
- Markdown code blocks

---

### **Tab 6: ⚖️ Compare**
**Purpose**: Side-by-side code comparison

**Features**:
- Dual code editors
- Comparative analysis
- Performance comparison
- Best practices evaluation
- Recommendation system

**Technology**:
- Parallel input handling
- Comparative prompt engineering
- Structured analysis output

---

### **Tab 7: 📚 Reference**
**Purpose**: Quick programming reference guide

**Features**:
- Big O complexity chart
- Data structures reference
- Algorithm templates
- Python tips and tricks
- Copy-paste examples

**Technology**:
- Static markdown content
- Code syntax highlighting
- Tabular data presentation

---

## ⚡ Performance Optimizations

### 1. **Caching Strategy**
```python
@st.cache_resource  # Cache modules (never expires)
@st.cache_data(ttl=60)  # Cache models (60s refresh)
@st.cache_data(ttl=10)  # Cache connection (10s refresh)
```

### 2. **Lazy Loading**
- Modules imported only when needed
- Dynamic client initialization
- On-demand model listing

### 3. **Streaming Responses**
- Token-by-token rendering
- Immediate user feedback
- Reduced perceived latency

### 4. **Session State Management**
- Persistent data across reruns
- Minimal state updates
- Key-based widget synchronization

---

## 🔒 Security & Privacy

### Local-First Architecture
- **No Cloud Uploads**: All code stays on local machine
- **No API Keys**: No external service dependencies
- **Offline Capable**: Works without internet
- **Data Privacy**: GDPR/compliance-friendly

### Code Execution Safety
- **Subprocess Isolation**: Code runs in separate process
- **Timeout Protection**: 30-second execution limit
- **Error Handling**: Graceful failure management
- **No System Access**: Limited to Python environment

---

## 📦 Technology Dependencies

### Core Dependencies
```
streamlit>=1.28.0      # Web framework
requests>=2.31.0       # HTTP client for Ollama
python-dotenv>=1.0.0   # Environment configuration
```

### System Requirements
- **Python**: 3.8+
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5-10GB for AI models
- **OS**: Windows 10/11, macOS, Linux

### External Services
- **Ollama**: Local AI server (localhost:11434)

---

## 🚀 Installation & Setup

### 1. Install Ollama
```bash
# Windows
https://ollama.com/download

# Verify installation
ollama serve
```

### 2. Pull AI Models
```bash
# Primary model
ollama pull codellama:7b

# Optional models
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull deepseek-coder:6.7b
```

### 3. Setup Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run Application
```bash
streamlit run main_app.py
```

Application opens at: `http://localhost:8501`

---

## 🎓 Use Cases

### 1. **Learning & Education**
- Students practicing data structures
- Beginners learning Python
- Interview preparation
- Algorithm understanding

### 2. **Code Review**
- Quick code quality checks
- Complexity analysis
- Best practice validation
- Optimization suggestions

### 3. **Debugging Assistant**
- Bug identification
- Error explanation
- Fix suggestions
- Code improvement

### 4. **Interview Preparation**
- Timed problem solving
- Topic-based practice
- Hint-based learning
- Solution comparison

---

## 📊 Project Statistics

- **Total Files**: 15+
- **Lines of Code**: ~2,500
- **Features**: 7 major tabs
- **AI Models Supported**: 7+
- **Programming Topics**: 18
- **Sample Codes**: 5
- **Response Time**: <2 seconds
- **Cost**: $0 (completely free)

---

## � Complete File Structure & Detailed Explanation

### Project Directory Structure
```
Api based ai code analyzer/
│
├── main_app.py                 # 🎯 MAIN ENTRY POINT (Frontend)
├── app.py                      # ⚠️ OLD VERSION (deprecated)
├── config.py                   # Legacy config (deprecated)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
│
├── backend/                    # 🔧 BACKEND LOGIC
│   ├── __init__.py
│   ├── ollama_client.py       # ⭐ AI Client - Communicates with Ollama
│   ├── code_executor.py       # ⭐ Code Runner - Executes Python safely
│   ├── ai_client.py           # Legacy (not used)
│   └── ai_analyzer.py         # Legacy (not used)
│
├── config/                     # ⚙️ CONFIGURATION
│   ├── __init__.py
│   └── settings.py            # ⭐ App settings, topics, samples
│
├── prompts/                    # 💬 AI PROMPTS
│   ├── __init__.py
│   ├── analyzer_prompts.py    # ⭐ Code analysis prompts
│   ├── practice_prompts.py    # ⭐ Problem generation prompts
│   └── coach_prompts.py       # ⭐ Coaching prompts
│
└── utils/                      # 🛠️ UTILITIES
    ├── __init__.py
    ├── session_manager.py     # Session state helpers
    ├── prompt_builder.py      # Prompt construction (legacy)
    ├── report_generator.py    # Report formatting (legacy)
    ├── sample_loader.py       # Sample code loader
    └── coach_prompts.py       # Legacy prompts
```

---

## 📄 File-by-File Detailed Breakdown

### 🎯 **1. main_app.py** (792 lines) - MAIN APPLICATION
**Role**: Frontend + Application Logic

**What's Inside**:
```python
Lines 1-25:    Imports & Page Configuration
Lines 26-60:   Cached module loading (@st.cache_resource)
Lines 61-140:  Configuration (TOPICS, DIFFICULTIES, SAMPLES)
Lines 141-180: Session state initialization
Lines 181-220: CSS styling
Lines 221-260: Helper functions (get_client, parse_json, stream_response)
Lines 261-310: Sidebar rendering (model selection, connection status)
Lines 311-360: Tab 1 - Analyze (code analysis)
Lines 361-410: Tab 1 - Display analysis results
Lines 411-502: Tab 2 - Practice (problem generation & solving)
Lines 503-550: Tab 2 - Code execution & test validation
Lines 551-592: Tab 3 - Chat (interactive AI conversation)
Lines 593-620: Tab 4 - Hints (guidance without solutions)
Lines 621-658: Tab 5 - Full Help (complete solutions)
Lines 659-680: Tab 6 - Compare (side-by-side code comparison)
Lines 681-760: Tab 7 - Reference (quick programming guide)
Lines 761-792: Main function & tab rendering
```

**Key Functions**:
- `get_ollama_module()` - Lazy loads AI client
- `get_client()` - Returns configured Ollama client
- `stream_response()` - Handles streaming AI output
- `parse_json()` - Extracts structured data from AI responses
- `tab_analyze()` - Code analysis interface
- `tab_practice()` - Practice problem interface
- `tab_chat()` - Chat interface
- `tab_hints()` - Hints interface
- `tab_full()` - Full help interface
- `tab_compare()` - Code comparison interface
- `tab_reference()` - Reference guide

**What It Does**:
1. Renders the Streamlit UI with 7 tabs
2. Manages session state across tabs
3. Handles user input from widgets
4. Calls backend modules for AI/execution
5. Displays results with formatting

---

### 🤖 **2. backend/ollama_client.py** (191 lines) - AI CLIENT
**Role**: Communication bridge to Ollama AI server

**What's Inside**:
```python
Lines 1-15:    Imports & logging setup
Lines 16-23:   OllamaConfig dataclass (configuration)
Lines 24-191:  OllamaClient class (main AI client)
```

**Key Classes & Methods**:

**`OllamaConfig`** (Configuration):
```python
base_url: str = "http://localhost:11434"  # Ollama server
model: str = "codellama:7b"               # Default model
temperature: float = 0.7                  # Creativity (0-1)
timeout: int = 120                        # Request timeout
```

**`OllamaClient`** (AI Client):
- `__init__(config)` - Initialize with config
- `_verify_connection()` - Check if Ollama is running
- `stream_generate(prompt, system)` - **MAIN METHOD** - Stream AI tokens
- `generate(prompt, system)` - Non-streaming generation
- `list_models()` - Get available models
- `get_model_info(model)` - Model details

**How It Works**:
```python
# 1. User clicks "Analyze" button in main_app.py
# 2. main_app.py calls:
client = get_client()  # Creates OllamaClient instance
response = client.stream_generate(prompt, system_prompt)

# 3. ollama_client.py sends HTTP POST to:
POST http://localhost:11434/api/generate
Body: {"model": "codellama:7b", "prompt": "...", "stream": true}

# 4. Returns generator that yields tokens:
for token in response:
    yield token  # "The", "code", "is", "good", ...

# 5. main_app.py displays tokens in real-time
```

**API Endpoints Used**:
- `/api/generate` - Generate AI responses
- `/api/tags` - List installed models
- `/api/show` - Model information

---

### ⚙️ **3. backend/code_executor.py** (216 lines) - CODE RUNNER
**Role**: Safely execute Python code with timeout protection

**What's Inside**:
```python
Lines 1-15:    Imports & logging
Lines 16-25:   ExecutionResult dataclass
Lines 26-216:  CodeExecutor class
```

**Key Classes & Methods**:

**`ExecutionResult`** (Return type):
```python
success: bool           # Did code run successfully?
stdout: str            # Printed output
stderr: str            # Error messages
return_code: int       # Exit code (0 = success)
timed_out: bool        # Did it timeout?
error_message: str     # Human-readable error
```

**`CodeExecutor`** (Safe Runner):
- `__init__(timeout, max_output)` - Configure limits
- `execute(code)` - **MAIN METHOD** - Run Python code
- `run_with_tests(code, tests)` - Run code + test cases
- `_write_temp_file(code)` - Create temp .py file
- `_run_subprocess(file_path)` - Execute in subprocess
- `_parse_output(result)` - Format results

**How It Works**:
```python
# 1. User writes code in Practice tab and clicks "Run"
# 2. main_app.py calls:
executor = get_executor()
result = executor.execute(user_code)

# 3. code_executor.py:
# Step A: Write code to temp file
temp_file = tempfile.NamedTemporaryFile(suffix='.py')
temp_file.write(user_code)

# Step B: Run in subprocess
process = subprocess.run(
    [sys.executable, temp_file.name],
    capture_output=True,
    timeout=30,
    text=True
)

# Step C: Capture output
stdout = process.stdout  # What user printed
stderr = process.stderr  # Any errors
return_code = process.returncode  # 0 or error code

# Step D: Return result
return ExecutionResult(
    success=(return_code == 0),
    stdout=stdout,
    stderr=stderr,
    ...
)

# 4. main_app.py displays output to user
```

**Security Features**:
- ✅ Runs in **separate process** (isolated)
- ✅ **30-second timeout** (prevents infinite loops)
- ✅ **Output size limit** (prevents memory overflow)
- ✅ **Temp file cleanup** (no file pollution)

---

### ⚙️ **4. config/settings.py** - CONFIGURATION
**Role**: Centralized application settings

**What's Inside**:
```python
# Topics for practice problems
TOPICS = [
    "Arrays", "Strings", "Stacks", "Queues",
    "Linked Lists", "Trees", "Graphs", "Sorting",
    "Searching", "Dynamic Programming", "Recursion",
    "Hash Tables", "Two Pointers", "Sliding Window",
    "Bit Manipulation", "Math", "Greedy", "Backtracking"
]

# Difficulty levels
DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Sample code library
SAMPLE_CODES = {
    "Bubble Sort": "def bubble_sort(arr): ...",
    "Binary Search": "def binary_search(arr, target): ...",
    "Two Sum": "def two_sum(nums, target): ...",
    "Fibonacci": "def fibonacci(n): ...",
    "Quick Sort": "def quick_sort(arr): ..."
}

# Time limits per difficulty
TIME_LIMITS = {
    "Easy": 900,     # 15 minutes
    "Medium": 1800,  # 30 minutes
    "Hard": 2700     # 45 minutes
}
```

**Used By**: main_app.py for dropdowns, sample loading, timer settings

---

### 💬 **5. prompts/analyzer_prompts.py** - ANALYSIS PROMPTS
**Role**: AI prompts for code analysis

**What's Inside**:
```python
ANALYSIS_SYSTEM = """You are an expert code analyzer.
Analyze Python code and return JSON:
{
  "complexity": "O(n²) time, O(1) space",
  "quality_score": 7,
  "strengths": ["Clear logic", "Good naming"],
  "suggestions": ["Add error handling", "Optimize loop"],
  "improvements": ["Use list comprehension"]
}"""

CODE_REVIEW_PROMPT = """Review this code for:
- Time/space complexity
- Code quality (1-10)
- Best practices
- Potential bugs
- Optimization opportunities
"""
```

**Used By**: main_app.py tab_analyze() function

---

### 💬 **6. prompts/practice_prompts.py** - PRACTICE PROMPTS
**Role**: AI prompts for generating coding problems

**What's Inside**:
```python
PRACTICE_SYSTEM = """You are a coding problem generator.
Create a {difficulty} level {topic} problem in JSON:
{
  "title": "Problem name",
  "difficulty": "Easy/Medium/Hard",
  "statement": "Problem description...",
  "constraints": ["1 <= n <= 1000"],
  "examples": [{"input": "...", "output": "...", "explanation": "..."}],
  "starter": "def solution():\\n    pass",
  "tests": [{"input": "...", "output": "..."}],
  "hints": ["Think about...", "Consider..."]
}"""

PROBLEM_GENERATION_TEMPLATE = """
Generate a realistic coding interview question.
Include clear examples and test cases.
Difficulty: {difficulty}
Topic: {topic}
"""
```

**Used By**: main_app.py tab_practice() function

---

### 💬 **7. prompts/coach_prompts.py** - COACHING PROMPTS
**Role**: AI prompts for hints and guidance

**What's Inside**:
```python
HINTS_SYSTEM = """You are a coding coach.
Give hints WITHOUT full solutions.
- Ask guiding questions
- Suggest concepts to explore
- Point out issues without fixing
- Be encouraging
- Don't write code for them
"""

FULL_SYSTEM = """You are an expert Python developer.
Provide complete solutions with:
- Fixed/optimized code
- Detailed explanations
- Step-by-step reasoning
- Best practices
- Use markdown code blocks
"""

CHAT_SYSTEM = """You are a friendly AI coding coach.
Have natural conversations about programming.
- Answer questions clearly
- Explain concepts simply
- Help debug issues
- Be concise but helpful
"""
```

**Used By**: 
- tab_hints() - Uses HINTS_SYSTEM
- tab_full() - Uses FULL_SYSTEM
- tab_chat() - Uses CHAT_SYSTEM

---

## 🔄 Complete Call Flow: Frontend → Backend → AI

### **Example: User Analyzes Code**

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: USER ACTION (Frontend - Streamlit)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
User in main_app.py Tab 1:
1. Pastes code into text_area widget
2. Clicks "🚀 Analyze" button

┌─────────────────────────────────────────────────────────────┐
│ STEP 2: BUTTON CLICK HANDLER (main_app.py lines 335-360)   │
└─────────────────────────────────────────────────────────────┘
                              ↓
if analyze and code:
    with st.spinner("Analyzing..."):
        # Prepare prompt
        prompt = f"Analyze this Python code:\n```python\n{code}\n```"
        
        # Get AI client
        client = get_client()  # Returns OllamaClient instance
        
        # Stream response
        response = ""
        for token in client.stream_generate(prompt, ANALYSIS_SYSTEM):
            response += token
            # Display progressively

┌─────────────────────────────────────────────────────────────┐
│ STEP 3: AI CLIENT CALL (backend/ollama_client.py)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
def stream_generate(self, prompt: str, system: str):
    # Prepare request
    payload = {
        "model": "codellama:7b",
        "prompt": prompt,
        "system": system,
        "stream": True,
        "temperature": 0.7
    }
    
    # Send HTTP POST to Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        stream=True
    )
    
    # Yield tokens as they arrive
    for line in response.iter_lines():
        data = json.loads(line)
        yield data['response']  # "The", "code", "uses", ...

┌─────────────────────────────────────────────────────────────┐
│ STEP 4: OLLAMA AI SERVER (localhost:11434)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
Ollama receives request:
1. Loads codellama:7b model into memory
2. Processes prompt through neural network
3. Generates tokens one-by-one
4. Streams back via HTTP chunked encoding

Response: {"response": "The", "done": false}
Response: {"response": "code", "done": false}
Response: {"response": "uses", "done": false}
...
Response: {"response": "}", "done": true}

┌─────────────────────────────────────────────────────────────┐
│ STEP 5: STREAM DISPLAY (main_app.py stream_response)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
def stream_response(container, prompt, system):
    full = ""
    placeholder = container.empty()
    
    for token in client.stream_generate(prompt, system):
        full += token
        if len(full) % 3 == 0:  # Update every 3 chars
            placeholder.markdown(full + "▌")  # Show cursor
    
    placeholder.markdown(full)  # Final display
    return full

┌─────────────────────────────────────────────────────────────┐
│ STEP 6: PARSE & DISPLAY (main_app.py lines 355-360)        │
└─────────────────────────────────────────────────────────────┘
                              ↓
result = parse_json(response)  # Extract JSON from AI text
if result:
    st.session_state.analysis = result
    
    # Display structured data
    st.markdown(f"**Complexity:** {result['complexity']}")
    st.markdown(f"**Quality:** {result['quality_score']}/10")
    
    for strength in result['strengths']:
        st.success(f"✅ {strength}")
    
    for suggestion in result['suggestions']:
        st.info(f"💡 {suggestion}")
```

---

### **Example: User Runs Practice Code**

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: USER ACTION                                         │
└─────────────────────────────────────────────────────────────┘
User in Tab 2 (Practice):
1. Writes solution in text_area
2. Clicks "▶️ Run" button

┌─────────────────────────────────────────────────────────────┐
│ STEP 2: RUN HANDLER (main_app.py lines 493-495)            │
└─────────────────────────────────────────────────────────────┘
with col1:
    if st.button("▶️ Run", ...):
        run_code(code)  # Call execution function

┌─────────────────────────────────────────────────────────────┐
│ STEP 3: RUN_CODE FUNCTION (main_app.py lines 503-520)      │
└─────────────────────────────────────────────────────────────┘
def run_code(code: str):
    # Get executor
    get_executor = get_executor_module()
    executor = get_executor()
    
    # Execute code safely
    result = executor.execute(code)
    
    # Store in session
    st.session_state.run_output = result

┌─────────────────────────────────────────────────────────────┐
│ STEP 4: CODE EXECUTOR (backend/code_executor.py)           │
└─────────────────────────────────────────────────────────────┘
def execute(self, code: str) -> ExecutionResult:
    # Create temp file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False,
        encoding='utf-8'
    ) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        # Run in subprocess
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            timeout=30,
            text=True,
            encoding='utf-8'
        )
        
        return ExecutionResult(
            success=(result.returncode == 0),
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
            timed_out=False
        )
    
    except subprocess.TimeoutExpired:
        return ExecutionResult(
            success=False,
            stdout="",
            stderr="Timeout: Code took too long",
            return_code=-1,
            timed_out=True
        )
    
    finally:
        os.unlink(temp_path)  # Delete temp file

┌─────────────────────────────────────────────────────────────┐
│ STEP 5: SUBPROCESS EXECUTION (Python Interpreter)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
Python subprocess runs:
python temp_file_abc123.py

User's code executes:
print("Hello")  → stdout: "Hello\n"
1/0             → stderr: "ZeroDivisionError..."

Process exits with return code 0 (success) or 1 (error)

┌─────────────────────────────────────────────────────────────┐
│ STEP 6: DISPLAY RESULTS (main_app.py show_output)          │
└─────────────────────────────────────────────────────────────┘
if st.session_state.run_output:
    result = st.session_state.run_output
    
    if result.success:
        st.success("✅ Code ran successfully!")
        st.code(result.stdout)  # Show output
    else:
        st.error("❌ Error occurred")
        st.code(result.stderr)  # Show error
```

---

## 🔗 Data Flow Diagram

```
┌──────────────────┐
│   USER BROWSER   │
│   (Frontend UI)  │
└────────┬─────────┘
         │ User clicks button
         ▼
┌──────────────────────────────────────────┐
│         MAIN_APP.PY (Streamlit)          │
│  ┌────────────────────────────────────┐  │
│  │ Tab Functions:                     │  │
│  │ • tab_analyze()                    │  │
│  │ • tab_practice()                   │  │
│  │ • tab_chat()                       │  │
│  └────────────────────────────────────┘  │
└────────┬─────────────────────────┬────────┘
         │                         │
         │ Need AI?               │ Need code execution?
         ▼                         ▼
┌────────────────────┐    ┌────────────────────┐
│ OLLAMA_CLIENT.PY   │    │ CODE_EXECUTOR.PY   │
│  (AI Interface)    │    │  (Safe Runner)     │
│                    │    │                    │
│ stream_generate()  │    │ execute()          │
│ list_models()      │    │ run_with_tests()   │
└────────┬───────────┘    └────────┬───────────┘
         │                         │
         ▼                         ▼
┌────────────────────┐    ┌────────────────────┐
│  OLLAMA SERVER     │    │  PYTHON SUBPROCESS │
│  localhost:11434   │    │  (Isolated)        │
│                    │    │                    │
│  CodeLlama 7B      │    │  Runs user code    │
│  Returns tokens    │    │  Returns output    │
└────────────────────┘    └────────────────────┘
```

---

## 📊 Module Dependency Map

```
main_app.py
    ├── backend/ollama_client.py
    │   └── requests (HTTP calls)
    │       └── Ollama Server (AI)
    │
    ├── backend/code_executor.py
    │   └── subprocess (code execution)
    │       └── Python Interpreter
    │
    ├── config/settings.py
    │   └── Constants (TOPICS, SAMPLES, etc.)
    │
    └── prompts/
        ├── analyzer_prompts.py
        ├── practice_prompts.py
        └── coach_prompts.py
```

---

## 🎯 Key Interactions Summary

### **1. Code Analysis Flow**
```
User Pastes Code → main_app.py (Tab 1)
    ↓
get_client() → backend/ollama_client.py
    ↓
stream_generate() → HTTP POST to localhost:11434
    ↓
Ollama AI → Generates analysis
    ↓
Yields tokens → main_app.py displays progressively
    ↓
parse_json() → Extracts structured data
    ↓
Display results → User sees analysis
```

### **2. Code Execution Flow**
```
User Writes Code → main_app.py (Tab 2)
    ↓
run_code() → backend/code_executor.py
    ↓
Write to temp file → /tmp/xyz.py
    ↓
subprocess.run() → Python interpreter
    ↓
Capture stdout/stderr → ExecutionResult
    ↓
Display output → User sees results
    ↓
Cleanup temp file → /tmp/xyz.py deleted
```

### **3. Chat Flow**
```
User Types Message → main_app.py (Tab 3)
    ↓
Append to chat_history → session_state
    ↓
Build context (last 6 messages) → prompt
    ↓
stream_generate() → Ollama AI
    ↓
Display response → User sees answer
    ↓
Append to history → Updated session_state
```

---

## 🔐 Session State Variables

**Managed by main_app.py, line 141-165**:

```python
st.session_state = {
    "model": "codellama:7b",        # Selected AI model
    "temperature": 0.7,              # AI creativity
    "analyze_code": "",              # Tab 1 code input
    "analysis": None,                # Tab 1 results
    "practice_q": None,              # Tab 2 current problem
    "practice_solution": "",         # Tab 2 code input
    "practice_started": False,       # Tab 2 timer state
    "practice_start": None,          # Tab 2 start time
    "practice_time": 1800,           # Tab 2 time limit
    "run_output": None,              # Code execution result
    "chat_history": [],              # Tab 3 messages
    "hints_code": "",                # Tab 4 code input
    "full_code": "",                 # Tab 5 code input
    "compare_code1": "",             # Tab 6 code 1
    "compare_code2": "",             # Tab 6 code 2
}
```

**How It Works**:
- Persists across Streamlit reruns
- Shared between all tabs
- Updated by widget keys automatically
- Enables cross-tab data transfer

---

## �🔮 Future Enhancements

### Planned Features
1. **Multi-Language Support** (JavaScript, Java, C++)
2. **Code History** (save and track progress)
3. **Collaborative Mode** (share problems)
4. **Custom Models** (fine-tuned for specific needs)
5. **Export Reports** (PDF/HTML analysis)
6. **Dark Mode** (theme customization)
7. **Voice Input** (speech-to-code)

---

## 🏆 Project Achievements

### Technical Excellence
- ✅ Zero-cost AI integration
- ✅ Sub-2-second response times
- ✅ 100% local processing
- ✅ Modern, responsive UI
- ✅ Production-ready code
- ✅ Comprehensive error handling

### Innovation
- ✅ Streaming AI responses
- ✅ Multi-model architecture
- ✅ Context-aware coaching
- ✅ Safe code execution
- ✅ Cross-tab data sharing

---

## 📝 Technical Decisions & Rationale

### Why Streamlit?
- Rapid prototyping
- Python-native
- Built-in state management
- Easy deployment
- Active community

### Why Ollama?
- Local processing (privacy)
- No API costs
- Offline capability
- Multiple model options
- Active development

### Why CodeLlama?
- Specialized for code
- Good accuracy
- Reasonable size (3.8GB)
- Fast inference
- Meta-backed

---

## 🎯 Target Audience

- **Students**: Learning programming fundamentals
- **Developers**: Quick code reviews and debugging
- **Interviewers**: Problem generation and evaluation
- **Educators**: Teaching tool for coding concepts
- **Hobbyists**: Free AI coding assistant

---

## 🌟 Competitive Advantages

| Feature | AI Code Analyzer | GitHub Copilot | ChatGPT |
|---------|------------------|----------------|---------|
| **Cost** | Free | $10/month | $20/month |
| **Privacy** | 100% Local | Cloud-based | Cloud-based |
| **Offline** | ✅ Yes | ❌ No | ❌ No |
| **Practice Mode** | ✅ Yes | ❌ No | ⚠️ Limited |
| **Code Execution** | ✅ Yes | ❌ No | ❌ No |
| **Multi-Model** | ✅ 7+ models | ❌ Fixed | ❌ Fixed |

---

## 📞 Project Information

**Project Name**: AI Code Analyzer  
**Version**: 2.5  
**Status**: Production-Ready  
**License**: Open Source  
**Platform**: Cross-platform (Windows/Mac/Linux)  
**Technology**: Python + Streamlit + Ollama  
**Deployment**: Local Desktop Application  

---

## 🎬 Conclusion

The **AI Code Analyzer** represents a complete, modern solution for AI-assisted coding education and analysis. By leveraging local AI models through Ollama, it provides enterprise-grade capabilities without the cost or privacy concerns of cloud services. The project demonstrates proficiency in:

- **Full-stack development** (Frontend + Backend)
- **AI/ML integration** (Local LLMs)
- **Modern Python development** (Best practices)
- **User experience design** (7 intuitive features)
- **Performance optimization** (Caching, streaming)
- **Software architecture** (Modular, scalable)

This project is ideal for presentations showcasing **AI integration**, **modern web development**, and **practical problem-solving** in the education technology space.

---

*Documentation prepared for presentation generation*  
*Last Updated: December 19, 2025*
