# Type Hints in Python

## 📜 Brief History: Why Python Added Types

**Python's Philosophy (1991-2014):** "We are all consenting adults here"
- Created by Guido van Rossum for simplicity and readability
- Dynamic typing = flexibility, rapid prototyping
- No type declarations = less code, faster development

**The Problem (2010s):**
- Python used in large codebases (Google, Dropbox, Instagram)
- Bugs discovered late in production
- Hard to refactor without types
- IDE autocomplete limited

**The Evolution:**
```
1991: Python born (pure dynamic)
2006: PEP 3107 - Function annotations (syntax only)
2014: PEP 484 - Type hints (Guido @ Dropbox saw the need)
2015: Python 3.5 - typing module added
2020: Python 3.9 - Simplified syntax (list[int] vs List[int])
2022: Python 3.10 - Union types (int | str)
2023: Python 3.12 - Generic syntax cleanup
```

**Key Insight:** Python added types WITHOUT breaking philosophy
- Types are OPTIONAL (gradual typing)
- Not enforced at runtime (stay dynamic)
- Best of both worlds: flexibility + safety

**vs Other Languages:**
- Java/C++: Born with static typing (can't change)
- JavaScript → TypeScript: Separate language needed
- **Python: Evolved gracefully, kept backward compatibility**

---

## What is Typing?

**Explicitly declaring what type a variable/parameter/return value should be**

```python
# Without typing (the old way)
def add(a, b):
    return a + b

# With typing (the modern way)
def add(a: int, b: int) -> int:
    return a + b
```

---

## Why Do We Need Type Hints?

### 1. **Catch Bugs Early**

**Bad example (no types):**
```python
def calculate_discount(price, discount):
    return price - (price * discount)

# This will break at runtime!
calculate_discount("100", "0.1")  # TypeError: can't multiply str
```

**Good example (with types):**
```python
def calculate_discount(price: float, discount: float) -> float:
    return price - (price * discount)

# IDE/mypy catches this BEFORE running!
calculate_discount("100", "0.1")  # Error: Expected float, got str
```

### 2. **Self-Documenting Code**

```python
# Without types - unclear what this does
def process(data, flag, count):
    pass

# With types - immediately clear!
def process(data: list[str], flag: bool, count: int) -> dict[str, int]:
    pass
```

### 3. **Better IDE Support**

```python
def get_user(user_id: int) -> dict[str, str]:
    return {"name": "Alice", "email": "alice@example.com"}

user = get_user(123)
user.  # IDE shows: keys(), values(), get(), etc.
```

### 4. **Team Communication**

**Without types:**
```python
def send_email(to, subject, body, attachments):
    # What types are these? Must read implementation!
    pass
```

**With types:**
```python
def send_email(
    to: list[str], 
    subject: str, 
    body: str, 
    attachments: list[str] | None = None
) -> bool:
    # Crystal clear what's expected!
    pass
```

---

## Python vs Other Languages

### Static Typing (Java, C++, TypeScript)
```java
// Java - MUST declare types, checked at compile time
int add(int a, int b) {
    return a + b;
}
```

### Dynamic Typing (Python, JavaScript)
```python
# Python - types optional, checked at runtime
def add(a, b):
    return a + b
```

### Gradual Typing (Python 3.5+, TypeScript)
```python
# Python with type hints - OPTIONAL static checking
def add(a: int, b: int) -> int:
    return a + b
```

**Key Difference:**
- Java: Types enforced by compiler
- Python: Types are HINTS, not enforced at runtime
- Python with mypy: Types checked by external tool

---

## Important: Type Hints Don't Enforce!

```python
def add(a: int, b: int) -> int:
    return a + b

# This RUNS without error!
result = add("hello", "world")  # Returns "helloworld"
print(result)  # Works fine at runtime!
```

**Why?** Python is dynamically typed. Type hints are for:
- Tools (mypy, pyright, IDE)
- Developers (documentation)
- NOT for runtime enforcement

---

## Where to Use Type Hints

### 1. Function Parameters and Returns
```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

### 2. Variables
```python
age: int = 25
names: list[str] = ["Alice", "Bob"]
user: dict[str, int] = {"age": 25}
```

### 3. Class Attributes
```python
class User:
    name: str
    age: int
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
```

### 4. Instance Variables
```python
class Counter:
    def __init__(self):
        self.count: int = 0
```

---

## Common Type Hints

```python
# Basic types
name: str = "Alice"
age: int = 25
price: float = 19.99
is_active: bool = True

# Collections (Python 3.9+)
numbers: list[int] = [1, 2, 3]
names: set[str] = {"Alice", "Bob"}
scores: dict[str, int] = {"Alice": 95}
point: tuple[int, int] = (10, 20)

# Optional (can be None)
from typing import Optional
middle_name: Optional[str] = None
# OR (Python 3.10+)
middle_name: str | None = None

# Union (multiple types)
from typing import Union
id: Union[int, str] = 123
# OR (Python 3.10+)
id: int | str = 123

# Any (any type)
from typing import Any
data: Any = "could be anything"

# Callable (function type)
from typing import Callable
def execute(func: Callable[[int, int], int]) -> int:
    return func(10, 20)
```

---

## Tools to Check Type Hints

### 1. **mypy** (Most Popular)

```bash
pip install mypy
mypy your_script.py
```

**Example:**
```python
# bad_code.py
def add(a: int, b: int) -> int:
    return a + b

result = add("hello", "world")
```

```bash
$ mypy bad_code.py
bad_code.py:4: error: Argument 1 to "add" has incompatible type "str"; expected "int"
bad_code.py:4: error: Argument 2 to "add" has incompatible type "str"; expected "int"
```

### 2. **pyright** (Fast, Used by VS Code)

```bash
pip install pyright
pyright your_script.py
```

### 3. **pyre** (Facebook's Type Checker)

```bash
pip install pyre-check
pyre check
```

### 4. **pytype** (Google's Type Checker)

```bash
pip install pytype
pytype your_script.py
```

**Comparison:**

| Tool | Speed | Strictness | Best For |
|------|-------|-----------|----------|
| mypy | Medium | High | General use |
| pyright | Fast | High | VS Code users |
| pyre | Fast | Very High | Large codebases |
| pytype | Slow | Infers types | Existing code |

---

## IDE Integration

### VS Code
- Install Python extension
- Enable type checking: `"python.analysis.typeCheckingMode": "basic"`
- Shows errors inline!

### PyCharm
- Built-in type checking
- Automatic type hints suggestions
- Real-time error highlighting

### Vim/Neovim
- Install ALE or coc.nvim
- Configure mypy as linter

---

## Bad Examples (Why Types Help)

### Example 1: Runtime Error
```python
def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"]
    return total

# Crashes at runtime!
calculate_total([{"name": "Apple"}])  # KeyError: 'price'
```

**With types:**
```python
from typing import TypedDict

class Item(TypedDict):
    name: str
    price: float

def calculate_total(items: list[Item]) -> float:
    total = 0
    for item in items:
        total += item["price"]
    return total

# mypy catches this!
calculate_total([{"name": "Apple"}])  # Error: Missing key 'price'
```

### Example 2: Wrong Return Type
```python
def get_user_age(user_id):
    # Oops, returns string sometimes!
    if user_id == 0:
        return "Unknown"
    return 25

age = get_user_age(0)
next_year = age + 1  # TypeError at runtime!
```

**With types:**
```python
def get_user_age(user_id: int) -> int:
    if user_id == 0:
        return "Unknown"  # mypy error: Expected int, got str
    return 25
```

### Example 3: None Handling
```python
def find_user(name):
    if name in database:
        return database[name]
    return None

user = find_user("Alice")
print(user.email)  # AttributeError if None!
```

**With types:**
```python
def find_user(name: str) -> dict | None:
    if name in database:
        return database[name]
    return None

user = find_user("Alice")
print(user.email)  # mypy: Item "None" has no attribute "email"

# Forces you to handle None
if user is not None:
    print(user.email)  # Now safe!
```

---

## Best Practices

✅ **DO:**
- Add types to function signatures
- Use type hints for public APIs
- Run mypy in CI/CD
- Use strict mode for new projects

❌ **DON'T:**
- Don't use `Any` everywhere (defeats purpose)
- Don't ignore type errors without reason
- Don't over-complicate with complex types
- Don't add types to private helper functions (optional)

---

## Gradual Adoption

**Start small:**
```python
# 1. Start with function signatures
def process(data: list[int]) -> int:
    pass

# 2. Add variable types where helpful
result: int = process([1, 2, 3])

# 3. Gradually expand to whole codebase
```

**Use `# type: ignore` sparingly:**
```python
# When third-party library has no types
import some_library  # type: ignore
```

---

## Summary

| Aspect | Python | Java | TypeScript |
|--------|--------|------|------------|
| Types | Optional | Required | Optional |
| Checking | External tool | Compiler | Compiler |
| Runtime | No enforcement | Enforced | Transpiled to JS |
| Adoption | Gradual | All or nothing | Gradual |

**Key Points:**
- Type hints = better code, fewer bugs
- Not enforced at runtime (use mypy/pyright)
- Start with function signatures
- IDE support is excellent
- Gradual adoption possible