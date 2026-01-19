"""
Type Checking with mypy
Run: mypy typing_02_mypy_demo.py
"""
from __future__ import annotations


# ============================================================
# Example 1: Basic Type Errors
# ============================================================

def add_numbers(a: int, b: int) -> int:
    return a + b

# mypy error: Argument 1 has incompatible type "str"; expected "int"
result1 = add_numbers("5", 10)

# mypy error: Argument 2 has incompatible type "str"; expected "int"
result2 = add_numbers(5, "10")

# ✓ No error
result3 = add_numbers(5, 10)

# ============================================================
# Example 2: Return Type Mismatch
# ============================================================

def get_name() -> str:
    return 123  # mypy error: Expected str, got int

def get_age() -> int:
    return "25"  # mypy error: Expected int, got str

# ============================================================
# Example 3: None Handling
# ============================================================

def find_item(name: str) -> dict | None:
    if name == "found":
        return {"value": 42}
    return None

item = find_item("missing")
# mypy error: Item "None" has no attribute "__getitem__"
value = item["value"]

# ✓ Correct way
item2 = find_item("found")
if item2 is not None:
    value2 = item2["value"]  # No error

# ============================================================
# Example 4: List Type Mismatch
# ============================================================

def process_numbers(nums: list[int]) -> int:
    return sum(nums)

# mypy error: List item 2 has incompatible type "str"; expected "int"
result = process_numbers([1, 2, "3", 4])

# ✓ No error
result_good = process_numbers([1, 2, 3, 4])

# ============================================================
# Example 5: Missing Type Annotations
# ============================================================

# mypy error (with --strict): Function is missing a type annotation
def unclear_function(x, y):
    return x + y

# ✓ Proper annotation
def clear_function(x: int, y: int) -> int:
    return x + y

# ============================================================
# Example 6: TypedDict
# ============================================================

from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int

def create_person(name: str, age: int) -> Person:
    # mypy error: Missing key "age"
    return {"name": name}

# ✓ Correct
def create_person_good(name: str, age: int) -> Person:
    return {"name": name, "age": age}

# ============================================================
# How to Run mypy
# ============================================================

"""
Install:
    pip install mypy

Run:
    mypy typing_02_mypy_demo.py

Output will show:
    typing_02_mypy_demo.py:13: error: Argument 1 to "add_numbers" has incompatible type "str"; expected "int"
    typing_02_mypy_demo.py:16: error: Argument 2 to "add_numbers" has incompatible type "str"; expected "int"
    ... (more errors)

Strict mode (recommended for new projects):
    mypy --strict typing_02_mypy_demo.py

Ignore specific line:
    result = add_numbers("5", 10)  # type: ignore

Configuration (.mypy.ini):
    [mypy]
    python_version = 3.11
    warn_return_any = True
    warn_unused_configs = True
    disallow_untyped_defs = True
"""

if __name__ == "__main__":
    print("Run: mypy typing_02_mypy_demo.py")
    print("This file has intentional type errors for demonstration!")