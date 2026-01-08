# Mocking and Web Tests - Start Here

## Learning Path

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Why Mocking? (Theory)                              │
│  📄 MOCKING_CONCEPTS.md                                     │
│  Complete guide: Mock, Patch, Side Effects, Assertions      │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Understand the Code to Test                        │
│  📄 README.md (overview)                                    │
│  📄 mocking_basics.py (read the e-commerce code)            │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Learn Mocking Patterns (Hands-on)                  │
│  📄 test_mocking_basics.py                                  │
│  Run: pytest test_mocking_basics.py -v                      │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Web/API Testing                                    │
│  📄 web_api_testing.py                                      │
│  Run: pytest web_api_testing.py -v                          │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Important Points & Best Practices                  │
│  📄 IMPORTANT_POINTS.md                                     │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Test Your Knowledge                                │
│  📄 QUIZ_CLASS_2.md                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick File Reference

| File | Type | Description |
|------|------|-------------|
| `MOCKING_CONCEPTS.md` | Markdown | Complete mocking guide (start here!) |
| `README.md` | Markdown | Overview of mocking concepts |
| `mocking_basics.py` | Python | E-commerce service with external deps |
| `test_mocking_basics.py` | Python | Comprehensive mocking test examples |
| `web_api_testing.py` | Python | Flask API testing examples |
| `IMPORTANT_POINTS.md` | Markdown | Key concepts, gotchas, cheat sheets |
| `QUIZ_CLASS_2.md` | Markdown | Interactive quiz (10 questions) |

---

## Running the Examples

```bash
# Install dependencies
pip install pytest pytest-mock flask freezegun

# Run mocking tests
pytest test_mocking_basics.py -v

# Run web API tests
pytest web_api_testing.py -v

# Run all tests with coverage
pytest --cov=. --cov-report=term-missing -v
```

---

## Prerequisites

Before this module, you should understand:
- Basic unit testing (`unittest` or `pytest`)
- Python classes and functions
- What external dependencies are (databases, APIs)

See: `../Intro-to-Unit-Testing/` for fundamentals.
