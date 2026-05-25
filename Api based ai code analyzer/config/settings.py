"""Shared settings and content for the active Ollama app."""

from dataclasses import dataclass


TOPICS = [
    "Arrays",
    "Strings",
    "Stacks",
    "Queues",
    "Linked Lists",
    "Trees",
    "Graphs",
    "Sorting",
    "Searching",
    "Dynamic Programming",
    "Recursion",
    "Hash Tables",
    "Two Pointers",
    "Sliding Window",
    "Bit Manipulation",
    "Math",
    "Greedy",
    "Backtracking",
]

DIFFICULTIES = ["Easy", "Medium", "Hard"]

PRACTICE_TIMES = {
    "Easy": 900,
    "Medium": 1800,
    "Hard": 2700,
}

RECOMMENDED_MODELS = {
    "codellama:7b": "Best default coding model",
    "codellama:13b": "Stronger but heavier coding model",
    "llama3.2:3b": "Fast general-purpose model",
    "llama3.2:1b": "Very light model for simple prompts",
    "mistral:7b": "Balanced general assistant",
    "deepseek-coder:6.7b": "Strong coding-focused model",
    "qwen2.5-coder:7b": "Modern coding-focused model",
}

SAMPLE_CODES = {
    "Bubble Sort": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
""",
    "Binary Search": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


print(binary_search([1, 3, 5, 7, 9, 11], 7))
""",
    "Two Sum": """def two_sum(nums, target):
    seen = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], index]
        seen[num] = index
    return []


print(two_sum([2, 7, 11, 15], 9))
""",
    "Fibonacci DP": """def fibonacci(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for index in range(2, n + 1):
        dp[index] = dp[index - 1] + dp[index - 2]

    return dp[n]


print([fibonacci(i) for i in range(10)])
""",
    "Quick Sort": """def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [item for item in arr if item < pivot]
    middle = [item for item in arr if item == pivot]
    right = [item for item in arr if item > pivot]

    return quick_sort(left) + middle + quick_sort(right)


print(quick_sort([3, 6, 8, 10, 1, 2, 1]))
""",
}

REFERENCE_CONTENT = {
    "Big O": """
| Complexity | Name | Example |
|------------|------|---------|
| O(1) | Constant | Hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Linear scan |
| O(n log n) | Linearithmic | Merge sort |
| O(n^2) | Quadratic | Bubble sort |
| O(2^n) | Exponential | Brute-force recursion |
""",
    "Data Structures": """
```python
lst = [1, 2, 3]
mapping = {"a": 1}
items = {1, 2, 3}

from collections import deque
queue = deque([1, 2, 3])
```
""",
    "Algorithms": """
```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
```
""",
    "Python Tips": """
```python
[item * 2 for item in range(5) if item % 2 == 0]

for index, value in enumerate(lst):
    ...

for left, right in zip(list_one, list_two):
    ...

from collections import Counter, defaultdict

counts = Counter([1, 1, 2])
groups = defaultdict(list)
```
""",
}


@dataclass(frozen=True)
class AnalysisConfig:
    """Model settings for analysis-style requests."""

    QUICK_MAX_TOKENS: int = 1500
    DETAILED_MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.0
    MAX_CODE_LENGTH: int = 50000
    MIN_CODE_LENGTH: int = 10


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration."""

    APP_NAME: str = "AI Code Analyzer"
    APP_VERSION: str = "2.6.0"
    APP_DESCRIPTION: str = "Local AI-powered code analysis, practice, and coaching"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "codellama:7b"
    DEFAULT_TEMPERATURE: float = 0.7
    REQUEST_TIMEOUT: int = 180
    EXECUTION_TIMEOUT: int = 10
    MAX_OUTPUT_LENGTH: int = 10000
