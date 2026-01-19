# Unit Testing Learning Path - Start Here

## Directory Overview

This directory contains comprehensive materials for learning unit testing in Python. Follow the order below for the best learning experience.

---

## Learning Order

### Phase 1: Foundation (Start Here)

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Understand the Problem                             │
├─────────────────────────────────────────────────────────────┤
│  📄 problem_without_tests.py                                │
│                                                             │
│  What you'll learn:                                         │
│  • Why manual testing fails                                 │
│  • How bugs slip through without automated tests            │
│  • The scale problem with manual verification               │
│                                                             │
│  Run: python problem_without_tests.py                       │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Your First Unit Test                               │
├─────────────────────────────────────────────────────────────┤
│  📄 first_unit_test.py                                      │
│                                                             │
│  What you'll learn:                                         │
│  • unittest module basics                                   │
│  • Test class structure                                     │
│  • Common assertions                                        │
│  • setUp/tearDown methods                                   │
│  • The AAA pattern                                          │
│                                                             │
│  Run: python first_unit_test.py                             │
│       python -m unittest first_unit_test -v                 │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Best Practices                                     │
├─────────────────────────────────────────────────────────────┤
│  📄 best_practices_demo.py                                  │
│  📄 best_practices.md                                       │
│                                                             │
│  What you'll learn:                                         │
│  • Good vs bad test patterns                                │
│  • Descriptive naming conventions                           │
│  • Test isolation                                           │
│  • Testing behavior, not implementation                     │
│  • Edge case coverage                                       │
│                                                             │
│  Run: python -m unittest best_practices_demo -v             │
└─────────────────────────────────────────────────────────────┘
```

---

### Phase 2: Core Concepts

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Types of Testing                                   │
├─────────────────────────────────────────────────────────────┤
│  📄 TYPES_OF_TESTING.md                                     │
│                                                             │
│  What you'll learn:                                         │
│  • Unit vs Integration vs E2E tests                         │
│  • When to use each type                                    │
│  • Testing pyramid                                          │
│  • Examples for each type                                   │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: TDD (Test-Driven Development)                      │
├─────────────────────────────────────────────────────────────┤
│  📄 TDD_GUIDE.md                                            │
│  📄 tdd_example_user_service.py                             │
│  📄 test_tdd_example_user_service.py                        │
│                                                             │
│  What you'll learn:                                         │
│  • Red-Green-Refactor cycle                                 │
│  • Writing tests first                                      │
│  • Practical TDD example                                    │
│                                                             │
│  Run: pytest test_tdd_example_user_service.py -v            │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Flaky Tests                                        │
├─────────────────────────────────────────────────────────────┤
│  📄 FLAKY_TESTS.md                                          │
│                                                             │
│  What you'll learn:                                         │
│  • What makes tests flaky                                   │
│  • Common causes (race conditions, timing, etc.)            │
│  • How to fix flaky tests                                   │
│  • Tools for detection                                      │
└─────────────────────────────────────────────────────────────┘
```

---

### Phase 3: Production Readiness

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: CI/CD & Code Coverage                              │
├─────────────────────────────────────────────────────────────┤
│  📄 CICD_COVERAGE_RESOURCES.md                              │
│                                                             │
│  What you'll learn:                                         │
│  • Setting up pytest-cov                                    │
│  • GitHub Actions for automated testing                     │
│  • Coverage reports                                         │
│  • Open source repos to study                               │
│  • Platforms to practice                                    │
└─────────────────────────────────────────────────────────────┘
```

---

### Reference Materials (Use Anytime)

```
┌─────────────────────────────────────────────────────────────┐
│  REFERENCE: JUnit vs pytest Cheatsheet                      │
├─────────────────────────────────────────────────────────────┤
│  📄 JUNIT_VS_PYTEST_CHEATSHEET.md                           │
│                                                             │
│  For Java developers transitioning to Python:               │
│  • @Before/@After → fixtures                                │
│  • Assertion mappings                                       │
│  • Mocking comparison                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  REFERENCE: Main README                                     │
├─────────────────────────────────────────────────────────────┤
│  📄 README.md                                               │
│                                                             │
│  Quick reference for:                                       │
│  • Testing pyramid                                          │
│  • Common assertions                                        │
│  • AAA pattern                                              │
│  • Running tests                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick File Reference

| Order | File | Type | Description |
|-------|------|------|-------------|
| 1 | `problem_without_tests.py` | Python | Why we need tests |
| 2 | `first_unit_test.py` | Python | First unittest examples |
| 3 | `best_practices_demo.py` | Python | Good vs bad patterns |
| 3 | `best_practices.md` | Markdown | Best practices guide |
| 4 | `TYPES_OF_TESTING.md` | Markdown | All testing types explained |
| 5 | `TDD_GUIDE.md` | Markdown | TDD methodology |
| 5 | `tdd_example_user_service.py` | Python | TDD code example |
| 5 | `test_tdd_example_user_service.py` | Python | TDD test example |
| 6 | `FLAKY_TESTS.md` | Markdown | Handling flaky tests |
| 7 | `CICD_COVERAGE_RESOURCES.md` | Markdown | CI/CD & coverage |
| - | `JUNIT_VS_PYTEST_CHEATSHEET.md` | Markdown | Java → Python reference |
| - | `README.md` | Markdown | Quick reference |

---

## Running the Examples

### Using unittest (built-in)
```bash
# Run a specific file
python first_unit_test.py

# Run with verbose output
python -m unittest first_unit_test -v

# Run all tests in directory
python -m unittest discover -v
```

### Using pytest (recommended)
```bash
# Install pytest
pip install pytest pytest-cov

# Run a specific file
pytest first_unit_test.py -v

# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

### In PyCharm
1. Right-click any test file
2. Select **"Run 'Unittests in ...'"** or **"Run 'pytest in ...'"**

---

## Suggested Practice Order

1. **Day 1**: Files 1-3 (Foundation)
2. **Day 2**: File 4 (Types of Testing)
3. **Day 3**: File 5 (TDD - read guide, then study example)
4. **Day 4**: Files 6-7 (Flaky tests, CI/CD)
5. **Ongoing**: Practice on platforms listed in CICD_COVERAGE_RESOURCES.md

---

---

## Test Your Knowledge

```
┌─────────────────────────────────────────────────────────────┐
│  📝 QUIZ: Class 1 Assessment                                │
├─────────────────────────────────────────────────────────────┤
│  📄 QUIZ_CLASS_1.md                                         │
│                                                             │
│  Topics covered:                                            │
│  • Unit Testing Fundamentals                                │
│  • Best Practices & AAA Pattern                             │
│  • TDD (Red-Green-Refactor)                                 │
│  • Flaky Tests & Test Isolation                             │
│  • Testing Pyramid                                          │
│                                                             │
│  10 Questions with detailed explanations                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Need Help?

- For running tests in PyCharm, see `JUNIT_VS_PYTEST_CHEATSHEET.md`
- For CI/CD setup, see `CICD_COVERAGE_RESOURCES.md`
- For TDD practice platforms, see `CICD_COVERAGE_RESOURCES.md`

Happy Testing!
