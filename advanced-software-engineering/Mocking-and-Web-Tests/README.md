# Mocking and Web/API Testing in Python

## Why Mocking?

```
┌─────────────────────────────────────────────────────────────┐
│              WITHOUT MOCKING                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Your Test ──► Real Database ──► Real API ──► Real Email   │
│                                                             │
│   Problems:                                                 │
│   ❌ Slow (network calls, DB queries)                       │
│   ❌ Flaky (network down, API rate limits)                  │
│   ❌ Side effects (sends real emails, charges cards!)       │
│   ❌ Hard to test edge cases (how to test "API down"?)      │
│   ❌ Expensive (external API costs per call)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                WITH MOCKING                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Your Test ──► Mock Database ──► Mock API ──► Mock Email   │
│                                                             │
│   Benefits:                                                 │
│   ✅ Fast (no I/O, runs in memory)                          │
│   ✅ Reliable (no external dependencies)                    │
│   ✅ Safe (no side effects)                                 │
│   ✅ Flexible (simulate any scenario: errors, timeouts)     │
│   ✅ Free (no API costs)                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## What is a Mock?

A **mock** is a fake object that simulates the behavior of a real object in controlled ways.

```python
# Real object (hits actual API)
response = payment_gateway.charge(card, amount)

# Mock object (simulates the API)
mock_gateway.charge.return_value = {"status": "success", "txn_id": "123"}
response = mock_gateway.charge(card, amount)
```

---

## Types of Test Doubles

| Type | Purpose | Example |
|------|---------|---------|
| **Mock** | Verify interactions (was method called?) | `mock.assert_called_with(...)` |
| **Stub** | Return canned responses | `stub.get_user.return_value = user` |
| **Fake** | Working implementation (simplified) | In-memory database |
| **Spy** | Records calls but uses real implementation | Audit logging |
| **Dummy** | Placeholder (never used) | Required parameter we don't care about |

---

## Python Mocking Tools

| Tool | Description |
|------|-------------|
| `unittest.mock` | Built-in Python mocking library |
| `pytest-mock` | pytest plugin wrapping unittest.mock |
| `responses` | Mock HTTP requests (for `requests` library) |
| `httpretty` | HTTP request mocking |
| `freezegun` | Mock datetime/time |
| `fakeredis` | In-memory Redis fake |

---

## Interactive Mocking Guide (Recommended)

```
┌─────────────────────────────────────────────────────────────┐
│  📚 VISUAL LEARNING: Interactive HTML Guide                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📁 mocking_guide/index.html                                │
│                                                             │
│  Open in your browser for an interactive learning           │
│  experience with:                                           │
│                                                             │
│  • 9 pages covering all mocking concepts                    │
│  • Syntax-highlighted code examples                         │
│  • Interactive quizzes on each topic                        │
│  • Visual diagrams and comparisons                          │
│  • Comprehensive cheat sheet                                │
│                                                             │
│  Topics covered:                                            │
│  1. Why Mocking? (The problem it solves)                    │
│  2. What is a Mock? (Mock basics & return_value)            │
│  3. MagicMock (For len, iter, context managers)             │
│  4. Patching (Decorator, context manager, pytest-mock)      │
│  5. Mock vs Patch (When to use which)                       │
│  6. side_effect (Dynamic behavior, exceptions)              │
│  7. unittest vs pytest (Comparing approaches)               │
│  8. spec & autospec (Catching typos & signature errors)     │
│  9. Cheat Sheet (Quick reference for all patterns)          │
│                                                             │
│  How to use:                                                │
│  Open mocking_guide/index.html in any browser               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Files in This Module

| File | Description |
|------|-------------|
| `mocking_guide/` | **Interactive HTML guide** - Open `index.html` in browser |
| `mocking_basics.py` | Core mocking concepts with examples |
| `test_mocking_basics.py` | Tests demonstrating mocking patterns |
| `web_api_testing.py` | Flask/FastAPI testing examples |
| `MOCKING_CONCEPTS.md` | Detailed mocking concepts & Mock vs Patch guide |
| `IMPORTANT_POINTS.md` | Key concepts and gotchas |
| `QUIZ_CLASS_2.md` | Quiz on mocking and patching topics |

---

## Quick Start

```bash
# Install dependencies
pip install pytest pytest-mock responses freezegun flask

# Run examples
python mocking_basics.py
pytest test_mocking_basics.py -v

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

---

## Key Concepts Covered

1. **Mocking Basics** - Mock, MagicMock, patch
2. **Patching** - Where to patch, context managers, decorators
3. **Return Values** - return_value, side_effect
4. **Assertions** - assert_called, assert_called_with, call_count
5. **Web Testing** - Test clients, request mocking
6. **Best Practices** - When to mock, when not to mock

---

## When to Mock vs When Not to Mock

```
✅ MOCK THESE:
├── External APIs (payment gateways, email services)
├── Database calls (in unit tests)
├── File system operations
├── Network requests
├── Time/date functions
└── Third-party services

❌ DON'T MOCK THESE:
├── The code you're testing (defeats the purpose!)
├── Simple data structures
├── Pure functions with no side effects
└── Everything (over-mocking makes tests brittle)
```
