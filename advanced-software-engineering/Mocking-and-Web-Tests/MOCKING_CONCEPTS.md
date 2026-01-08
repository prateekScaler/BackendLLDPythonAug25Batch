# Mocking in Python: A Complete Guide

## Table of Contents
1. [Why Do We Need Mocking?](#1-why-do-we-need-mocking)
2. [The Problem Without Mocks](#2-the-problem-without-mocks)
3. [Mock and MagicMock Basics](#3-mock-and-magicmock-basics)
4. [Patching: Replacing Real Objects](#4-patching-replacing-real-objects)
   - 4.4 [Mock vs patch: When to Use Which?](#44-mock-vs-patch-when-to-use-which) (KEY SECTION)
5. [Return Values and Side Effects](#5-return-values-and-side-effects)
6. [Assertions on Mock Calls](#6-assertions-on-mock-calls)
7. [Spec and Autospec: Catching Mistakes](#7-spec-and-autospec-catching-mistakes)
8. [Real-World Testing Patterns](#8-real-world-testing-patterns)

---

## 1. Why Do We Need Mocking?

### The Context

In real applications, your code doesn't work in isolation. It depends on:
- **Databases** - to store and retrieve data
- **External APIs** - payment gateways, email services, SMS providers
- **File systems** - reading config files, writing logs
- **Network services** - other microservices, third-party integrations

### The Problem

When writing **unit tests**, we want to test **our code**, not these external dependencies. But:

```python
class OrderService:
    def place_order(self, order):
        # Calls real payment gateway - charges real money!
        result = PaymentGateway().charge(order.card, order.amount)

        # Sends real email
        EmailService().send("Order confirmed!")

        return result
```

If we test this directly:
- We charge **real money** on every test run
- We send **real emails** to customers
- Tests are **slow** (network calls)
- Tests are **flaky** (network failures)
- Tests **fail** when external services are down

### The Solution: Mocking

**Mocking** = Replacing real objects with fake ones that we control.

```python
# Instead of real PaymentGateway:
mock_gateway = Mock()
mock_gateway.charge.return_value = {"status": "success"}

# Now our test uses the fake gateway - no real charges!
```

---

## 2. The Problem Without Mocks

### Real Dependencies Are Problematic

```
┌─────────────────┐     ┌─────────────────┐
│   OrderService  │────▶│  PaymentGateway │ ← Real API, real money!
│   (Our Code)    │     │  (External)     │
└─────────────────┘     └─────────────────┘
         │
         │              ┌─────────────────┐
         └─────────────▶│   EmailService  │ ← Sends real emails!
                        │   (External)    │
                        └─────────────────┘
```

### Issues with Testing Real Dependencies

| Problem | Impact |
|---------|--------|
| **Cost** | Payment gateway charges real money |
| **Side effects** | Emails sent to real customers |
| **Speed** | Network calls take 100-500ms each |
| **Reliability** | External service downtime = test failure |
| **Data pollution** | Test data in production databases |

### With Mocks: Clean Isolation

```
┌─────────────────┐     ┌─────────────────┐
│   OrderService  │────▶│   Mock Gateway  │ ← Fake! Returns what we tell it
│   (Our Code)    │     │   (Controlled)  │
└─────────────────┘     └─────────────────┘
         │
         │              ┌─────────────────┐
         └─────────────▶│   Mock Email    │ ← Fake! No emails sent
                        │   (Controlled)  │
                        └─────────────────┘
```

---

## 3. Mock and MagicMock Basics

### 3.1 Creating a Mock

```python
from unittest.mock import Mock

mock = Mock()
```

### 3.2 Mocks Accept Any Attribute/Method

A Mock object **doesn't complain** about anything - it just works:

```python
mock = Mock()

# These all work - Mock doesn't care!
mock.foo                    # Returns another Mock
mock.bar.baz               # Returns another Mock
mock.any_method()          # Returns another Mock
mock.calculate(1, 2, 3)    # Returns another Mock
```

**Why?** This flexibility lets you mock any object without defining its structure upfront.

### 3.3 Configuring Return Values

```python
mock = Mock()

# Configure what the mock returns
mock.get_user.return_value = {"id": 1, "name": "John"}

# Now calling it returns our configured value
result = mock.get_user(user_id=1)
print(result)  # {"id": 1, "name": "John"}
```

### 3.4 Nested Return Values

```python
mock = Mock()

# Configure nested structure
mock.db.query.execute.return_value = [{"id": 1}, {"id": 2}]

# Access nested mock
result = mock.db.query.execute()
print(result)  # [{"id": 1}, {"id": 2}]
```

### 3.5 Mock vs MagicMock

| Feature | Mock | MagicMock |
|---------|------|-----------|
| Basic attributes | Yes | Yes |
| Method calls | Yes | Yes |
| Magic methods (`__len__`, `__iter__`) | No | Yes |
| Context managers (`__enter__`, `__exit__`) | No | Yes |

```python
from unittest.mock import Mock, MagicMock

# Mock doesn't support magic methods
mock = Mock()
# len(mock)  # TypeError!

# MagicMock supports them
magic = MagicMock()
magic.__len__.return_value = 5
print(len(magic))  # 5

# Iteration
magic.__iter__.return_value = iter([1, 2, 3])
print(list(magic))  # [1, 2, 3]
```

**Rule of thumb**: Use `MagicMock` when you need `len()`, iteration, or context managers. Otherwise, `Mock` is fine.

---

## 4. Patching: Replacing Real Objects

### 4.1 What is Patching?

**Patching** = Temporarily replacing a real object with a mock during a test.

```python
# Real code
from external import PaymentGateway

# During test, PaymentGateway becomes our mock
# After test, it's restored to the real class
```

### 4.2 Three Ways to Patch

#### Method 1: Decorator

```python
from unittest.mock import patch

@patch('mymodule.PaymentGateway')
def test_payment(mock_gateway_class):
    mock_gateway_class.return_value.charge.return_value = {"status": "success"}

    # Test code here
    result = process_payment()

    assert result == "success"
```

#### Method 2: Context Manager

```python
def test_payment():
    with patch('mymodule.PaymentGateway') as mock_gateway_class:
        mock_gateway_class.return_value.charge.return_value = {"status": "success"}

        result = process_payment()

        assert result == "success"
```

#### Method 3: patch.object (For Specific Instances)

```python
def test_payment():
    gateway = PaymentGateway()

    with patch.object(gateway, 'charge', return_value={"status": "mocked"}):
        result = gateway.charge("1234", 100)
        assert result == {"status": "mocked"}

    # After the 'with' block, original method is restored
```

### 4.3 Critical Rule: Patch Where USED, Not Where DEFINED

This is the **most common mistake** in mocking!

```python
# payment_gateway.py
class PaymentGateway:
    def charge(self, amount):
        # Real implementation
        pass

# order_service.py
from payment_gateway import PaymentGateway  # Imports here!

class OrderService:
    def process(self):
        gateway = PaymentGateway()
        return gateway.charge(100)
```

**Wrong:**
```python
@patch('payment_gateway.PaymentGateway')  # Where it's DEFINED
def test_order(mock):
    # This won't work! order_service already has its own reference
```

**Correct:**
```python
@patch('order_service.PaymentGateway')  # Where it's USED
def test_order(mock):
    # This works!
```

**Why?** When `order_service.py` does `from payment_gateway import PaymentGateway`, it creates a **copy** of the reference in its own namespace. You must patch that namespace.

---

## 4.4 Mock vs patch: When to Use Which?

This is one of the most confusing aspects of mocking. Here's a clear comparison:

### Decision Table

| Scenario | Use Mock | Use patch |
|----------|----------|-----------|
| Dependency is **injected** via constructor/method | Yes | No |
| Dependency is **created inside** the function | No | Yes |
| You **control** how the object is passed | Yes | No |
| Code uses **hardcoded** `ClassName()` internally | No | Yes |
| Testing a **standalone function** with imports | No | Yes |
| You have an **existing instance** to modify | `patch.object` | - |

### The Key Question

> **"Can I pass the fake object into my code?"**
> - **YES** → Use `Mock()` directly
> - **NO** → Use `patch()` to intercept

---

### Example 1: Use Mock (Dependency Injection)

```python
# Code with dependency injection - EASY TO TEST
class OrderService:
    def __init__(self, payment_gateway):  # Dependency injected!
        self.gateway = payment_gateway

    def checkout(self, amount):
        return self.gateway.charge(amount)
```

**Test with Mock:**
```python
def test_checkout_with_mock():
    # Create mock
    mock_gateway = Mock()
    mock_gateway.charge.return_value = {"status": "success"}

    # Inject mock directly - no patch needed!
    service = OrderService(payment_gateway=mock_gateway)

    # Test
    result = service.checkout(100)

    assert result["status"] == "success"
    mock_gateway.charge.assert_called_once_with(100)
```

**Why Mock works here:** You control how `payment_gateway` is provided, so you just pass your mock directly.

---

### Example 2: Use patch (Hardcoded Dependency)

```python
# Code WITHOUT dependency injection - HARDER TO TEST
class OrderService:
    def checkout(self, amount):
        gateway = PaymentGateway()  # Created inside! Can't inject!
        return gateway.charge(amount)
```

**Test with patch:**
```python
@patch('order_service.PaymentGateway')  # Intercept the class
def test_checkout_with_patch(mock_gateway_class):
    # Configure the mock instance that will be created
    mock_instance = mock_gateway_class.return_value
    mock_instance.charge.return_value = {"status": "success"}

    # Test - patch intercepts PaymentGateway() call
    service = OrderService()
    result = service.checkout(100)

    assert result["status"] == "success"
    mock_instance.charge.assert_called_once_with(100)
```

**Why patch is needed:** You can't pass a mock because the code creates `PaymentGateway()` internally. `patch` intercepts that creation.

---

### Side-by-Side Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                    MOCK (Direct Injection)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   # Your code                                                   │
│   class Service:                                                │
│       def __init__(self, dependency):  ← You pass it in        │
│           self.dep = dependency                                 │
│                                                                 │
│   # Your test                                                   │
│   mock = Mock()                                                 │
│   service = Service(mock)  ← Direct injection                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    PATCH (Intercept Creation)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   # Your code                                                   │
│   class Service:                                                │
│       def do_something(self):                                   │
│           dep = Dependency()  ← Created inside, can't inject   │
│           return dep.call()                                     │
│                                                                 │
│   # Your test                                                   │
│   @patch('module.Dependency')  ← Intercept the class           │
│   def test(mock_class):                                         │
│       mock_class.return_value.call.return_value = "mocked"     │
│       service = Service()                                       │
│       result = service.do_something()  ← patch intercepts      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Quick Reference Table

| Aspect | `Mock()` | `patch()` |
|--------|----------|-----------|
| **What it does** | Creates a fake object | Replaces a real object temporarily |
| **When to use** | Dependency injection | Hardcoded dependencies |
| **Scope** | Manual - you control lifecycle | Automatic - restored after test |
| **Complexity** | Simple | More complex (path strings) |
| **Code design** | Works with good design (DI) | Works with any design |
| **Typical pattern** | `service = Service(mock)` | `@patch('module.Class')` |

---

### Real-World Analogy

Think of it like replacing a car part:

| Scenario | Analogy | Technique |
|----------|---------|-----------|
| **Mock** | Car has a socket where you plug in the engine. You bring your test engine and plug it in. | Dependency Injection |
| **patch** | Engine is welded inside the car. You need to secretly swap it while no one is looking, then swap it back. | Monkey patching at runtime |

---

### Best Practice: Prefer Mock over patch

```python
# GOOD: Design for testability with DI
class OrderService:
    def __init__(self, payment_gateway, email_service):
        self.payment = payment_gateway
        self.email = email_service

# Test is simple - just pass mocks
def test_order():
    service = OrderService(Mock(), Mock())
```

```python
# AVOID: Hardcoded dependencies require patch
class OrderService:
    def process(self):
        gateway = PaymentGateway()  # Hard to test!
        email = EmailService()       # Hard to test!

# Test needs patch - more complex
@patch('order_service.EmailService')
@patch('order_service.PaymentGateway')
def test_order(mock_payment, mock_email):
    # More setup needed...
```

**Rule of thumb:** If you find yourself using `patch` a lot, consider refactoring your code to use dependency injection!

---

## 5. Return Values and Side Effects

### 5.1 Simple Return Value

Same value every time:

```python
mock = Mock()
mock.get_price.return_value = 99.99

print(mock.get_price())  # 99.99
print(mock.get_price())  # 99.99 (same)
```

### 5.2 Side Effect: List of Values

Different value on each call (like a queue):

```python
mock = Mock()
mock.get_next.side_effect = [1, 2, 3]

print(mock.get_next())  # 1
print(mock.get_next())  # 2
print(mock.get_next())  # 3
# mock.get_next()       # StopIteration!
```

**Use case**: Testing pagination, retry logic, or state changes.

### 5.3 Side Effect: Exception

Simulate errors:

```python
mock = Mock()
mock.connect.side_effect = ConnectionError("Network unreachable")

try:
    mock.connect()
except ConnectionError as e:
    print(f"Caught: {e}")  # Caught: Network unreachable
```

**Use case**: Testing error handling, retry logic, fallbacks.

### 5.4 Side Effect: Function

Compute return value dynamically:

```python
mock = Mock()

def double(x):
    return x * 2

mock.calculate.side_effect = double

print(mock.calculate(5))   # 10
print(mock.calculate(3))   # 6
print(mock.calculate(100)) # 200
```

**Use case**: When return value depends on input arguments.

### 5.5 Side Effect: Mixed Values and Exceptions

Simulate intermittent failures:

```python
mock = Mock()
mock.api_call.side_effect = [
    {"status": "success"},        # First call: success
    TimeoutError("Gateway timeout"),  # Second call: failure
    {"status": "success"},        # Third call: success (retry worked!)
]

print(mock.api_call())  # {"status": "success"}

try:
    mock.api_call()     # Raises TimeoutError
except TimeoutError:
    pass

print(mock.api_call())  # {"status": "success"}
```

**Use case**: Testing retry mechanisms, circuit breakers, resilience patterns.

---

## 6. Assertions on Mock Calls

After running your code, verify that mocks were called correctly.

### 6.1 Was It Called?

```python
mock = Mock()
mock.save()

mock.save.assert_called()         # At least once
mock.save.assert_called_once()    # Exactly once
mock.delete.assert_not_called()   # Never called
```

### 6.2 With What Arguments?

```python
mock = Mock()
mock.create_user(name="John", email="john@example.com")

# Check last call arguments
mock.create_user.assert_called_with(name="John", email="john@example.com")

# Check called once with these exact args
mock.create_user.assert_called_once_with(name="John", email="john@example.com")
```

### 6.3 How Many Times?

```python
mock = Mock()
mock.log("msg1")
mock.log("msg2")
mock.log("msg3")

assert mock.log.call_count == 3
```

### 6.4 Check Any Call (Among Many)

```python
mock = Mock()
mock.process("a")
mock.process("b")
mock.process("c")

# Was it called with "b" at any point?
mock.process.assert_any_call("b")  # Passes
```

### 6.5 Inspect All Calls

```python
from unittest.mock import call

mock = Mock()
mock.log("first")
mock.log("second")
mock.log("third")

# Get complete call history
assert mock.log.call_args_list == [
    call("first"),
    call("second"),
    call("third"),
]
```

### 6.6 Access Last Call Arguments

```python
mock = Mock()
mock.process(1, 2, key="value")

# Positional args
print(mock.process.call_args.args)    # (1, 2)

# Keyword args
print(mock.process.call_args.kwargs)  # {"key": "value"}
```

### Assertion Cheat Sheet

| Assertion | Meaning |
|-----------|---------|
| `assert_called()` | Called at least once |
| `assert_called_once()` | Called exactly once |
| `assert_called_with(...)` | Last call had these args |
| `assert_called_once_with(...)` | Called once with these args |
| `assert_any_call(...)` | At least one call had these args |
| `assert_not_called()` | Never called |
| `call_count` | Number of times called |
| `call_args` | Arguments of last call |
| `call_args_list` | List of all calls |

---

## 7. Spec and Autospec: Catching Mistakes

### 7.1 The Problem Without Spec

```python
class PaymentGateway:
    def charge(self, card_number, amount):
        pass

# Without spec, typos go unnoticed!
mock = Mock()
mock.chrage(100)  # Typo! Should be 'charge'
mock.chrage.assert_called()  # Test passes, but code is wrong!
```

### 7.2 Using Spec

`spec` restricts the mock to only allow attributes that exist on the real class:

```python
mock = Mock(spec=PaymentGateway)

mock.charge(card_number="1234", amount=100)  # Works

mock.chrage(100)  # AttributeError! Typo caught!
```

### 7.3 Using Autospec

`autospec` goes further - it also validates method signatures:

```python
from unittest.mock import create_autospec

mock = create_autospec(PaymentGateway)

# This fails - wrong signature!
# mock.charge(100)  # TypeError: missing 'card_number'

# This works
mock.charge(card_number="1234", amount=100)
```

### 7.4 Comparison

| Feature | `Mock()` | `Mock(spec=X)` | `create_autospec(X)` |
|---------|----------|----------------|---------------------|
| Catches attribute typos | No | Yes | Yes |
| Validates method signatures | No | No | Yes |
| Validates nested objects | No | No | Yes |

### 7.5 Best Practice: Always Use Spec

```python
# In fixtures
@pytest.fixture
def mock_gateway():
    return Mock(spec=PaymentGateway)

# In patches
@patch('module.PaymentGateway', autospec=True)
def test_payment(mock_gateway):
    # Now typos and wrong signatures are caught!
```

---

## 8. Real-World Testing Patterns

### 8.1 Testing with Dependency Injection

**Code Structure:**
```python
class OrderService:
    def __init__(self, payment_gateway, email_service):
        self.payment = payment_gateway
        self.email = email_service

    def place_order(self, order):
        result = self.payment.charge(order.amount)
        if result["status"] == "success":
            self.email.send("Order confirmed!")
        return result
```

**Test:**
```python
def test_place_order_success():
    # Arrange - create mocks
    mock_payment = Mock(spec=PaymentGateway)
    mock_email = Mock(spec=EmailService)

    mock_payment.charge.return_value = {"status": "success"}

    service = OrderService(mock_payment, mock_email)
    order = Order(amount=100)

    # Act
    result = service.place_order(order)

    # Assert - verify behavior
    assert result["status"] == "success"
    mock_payment.charge.assert_called_once_with(100)
    mock_email.send.assert_called_once_with("Order confirmed!")
```

### 8.2 Testing Failure Scenarios

```python
def test_place_order_payment_fails():
    # Arrange
    mock_payment = Mock(spec=PaymentGateway)
    mock_email = Mock(spec=EmailService)

    mock_payment.charge.return_value = {"status": "failed"}

    service = OrderService(mock_payment, mock_email)

    # Act & Assert
    with pytest.raises(ValueError, match="Payment failed"):
        service.place_order(Order(amount=100))

    # Email should NOT be sent on failure
    mock_email.send.assert_not_called()
```

### 8.3 Testing Retry Logic

```python
def test_payment_retries_on_timeout():
    mock_payment = Mock()
    mock_payment.charge.side_effect = [
        TimeoutError("Gateway timeout"),  # First attempt fails
        {"status": "success"}              # Retry succeeds
    ]

    service = OrderService(mock_payment, Mock())

    result = service.place_order_with_retry(Order(amount=100))

    assert result["status"] == "success"
    assert mock_payment.charge.call_count == 2  # Called twice
```

### 8.4 Fixture Pattern for Multiple Tests

```python
class TestOrderService:
    @pytest.fixture
    def mock_dependencies(self):
        return {
            "payment": Mock(spec=PaymentGateway),
            "email": Mock(spec=EmailService),
            "inventory": Mock(spec=InventoryService),
        }

    @pytest.fixture
    def order_service(self, mock_dependencies):
        return OrderService(
            payment_gateway=mock_dependencies["payment"],
            email_service=mock_dependencies["email"],
            inventory_service=mock_dependencies["inventory"],
        )

    def test_success(self, order_service, mock_dependencies):
        mock_dependencies["payment"].charge.return_value = {"status": "success"}
        # ... test code

    def test_failure(self, order_service, mock_dependencies):
        mock_dependencies["payment"].charge.side_effect = ValueError("Declined")
        # ... test code
```

---

## Summary: Mocking Mental Model

```
┌─────────────────────────────────────────────────────────────────┐
│                         MOCKING FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. IDENTIFY dependencies (what does your code call?)          │
│                          ↓                                      │
│  2. CREATE mocks (Mock, MagicMock, spec=...)                   │
│                          ↓                                      │
│  3. CONFIGURE behavior (return_value, side_effect)             │
│                          ↓                                      │
│  4. INJECT mocks (constructor, patch decorator/context)        │
│                          ↓                                      │
│  5. RUN your code (call the function/method under test)        │
│                          ↓                                      │
│  6. ASSERT results (check return value)                        │
│                          ↓                                      │
│  7. VERIFY interactions (assert_called_with, call_count)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference

```python
from unittest.mock import Mock, MagicMock, patch, call

# Create mocks
mock = Mock()                    # Basic mock
mock = Mock(spec=SomeClass)      # With attribute checking
mock = MagicMock()               # Supports __len__, __iter__, etc.

# Configure behavior
mock.method.return_value = 42                    # Always return 42
mock.method.side_effect = [1, 2, 3]             # Return 1, then 2, then 3
mock.method.side_effect = ValueError("error")   # Always raise
mock.method.side_effect = lambda x: x * 2       # Compute from args

# Patch (use during tests)
@patch('module.ClassName')                       # Decorator
with patch('module.ClassName') as mock:          # Context manager
patch.object(instance, 'method')                 # Specific instance

# Assertions
mock.method.assert_called()
mock.method.assert_called_once()
mock.method.assert_called_with(arg1, arg2)
mock.method.assert_called_once_with(arg1, arg2)
mock.method.assert_any_call(arg1)
mock.method.assert_not_called()
assert mock.method.call_count == 3
```

---

## Next Steps

1. Study `test_mocking_basics.py` for complete examples
2. Practice with the exercises in `mocking_basics.py`
3. Apply these patterns to your own projects
