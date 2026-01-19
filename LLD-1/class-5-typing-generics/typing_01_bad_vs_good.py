"""
Type Hints - Bad vs Good Examples
Shows why type hints catch bugs early
"""
from __future__ import annotations

print("=" * 60)
print("Example 1: Function Parameter Type Confusion")
print("=" * 60)

# ❌ BAD - No type hints
def calculate_discount_bad(price, discount):
    return price - (price * discount)

# This runs but gives wrong result!
result = calculate_discount_bad("100", "0.1")
print(f"Bad result: {result}")  # "100100" (string concatenation!)



# ✅ GOOD - With type hints
def calculate_discount_good(price: float, discount: float) -> float:
    return price - (price * discount)

# mypy would catch this before running!
# result = calculate_discount_good("100", "0.1")  # Type error!

result = calculate_discount_good(100, 0.1)
print(f"Good result: {result}")  # 90.0

print()
print("=" * 60)
print("Example 2: Return Type Inconsistency")
print("=" * 60)

# ❌ BAD - Returns different types
def get_user_age_bad(user_id):
    if user_id == 0:
        return "Unknown"  # Oops, string!
    return 25

age = get_user_age_bad(0)
# next_year = age + 1  # TypeError at runtime!
print(f"Bad: age is '{age}' (type: {type(age).__name__})")

# ✅ GOOD - Consistent return type
def get_user_age_good(user_id: int) -> int | None:
    if user_id == 0:
        return None  # Explicit None
    return 25

age = get_user_age_good(0)

if age is not None:
    next_year = age + 1
    print(f"Good: Next year age is {next_year}")
else:
    print("Good: Age is unknown")

print()
print("=" * 60)
print("Example 3: List Element Type")
print("=" * 60)

# ❌ BAD - Mixed types in list
def sum_numbers_bad(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

# This crashes!
try:
    result = sum_numbers_bad([1, 2, "3", 4])
except TypeError as e:
    print(f"Bad: {e}")

# ✅ GOOD - Type-safe list
def sum_numbers_good(numbers: list[int]) -> int:
    total = 0
    for num in numbers:
        total += num
    return total

result = sum_numbers_good([1, 2, 3, 4])
print(f"Good: {result}")
# mypy would catch: sum_numbers_good([1, 2, "3", 4])

print()
print("=" * 60)
print("Example 4: Dictionary Keys")
print("=" * 60)

# ❌ BAD - Unclear dictionary structure
def get_user_info_bad(user_id):
    return {"name": "Alice", "age": 25}

user = get_user_info_bad(1)
# What if key doesn't exist?
# email = user["email"]  # KeyError at runtime!

# ✅ GOOD - Explicit dictionary type
from typing import TypedDict

class UserInfo(TypedDict):
    name: str
    age: int
    email: str

def get_user_info_good(user_id: int) -> UserInfo:
    return {"name": "Alice", "age": 25, "email": "alice@example.com"}

user = get_user_info_good(1)
print(f"Good: {user['name']}, {user['email']}")
# mypy ensures all required keys exist!

print()
print("=" * 60)
print("Example 5: None Handling")
print("=" * 60)

# ❌ BAD - Unexpected None
def find_user_bad(name):
    database = {"Alice": {"email": "alice@example.com"}}
    if name in database:
        return database[name]
    return None

user = find_user_bad("Bob")
# print(user["email"])  # TypeError: 'NoneType' object is not subscriptable

# ✅ GOOD - Explicit None handling
def find_user_good(name: str) -> dict[str, str] | None:
    database = {"Alice": {"email": "alice@example.com"}}
    if name in database:
        return database[name]
    return None

user = find_user_good("Bob")
if user is not None:
    print(f"Good: {user['email']}")
else:
    print("Good: User not found (handled safely)")



print()
print("=" * 60)
print("KEY LESSONS:")
print("=" * 60)
print("✓ Type hints catch bugs BEFORE runtime")
print("✓ Make code self-documenting")
print("✓ IDE provides better autocomplete")
print("✓ Force proper None handling")
print("✓ Ensure consistent return types")