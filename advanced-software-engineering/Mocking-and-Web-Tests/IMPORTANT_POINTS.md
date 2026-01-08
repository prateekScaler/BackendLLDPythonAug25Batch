# Mocking & Testing - Important Points and Tidbits

## The Golden Rules of Mocking

### 1. Patch Where It's Used, Not Where It's Defined

```python
# module_a.py
from module_b import SomeClass

def do_something():
    obj = SomeClass()
    return obj.method()

# ❌ WRONG - Patching where defined
@patch('module_b.SomeClass')
def test_wrong(mock):
    pass

# ✅ CORRECT - Patching where used
@patch('module_a.SomeClass')
def test_correct(mock):
    pass
```

**Why?** When you `from x import y`, a reference to `y` is created in the importing module. Patching the original doesn't affect the imported reference.

---

### 2. Use `spec` or `autospec` to Catch Typos

```python
# Without spec - silent failures
mock = Mock()
mock.chrage(100)  # Typo! But test passes

# With spec - catches errors
mock = Mock(spec=PaymentGateway)
mock.chrage(100)  # AttributeError: 'chrage' not in spec
```

---

### 3. Don't Mock What You Don't Own (Usually)

```python
# ❌ Avoid mocking standard library internals
@patch('json.loads')  # Risky - json.loads is stable

# ✅ Mock your own abstractions
@patch('myapp.services.PaymentService')  # Better
```

---

### 4. Prefer Dependency Injection Over Patching

```python
# ❌ Hard to test - creates its own dependencies
class OrderService:
    def __init__(self):
        self.payment = PaymentGateway()  # Hard-coded!

# ✅ Easy to test - dependencies injected
class OrderService:
    def __init__(self, payment_gateway):
        self.payment = payment_gateway  # Inject mock in tests!
```

---

## Common Mocking Mistakes

### Mistake 1: Forgetting `return_value` for Instances

```python
# Creating mock of a CLASS
@patch('mymodule.SomeClass')
def test_something(MockClass):
    # MockClass is the CLASS, not an instance!

    # ❌ WRONG
    MockClass.some_method.return_value = "value"

    # ✅ CORRECT - use return_value to get instance
    MockClass.return_value.some_method.return_value = "value"
```

---

### Mistake 2: Not Resetting Mocks Between Tests

```python
# ❌ State leaks between tests
mock = Mock()

def test_one():
    mock.call_api()
    assert mock.call_api.call_count == 1  # ✅ Pass

def test_two():
    mock.call_api()
    assert mock.call_api.call_count == 1  # ❌ Fails! Count is 2

# ✅ Use fixtures with fresh mocks
@pytest.fixture
def fresh_mock():
    return Mock()
```

---

### Mistake 3: Over-Mocking (Testing Mocks, Not Code)

```python
# ❌ This test only tests the mock, not real behavior
def test_overmocked():
    service = Mock()
    service.calculate_total.return_value = 100

    result = service.calculate_total([10, 20, 30])

    assert result == 100  # Testing mock, not real logic!

# ✅ Mock dependencies, test YOUR code
def test_real_code():
    mock_db = Mock()
    mock_db.get_prices.return_value = [10, 20, 30]

    service = PricingService(db=mock_db)  # Real service
    result = service.calculate_total()     # Real method

    assert result == 60  # Testing real calculation
```

---

## Flaky Tests - Quick Reference

### Common Causes & Fixes

| Cause | Fix |
|-------|-----|
| **Time dependency** | Mock `datetime.now()` with freezegun |
| **Random data** | Seed random generators: `random.seed(42)` |
| **Race conditions** | Use locks, or test with `threading.Event` |
| **Test order dependency** | Use `setup/teardown` to reset state |
| **External services** | Mock all external calls |
| **Floating point** | Use `pytest.approx()` |
| **File system** | Use `tmp_path` fixture or mock |

### Quick Fixes

```python
# Time-dependent
from freezegun import freeze_time

@freeze_time("2024-01-15 10:00:00")
def test_time_sensitive():
    assert is_business_hours() == True

# Random-dependent
def test_random():
    random.seed(42)  # Deterministic
    result = get_random_item()
    assert result == expected

# Float comparison
def test_float():
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)

# Async wait
def test_async():
    # ❌ time.sleep(1)  # Arbitrary wait
    # ✅ Poll with timeout
    wait_until(lambda: condition, timeout=5)
```

---

## Test Doubles Cheat Sheet

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST DOUBLES                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DUMMY                                                      │
│  └── Placeholder, never actually used                       │
│      def test(dummy_logger):  # Don't care about logging    │
│                                                             │
│  STUB                                                       │
│  └── Returns canned answers                                 │
│      stub.get_user.return_value = User("John")              │
│                                                             │
│  SPY                                                        │
│  └── Records calls, uses real implementation                │
│      spy = create_autospec(real_service, wraps=real_service)│
│                                                             │
│  MOCK                                                       │
│  └── Verifies interactions                                  │
│      mock.send_email.assert_called_once()                   │
│                                                             │
│  FAKE                                                       │
│  └── Working but simplified implementation                  │
│      fake_db = InMemoryDatabase()                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Mock Assertion Cheat Sheet

```python
mock = Mock()

# Was it called?
mock.method.assert_called()              # At least once
mock.method.assert_called_once()         # Exactly once
mock.method.assert_not_called()          # Never called

# With what arguments?
mock.method.assert_called_with(1, 2, key="value")
mock.method.assert_called_once_with(1, 2)
mock.method.assert_any_call(1, 2)        # Among all calls

# How many times?
assert mock.method.call_count == 3

# What were the calls?
assert mock.method.call_args_list == [
    call(1),
    call(2),
    call(3),
]

# Last call arguments
args, kwargs = mock.method.call_args
```

---

## Web Testing Checklist

### For Each Endpoint Test:

- [ ] **Happy path** - Valid request returns expected response
- [ ] **Status codes** - 200, 201, 400, 401, 403, 404, 500
- [ ] **Validation errors** - Missing fields, invalid data
- [ ] **Authentication** - Unauthorized access blocked
- [ ] **Authorization** - Can't access others' resources
- [ ] **Edge cases** - Empty lists, null values, boundaries
- [ ] **Content type** - Response is JSON/expected type
- [ ] **Response structure** - All fields present

### HTTP Status Code Reference

```
2xx Success
├── 200 OK           - GET/PUT/PATCH success
├── 201 Created      - POST success (new resource)
└── 204 No Content   - DELETE success

4xx Client Errors
├── 400 Bad Request  - Validation error
├── 401 Unauthorized - Not authenticated
├── 403 Forbidden    - Authenticated but not allowed
├── 404 Not Found    - Resource doesn't exist
├── 409 Conflict     - Resource state conflict
└── 422 Unprocessable- Semantic validation error

5xx Server Errors
├── 500 Internal     - Unexpected server error
└── 503 Unavailable  - Service temporarily down
```

---

## Best Practices Summary

### DO ✅

1. **Mock external dependencies** (APIs, databases, email)
2. **Use dependency injection** for testability
3. **Keep tests fast** (< 100ms per unit test)
4. **Test one thing per test**
5. **Use descriptive test names**
6. **Reset state between tests**
7. **Use `spec` to catch API mismatches**

### DON'T ❌

1. **Don't mock the code under test**
2. **Don't mock everything** (over-mocking)
3. **Don't use `time.sleep`** (use polling/events)
4. **Don't share state between tests**
5. **Don't test implementation details**
6. **Don't ignore flaky tests** (fix them!)
7. **Don't use real external services**

---

## Quick Reference Commands

```bash
# Run tests
pytest                              # All tests
pytest test_file.py                 # Specific file
pytest -k "test_name"               # Match pattern
pytest -v                           # Verbose
pytest -x                           # Stop on first failure
pytest --lf                         # Rerun last failed

# Coverage
pytest --cov=src                    # Basic coverage
pytest --cov=src --cov-report=html  # HTML report
pytest --cov-fail-under=80          # Fail if < 80%

# Debugging
pytest --pdb                        # Debug on failure
pytest -s                           # Show print statements

# Parallel
pytest -n auto                      # Auto-detect CPUs (pytest-xdist)
```
