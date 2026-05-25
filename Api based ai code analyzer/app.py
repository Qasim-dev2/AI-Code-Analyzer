"""
AI Code Analyzer - Streamlit Frontend

A professional web interface for AI-powered Python code analysis.
Supports code input via text area, file upload, and sample selection.
"""

import os
import streamlit as st
from typing import Optional
import time

# Load environment variables FIRST before any other imports
from dotenv import load_dotenv
load_dotenv()

from backend.ai_analyzer import create_analyzer, AnalysisResult
from backend.ai_client import validate_configuration
from backend.ollama_client import get_ollama_client, check_ollama_status, OllamaConfig
from utils.report_generator import ReportGenerator
from utils.sample_loader import SampleLoader, get_sample_info
from utils.coach_prompts import get_coach_prompts
from config import (
    APP_NAME, 
    APP_VERSION, 
    APP_DESCRIPTION,
    ANALYSIS_DEPTHS,
    GRADE_DESCRIPTIONS,
    SEVERITY_COLORS
)


# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables."""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "code_input" not in st.session_state:
        st.session_state.code_input = ""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "model_name" not in st.session_state:
        st.session_state.model_name = "gemini-2.0-flash"
    if "coach_response" not in st.session_state:
        st.session_state.coach_response = ""
    if "current_code" not in st.session_state:
        st.session_state.current_code = ""
    if "ollama_model" not in st.session_state:
        st.session_state.ollama_model = "codellama:7b"


def render_custom_css():
    """Inject custom CSS styles."""
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
        }
        .grade-display {
            font-size: 4rem;
            font-weight: bold;
            text-align: center;
            padding: 1rem;
            border-radius: 50%;
            width: 120px;
            height: 120px;
            line-height: 100px;
            margin: 0 auto;
            color: white;
        }
        .grade-A { background: linear-gradient(135deg, #28a745, #20c997); }
        .grade-B { background: linear-gradient(135deg, #5cb85c, #28a745); }
        .grade-C { background: linear-gradient(135deg, #ffc107, #fd7e14); }
        .grade-D { background: linear-gradient(135deg, #dc3545, #c82333); }
        .metric-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            border: 1px solid #e9ecef;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #333;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #666;
        }
        .issue-card {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            border-left: 4px solid;
        }
        .issue-error {
            background: #fff5f5;
            border-left-color: #dc3545;
        }
        .issue-warning {
            background: #fffbeb;
            border-left-color: #ffc107;
        }
        .issue-info {
            background: #f0f9ff;
            border-left-color: #17a2b8;
        }
        .strength-item {
            background: #f0fff4;
            padding: 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            border-left: 3px solid #28a745;
        }
        .improvement-item {
            background: #f8f4ff;
            padding: 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            border-left: 3px solid #667eea;
        }
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar() -> tuple[str, str, str]:
    """
    Render the sidebar with configuration options.
    
    Returns:
        Tuple of (api_key, analysis_depth, input_method)
    """
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # API Key input for Gemini
        st.markdown("### 🔑 Google AI Studio")
        api_key = st.text_input(
            "Google API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your Google AI Studio API key"
        )
        st.session_state.api_key = api_key
        
        # Set in environment
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
        
        # Model name (optional override)
        model_name = st.text_input(
            "Model Name",
            value=st.session_state.get("model_name", "gemini-2.0-flash"),
            placeholder="gemini-2.0-flash",
            help="Gemini model to use for analysis"
        )
        st.session_state.model_name = model_name
        if model_name:
            os.environ["AI_MODEL_NAME"] = model_name
        
        st.markdown("---")
        
        # Analysis depth selection
        st.markdown("### 📊 Analysis Depth")
        depth = st.radio(
            "Select depth",
            options=list(ANALYSIS_DEPTHS.keys()),
            help="Quick: Fast overview | Detailed: Comprehensive analysis"
        )
        st.caption(ANALYSIS_DEPTHS[depth]["description"])
        
        st.markdown("---")
        
        # Input method selection
        st.markdown("### 📥 Input Method")
        input_method = st.radio(
            "Choose input method",
            options=["✏️ Paste Code", "📁 Upload File", "📚 Sample Code"],
            index=0
        )
        
        st.markdown("---")
        
        # About section
        st.markdown("### ℹ️ About")
        st.markdown(f"""
        **{APP_NAME}** v{APP_VERSION}
        
        {APP_DESCRIPTION}
        
        Powered by Google Gemini.
        """)
        
    return api_key, depth, input_method


def render_code_input(input_method: str) -> Optional[str]:
    """
    Render the code input section based on selected method.
    
    Args:
        input_method: The selected input method.
    
    Returns:
        The code to analyze, or None.
    """
    code = None
    
    if "Paste" in input_method:
        st.markdown("### ✏️ Paste Your Python Code")
        code = st.text_area(
            "Enter Python code to analyze",
            height=400,
            placeholder="Paste your Python code here...",
            key="code_text_area"
        )
        
    elif "Upload" in input_method:
        st.markdown("### 📁 Upload Python File")
        uploaded_file = st.file_uploader(
            "Choose a Python file",
            type=["py"],
            help="Upload a .py file for analysis"
        )
        
        if uploaded_file is not None:
            code = uploaded_file.read().decode("utf-8")
            with st.expander("📄 View uploaded code", expanded=False):
                st.code(code, language="python")
                
    elif "Sample" in input_method:
        st.markdown("### 📚 Select Sample Code")
        
        # Get sample choices
        samples = SampleLoader.get_all_samples()
        sample_names = ["-- Select a sample --"] + [s.name for s in samples.values()]
        
        selected_name = st.selectbox(
            "Choose a sample program",
            options=sample_names,
            index=0
        )
        
        if selected_name != "-- Select a sample --":
            sample_info = get_sample_info(selected_name)
            sample = SampleLoader.get_sample_by_name(selected_name)
            
            if sample and sample_info:
                # Show sample info
                quality_colors = {"good": "🟢", "average": "🟡", "poor": "🔴"}
                quality_icon = quality_colors.get(sample_info["quality"], "⚪")
                
                st.info(f"{quality_icon} **Quality Level:** {sample_info['quality'].title()}\n\n{sample_info['description']}")
                
                code = sample.code
                
                with st.expander("📄 View sample code", expanded=True):
                    st.code(code, language="python")
    
    return code


def render_analysis_button(code: Optional[str], api_key: str, depth: str) -> None:
    """
    Render the analyze button and handle analysis.
    
    Args:
        code: The code to analyze.
        api_key: The API key.
        depth: Analysis depth setting.
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Check configuration validity
        is_valid, config_error = validate_configuration()
        
        analyze_disabled = not code or not is_valid
        
        if not is_valid:
            st.error(f"⚠️ Configuration required: {config_error}")
        elif not code:
            st.info("📝 Enter or select code to analyze.")
        
        if st.button(
            "🔍 Analyze Code",
            type="primary",
            use_container_width=True,
            disabled=analyze_disabled
        ):
            run_analysis(code, api_key, depth)


def run_analysis(code: str, api_key: str, depth: str) -> None:
    """
    Run the AI analysis on the provided code using Gemini.
    
    Args:
        code: The code to analyze.
        api_key: The API key.
        depth: Analysis depth setting.
    """
    # Store current code for AI Coach
    st.session_state.current_code = code
    
    with st.spinner("🔄 Analyzing code with Gemini..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate progress stages
        status_text.text("📤 Sending code to Gemini...")
        progress_bar.progress(20)
        
        # Create analyzer and run analysis
        analyzer = create_analyzer(api_key)
        
        status_text.text("🧠 AI is analyzing your code...")
        progress_bar.progress(50)
        
        result = analyzer.analyze(code, depth)
        
        status_text.text("📥 Processing results...")
        progress_bar.progress(80)
        
        time.sleep(0.3)  # Brief pause for UX
        
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        
        # Store result in session state
        st.session_state.analysis_result = result
        
        if result.success:
            st.success(f"✅ Analysis completed in {result.processing_time:.2f} seconds!")
        else:
            st.error(f"❌ Analysis failed: {result.error}")


def render_results() -> None:
    """Render the analysis results."""
    result: AnalysisResult = st.session_state.analysis_result
    
    if not result or not result.success:
        return
    
    data = result.data
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Summary Section
    render_summary_section(data)
    
    st.markdown("---")
    
    # Metrics Section
    render_metrics_section(data)
    
    st.markdown("---")
    
    # Issues Section
    render_issues_section(data)
    
    # Strengths and Improvements
    col1, col2 = st.columns(2)
    
    with col1:
        render_strengths_section(data)
    
    with col2:
        render_improvements_section(data)
    
    # AI Coach Section (using current code from session state)
    if st.session_state.current_code:
        render_ai_coach_section(st.session_state.current_code, data)
    
    st.markdown("---")
    
    # Download Section
    render_download_section(data)


def render_summary_section(data: dict) -> None:
    """Render the summary section with grade and scores."""
    summary = data.get("summary", {})
    
    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
    
    # Grade display
    with col1:
        grade = summary.get("overall_grade", "N/A")
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="grade-display grade-{grade}">{grade}</div>
            <p style="margin-top: 0.5rem; color: #666; font-size: 0.9rem;">
                {GRADE_DESCRIPTIONS.get(grade, "Unknown")}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Readability score
    with col2:
        readability = summary.get("readability_score", 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{readability}/10</div>
            <div class="metric-label">Readability</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(readability / 10)
    
    # Maintainability score
    with col3:
        maintainability = summary.get("maintainability_score", 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{maintainability}/100</div>
            <div class="metric-label">Maintainability</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(maintainability / 100)
    
    # Complexity level
    with col4:
        complexity = summary.get("complexity_level", "N/A")
        complexity_colors = {"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"}
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {complexity_colors.get(complexity, '#333')};">
                {complexity}
            </div>
            <div class="metric-label">Complexity</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Documentation quality
    with col5:
        doc_quality = summary.get("documentation_quality", "N/A")
        doc_colors = {"Poor": "#dc3545", "Average": "#ffc107", "Good": "#5cb85c", "Excellent": "#28a745"}
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {doc_colors.get(doc_quality, '#333')}; font-size: 1.4rem;">
                {doc_quality}
            </div>
            <div class="metric-label">Documentation</div>
        </div>
        """, unsafe_allow_html=True)


def render_metrics_section(data: dict) -> None:
    """Render the code metrics section."""
    st.markdown("### 📈 Code Metrics")
    
    metrics = data.get("metrics", {})
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metric_items = [
        (col1, "Lines of Code", metrics.get("lines_of_code", "N/A"), "📝"),
        (col2, "Functions", metrics.get("functions_count", "N/A"), "🔧"),
        (col3, "Classes", metrics.get("classes_count", "N/A"), "📦"),
        (col4, "Avg Func Length", metrics.get("average_function_length", "N/A"), "📏"),
        (col5, "Est. Complexity", metrics.get("estimated_cyclomatic_complexity", "N/A"), "🔀"),
    ]
    
    for col, label, value, icon in metric_items:
        with col:
            st.metric(label=f"{icon} {label}", value=value)


def render_issues_section(data: dict) -> None:
    """Render the issues section grouped by severity."""
    issues = data.get("issues", [])
    
    st.markdown(f"### ⚠️ Issues Found ({len(issues)})")
    
    if not issues:
        st.success("🎉 No issues detected! Your code looks great.")
        return
    
    # Group issues by type
    errors = [i for i in issues if i.get("type") == "Error"]
    warnings = [i for i in issues if i.get("type") == "Warning"]
    infos = [i for i in issues if i.get("type") == "Info"]
    
    # Tabs for different severity levels
    tab1, tab2, tab3 = st.tabs([
        f"🔴 Errors ({len(errors)})",
        f"🟡 Warnings ({len(warnings)})",
        f"🔵 Info ({len(infos)})"
    ])
    
    with tab1:
        render_issue_list(errors, "error")
    
    with tab2:
        render_issue_list(warnings, "warning")
    
    with tab3:
        render_issue_list(infos, "info")


def render_issue_list(issues: list, severity: str) -> None:
    """Render a list of issues."""
    if not issues:
        st.info(f"No {severity}s found.")
        return
    
    for issue in issues:
        with st.container():
            st.markdown(f"""
            <div class="issue-card issue-{severity}">
                <strong>{issue.get('title', 'Untitled')}</strong>
                <br><small>📍 {issue.get('location', 'Unknown location')}</small>
                <p style="margin: 0.5rem 0;">{issue.get('description', 'No description')}</p>
                <div style="background: white; padding: 0.5rem; border-radius: 4px;">
                    <strong style="color: #28a745;">💡 Recommendation:</strong> 
                    {issue.get('recommendation', 'No recommendation')}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_strengths_section(data: dict) -> None:
    """Render the strengths section."""
    st.markdown("### ✅ Strengths")
    
    strengths = data.get("strengths", [])
    
    if not strengths:
        st.info("No specific strengths identified.")
        return
    
    for strength in strengths:
        st.markdown(f"""
        <div class="strength-item">✓ {strength}</div>
        """, unsafe_allow_html=True)


def render_improvements_section(data: dict) -> None:
    """Render the improvements section."""
    st.markdown("### 🚀 Suggested Improvements")
    
    improvements = data.get("improvements", [])
    
    if not improvements:
        st.info("No additional improvements suggested.")
        return
    
    for improvement in improvements:
        st.markdown(f"""
        <div class="improvement-item">→ {improvement}</div>
        """, unsafe_allow_html=True)


def render_ai_coach_section(code: str, analysis_data: Optional[dict] = None) -> None:
    """
    Render the AI Coach section with streaming Ollama responses.
    
    Args:
        code: The user's code.
        analysis_data: Optional analysis results for context.
    """
    st.markdown("---")
    st.markdown("## 🤖 AI Coach (Local - Free)")
    
    # Check Ollama status
    ollama_available, status_msg = check_ollama_status()
    
    if not ollama_available:
        st.warning(status_msg)
        st.info("""
        **To enable AI Coach:**
        1. Install Ollama: https://ollama.com/download
        2. Run: `ollama serve` (starts the server)
        3. Run: `ollama pull codellama:7b` (downloads the model)
        """)
        return
    
    st.success(status_msg)
    
    # Model selection
    try:
        client = get_ollama_client()
        available_models = client.list_models()
    except Exception:
        available_models = ["codellama:7b"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_model = st.selectbox(
            "🧠 Select Local Model",
            options=available_models if available_models else ["codellama:7b"],
            index=0,
            help="Choose which Ollama model to use for coaching"
        )
        st.session_state.ollama_model = selected_model
    
    with col2:
        coach_mode = st.radio(
            "📝 Mode",
            options=["💡 Hints Only", "✨ Full Solution"],
            index=0,
            horizontal=True,
            help="Hints: Guidance without solutions | Solution: Complete improved code"
        )
    
    # Optional problem description
    with st.expander("📋 Add Problem Context (Optional)", expanded=False):
        problem_desc = st.text_area(
            "Problem Description",
            placeholder="Describe what the code should do, any constraints, or expected behavior...",
            height=100
        )
        test_results = st.text_area(
            "Test Results (if any)",
            placeholder="Paste any test failures or error messages here...",
            height=100
        )
    
    # Generate button
    mode = "hints" if "Hints" in coach_mode else "solution"
    
    if st.button("🚀 Get AI Coach Feedback", type="primary", use_container_width=True):
        if not code:
            st.warning("⚠️ Please enter some code first!")
            return
        
        # Build prompts
        system_prompt, user_prompt = get_coach_prompts(
            code=code,
            mode=mode,
            analysis_data=analysis_data,
            problem_description=problem_desc if 'problem_desc' in dir() and problem_desc else None,
            test_results=test_results if 'test_results' in dir() and test_results else None
        )
        
        # Create client and stream response
        try:
            config = OllamaConfig(model=selected_model)
            client = get_ollama_client(selected_model)
            
            st.markdown("### 💬 Coach Response")
            
            # Streaming container
            response_container = st.empty()
            full_response = ""
            
            with st.spinner("🧠 AI Coach is thinking..."):
                for token in client.stream_generate(user_prompt, system_prompt):
                    full_response += token
                    # Update the display with streaming effect
                    response_container.markdown(full_response + "▌")
            
            # Final display without cursor
            response_container.markdown(full_response)
            st.session_state.coach_response = full_response
            
            # Copy button
            st.code(full_response, language="markdown")
            
        except Exception as e:
            st.error(f"❌ Error getting coach feedback: {str(e)}")


def render_download_section(data: dict) -> None:
    """Render the report download section."""
    st.markdown("### 📥 Download Report")
    
    generator = ReportGenerator(data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        text_report = generator.generate_text_report()
        st.download_button(
            label="📄 Download Text Report",
            data=text_report,
            file_name="code_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        html_report = generator.generate_html_report()
        st.download_button(
            label="🌐 Download HTML Report",
            data=html_report,
            file_name="code_analysis_report.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col3:
        json_report = generator.generate_json_report()
        st.download_button(
            label="📊 Download JSON Report",
            data=json_report,
            file_name="code_analysis_report.json",
            mime="application/json",
            use_container_width=True
        )


def main():
    """Main application entry point."""
    # Initialize
    init_session_state()
    render_custom_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 AI Code Analyzer</h1>
        <p style="color: #666; font-size: 1.1rem;">
            Google Gemini-powered semantic analysis for Python code quality
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    api_key, depth, input_method = render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        code = render_code_input(input_method)
    
    with col2:
        st.markdown("### 📋 How It Works")
        st.markdown("""
        1. **Enter your Google API key** in the sidebar
        2. **Choose input method**: paste, upload, or select sample
        3. **Select analysis depth**: Quick or Detailed
        4. **Click Analyze** to get AI-powered insights
        5. **Review results** and download reports
        
        ---
        
        **What Gemini analyzes:**
        - Code quality and readability
        - Design patterns and best practices
        - Potential bugs and code smells
        - Documentation completeness
        - Maintainability and complexity
        """)
        
        if code:
            st.success(f"✅ Code loaded: {len(code)} characters, {code.count(chr(10)) + 1} lines")
    
    # Analyze button
    render_analysis_button(code, api_key, depth)
    
    # Results
    render_results()
    
    # Standalone AI Coach (always visible if code exists)
    if code and not st.session_state.analysis_result:
        st.markdown("---")
        st.markdown("## 🤖 AI Coach (Local - Free)")
        st.info("💡 **Tip:** You can use the AI Coach without Gemini analysis! Just paste code above and get AI-powered feedback using the local Ollama model.")
        render_ai_coach_section(code, None)


if __name__ == "__main__":
    main()
