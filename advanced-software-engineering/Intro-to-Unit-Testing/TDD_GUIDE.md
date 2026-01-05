# Test-Driven Development (TDD): A Practical Guide

## What is TDD?

**Test-Driven Development** is a software development practice where you write tests **before** writing the production code. It follows a simple but powerful cycle known as **Red-Green-Refactor**.

```
┌─────────────────────────────────────────────────────────────┐
│                    TDD Cycle                                │
│                                                             │
│     ┌──────────┐                                           │
│     │   RED    │  Write a failing test                     │
│     └────┬─────┘                                           │
│          │                                                  │
│          ▼                                                  │
│     ┌──────────┐                                           │
│     │  GREEN   │  Write minimum code to pass               │
│     └────┬─────┘                                           │
│          │                                                  │
│          ▼                                                  │
│     ┌──────────┐                                           │
│     │ REFACTOR │  Clean up, remove duplication             │
│     └────┬─────┘                                           │
│          │                                                  │
│          └──────────► Repeat                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Three Laws of TDD (by Robert C. Martin)

1. **You may not write production code until you have written a failing unit test.**
2. **You may not write more of a unit test than is sufficient to fail.**
3. **You may not write more production code than is sufficient to pass the currently failing test.**

---

## Why Practice TDD?

| Benefit | Description |
|---------|-------------|
| **Better Design** | Writing tests first forces you to think about the API before implementation |
| **Confidence** | Comprehensive test suite gives confidence to refactor |
| **Documentation** | Tests serve as living documentation of expected behavior |
| **Fewer Bugs** | Bugs are caught immediately when they're introduced |
| **Simpler Code** | You write only what's needed to pass tests |
| **Faster Debugging** | When a test fails, you know exactly what broke |

---

## How to Practice TDD: Step-by-Step

### Step 1: Understand the Requirement
Before writing any code, clearly understand what you need to build.

**Example Requirement**: Build a shopping cart that can:
- Add items with quantity
- Calculate total price
- Apply discount codes

### Step 2: Write the First Failing Test (RED)

Start with the simplest possible test case.

```python
# test_shopping_cart.py

def test_new_cart_is_empty():
    cart = ShoppingCart()
    assert cart.item_count() == 0
```

Run the test - it will fail because `ShoppingCart` doesn't exist yet.

```bash
$ pytest test_shopping_cart.py
FAILED - NameError: name 'ShoppingCart' is not defined
```

### Step 3: Write Minimum Code to Pass (GREEN)

Write just enough code to make the test pass.

```python
# shopping_cart.py

class ShoppingCart:
    def item_count(self):
        return 0
```

```bash
$ pytest test_shopping_cart.py
PASSED
```

### Step 4: Refactor (if needed)

Look for opportunities to improve the code without changing behavior. In this simple case, no refactoring is needed yet.

### Step 5: Write the Next Test

Continue the cycle with more tests.

```python
def test_add_item_increases_count():
    cart = ShoppingCart()
    cart.add_item("apple", price=1.50, quantity=2)
    assert cart.item_count() == 2
```

### Step 6: Repeat the Cycle

Continue until all requirements are met.

---

## TDD Example: Building a Calculator

Here's a complete TDD example showing the progression:

### Iteration 1: Basic Addition

```python
# RED: Write failing test
def test_add_two_numbers():
    calc = Calculator()
    assert calc.add(2, 3) == 5

# GREEN: Write minimum code
class Calculator:
    def add(self, a, b):
        return a + b

# REFACTOR: Nothing to refactor yet
```

### Iteration 2: Handle Negative Numbers

```python
# RED: New test case
def test_add_negative_numbers():
    calc = Calculator()
    assert calc.add(-2, -3) == -5

# GREEN: Already passes! Our implementation handles this.
```

### Iteration 3: Subtraction

```python
# RED: New functionality
def test_subtract_two_numbers():
    calc = Calculator()
    assert calc.subtract(5, 3) == 2

# GREEN: Add subtract method
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b
```

### Iteration 4: Division with Edge Case

```python
# RED: Division test
def test_divide_two_numbers():
    calc = Calculator()
    assert calc.divide(10, 2) == 5

# GREEN: Add divide
class Calculator:
    # ... previous methods ...
    def divide(self, a, b):
        return a / b

# RED: Edge case - division by zero
def test_divide_by_zero_raises_error():
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)

# GREEN: Handle edge case
class Calculator:
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

---

## TDD Patterns and Best Practices

### 1. Start Simple
Begin with the simplest possible test case, then add complexity gradually.

### 2. One Assert Per Test (Usually)
Each test should verify one specific behavior.

```python
# Good: Clear what failed
def test_cart_total_with_single_item():
    cart = ShoppingCart()
    cart.add_item("book", 10.00)
    assert cart.total() == 10.00

def test_cart_total_with_multiple_items():
    cart = ShoppingCart()
    cart.add_item("book", 10.00)
    cart.add_item("pen", 2.00)
    assert cart.total() == 12.00
```

### 3. Use Descriptive Test Names
Test names should describe the scenario and expected outcome.

```python
# Bad
def test_1():
    ...

# Good
def test_empty_cart_returns_zero_total():
    ...
```

### 4. Arrange-Act-Assert (AAA) Pattern

```python
def test_applying_discount_reduces_total():
    # Arrange
    cart = ShoppingCart()
    cart.add_item("laptop", 1000.00)

    # Act
    cart.apply_discount("SAVE10")  # 10% off

    # Assert
    assert cart.total() == 900.00
```

### 5. Test Behavior, Not Implementation
Focus on what the code does, not how it does it.

```python
# Bad: Tests implementation details
def test_items_stored_in_list():
    cart = ShoppingCart()
    cart.add_item("book", 10)
    assert isinstance(cart._items, list)  # Don't test private attributes!

# Good: Tests behavior
def test_added_item_appears_in_cart():
    cart = ShoppingCart()
    cart.add_item("book", 10)
    assert "book" in cart.get_items()
```

### 6. Write Tests for Edge Cases

```python
def test_empty_string_input():
    ...

def test_negative_quantity_raises_error():
    ...

def test_very_large_numbers():
    ...

def test_special_characters():
    ...
```

---

## Common TDD Mistakes to Avoid

### 1. Writing Too Much Test at Once
```python
# Bad: Testing too many things
def test_shopping_cart():
    cart = ShoppingCart()
    cart.add_item("a", 10)
    cart.add_item("b", 20)
    assert cart.item_count() == 2
    assert cart.total() == 30
    cart.apply_discount("HALF")
    assert cart.total() == 15
    cart.remove_item("a")
    assert cart.total() == 10
```

### 2. Writing Too Much Code at Once
Write only enough code to pass the current failing test.

### 3. Skipping the Refactor Step
Technical debt accumulates if you don't refactor.

### 4. Testing Private Methods
Test the public interface, not implementation details.

### 5. Not Running Tests Frequently
Run tests after every small change.

---

## TDD for Different Scenarios

### API Endpoint Testing

```python
def test_get_user_returns_user_data():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_nonexistent_user_returns_404():
    response = client.get("/api/users/99999")
    assert response.status_code == 404
```

### Database Operations

```python
def test_create_user_saves_to_database():
    user = create_user("john@example.com", "John Doe")

    saved_user = get_user_by_email("john@example.com")
    assert saved_user.name == "John Doe"
```

### Business Logic

```python
def test_premium_user_gets_discount():
    user = User(membership="premium")
    order = Order(user=user, amount=100)

    assert order.calculate_total() == 90  # 10% discount
```

---

## Recommended Reading

### Essential TDD Resources

1. **[Everything I Know About TDD](https://www.engineeringorg.com/everything-i-know-about-tdd/)**

   A comprehensive guide covering TDD fundamentals, practical tips, and real-world insights from experienced practitioners.

2. **[Everything I Know About Introducing TDD](https://www.engineeringorg.com/everything-i-know-about-introducing/)**

   Learn how to introduce TDD to your team or organization, overcome resistance, and build a testing culture.

### Books
- "Test-Driven Development: By Example" by Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" by Steve Freeman & Nat Pryce
- "Clean Code" by Robert C. Martin

---

## Practice Exercise

Try implementing these features using TDD:

1. **Password Validator**
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one number
   - At least one special character

2. **String Calculator**
   - Add numbers from a string: "1,2,3" → 6
   - Handle newlines as delimiters: "1\n2,3" → 6
   - Support custom delimiters: "//;\n1;2" → 3

3. **FizzBuzz**
   - Return "Fizz" for multiples of 3
   - Return "Buzz" for multiples of 5
   - Return "FizzBuzz" for multiples of both

---

## Quick Reference

```bash
# Run specific test
pytest test_file.py::test_function_name -v

# Run tests with coverage
pytest --cov=src tests/

# Run tests in watch mode (with pytest-watch)
ptw

# Run tests and stop on first failure
pytest -x

# Run tests matching a pattern
pytest -k "test_add"
```

---

## TDD Checklist

Before committing code, ask yourself:

- [ ] Did I write the test first?
- [ ] Does the test clearly describe the expected behavior?
- [ ] Did I see the test fail before writing the code?
- [ ] Did I write only enough code to pass the test?
- [ ] Did I refactor to remove duplication?
- [ ] Are all tests passing?
- [ ] Is the code clean and readable?

---

*"TDD is not about testing. It's about design, documentation, and confidence."*
