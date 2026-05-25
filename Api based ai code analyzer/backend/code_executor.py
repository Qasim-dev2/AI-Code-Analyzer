"""
Safe Code Executor
Runs Python code in a subprocess with timeouts and output capture.
Designed for Windows compatibility.
"""

import subprocess
import sys
import tempfile
import os
from dataclasses import dataclass
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of code execution."""
    success: bool
    stdout: str
    stderr: str
    return_code: int
    timed_out: bool
    error_message: Optional[str] = None


class CodeExecutor:
    """
    Safe Python code executor with timeout and output limits.
    
    Security measures:
    - Runs in subprocess (isolated from main process)
    - Timeout enforcement
    - Output length limits
    - Temp file cleanup
    
    Note: This is NOT a full sandbox. For production, consider Docker or RestrictedPython.
    """
    
    def __init__(
        self, 
        timeout: int = 10, 
        max_output: int = 10000
    ):
        """
        Initialize the executor.
        
        Args:
            timeout: Max execution time in seconds
            max_output: Max output length in characters
        """
        self.timeout = timeout
        self.max_output = max_output
    
    def execute(self, code: str, stdin_input: str = "") -> ExecutionResult:
        """
        Execute Python code safely.
        
        Args:
            code: Python code to execute
            stdin_input: Optional input to pass via stdin
        
        Returns:
            ExecutionResult with output and status
        """
        # Create temp file for the code
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.py', 
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(code)
                temp_file = f.name
            
            # Run in subprocess
            result = self._run_subprocess(temp_file, stdin_input)
            return result
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                timed_out=False,
                error_message=str(e)
            )
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass
    
    def _run_subprocess(
        self, 
        script_path: str, 
        stdin_input: str = ""
    ) -> ExecutionResult:
        """Run the script in a subprocess."""
        try:
            # Use the same Python interpreter
            python_exe = sys.executable
            
            process = subprocess.Popen(
                [python_exe, script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            try:
                stdout, stderr = process.communicate(
                    input=stdin_input if stdin_input else None,
                    timeout=self.timeout
                )
                
                # Truncate output if too long
                if len(stdout) > self.max_output:
                    stdout = stdout[:self.max_output] + "\n... [Output truncated]"
                if len(stderr) > self.max_output:
                    stderr = stderr[:self.max_output] + "\n... [Error truncated]"
                
                return ExecutionResult(
                    success=(process.returncode == 0),
                    stdout=stdout,
                    stderr=stderr,
                    return_code=process.returncode,
                    timed_out=False
                )
                
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()  # Clean up
                return ExecutionResult(
                    success=False,
                    stdout="",
                    stderr=f"⏱️ Execution timed out after {self.timeout} seconds",
                    return_code=-1,
                    timed_out=True,
                    error_message="Timeout"
                )
                
        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                timed_out=False,
                error_message=str(e)
            )
    
    def run_with_tests(
        self, 
        code: str, 
        test_cases: list
    ) -> Tuple[list, int, int]:
        """
        Run code against test cases.
        
        Args:
            code: The solution code
            test_cases: List of {"input": ..., "expected_output": ...}
        
        Returns:
            Tuple of (results list, passed count, total count)
        """
        results = []
        passed = 0
        
        for i, test in enumerate(test_cases):
            test_input = str(test.get("input", test.get("stdin", "")))
            expected = str(
                test.get(
                    "expected_output",
                    test.get("output", test.get("expected", "")),
                )
            ).strip()
            
            # Execute with test input
            result = self.execute(code, test_input)
            actual = result.stdout.strip()
            
            # Check if output matches
            is_pass = (actual == expected) and result.success
            if is_pass:
                passed += 1
            
            results.append({
                "test_num": i + 1,
                "input": test_input,
                "expected": expected,
                "actual": actual,
                "passed": is_pass,
                "error": result.stderr if not result.success else None,
                "timed_out": result.timed_out
            })
        
        return results, passed, len(test_cases)


# Global executor instance
_executor = None

def get_executor(timeout: int = 10) -> CodeExecutor:
    """Get or create a code executor instance."""
    global _executor
    if _executor is None or _executor.timeout != timeout:
        _executor = CodeExecutor(timeout=timeout)
    return _executor
