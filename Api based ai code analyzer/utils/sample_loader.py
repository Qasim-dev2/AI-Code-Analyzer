"""
Sample Code Loader Module

Provides sample Python code examples of varying quality for demonstration
and testing of the AI Code Analyzer.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SampleCode:
    """Container for sample code with metadata."""
    
    name: str
    description: str
    quality: str  # "good", "average", "poor"
    code: str


# Sample code collection
SAMPLES: Dict[str, SampleCode] = {
    "good_calculator": SampleCode(
        name="Calculator Module (Good Quality)",
        description="Well-structured calculator with proper documentation, type hints, and error handling.",
        quality="good",
        code='''"""
Calculator Module

A simple but well-designed calculator module demonstrating best practices
in Python development including type hints, documentation, and error handling.
"""

from typing import Union
from enum import Enum


class Operation(Enum):
    """Supported mathematical operations."""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass


class Calculator:
    """
    A calculator class supporting basic arithmetic operations.
    
    Attributes:
        history: List of previous calculation results.
        precision: Number of decimal places for results.
    
    Example:
        >>> calc = Calculator()
        >>> calc.calculate(10, 5, Operation.ADD)
        15.0
    """
    
    def __init__(self, precision: int = 2):
        """
        Initialize the calculator.
        
        Args:
            precision: Number of decimal places for rounding results.
        """
        self.history: list[float] = []
        self.precision = precision
    
    def calculate(
        self,
        a: Union[int, float],
        b: Union[int, float],
        operation: Operation
    ) -> float:
        """
        Perform a calculation with two operands.
        
        Args:
            a: First operand.
            b: Second operand.
            operation: The mathematical operation to perform.
        
        Returns:
            The result of the calculation, rounded to precision.
        
        Raises:
            CalculatorError: If division by zero is attempted.
            ValueError: If an unsupported operation is provided.
        """
        result = self._execute_operation(a, b, operation)
        rounded_result = round(result, self.precision)
        self.history.append(rounded_result)
        return rounded_result
    
    def _execute_operation(
        self,
        a: Union[int, float],
        b: Union[int, float],
        operation: Operation
    ) -> float:
        """Execute the actual mathematical operation."""
        if operation == Operation.ADD:
            return float(a + b)
        elif operation == Operation.SUBTRACT:
            return float(a - b)
        elif operation == Operation.MULTIPLY:
            return float(a * b)
        elif operation == Operation.DIVIDE:
            if b == 0:
                raise CalculatorError("Cannot divide by zero")
            return float(a / b)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def get_history(self) -> list[float]:
        """Return a copy of the calculation history."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.history.clear()


def main():
    """Demonstrate calculator usage."""
    calc = Calculator(precision=3)
    
    print("Calculator Demo")
    print("-" * 30)
    
    operations = [
        (10, 5, Operation.ADD),
        (20, 8, Operation.SUBTRACT),
        (7, 6, Operation.MULTIPLY),
        (100, 7, Operation.DIVIDE),
    ]
    
    for a, b, op in operations:
        result = calc.calculate(a, b, op)
        print(f"{a} {op.value} {b} = {result}")
    
    print(f"\\nHistory: {calc.get_history()}")


if __name__ == "__main__":
    main()
'''
    ),
    
    "average_data_processor": SampleCode(
        name="Data Processor (Average Quality)",
        description="Functional data processing code with some documentation gaps and minor issues.",
        quality="average",
        code='''"""
Data Processor - processes CSV data
"""

import csv
from typing import List, Dict, Any

class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []
        self.processed = False
    
    def load_data(self):
        """Load data from CSV file"""
        try:
            with open(self.filepath, 'r') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def filter_data(self, column, value):
        # Filter rows where column equals value
        result = []
        for row in self.data:
            if row.get(column) == value:
                result.append(row)
        return result
    
    def calculate_average(self, column):
        """Calculate average for numeric column"""
        total = 0
        count = 0
        for row in self.data:
            try:
                val = float(row[column])
                total += val
                count += 1
            except:
                pass
        
        if count == 0:
            return 0
        return total / count
    
    def transform_data(self, transformations: Dict[str, callable]):
        """Apply transformations to columns"""
        transformed = []
        for row in self.data:
            new_row = dict(row)
            for col, func in transformations.items():
                if col in new_row:
                    new_row[col] = func(new_row[col])
            transformed.append(new_row)
        return transformed
    
    def get_summary(self):
        summary = {
            'total_rows': len(self.data),
            'columns': list(self.data[0].keys()) if self.data else [],
        }
        return summary
    
    def export_data(self, output_path, data=None):
        data_to_export = data if data else self.data
        if not data_to_export:
            print("No data to export")
            return False
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data_to_export[0].keys())
            writer.writeheader()
            writer.writerows(data_to_export)
        return True


# Usage
if __name__ == "__main__":
    processor = DataProcessor("data.csv")
    if processor.load_data():
        print(processor.get_summary())
        filtered = processor.filter_data("status", "active")
        print(f"Active records: {len(filtered)}")
'''
    ),
    
    "poor_user_manager": SampleCode(
        name="User Manager (Poor Quality)",
        description="Poorly structured code with multiple issues: no documentation, bad naming, security issues.",
        quality="poor",
        code='''import sqlite3

class um:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS u (id INTEGER PRIMARY KEY, n TEXT, p TEXT, e TEXT)')
    
    def add(self, n, p, e):
        q = f"INSERT INTO u (n, p, e) VALUES ('{n}', '{p}', '{e}')"
        self.c.execute(q)
        self.conn.commit()
        return True
    
    def get(self, id):
        self.c.execute(f"SELECT * FROM u WHERE id = {id}")
        return self.c.fetchone()
    
    def getall(self):
        self.c.execute("SELECT * FROM u")
        r = self.c.fetchall()
        return r
    
    def upd(self, id, n=None, p=None, e=None):
        u = self.get(id)
        if not u:
            return False
        nn = n if n else u[1]
        np = p if p else u[2]
        ne = e if e else u[3]
        self.c.execute(f"UPDATE u SET n='{nn}', p='{np}', e='{ne}' WHERE id={id}")
        self.conn.commit()
        return True
    
    def rm(self, id):
        self.c.execute(f"DELETE FROM u WHERE id = {id}")
        self.conn.commit()
    
    def find(self, x):
        r = []
        all = self.getall()
        for u in all:
            if x in str(u):
                r.append(u)
        return r
    
    def chkpw(self, n, p):
        self.c.execute(f"SELECT * FROM u WHERE n = '{n}' AND p = '{p}'")
        if self.c.fetchone():
            return True
        return False

def test():
    m = um()
    m.add("john", "123456", "john@test.com")
    m.add("jane", "password", "jane@test.com")
    print(m.getall())
    print(m.chkpw("john", "123456"))
    m.rm(1)

test()
'''
    ),
    
    "good_api_client": SampleCode(
        name="REST API Client (Good Quality)",
        description="Clean API client implementation with proper error handling, retry logic, and typing.",
        quality="good",
        code='''"""
REST API Client Module

A robust HTTP client for interacting with REST APIs, featuring
automatic retries, proper error handling, and response validation.
"""

import time
import logging
from typing import Any, Dict, Optional, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum
import json

# Configure module logger
logger = logging.getLogger(__name__)


class HttpMethod(Enum):
    """HTTP methods supported by the client."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class ApiResponse:
    """
    Container for API response data.
    
    Attributes:
        success: Whether the request was successful.
        status_code: HTTP status code.
        data: Response payload (if successful).
        error: Error message (if failed).
    """
    success: bool
    status_code: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ApiError(Exception):
    """Custom exception for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class ApiClient:
    """
    A configurable REST API client with retry support.
    
    Features:
        - Automatic retry with exponential backoff
        - Request/response logging
        - Timeout handling
        - Header management
    
    Example:
        >>> client = ApiClient("https://api.example.com")
        >>> response = client.get("/users/1")
        >>> if response.success:
        ...     print(response.data)
    """
    
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 3
    RETRY_BACKOFF = 2
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_RETRIES
    ):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for the API.
            api_key: Optional API key for authentication.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._headers = self._build_default_headers(api_key)
    
    def _build_default_headers(self, api_key: Optional[str]) -> Dict[str, str]:
        """Build default headers for requests."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        return headers
    
    def set_header(self, key: str, value: str) -> None:
        """Set a custom header for all requests."""
        self._headers[key] = value
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> ApiResponse:
        """Send a GET request."""
        return self._request(HttpMethod.GET, endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> ApiResponse:
        """Send a POST request."""
        return self._request(HttpMethod.POST, endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> ApiResponse:
        """Send a PUT request."""
        return self._request(HttpMethod.PUT, endpoint, data=data)
    
    def delete(self, endpoint: str) -> ApiResponse:
        """Send a DELETE request."""
        return self._request(HttpMethod.DELETE, endpoint)
    
    def _request(
        self,
        method: HttpMethod,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> ApiResponse:
        """
        Execute an HTTP request with retry logic.
        
        Args:
            method: HTTP method to use.
            endpoint: API endpoint (appended to base_url).
            data: Request body data.
            params: Query parameters.
        
        Returns:
            ApiResponse containing the result.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Request {method.value} {url} (attempt {attempt + 1})")
                
                # Simulate HTTP request (replace with actual HTTP library)
                response = self._execute_request(method, url, data, params)
                
                return ApiResponse(
                    success=True,
                    status_code=200,
                    data=response
                )
                
            except ApiError as e:
                if attempt == self.max_retries - 1:
                    return ApiResponse(
                        success=False,
                        status_code=e.status_code or 500,
                        error=str(e)
                    )
                
                # Exponential backoff
                wait_time = self.RETRY_BACKOFF ** attempt
                logger.warning(f"Request failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
        
        return ApiResponse(
            success=False,
            status_code=500,
            error="Max retries exceeded"
        )
    
    def _execute_request(
        self,
        method: HttpMethod,
        url: str,
        data: Optional[Dict],
        params: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Execute the actual HTTP request.
        
        Note: This is a placeholder. In production, use httpx or requests.
        """
        # Placeholder for actual HTTP implementation
        logger.info(f"Executing {method.value} request to {url}")
        return {"status": "ok", "method": method.value}


def create_client(base_url: str, api_key: Optional[str] = None) -> ApiClient:
    """Factory function to create an API client instance."""
    return ApiClient(base_url, api_key)
'''
    ),
    
    "average_file_handler": SampleCode(
        name="File Handler (Average Quality)",
        description="Basic file handling utility with some issues in error handling and structure.",
        quality="average",
        code='''"""File handling utilities"""

import os
import json
import shutil

class FileHandler:
    def __init__(self, base_path="."):
        self.base_path = base_path
    
    def read_file(self, filename):
        """Read contents of a file"""
        path = os.path.join(self.base_path, filename)
        try:
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def write_file(self, filename, content, mode='w'):
        path = os.path.join(self.base_path, filename)
        with open(path, mode) as f:
            f.write(content)
        return True
    
    def read_json(self, filename):
        content = self.read_file(filename)
        if content:
            return json.loads(content)
        return {}
    
    def write_json(self, filename, data):
        content = json.dumps(data, indent=2)
        return self.write_file(filename, content)
    
    def list_files(self, extension=None):
        files = []
        for f in os.listdir(self.base_path):
            full_path = os.path.join(self.base_path, f)
            if os.path.isfile(full_path):
                if extension is None or f.endswith(extension):
                    files.append(f)
        return files
    
    def copy_file(self, src, dst):
        src_path = os.path.join(self.base_path, src)
        dst_path = os.path.join(self.base_path, dst)
        try:
            shutil.copy2(src_path, dst_path)
            return True
        except:
            return False
    
    def delete_file(self, filename):
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
    
    def get_file_info(self, filename):
        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            return None
        
        stat = os.stat(path)
        return {
            'name': filename,
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'created': stat.st_ctime
        }
    
    def ensure_directory(self, dirname):
        path = os.path.join(self.base_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)
        return path


# Quick utility functions
def quick_read(filepath):
    with open(filepath) as f:
        return f.read()

def quick_write(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)
'''
    ),
    
    "poor_shopping_cart": SampleCode(
        name="Shopping Cart (Poor Quality)", 
        description="Messy shopping cart implementation with globals, no validation, and poor structure.",
        quality="poor",
        code='''# shopping cart

items = []
total = 0
tax = 0.08
disc = 0

def add(name, price, qty=1):
    global items, total
    items.append({'n': name, 'p': price, 'q': qty})
    total = total + (price * qty)

def rem(idx):
    global items, total
    if idx < len(items):
        i = items[idx]
        total = total - (i['p'] * i['q'])
        del items[idx]

def settax(t):
    global tax
    tax = t

def setdisc(d):
    global disc
    disc = d

def calc():
    global total, tax, disc
    t = total
    if disc > 0:
        t = t - (t * disc)
    t = t + (t * tax)
    return t

def show():
    global items
    print("Cart:")
    for i, item in enumerate(items):
        print(f"{i}. {item['n']} x{item['q']} - ${item['p']}")
    print(f"Total: ${calc()}")

def clear():
    global items, total
    items = []
    total = 0

def apply_coupon(code):
    global disc
    if code == "SAVE10":
        disc = 0.1
    elif code == "SAVE20":
        disc = 0.2
    elif code == "HALF":
        disc = 0.5
    else:
        print("invalid code")

def checkout():
    t = calc()
    print(f"Processing payment for ${t}")
    clear()
    print("Order complete")
    return t

# test
add("Apple", 1.5, 3)
add("Bread", 2.5)
add("Milk", 3.0, 2)
show()
apply_coupon("SAVE10")
show()
checkout()
'''
    ),
}


class SampleLoader:
    """
    Loader class for managing sample code examples.
    
    Provides methods to list, retrieve, and filter sample code
    for demonstration and testing purposes.
    """
    
    @staticmethod
    def get_all_samples() -> Dict[str, SampleCode]:
        """Get all available sample codes."""
        return SAMPLES
    
    @staticmethod
    def get_sample_names() -> List[str]:
        """Get list of all sample names for display."""
        return [sample.name for sample in SAMPLES.values()]
    
    @staticmethod
    def get_sample_by_key(key: str) -> Optional[SampleCode]:
        """Get a specific sample by its key."""
        return SAMPLES.get(key)
    
    @staticmethod
    def get_sample_by_name(name: str) -> Optional[SampleCode]:
        """Get a specific sample by its display name."""
        for sample in SAMPLES.values():
            if sample.name == name:
                return sample
        return None
    
    @staticmethod
    def get_samples_by_quality(quality: str) -> List[SampleCode]:
        """Get all samples of a specific quality level."""
        return [s for s in SAMPLES.values() if s.quality == quality]
    
    @staticmethod
    def get_sample_choices() -> List[tuple]:
        """Get sample choices formatted for UI dropdown."""
        return [(key, sample.name) for key, sample in SAMPLES.items()]


# Convenience functions
def get_sample_names() -> List[str]:
    """Get list of all sample names."""
    return SampleLoader.get_sample_names()


def load_sample(name: str) -> Optional[str]:
    """Load sample code by name, returns the code string."""
    sample = SampleLoader.get_sample_by_name(name)
    return sample.code if sample else None


def get_sample_info(name: str) -> Optional[Dict[str, str]]:
    """Get sample metadata by name."""
    sample = SampleLoader.get_sample_by_name(name)
    if sample:
        return {
            "name": sample.name,
            "description": sample.description,
            "quality": sample.quality
        }
    return None
