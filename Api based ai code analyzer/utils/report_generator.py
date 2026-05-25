"""
Report Generator Module

Converts AI-generated JSON analysis results into various report formats:
- Human-readable text reports
- Styled HTML reports
- Raw JSON export
"""

import json
from datetime import datetime
from typing import Any, Dict


class ReportGenerator:
    """
    Generates formatted reports from AI analysis results.
    
    Supports multiple output formats while preserving severity levels,
    recommendations, and all analysis details.
    """
    
    def __init__(self, analysis_data: Dict[str, Any]):
        """
        Initialize the report generator.
        
        Args:
            analysis_data: The JSON analysis result from the AI analyzer.
        """
        self.data = analysis_data
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_text_report(self) -> str:
        """
        Generate a human-readable text report.
        
        Returns:
            Formatted text report string.
        """
        lines = []
        lines.append("=" * 70)
        lines.append("AI CODE ANALYSIS REPORT")
        lines.append(f"Generated: {self.timestamp}")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary section
        summary = self.data.get("summary", {})
        lines.append("SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Overall Grade:        {summary.get('overall_grade', 'N/A')}")
        lines.append(f"Readability Score:    {summary.get('readability_score', 'N/A')}/10")
        lines.append(f"Maintainability:      {summary.get('maintainability_score', 'N/A')}/100")
        lines.append(f"Complexity Level:     {summary.get('complexity_level', 'N/A')}")
        lines.append(f"Documentation:        {summary.get('documentation_quality', 'N/A')}")
        lines.append("")
        
        # Metrics section
        metrics = self.data.get("metrics", {})
        lines.append("METRICS")
        lines.append("-" * 40)
        lines.append(f"Lines of Code:              {metrics.get('lines_of_code', 'N/A')}")
        lines.append(f"Functions Count:            {metrics.get('functions_count', 'N/A')}")
        lines.append(f"Classes Count:              {metrics.get('classes_count', 'N/A')}")
        lines.append(f"Avg Function Length:        {metrics.get('average_function_length', 'N/A')}")
        lines.append(f"Est. Cyclomatic Complexity: {metrics.get('estimated_cyclomatic_complexity', 'N/A')}")
        lines.append("")
        
        # Issues section
        issues = self.data.get("issues", [])
        if issues:
            lines.append("ISSUES FOUND")
            lines.append("-" * 40)
            
            # Group by severity
            for severity in ["Error", "Warning", "Info"]:
                severity_issues = [i for i in issues if i.get("type") == severity]
                if severity_issues:
                    lines.append(f"\n[{severity.upper()}S]")
                    for idx, issue in enumerate(severity_issues, 1):
                        lines.append(f"\n  {idx}. {issue.get('title', 'Untitled')}")
                        lines.append(f"     Location: {issue.get('location', 'Unknown')}")
                        lines.append(f"     Description: {issue.get('description', 'N/A')}")
                        lines.append(f"     Recommendation: {issue.get('recommendation', 'N/A')}")
            lines.append("")
        else:
            lines.append("ISSUES FOUND")
            lines.append("-" * 40)
            lines.append("No issues detected.")
            lines.append("")
        
        # Strengths section
        strengths = self.data.get("strengths", [])
        lines.append("STRENGTHS")
        lines.append("-" * 40)
        if strengths:
            for idx, strength in enumerate(strengths, 1):
                lines.append(f"  {idx}. {strength}")
        else:
            lines.append("  No specific strengths identified.")
        lines.append("")
        
        # Improvements section
        improvements = self.data.get("improvements", [])
        lines.append("SUGGESTED IMPROVEMENTS")
        lines.append("-" * 40)
        if improvements:
            for idx, improvement in enumerate(improvements, 1):
                lines.append(f"  {idx}. {improvement}")
        else:
            lines.append("  No additional improvements suggested.")
        lines.append("")
        
        lines.append("=" * 70)
        lines.append("End of Report")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def generate_html_report(self) -> str:
        """
        Generate a styled HTML report.
        
        Returns:
            Complete HTML document string.
        """
        summary = self.data.get("summary", {})
        metrics = self.data.get("metrics", {})
        issues = self.data.get("issues", [])
        strengths = self.data.get("strengths", [])
        improvements = self.data.get("improvements", [])
        
        grade = summary.get("overall_grade", "N/A")
        grade_color = self._get_grade_color(grade)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Code Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .timestamp {{
            opacity: 0.8;
            font-size: 14px;
        }}
        .grade-badge {{
            display: inline-block;
            width: 80px;
            height: 80px;
            line-height: 80px;
            font-size: 42px;
            font-weight: bold;
            border-radius: 50%;
            background: {grade_color};
            color: white;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .metric-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }}
        .metric-label {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}
        .score-bar {{
            background: #e9ecef;
            border-radius: 10px;
            height: 12px;
            margin-top: 8px;
            overflow: hidden;
        }}
        .score-fill {{
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }}
        .issue {{
            background: #f8f9fa;
            border-left: 4px solid #ddd;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 0 8px 8px 0;
        }}
        .issue.error {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        .issue.warning {{
            border-left-color: #ffc107;
            background: #fffbeb;
        }}
        .issue.info {{
            border-left-color: #17a2b8;
            background: #f0f9ff;
        }}
        .issue-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .issue-title {{
            font-weight: 600;
            font-size: 16px;
        }}
        .issue-badge {{
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .issue-badge.error {{
            background: #dc3545;
            color: white;
        }}
        .issue-badge.warning {{
            background: #ffc107;
            color: #333;
        }}
        .issue-badge.info {{
            background: #17a2b8;
            color: white;
        }}
        .issue-location {{
            font-size: 13px;
            color: #666;
            margin-bottom: 8px;
        }}
        .issue-description {{
            margin-bottom: 10px;
        }}
        .issue-recommendation {{
            background: white;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
        }}
        .issue-recommendation strong {{
            color: #28a745;
        }}
        .list-item {{
            background: #f8f9fa;
            padding: 12px 15px;
            margin-bottom: 8px;
            border-radius: 6px;
            display: flex;
            align-items: flex-start;
        }}
        .list-item::before {{
            content: "✓";
            color: #28a745;
            font-weight: bold;
            margin-right: 10px;
        }}
        .improvement-item::before {{
            content: "→";
            color: #667eea;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Code Analysis Report</h1>
            <p class="timestamp">Generated: {self.timestamp}</p>
            <div class="grade-badge">{grade}</div>
            <p>Overall Code Quality Grade</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2 class="section-title">Summary Scores</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('readability_score', 'N/A')}/10</div>
                        <div class="metric-label">Readability</div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {summary.get('readability_score', 0) * 10}%; background: #28a745;"></div>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('maintainability_score', 'N/A')}/100</div>
                        <div class="metric-label">Maintainability</div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: {summary.get('maintainability_score', 0)}%; background: #667eea;"></div>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('complexity_level', 'N/A')}</div>
                        <div class="metric-label">Complexity Level</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary.get('documentation_quality', 'N/A')}</div>
                        <div class="metric-label">Documentation</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">Code Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('lines_of_code', 'N/A')}</div>
                        <div class="metric-label">Lines of Code</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('functions_count', 'N/A')}</div>
                        <div class="metric-label">Functions</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('classes_count', 'N/A')}</div>
                        <div class="metric-label">Classes</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('average_function_length', 'N/A')}</div>
                        <div class="metric-label">Avg Function Length</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('estimated_cyclomatic_complexity', 'N/A')}</div>
                        <div class="metric-label">Est. Complexity</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">Issues Found ({len(issues)})</h2>
                {self._generate_issues_html(issues)}
            </div>
            
            <div class="section">
                <h2 class="section-title">Strengths</h2>
                {self._generate_list_html(strengths, "strength")}
            </div>
            
            <div class="section">
                <h2 class="section-title">Suggested Improvements</h2>
                {self._generate_list_html(improvements, "improvement")}
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by AI Code Analyzer | Powered by LLM-based semantic analysis</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _get_grade_color(self, grade: str) -> str:
        """Get color for grade badge."""
        colors = {
            "A": "#28a745",
            "B": "#5cb85c",
            "C": "#ffc107",
            "D": "#dc3545"
        }
        return colors.get(grade, "#6c757d")
    
    def _generate_issues_html(self, issues: list) -> str:
        """Generate HTML for issues section."""
        if not issues:
            return '<p style="color: #666; padding: 15px;">No issues detected. Great job!</p>'
        
        html_parts = []
        for issue in issues:
            issue_type = issue.get("type", "Info").lower()
            html_parts.append(f"""
            <div class="issue {issue_type}">
                <div class="issue-header">
                    <span class="issue-title">{issue.get('title', 'Untitled')}</span>
                    <span class="issue-badge {issue_type}">{issue.get('type', 'Info')}</span>
                </div>
                <div class="issue-location">📍 {issue.get('location', 'Unknown location')}</div>
                <div class="issue-description">{issue.get('description', 'No description')}</div>
                <div class="issue-recommendation">
                    <strong>💡 Recommendation:</strong> {issue.get('recommendation', 'No recommendation')}
                </div>
            </div>
            """)
        
        return "".join(html_parts)
    
    def _generate_list_html(self, items: list, item_type: str) -> str:
        """Generate HTML for list sections."""
        if not items:
            return f'<p style="color: #666; padding: 15px;">No {item_type}s identified.</p>'
        
        css_class = f"{item_type}-item" if item_type == "improvement" else "list-item"
        html_parts = []
        for item in items:
            html_parts.append(f'<div class="list-item {css_class}">{item}</div>')
        
        return "".join(html_parts)
    
    def generate_json_report(self, pretty: bool = True) -> str:
        """
        Generate a JSON report with metadata.
        
        Args:
            pretty: Whether to format with indentation.
        
        Returns:
            JSON string with analysis data and metadata.
        """
        report = {
            "metadata": {
                "generated_at": self.timestamp,
                "report_version": "1.0",
                "analyzer": "AI Code Analyzer"
            },
            "analysis": self.data
        }
        
        if pretty:
            return json.dumps(report, indent=2, ensure_ascii=False)
        return json.dumps(report, ensure_ascii=False)
    
    def generate_report(self, format: str = "text") -> str:
        """
        Generate a report in the specified format.
        
        Args:
            format: Output format - "text", "html", or "json".
        
        Returns:
            Formatted report string.
        
        Raises:
            ValueError: If format is not supported.
        """
        format_lower = format.lower()
        
        if format_lower == "text":
            return self.generate_text_report()
        elif format_lower == "html":
            return self.generate_html_report()
        elif format_lower == "json":
            return self.generate_json_report()
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'text', 'html', or 'json'.")
