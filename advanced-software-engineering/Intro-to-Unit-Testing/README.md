# Introduction to Unit Testing in Python

## What is Testing?

Testing is the process of **verifying that your code behaves as expected**. Instead of assuming your code works, you prove it works.

```
┌─────────────────────────────────────────────────────────────┐
│                     WITHOUT TESTING                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Write Code ──► "Looks good" ──► Deploy ──► 💥 BUG!       │
│                                                             │
│   Discovery: In Production (by users)                       │
│   Cost: High (reputation, money, time)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      WITH TESTING                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Write Code ──► Run Tests ──► Fix ──► Deploy ──► ✅       │
│                       │                                     │
│                       ▼                                     │
│                  ❌ Fail? Fix before deploy                 │
│                                                             │
│   Discovery: Before Production                              │
│   Cost: Low (just developer time)                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Manual Testing vs Automated Testing

### Manual Testing
```
┌──────────────────────────────────────┐
│           MANUAL TESTING             │
├──────────────────────────────────────┤
│                                      │
│  1. Run program                      │
│  2. Type inputs manually             │
│  3. Check output with eyes           │
│  4. Repeat for each scenario         │
│                                      │
│  Problems:                           │
│  ❌ Time consuming                   │
│  ❌ Human error prone                │
│  ❌ Not repeatable consistently      │
│  ❌ Skipped under deadline pressure  │
│                                      │
└──────────────────────────────────────┘
```

### Automated Testing
```
┌──────────────────────────────────────┐
│         AUTOMATED TESTING            │
├──────────────────────────────────────┤
│                                      │
│  1. Write test code ONCE             │
│  2. Run anytime: python -m unittest  │
│  3. Executes in seconds              │
│  4. Same result every time           │
│                                      │
│  Benefits:                           │
│  ✅ Fast (runs in milliseconds)      │
│  ✅ Consistent & reliable            │
│  ✅ Catches regressions              │
│  ✅ Documents expected behavior      │
│                                      │
└──────────────────────────────────────┘
```

---

## What is Unit Testing?

Unit testing tests the **smallest testable unit** of code — typically a single function or method.

```
┌─────────────────────────────────────────────────────────────┐
│                    TESTING PYRAMID                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                        /\                                   │
│                       /  \      E2E Tests                   │
│                      /    \     (Few, Slow)                 │
│                     /──────\                                │
│                    /        \   Integration Tests           │
│                   /          \  (Some, Medium)              │
│                  /────────────\                             │
│                 /              \                            │
│                / UNIT TESTS     \  ◄── We focus here        │
│               /  (Many, Fast)    \                          │
│              /____________________\                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Unit Test Characteristics
- **Fast**: Runs in milliseconds
- **Isolated**: No database, no network, no file system
- **Deterministic**: Same input = same output, always
- **Focused**: Tests ONE thing

---

## Python Testing Tools

| Tool | Description |
|------|-------------|
| `unittest` | Built-in Python module (we'll use this) |
| `pytest` | Popular third-party tool (industry favorite) |
| `doctest` | Tests embedded in docstrings |

---

## Anatomy of a Unit Test

```python
import unittest
from calculator import add

class TestCalculator(unittest.TestCase):    # Test class

    def test_add_positive_numbers(self):    # Test method (must start with test_)
        result = add(2, 3)                  # Act
        self.assertEqual(result, 5)         # Assert

if __name__ == "__main__":
    unittest.main()                         # Test runner
```

---

## Common Assertions

| Assertion | Purpose |
|-----------|---------|
| `assertEqual(a, b)` | Check `a == b` |
| `assertNotEqual(a, b)` | Check `a != b` |
| `assertTrue(x)` | Check `x` is True |
| `assertFalse(x)` | Check `x` is False |
| `assertIsNone(x)` | Check `x` is None |
| `assertIsNotNone(x)` | Check `x` is not None |
| `assertRaises(Error)` | Check exception is raised |
| `assertIn(a, b)` | Check `a` in `b` |

---

## Test Structure: AAA Pattern

Every test should follow the **Arrange-Act-Assert** pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                     AAA PATTERN                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐                                                │
│  │ ARRANGE │  Setup test data and preconditions            │
│  └────┬────┘                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────┐                                                │
│  │   ACT   │  Execute the code being tested                │
│  └────┬────┘                                                │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────┐                                                │
│  │ ASSERT  │  Verify the result is correct                 │
│  └─────────┘                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```python
def test_add_numbers(self):
    # Arrange
    a, b = 3, 4

    # Act
    result = add(a, b)

    # Assert
    self.assertEqual(result, 7)
```

---

## Running Tests

```bash
# Run a specific test file
python test_calculator.py

# Run using unittest discovery
python -m unittest discover

# Run with verbose output
python -m unittest -v test_calculator
```

---

## Files in This Module

| File | Description |
|------|-------------|
| `problem_without_tests.py` | Shows why manual testing doesn't scale |
| `first_unit_test.py` | Your first unit test with unittest |
| `best_practices_demo.py` | Good vs bad testing practices |
| `best_practices.md` | Detailed best practices guide |

---

## Key Takeaway

> "Code without tests works today. Code with tests works tomorrow."

Testing isn't extra work — it's **insurance** for your codebase.
