# Quiz: Unit Testing Fundamentals, Best Practices & TDD

Test your understanding of unit testing concepts covered in Class 1!

**Instructions**: Read each question carefully, think about your answer, then expand the solution to check.

---

## Question 1: The Mystery of the Failing Test

```python
import unittest

class Calculator:
    def divide(self, a, - B):
        return a / b

class TestCalculator(unittest.TestCase):
    def test_divide(self):
        calc = Calculator()
        result = calc.divide(10, 3)
        self.assertEqual(result, 3.33)

if __name__ == "__main__":
    unittest.main()
```

**Why does this test fail, and what's the best way to fix it?**

<details>
<summary>💡 Click to reveal answer</summary>
---
### Answer

**The test fails due to floating-point precision issues.**

`10 / 3 = 3.3333333333...` (repeating), not exactly `3.33`.

**Best fixes:**

```python
# Option 1: Use assertAlmostEqual (preferred for floats)
self.assertAlmostEqual(result, 3.33, places=2)

# Option 2: Use pytest.approx (if using pytest)
assert result == pytest.approx(3.33, rel=0.01)

# Option 3: Round the result
self.assertEqual(round(result, 2), 3.33)
```

**Key Lesson**: Never use `assertEqual` for floating-point comparisons. This is also a common cause of **flaky tests** - tests that pass sometimes and fail others due to floating-point inconsistencies across different machines.

</details>

---

## Question 2: Spot the Code Smell

```python
def test_user_registration_flow():
    # Create user
    user = UserService().create_user("john@example.com", "password123")
    assert user.id is not None

    # Login
    token = AuthService().login("john@example.com", "password123")
    assert token is not None

    # Update profile
    updated = ProfileService().update_profile(user.id, {"name": "John"})
    assert updated.name == "John"

    # Delete user
    result = UserService().delete_user(user.i- D)
    assert result == True
```

**What best practice violation(s) do you see in this test? Select all that apply:**

- A) Test name is not descriptive enough
- B) Testing multiple behaviors in one test
- C) Not following AAA pattern
- D) Missing teardown

<details>
<summary>💡 Click to reveal answer</summary>

---
### Answer: **B, C, and D**

**- B) Testing multiple behaviors in one test** ✅
- This test validates 4 separate operations: create, login, update, delete
- If it fails, you don't know which operation caused the failure
- Should be split into 4 separate tests

**- C) Not following AAA pattern** ✅
- The test mixes Arrange, Act, and Assert throughout
- Proper AAA: Setup all data → Perform ONE action → Assert results

**- D) Missing teardown** ✅
- If a test fails midway, the user remains in the database
- Can cause other tests to fail (shared state problem)

**- A) is debatable** - the name describes what it tests, though `test_user_crud_operations` might be clearer

**Refactored version:**
```python
class TestUserRegistration:
    @pytest.fixture
    def user_service(self):
        return UserService()

    def test_create_user_returns_user_with_id(self, user_service):
        # Arrange - nothing needed

        # Act
        user = user_service.create_user("john@example.com", "password123")

        # Assert
        assert user.id is not None
```

</details>

---

## Question 3: TDD Red-Green-Refactor

You're practicing TDD and need to implement a function that checks if a string is a palindrome.

**In TDD, what should be your FIRST step?**

- A) Write the `is_palindrome()` function with full implementation
- B) Write a failing test for `is_palindrome()`
- C) Create a code skeleton with `pass` in the function body
- D) Write documentation for how the function should work

<details>
<summary>💡 Click to reveal answer</summary>
---
### Answer: **- B) Write a failing test for `is_palindrome()`**

**TDD follows Red-Green-Refactor:**

1. **RED** 🔴: Write a failing test FIRST
   ```python
   def test_palindrome_with_valid_palindrome():
       assert is_palindrome("madam") == True
   ```
   This test will fail because `is_palindrome` doesn't exist yet!

2. **GREEN** 🟢: Write MINIMAL code to make the test pass
   ```python
   def is_palindrome(s):
       return s == s[::-1]
   ```

3. **REFACTOR** 🔵: Improve the code while keeping tests green

**Uncle Bob's Three Laws of TDD:**
1. Don't write production code until you have a failing test
2. Don't write more test than is sufficient to fail
3. Don't write more production code than is sufficient to pass

</details>

---

## Question 4: The Flaky Test Detective

Your CI/CD pipeline shows this test passes 90% of the time but fails randomly:

```python
def test_order_processing_time():
    start = time.time()
    result = process_order(order_dat- A)
    end = time.time()

    assert result.status == "completed"
    assert (end - start) < 2.0  # Should complete in under 2 seconds
```

**What is the MOST likely cause of flakiness, and how would you fix it?**

<details>
<summary>💡 Click to reveal answer</summary>
---
### Answer: **Timing/Performance Dependency**

**Problem**: The test asserts on execution time, which varies based on:
- System load
- CPU availability
- Network latency (if `process_order` makes external calls)
- CI/CD runner resources

**Fixes:**

```python
# Fix 1: Remove timing assertion from unit test (preferre- D)
def test_order_processing_completes():
    result = process_order(order_dat- A)
    assert result.status == "completed"
    # Move performance testing to dedicated load tests

# Fix 2: Use more generous timeout with retries
@pytest.mark.timeout(10)  # Generous timeout
def test_order_processing_time():
    result = process_order(order_dat- A)
    assert result.status == "completed"

# Fix 3: Mock slow external dependencies
def test_order_processing(mocker):
    mocker.patch('services.payment_gateway.charge', return_value=True)
    result = process_order(order_dat- A)
    assert result.status == "completed"
```

**Key Lesson**: Unit tests should test **correctness**, not **performance**. Performance tests belong in a separate test suite run in controlled environments.

</details>

---

## Question 6: Setup/Teardown Puzzle

```python
import unittest

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("A")
        cls.connection = create_db_connection()

    def setUp(self):
        print("B")
        self.transaction = self.connection.begin()

    def test_insert(self):
        print("C")

    def test_update(self):
        print("D")

    def tearDown(self):
        print("E")
        self.transaction.rollback()

    @classmethod
    def tearDownClass(cls):
        print("F")
        cls.connection.close()
```

**What is the output when running both tests?**

<details>
<summary>💡 Click to reveal answer</summary>
---
### Answer

```
A
B
C
E
B
D
E
F
```

**Explanation:**

1. `setUpClass` runs **once** before all tests → `A`
2. For `test_insert`:
   - `setUp` runs → `B`
   - Test runs → `C`
   - `tearDown` runs → `E`
3. For `test_update`:
   - `setUp` runs → `B`
   - Test runs → `D`
   - `tearDown` runs → `E`
4. `tearDownClass` runs **once** after all tests → `F`

**Key Pattern:**
```
setUpClass (once)
    setUp → test1 → tearDown
    setUp → test2 → tearDown
    setUp → test3 → tearDown
tearDownClass (once)
```

**pytest equivalent:**
```python
@pytest.fixture(scope="class")  # setUpClass
@pytest.fixture(scope="function")  # setUp (default)
@pytest.fixture(scope="module")  # Once per file
@pytest.fixture(scope="session")  # Once per test run
```

</details>

---

## Question 7: Test Isolation Gone Wrong

```python
class ShoppingCart:
    items = []  # Class variable!

    def add_item(self, item):
        self.items.append(item)

    def get_total_items(self):
        return len(self.items)

class TestShoppingCart(unittest.TestCase):
    def test_add_single_item(self):
        cart = ShoppingCart()
        cart.add_item("Apple")
        self.assertEqual(cart.get_total_items(), 1)

    def test_add_multiple_items(self):
        cart = ShoppingCart()
        cart.add_item("Banana")
        cart.add_item("Orange")
        self.assertEqual(cart.get_total_items(), 2)
```

**These tests pass individually but fail when run together. Why?**

<details>
<summary>💡 Click to reveal answer</summary>
---
### Answer: **Shared State via Class Variable**

**The Bug**: `items = []` is a **class variable**, shared across ALL instances!

```python
# Test 1 runs: items = ["Apple"] → passes (1 item)
# Test 2 runs: items = ["Apple", "Banana", "Orange"] → FAILS! (3 items, expected 2)
```

**This violates Test Isolation** - tests should not affect each other.

**Fixes:**

```python
# Fix 1: Use instance variable (proper OOP)
class ShoppingCart:
    def __init__(self):
        self.items = []  # Instance variable - unique per object

    def add_item(self, item):
        self.items.append(item)

# Fix 2: Clear state in setUp (if class variable is intentional)
class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        ShoppingCart.items = []  # Reset before each test
```

**Key Lesson**: This is one of the top causes of **flaky tests** - shared mutable state. Always ensure:
- Each test starts with clean state
- Tests don't depend on execution order
- Use fixtures to create fresh instances

</details>

---

## Question 8: TDD Kata Challenge

You're building a `StringCalculator` using TDD. The requirements are:
- `add("")` returns `0`
- `add("1")` returns `1`
- `add("1,2")` returns `3`

Following TDD, you write this first test:

```python
def test_empty_string_returns_zero():
    calc = StringCalculator()
    assert calc.add("") == 0
```
**What is the MINIMUM code to make this test pass?**

- A)
```python
class StringCalculator:
    def add(self, numbers):
        if numbers == "":
            return 0
        return sum(int(n) for n in numbers.split(","))
```

- B)
```python
class StringCalculator:
    def add(self, numbers):
        return 0
```

- C)
```python
class StringCalculator:
    def add(self, numbers):
        if not numbers:
            return 0
        return None
```


<details>
<summary>💡 Click to reveal answer</summary>
---
### Answer: **- B)**

```python
class StringCalculator:
    def add(self, numbers):
        return 0
```

**TDD Rule**: Write the **minimum code** to make the test pass. Nothing more!

- **Option A** is over-engineering - it handles cases we haven't tested yet
- **Option B** is correct - it makes the test pass with minimal code
- **Option C** handles the case but adds unnecessary complexity

**The TDD Journey:**

```python
# Test 1: add("") → 0
# Implementation: return 0

# Test 2: add("1") → 1
# Implementation: return int(numbers) if numbers else 0

# Test 3: add("1,2") → 3
# Implementation: full split and sum logic
```

**Why this matters**: TDD prevents over-engineering. You only write code that's proven necessary by a failing test.

</details>

---

## Question 9: The Testing Pyramid

```
        /\
       /  \
      / ?? \
     /______\
    /        \
   /    ??    \
  /____________\
 /              \
/       ??       \
\________________/
```

**Fill in the testing pyramid from bottom to top, and explain why this shape matters:**

<details>
<summary>💡 Click to reveal answer</summary>
---
### Answer

```
        /\
       /  \
      / E2E\        ← Few, Slow, Expensive
     /______\
    /        \
   /Integration\    ← Some, Medium speed
  /____________\
 /              \
/   Unit Tests   \  ← Many, Fast, Cheap
\________________/
```

**The Pyramid Shape Matters Because:**

| Level | Count | Speed | Cost | What it Tests |
|-------|-------|-------|------|---------------|
| **E2E** | Few (5-10%) | Slow (seconds-minutes) | Expensive | Full user journeys |
| **Integration** | Some (15-25%) | Medium (ms-seconds) | Medium | Component interactions |
| **Unit** | Many (70-80%) | Fast (ms) | Cheap | Individual functions/classes |

**Why More Unit Tests?**
1. **Fast feedback** - Run in milliseconds
2. **Easy to debug** - Failures point to exact location
3. **Cheap to write/maintain** - No external dependencies
4. **Stable** - Don't break due to UI/network changes

**Anti-pattern: Ice Cream Cone** 🍦
```
    Manual Testing
   ________________
  /                \
 /       E2E        \
/____________________\
\   Integration      /
 \ Unit Tests (few) /
  \_________________/
```
This is expensive, slow, and fragile!

</details>

---

## Next Steps
1. Practice TDD with the kata in `tdd_example_user_service.py`
2. Run the tests in `best_practices_demo.py` and study them
3. Move to Class 2: **Mocking, Patching & Web Testing**
