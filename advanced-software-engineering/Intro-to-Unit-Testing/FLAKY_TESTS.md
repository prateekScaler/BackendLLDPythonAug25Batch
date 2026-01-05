# Flaky Tests: Understanding, Identifying, and Fixing Them

## What are Flaky Tests?

A **flaky test** is a test that produces inconsistent results - sometimes passing, sometimes failing - without any changes to the code. They are one of the most frustrating issues in software testing because they erode trust in your test suite.

> "A test that sometimes passes and sometimes fails is worse than no test at all." - Common wisdom in testing

---

## Why Flaky Tests are Dangerous

1. **Erode Trust**: Developers start ignoring test failures
2. **Waste Time**: Hours spent debugging non-existent issues
3. **Slow Down CI/CD**: Pipelines need reruns, increasing build times
4. **Hide Real Bugs**: Real failures get dismissed as "just flaky"

---

## Common Causes of Flaky Tests

### 1. **Timing and Race Conditions**
Tests that depend on specific timing or async operations completing in a certain order.

```python
# FLAKY: Race condition
def test_async_operation():
    start_background_task()
    time.sleep(1)  # Hoping 1 second is enough...
    assert get_result() == expected  # Sometimes fails!
```

### 2. **Order Dependency**
Tests that pass only when run in a specific order because they share state.

```python
# FLAKY: Depends on test_a running first
class TestOrderDependent:
    shared_state = []

    def test_a(self):
        self.shared_state.append(1)
        assert len(self.shared_state) == 1

    def test_b(self):
        # Fails if test_a didn't run first!
        assert len(self.shared_state) == 1
```

### 3. **External Dependencies**
Tests relying on network, databases, or external services.

```python
# FLAKY: Network dependency
def test_fetch_user_data():
    response = requests.get("https://api.example.com/users/1")
    assert response.status_code == 200  # Network issues = flaky
```

### 4. **Time-Based Tests**
Tests that depend on current time, dates, or timezones.

```python
# FLAKY: Time-dependent
def test_is_morning():
    current_hour = datetime.now().hour
    # Passes only between 6 AM and 12 PM!
    assert is_morning() == (6 <= current_hour < 12)
```

### 5. **Random Data Without Seeds**
Tests using random data without controlling the seed.

```python
# FLAKY: Uncontrolled randomness
def test_random_selection():
    items = [1, 2, 3, 4, 5]
    selected = random.choice(items)
    assert selected == 3  # 20% chance of passing!
```

### 6. **Resource Leaks and Shared State**
Tests that don't properly clean up resources.

```python
# FLAKY: Resource leak
def test_file_operation():
    f = open("test.txt", "w")
    f.write("data")
    # Forgot to close! Next test might fail
```

### 7. **Floating Point Comparisons**
Comparing floating-point numbers without tolerance.

```python
# FLAKY: Floating point precision
def test_calculation():
    result = 0.1 + 0.2
    assert result == 0.3  # Actually 0.30000000000000004!
```

---

## Example: A Flaky Test File

```python
# flaky_examples.py
"""
This file demonstrates common flaky test patterns.
DO NOT use these patterns in production!
"""

import time
import random
import threading
from datetime import datetime


class Counter:
    """A non-thread-safe counter - source of flakiness"""
    def __init__(self):
        self.value = 0

    def increment(self):
        current = self.value
        time.sleep(0.001)  # Simulates some processing
        self.value = current + 1

    def get_value(self):
        return self.value


class DataProcessor:
    """Processes data with timing-sensitive operations"""
    def __init__(self):
        self.processed = False
        self.result = None

    def process_async(self, data):
        def _process():
            time.sleep(random.uniform(0.01, 0.1))  # Variable delay
            self.result = data.upper()
            self.processed = True

        thread = threading.Thread(target=_process)
        thread.start()

    def get_result(self):
        return self.result if self.processed else None


# Shared global state - recipe for flakiness
_cache = {}

def cache_value(key, value):
    _cache[key] = value

def get_cached_value(key):
    return _cache.get(key)

def clear_cache():
    _cache.clear()
```

---

## Example: Flaky Tests in Action

```python
# test_flaky_examples.py
"""
These tests demonstrate flaky behavior.
Run multiple times to see inconsistent results:
    pytest test_flaky_examples.py -v --count=10
"""

import pytest
import time
import random
import threading
from datetime import datetime
from flaky_examples import Counter, DataProcessor, cache_value, get_cached_value


class TestFlakyRaceCondition:
    """Demonstrates race condition flakiness"""

    def test_concurrent_counter(self):
        """FLAKY: Race condition causes inconsistent counts"""
        counter = Counter()
        threads = []

        for _ in range(10):
            t = threading.Thread(target=counter.increment)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Expected 10, but race condition means we might get less
        assert counter.get_value() == 10  # FLAKY!


class TestFlakyTiming:
    """Demonstrates timing-related flakiness"""

    def test_async_processing(self):
        """FLAKY: Timing assumption might fail"""
        processor = DataProcessor()
        processor.process_async("hello")

        time.sleep(0.05)  # Hoping this is enough...

        # Sometimes the processing takes longer!
        assert processor.get_result() == "HELLO"  # FLAKY!


class TestFlakySharedState:
    """Demonstrates shared state flakiness"""

    def test_cache_operation_a(self):
        """This test sets a cache value"""
        cache_value("key", "value_a")
        assert get_cached_value("key") == "value_a"

    def test_cache_operation_b(self):
        """FLAKY: Depends on test order and shared state"""
        # If test_a ran first, this might fail
        # If test_a didn't run, this might also fail differently
        cache_value("key", "value_b")
        assert get_cached_value("key") == "value_b"  # Might be "value_a"!


class TestFlakyTime:
    """Demonstrates time-dependent flakiness"""

    def test_is_business_hours(self):
        """FLAKY: Depends on when test runs"""
        current_hour = datetime.now().hour
        is_business = 9 <= current_hour < 17

        # This only passes during business hours!
        if is_business:
            assert self._check_something() == "business"  # FLAKY!

    def _check_something(self):
        return "business" if 9 <= datetime.now().hour < 17 else "off-hours"


class TestFlakyRandom:
    """Demonstrates randomness-related flakiness"""

    def test_random_without_seed(self):
        """FLAKY: Random without seed control"""
        result = random.randint(1, 10)
        # Only passes 10% of the time!
        assert result == 5  # FLAKY!


class TestFlakyFloatingPoint:
    """Demonstrates floating-point flakiness"""

    def test_float_equality(self):
        """FLAKY: Floating point precision issues"""
        result = 0.1 + 0.2
        # 0.1 + 0.2 = 0.30000000000000004 in floating point!
        assert result == 0.3  # FLAKY!
```

---

## How to Fix Flaky Tests

### 1. **Fix Race Conditions: Use Proper Synchronization**

```python
# FIXED: Thread-safe counter
import threading

class ThreadSafeCounter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.value += 1

def test_concurrent_counter_fixed():
    counter = ThreadSafeCounter()
    threads = []

    for _ in range(10):
        t = threading.Thread(target=counter.increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert counter.value == 10  # Now reliable!
```

### 2. **Fix Timing Issues: Use Polling with Timeouts**

```python
# FIXED: Poll with timeout instead of fixed sleep
import time

def wait_for_condition(condition_fn, timeout=5, interval=0.1):
    """Wait for a condition to be true with timeout"""
    start = time.time()
    while time.time() - start < timeout:
        if condition_fn():
            return True
        time.sleep(interval)
    return False

def test_async_processing_fixed():
    processor = DataProcessor()
    processor.process_async("hello")

    # Wait for processing to complete (with timeout)
    assert wait_for_condition(lambda: processor.processed, timeout=2)
    assert processor.get_result() == "HELLO"  # Reliable!
```

### 3. **Fix Shared State: Isolate Tests**

```python
# FIXED: Use fixtures for setup/teardown
import pytest

@pytest.fixture(autouse=True)
def clean_cache():
    """Clear cache before and after each test"""
    clear_cache()
    yield
    clear_cache()

def test_cache_isolated():
    cache_value("key", "value")
    assert get_cached_value("key") == "value"  # Isolated!
```

### 4. **Fix Time Dependencies: Mock Time**

```python
# FIXED: Mock the current time
from unittest.mock import patch
from datetime import datetime

def test_business_hours_fixed():
    # Test for business hours
    with patch('your_module.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2024, 1, 15, 10, 0)
        assert is_business_hours() == True

    # Test for off-hours
    with patch('your_module.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2024, 1, 15, 22, 0)
        assert is_business_hours() == False
```

### 5. **Fix Random: Seed Your Randomness**

```python
# FIXED: Control random seed
import random

def test_random_with_seed():
    random.seed(42)  # Fixed seed = reproducible results
    result = random.randint(1, 10)
    assert result == 2  # Always the same with seed 42!
```

### 6. **Fix Floating Point: Use Approximate Comparison**

```python
# FIXED: Use pytest.approx or math.isclose
import pytest
import math

def test_float_equality_fixed():
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)  # Works!
    assert math.isclose(result, 0.3)     # Also works!
```

### 7. **Fix External Dependencies: Use Mocks**

```python
# FIXED: Mock external calls
from unittest.mock import patch, Mock

def test_api_call_fixed():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"user": "test"}

    with patch('requests.get', return_value=mock_response):
        result = fetch_user_data(1)
        assert result == {"user": "test"}  # No network needed!
```

---

## Tools for Detecting Flaky Tests

### pytest-repeat
Run tests multiple times to detect flakiness:
```bash
pip install pytest-repeat
pytest --count=10 test_file.py
```

### pytest-randomly
Randomize test order to find order dependencies:
```bash
pip install pytest-randomly
pytest --randomly-seed=12345 test_file.py
```

### pytest-flakefinder
Specifically designed to find flaky tests:
```bash
pip install pytest-flakefinder
pytest --flake-finder --flake-runs=50 test_file.py
```

### flaky (Auto-retry decorator)
Automatically retry flaky tests:
```python
from flaky import flaky

@flaky(max_runs=3, min_passes=1)
def test_sometimes_fails():
    # Will retry up to 3 times
    pass
```

---

## Best Practices Summary

| Problem | Solution |
|---------|----------|
| Race conditions | Use locks, queues, or thread-safe structures |
| Timing issues | Poll with timeouts, not fixed sleeps |
| Shared state | Use fixtures, reset state in setup/teardown |
| Time dependencies | Mock datetime/time |
| Randomness | Seed your random generators |
| Floating point | Use `pytest.approx()` or `math.isclose()` |
| External services | Mock HTTP calls, use test doubles |
| File system | Use temp directories, clean up after tests |

---

## Further Reading

- [Google Testing Blog: Flaky Tests](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Martin Fowler: Eradicating Non-Determinism in Tests](https://martinfowler.com/articles/nonDeterminism.html)
