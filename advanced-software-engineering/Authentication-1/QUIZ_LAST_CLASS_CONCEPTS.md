# Quiz: Mocking, Patching & Web API Testing

Test your understanding of mocking concepts covered in Class 2!

**Instructions**: Read each question carefully, think about your answer, then expand the solution to check.

---

## Question 1: The Patch Location Puzzle

```python
# payment_service.py
class PaymentGateway:
    def charge(self, amount):
        # Calls external API
        return {"status": "success"}

# order_service.py
from payment_service import PaymentGateway

class OrderService:
    def process_order(self, order):
        gateway = PaymentGateway()
        return gateway.charge(order.amount)
```

**You're writing a test for `OrderService`. Which patch target is CORRECT?**

A) `@patch('payment_service.PaymentGateway')`
B) `@patch('order_service.PaymentGateway')`
C) `@patch('PaymentGateway')`
D) `@patch('order_service.payment_service.PaymentGateway')`

<details>
<summary>💡 Click to reveal answer</summary>

### Answer: **B) `@patch('order_service.PaymentGateway')`**

**Golden Rule**: Patch where the object is **USED**, not where it's **DEFINED**.

When `order_service.py` does `from payment_service import PaymentGateway`, it creates a **reference** to `PaymentGateway` in the `order_service` namespace.

```python
# ❌ WRONG - patches the original, but order_service has its own reference
@patch('payment_service.PaymentGateway')

# ✅ CORRECT - patches the reference that order_service actually uses
@patch('order_service.PaymentGateway')
```

**Why Option A fails:**
- `order_service` already imported `PaymentGateway` before the patch
- Patching the source doesn't affect existing references

**Complete test:**
```python
@patch('order_service.PaymentGateway')
def test_process_order(mock_gateway_class):
    mock_instance = mock_gateway_class.return_value
    mock_instance.charge.return_value = {"status": "success"}

    service = OrderService()
    result = service.process_order(order)

    assert result["status"] == "success"
```

</details>

---

## Question 2: Mock vs MagicMock

```python
from unittest.mock import Mock, MagicMock

mock1 = Mock()
mock2 = MagicMock()

# Which of these will work?
len(mock1)      # Line A
len(mock2)      # Line B
mock1["key"]    # Line C
mock2["key"]    # Line D
```

**Which lines will raise an error?**

<details>
<summary>💡 Click to reveal answer</summary>

### Answer: **Lines A and C will raise errors**

| Line | Mock Type | Result |
|------|-----------|--------|
| A: `len(mock1)` | Mock | ❌ `TypeError` |
| B: `len(mock2)` | MagicMock | ✅ Returns `0` (default) |
| C: `mock1["key"]` | Mock | ❌ `TypeError` |
| D: `mock2["key"]` | MagicMock | ✅ Returns a `MagicMock` |

**Key Difference:**

- **Mock**: Basic mock, doesn't support magic methods (`__len__`, `__getitem__`, etc.)
- **MagicMock**: Subclass of Mock that pre-configures all magic methods

```python
# Mock requires explicit configuration for magic methods
mock1 = Mock()
mock1.__len__ = Mock(return_value=5)
len(mock1)  # Now works, returns 5

# MagicMock has them built-in
mock2 = MagicMock()
mock2.__len__.return_value = 10
len(mock2)  # Returns 10
```

**When to use which:**
- `Mock`: When you don't need magic methods (most cases)
- `MagicMock`: When testing code that uses `len()`, iteration, context managers, etc.

</details>

---

## Question 3: The Return Value Trap

```python
@patch('services.EmailService')
def test_send_notification(mock_email_class):
    # Setup
    mock_email_class.send.return_value = True

    # Act
    service = NotificationService()
    result = service.notify("user@test.com", "Hello!")

    # Assert
    assert result == True
```

**The test fails with `AssertionError: assert <MagicMock...> == True`. What's wrong?**

<details>
<summary>💡 Click to reveal answer</summary>

### Answer: **Missing `.return_value` for the instance**

When you patch a **class**, the mock represents the **class itself**, not an instance.

```python
@patch('services.EmailService')
def test_send_notification(mock_email_class):
    # mock_email_class = the CLASS (EmailService)
    # mock_email_class() = calling the constructor = returns an instance
    # mock_email_class.return_value = the INSTANCE that gets created

    # ❌ WRONG - configuring method on the class
    mock_email_class.send.return_value = True

    # ✅ CORRECT - configuring method on the instance
    mock_email_class.return_value.send.return_value = True
```

**Visual breakdown:**
```python
# What your code does:
email_service = EmailService()  # Creates instance
email_service.send(...)         # Calls method on instance

# What you need to mock:
mock_email_class.return_value  # This IS the instance
mock_email_class.return_value.send.return_value = True  # Instance method
```

**Correct test:**
```python
@patch('services.EmailService')
def test_send_notification(mock_email_class):
    mock_instance = mock_email_class.return_value
    mock_instance.send.return_value = True

    service = NotificationService()
    result = service.notify("user@test.com", "Hello!")

    assert result == True
```

</details>

---

## Question 4: Side Effects Showdown

**Match each `side_effect` usage with its behavior:**

```python
mock = Mock()

# Setup A
mock.fetch.side_effect = [1, 2, 3]

# Setup B
mock.fetch.side_effect = ValueError("Not found")

# Setup C
mock.fetch.side_effect = lambda x: x * 2

# Setup D
mock.fetch.side_effect = [{"status": "ok"}, ConnectionError(), {"status": "ok"}]
```

| Setup | Behavior |
|-------|----------|
| A | 1. Raises exception on every call |
| B | 2. Returns different values on successive calls |
| C | 3. Computes return value from arguments |
| D | 4. Simulates intermittent failures |

<details>
<summary>💡 Click to reveal answer</summary>

### Answer

| Setup | Behavior |
|-------|----------|
| **A** `[1, 2, 3]` | **2. Returns different values on successive calls** |
| **B** `ValueError(...)` | **1. Raises exception on every call** |
| **C** `lambda x: x * 2` | **3. Computes return value from arguments** |
| **D** `[..., Error(), ...]` | **4. Simulates intermittent failures** |

**Examples:**

```python
# A: Sequential returns
mock.fetch.side_effect = [1, 2, 3]
mock.fetch()  # Returns 1
mock.fetch()  # Returns 2
mock.fetch()  # Returns 3
mock.fetch()  # Raises StopIteration!

# B: Always raises
mock.fetch.side_effect = ValueError("Not found")
mock.fetch()  # Raises ValueError
mock.fetch()  # Raises ValueError again

# C: Computed return
mock.fetch.side_effect = lambda x: x * 2
mock.fetch(5)   # Returns 10
mock.fetch(100) # Returns 200

# D: Mixed (great for retry testing!)
mock.fetch.side_effect = [
    {"status": "ok"},      # First call succeeds
    ConnectionError(),      # Second call fails
    {"status": "ok"}       # Third call succeeds (after retry)
]
```

**Pro tip**: Use `side_effect` with mixed values to test retry logic and error handling!

</details>

---

## Question 5: Flask Test Client

```python
def test_create_user(client):
    response = client.post(
        '/api/users',
        data={'name': 'John', 'email': 'john@test.com'},
        content_type='application/json'
    )

    assert response.status_code == 201
    assert response.json['name'] == 'John'
```

**This test fails with a 400 Bad Request. The API expects JSON. What's wrong?**

<details>
<summary>💡 Click to reveal answer</summary>

### Answer: **`data` parameter sends form data, not JSON**

Even with `content_type='application/json'`, the `data` parameter sends form-encoded data.

```python
# ❌ WRONG - sends form data with JSON content-type header
response = client.post(
    '/api/users',
    data={'name': 'John', 'email': 'john@test.com'},
    content_type='application/json'
)

# ✅ CORRECT - Option 1: Use json parameter (Flask 1.0+)
response = client.post(
    '/api/users',
    json={'name': 'John', 'email': 'john@test.com'}
)

# ✅ CORRECT - Option 2: Manually serialize JSON
import json
response = client.post(
    '/api/users',
    data=json.dumps({'name': 'John', 'email': 'john@test.com'}),
    content_type='application/json'
)
```

**Key difference:**
- `data={...}` → Form-encoded: `name=John&email=john@test.com`
- `json={...}` → JSON: `{"name": "John", "email": "john@test.com"}`

**The `json` parameter automatically:**
1. Serializes the dict to JSON
2. Sets `Content-Type: application/json`

</details>

---

## Question 6: Assertion Methods

```python
mock = Mock()

# These calls happen during the test:
mock.process("order_1", priority="high")
mock.process("order_2", priority="low")
mock.process("order_3", priority="high")
```

**Which assertions will PASS?**

A) `mock.process.assert_called_with("order_1", priority="high")`
B) `mock.process.assert_called_once_with("order_1", priority="high")`
C) `mock.process.assert_any_call("order_2", priority="low")`
D) `assert mock.process.call_count == 3`
E) `mock.process.assert_called()`

<details>
<summary>💡 Click to reveal answer</summary>

### Answer: **C, D, and E pass**

| Assertion | Result | Explanation |
|-----------|--------|-------------|
| **A** | ❌ FAIL | `assert_called_with` checks the **LAST** call. Last was `("order_3", priority="high")` |
| **B** | ❌ FAIL | `assert_called_once_with` fails because method was called 3 times, not once |
| **C** | ✅ PASS | `assert_any_call` checks if this call was made at any point |
| **D** | ✅ PASS | Correctly asserts 3 calls were made |
| **E** | ✅ PASS | `assert_called` just checks it was called at least once |

**Assertion cheat sheet:**

```python
# Was it called?
mock.method.assert_called()           # At least once
mock.method.assert_not_called()       # Never

# Exactly once?
mock.method.assert_called_once()      # Exactly 1 time
mock.method.assert_called_once_with(args)  # Once with specific args

# Last call?
mock.method.assert_called_with(args)  # Last call had these args

# Any call?
mock.method.assert_any_call(args)     # At least one call had these args

# All calls?
mock.method.call_args_list == [call(...), call(...)]
```

</details>

---

## Question 7: The spec Advantage

```python
# Real class
class PaymentGateway:
    def charge(self, card_number, amount, currency="USD"):
        pass

    def refund(self, transaction_id, amount):
        pass

# Test code
mock_gateway = Mock()  # Without spec
mock_gateway.chrage(card="1234", amount=100)  # Typo!
mock_gateway.chrage.assert_called()  # Passes!
```

**How would using `spec` help here, and what's the syntax?**

<details>
<summary>💡 Click to reveal answer</summary>

### Answer: **`spec` restricts mock to only allow real attributes**

```python
# Without spec - typos silently pass
mock_gateway = Mock()
mock_gateway.chrage(100)  # Creates mock.chrage, no error!
mock_gateway.chrage.assert_called()  # "Test passes" but bug exists

# With spec - typos raise AttributeError
mock_gateway = Mock(spec=PaymentGateway)
mock_gateway.chrage(100)  # ❌ AttributeError: 'chrage' not in spec
mock_gateway.charge(100)  # ✅ Works

# With autospec - also validates signatures!
from unittest.mock import create_autospec

mock_gateway = create_autospec(PaymentGateway)
mock_gateway.charge("1234", 100)  # ✅ Valid signature
mock_gateway.charge(100)  # ❌ TypeError: missing required argument 'card_number'
```

**Comparison:**

| Feature | `Mock()` | `Mock(spec=X)` | `create_autospec(X)` |
|---------|----------|----------------|---------------------|
| Catches typos | ❌ | ✅ | ✅ |
| Validates signatures | ❌ | ❌ | ✅ |
| Nests specs | ❌ | ❌ | ✅ |

**Best practice**: Always use `spec` or `autospec` to catch API mismatches early!

```python
# In tests
@patch('module.PaymentGateway', autospec=True)
def test_payment(mock_gateway_class):
    mock_instance = mock_gateway_class.return_value
    # Now typos and wrong signatures will fail!
```

</details>

---

## Question 8: HTTP Status Codes

**Match each scenario with the correct HTTP status code:**

| Scenario | Status Code |
|----------|-------------|
| 1. User created successfully | A. 400 |
| 2. Invalid JSON in request body | B. 401 |
| 3. User not logged in | C. 403 |
| 4. Logged in but accessing admin route | D. 404 |
| 5. User ID doesn't exist | E. 201 |
| 6. Server crashed unexpectedly | F. 500 |

<details>
<summary>💡 Click to reveal answer</summary>

### Answer

| Scenario | Status Code |
|----------|-------------|
| 1. User created successfully | **E. 201 Created** |
| 2. Invalid JSON in request body | **A. 400 Bad Request** |
| 3. User not logged in | **B. 401 Unauthorized** |
| 4. Logged in but accessing admin route | **C. 403 Forbidden** |
| 5. User ID doesn't exist | **D. 404 Not Found** |
| 6. Server crashed unexpectedly | **F. 500 Internal Server Error** |

**Status Code Families:**

```
2xx - Success
├── 200 OK              - General success (GET, PUT, PATCH)
├── 201 Created         - Resource created (POST)
└── 204 No Content      - Success, no body (DELETE)

4xx - Client Errors (your fault)
├── 400 Bad Request     - Malformed request/validation error
├── 401 Unauthorized    - Not authenticated (needs login)
├── 403 Forbidden       - Authenticated but not permitted
├── 404 Not Found       - Resource doesn't exist
└── 422 Unprocessable   - Valid JSON but semantic error

5xx - Server Errors (our fault)
├── 500 Internal Error  - Unexpected server crash
└── 503 Unavailable     - Server overloaded/maintenance
```

**Testing tip**: Always test both success and error status codes!

```python
def test_get_user_returns_404_for_unknown_id(client):
    response = client.get('/api/users/99999')
    assert response.status_code == 404
```

</details>

---

## Question 9: patch.object vs patch

```python
class EmailService:
    def send(self, to, subject, body):
        # External API call
        return True

email_service = EmailService()

# Option A
with patch.object(email_service, 'send', return_value=True):
    result = email_service.send("test@test.com", "Hi", "Body")

# Option B
with patch('mymodule.EmailService.send', return_value=True):
    result = email_service.send("test@test.com", "Hi", "Body")
```

**When would you use `patch.object` (Option A) vs `patch` (Option B)?**

<details>
<summary>💡 Click to reveal answer</summary>

### Answer

**Use `patch.object`** when you have a specific **instance** to mock:

```python
# You already have an instance
email_service = EmailService()
user_service = UserService(email=email_service)

# Patch that specific instance
with patch.object(email_service, 'send', return_value=True):
    user_service.create_user(...)  # Uses the mocked instance
```

**Use `patch`** when you want to mock at the **class level**:

```python
# Mock all instances created during the test
with patch('mymodule.EmailService') as mock_class:
    mock_class.return_value.send.return_value = True

    # Any new EmailService() gets the mock
    service = SomeService()  # Creates EmailService internally
```

**Comparison:**

| Aspect | `patch.object` | `patch` |
|--------|---------------|---------|
| Target | Specific instance | Class or module |
| Scope | Only that object | All new instances |
| Use when | Dependency injection | Internal instantiation |
| Syntax | `patch.object(obj, 'method')` | `patch('module.Class')` |

**Real-world example:**

```python
# Your code uses dependency injection (easy to test)
class OrderService:
    def __init__(self, payment_gateway):
        self.payment = payment_gateway

# Test with patch.object
def test_order():
    gateway = PaymentGateway()
    with patch.object(gateway, 'charge', return_value={"status": "ok"}):
        service = OrderService(gateway)
        service.place_order(...)

# Your code creates dependencies internally (harder to test)
class OrderService:
    def __init__(self):
        self.payment = PaymentGateway()  # Hard-coded!

# Must use patch to intercept class
@patch('orders.PaymentGateway')
def test_order(mock_gateway_class):
    mock_gateway_class.return_value.charge.return_value = {"status": "ok"}
    service = OrderService()
    service.place_order(...)
```

</details>

---

## Question 10: Integration Test Design

You need to test this endpoint:

```python
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    # Validate input
    if not data.get('product_id'):
        return jsonify({"error": "Product ID required"}), 400

    # Check inventory (external service)
    stock = InventoryService.check_stock(data['product_id'])
    if stock < data.get('quantity', 1):
        return jsonify({"error": "Insufficient stock"}), 400

    # Process payment (external service)
    payment = PaymentGateway.charge(data['card'], data['amount'])
    if payment['status'] != 'success':
        return jsonify({"error": "Payment failed"}), 402

    # Save order
    order = Order.create(data)

    # Send notification (external service)
    NotificationService.send_email(data['email'], "Order confirmed!")

    return jsonify({"order_id": order.id}), 201
```

**Design a test that:**
1. Mocks all external services
2. Tests the happy path
3. Verifies the correct services were called

<details>
<summary>💡 Click to reveal answer</summary>

### Answer

```python
class TestCreateOrder:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @patch('routes.NotificationService')
    @patch('routes.PaymentGateway')
    @patch('routes.InventoryService')
    @patch('routes.Order')
    def test_create_order_success(
        self,
        mock_order,
        mock_inventory,
        mock_payment,
        mock_notification,
        client
    ):
        # Arrange - Configure mocks
        mock_inventory.check_stock.return_value = 100
        mock_payment.charge.return_value = {"status": "success"}
        mock_order.create.return_value = Mock(id="ORD-123")

        order_data = {
            "product_id": "PROD-001",
            "quantity": 2,
            "card": "4111111111111111",
            "amount": 99.99,
            "email": "customer@test.com"
        }

        # Act
        response = client.post(
            '/api/orders',
            json=order_data
        )

        # Assert - Response
        assert response.status_code == 201
        assert response.json['order_id'] == "ORD-123"

        # Assert - Service interactions
        mock_inventory.check_stock.assert_called_once_with("PROD-001")
        mock_payment.charge.assert_called_once_with(
            "4111111111111111",
            99.99
        )
        mock_order.create.assert_called_once()
        mock_notification.send_email.assert_called_once_with(
            "customer@test.com",
            "Order confirmed!"
        )
```

**Key testing patterns demonstrated:**

1. **Mock external services** - Inventory, Payment, Notification
2. **Use `@patch` decorators** - Stacked (note reverse order in params!)
3. **Configure return values** - Set up expected responses
4. **Use `json=` parameter** - Send proper JSON request
5. **Assert response** - Status code and body
6. **Verify interactions** - Check services were called correctly

**Additional tests to write:**

```python
def test_create_order_missing_product_id_returns_400(self, client):
    response = client.post('/api/orders', json={})
    assert response.status_code == 400

@patch('routes.InventoryService')
def test_create_order_insufficient_stock_returns_400(
    self, mock_inventory, client
):
    mock_inventory.check_stock.return_value = 0
    response = client.post('/api/orders', json={"product_id": "X"})
    assert response.status_code == 400

@patch('routes.PaymentGateway')
@patch('routes.InventoryService')
def test_create_order_payment_failure_returns_402(
    self, mock_inventory, mock_payment, client
):
    mock_inventory.check_stock.return_value = 100
    mock_payment.charge.return_value = {"status": "failed"}
    response = client.post('/api/orders', json={...})
    assert response.status_code == 402
```

</details>

---

## 🏆 Scoring Guide

| Score | Level | Feedback |
|-------|-------|----------|
| 10/10 | 🌟 Mocking Master | You can mock anything! Ready for complex test suites |
| 8-9 | 🎯 Advanced | Strong skills, practice edge cases |
| 6-7 | 📚 Intermediate | Good foundation, review patch locations |
| 4-5 | 🌱 Beginner | Re-read mocking basics and try examples |
| 0-3 | 🔄 Needs Review | Start with `test_mocking_basics.py` examples |

---

## Key Takeaways

1. **Patch where used, not where defined**
2. **Use `.return_value` for instance methods when patching classes**
3. **`MagicMock` for magic methods, `Mock` otherwise**
4. **`side_effect` for sequences, exceptions, or computed values**
5. **Always use `spec` or `autospec` to catch typos**
6. **Use `json=` parameter in Flask test client for JSON requests**
7. **Verify both return values AND service interactions**

---

## Next Steps

1. Run `pytest test_mocking_basics.py -v` and study each test
2. Run `pytest web_api_testing.py -v` to see API testing patterns
3. Try modifying tests to break them, then fix them
4. Practice writing tests for your own projects!
