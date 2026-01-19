# Types of Testing - A Concise Guide

## Testing Pyramid

```
                    /\
                   /  \
                  / E2E \        ← Slow, Expensive, Few
                 /────────\
                /Integration\    ← Medium Speed, Some
               /──────────────\
              /   Unit Tests    \ ← Fast, Cheap, Many
             /____________________\
```

---

## Quick Comparison

| Type | Scope | Speed | Cost | Who Writes |
|------|-------|-------|------|------------|
| Unit | Single function/class | ⚡ Very Fast | 💰 Low | Developers |
| Integration | Multiple components | 🚗 Medium | 💰💰 Medium | Developers |
| E2E | Entire application | 🐢 Slow | 💰💰💰 High | QA/Developers |
| Smoke | Critical paths only | ⚡ Fast | 💰 Low | QA |
| Regression | Previously broken areas | 🚗 Medium | 💰💰 Medium | QA/Developers |
| Performance | Speed & resource usage | 🐢 Slow | 💰💰💰 High | Performance Engineers |
| Security | Vulnerabilities | 🚗 Medium | 💰💰💰 High | Security Engineers |

---

## 1. Unit Testing

**What:** Test individual functions/methods in isolation.

**Characteristics:**
- Tests ONE thing at a time
- No external dependencies (DB, API, filesystem)
- Uses mocks for dependencies
- Fastest to run

```python
# Code
class Calculator:
    def add(self, a, b):
        return a + b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

# Unit Test
import unittest

class TestCalculator(unittest.TestCase):
    def test_add_positive_numbers(self):
        calc = Calculator()
        self.assertEqual(calc.add(2, 3), 5)

    def test_divide_by_zero_raises_error(self):
        calc = Calculator()
        with self.assertRaises(ValueError):
            calc.divide(10, 0)
```

---

## 2. Integration Testing

**What:** Test how multiple components work together.

**Characteristics:**
- Tests interaction between modules
- May use real databases (often test DB)
- Tests API endpoints with actual handlers
- Slower than unit tests

```python
# Code: Service + Repository working together
class UserRepository:
    def __init__(self, db):
        self.db = db

    def save(self, user):
        self.db.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                       (user['name'], user['email']))
        return self.db.lastrowid

class UserService:
    def __init__(self, repo):
        self.repo = repo

    def create_user(self, name, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email")
        return self.repo.save({'name': name, 'email': email})

# Integration Test - Tests Service + Repository + Database together
import sqlite3
import unittest

class TestUserIntegration(unittest.TestCase):
    def setUp(self):
        # Real database (in-memory for testing)
        self.db = sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
        self.repo = UserRepository(self.db)
        self.service = UserService(self.repo)

    def tearDown(self):
        self.db.close()

    def test_create_user_saves_to_database(self):
        # Act - Tests service + repo + db together
        user_id = self.service.create_user("John", "john@example.com")

        # Assert - Verify data actually in database
        cursor = self.db.execute("SELECT name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        self.assertEqual(row[0], "John")
        self.assertEqual(row[1], "john@example.com")
```

---

## 3. End-to-End (E2E) Testing

**What:** Test the entire application flow from user's perspective.

**Characteristics:**
- Simulates real user behavior
- Tests UI + Backend + Database
- Uses tools like Selenium, Playwright, Cypress
- Slowest and most brittle

```python
# E2E Test using Selenium - Tests entire login flow
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestLoginE2E(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000")

    def tearDown(self):
        self.driver.quit()

    def test_user_can_login_and_see_dashboard(self):
        # Find and fill login form
        self.driver.find_element(By.ID, "email").send_keys("user@example.com")
        self.driver.find_element(By.ID, "password").send_keys("password123")
        self.driver.find_element(By.ID, "login-button").click()

        # Wait for dashboard to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard"))
        )

        # Verify user sees dashboard
        welcome = self.driver.find_element(By.ID, "welcome-message")
        self.assertIn("Welcome", welcome.text)
```

---

## 4. Functional Testing

**What:** Test features against business requirements.

**Characteristics:**
- Focuses on WHAT the system does (not HOW)
- Tests business logic and rules
- Black-box testing approach

```python
# Functional Test - Tests business requirement:
# "Users get 10% discount if order total > $100"

class TestDiscountFeature(unittest.TestCase):
    def test_discount_applied_for_orders_over_100(self):
        """Business Rule: Orders over $100 get 10% discount"""
        order = Order()
        order.add_item("Laptop", 150.00)

        total = order.calculate_total()

        # $150 - 10% = $135
        self.assertEqual(total, 135.00)

    def test_no_discount_for_orders_under_100(self):
        """Business Rule: Orders under $100 get no discount"""
        order = Order()
        order.add_item("Book", 50.00)

        total = order.calculate_total()

        self.assertEqual(total, 50.00)

    def test_discount_applied_at_exactly_100(self):
        """Edge case: What happens at exactly $100?"""
        order = Order()
        order.add_item("Item", 100.00)

        total = order.calculate_total()

        # Assuming >= 100 gets discount
        self.assertEqual(total, 90.00)
```

---

## 5. Regression Testing

**What:** Re-test after changes to ensure nothing broke.

**Characteristics:**
- Run existing tests after code changes
- Catch unintended side effects
- Often automated in CI/CD

```python
# Bug was found: negative quantities were allowed
# Regression test ensures it never happens again

class TestQuantityRegression(unittest.TestCase):
    """
    Regression test for Bug #1234
    Previously: System allowed negative quantities
    Fix: Added validation to reject negative quantities
    """

    def test_negative_quantity_rejected(self):
        """Regression: Ensure bug #1234 stays fixed"""
        cart = ShoppingCart()

        with self.assertRaises(ValueError) as context:
            cart.add_item("Apple", quantity=-5)

        self.assertIn("negative", str(context.exception).lower())

    def test_zero_quantity_rejected(self):
        """Regression: Related edge case"""
        cart = ShoppingCart()

        with self.assertRaises(ValueError):
            cart.add_item("Apple", quantity=0)
```

---

## 6. Smoke Testing

**What:** Quick tests to verify basic functionality works.

**Characteristics:**
- Run after deployment
- Tests critical paths only
- Fast sanity check
- "Does the app even start?"

```python
# Smoke Tests - Quick sanity checks after deployment
import requests
import unittest

class TestSmoke(unittest.TestCase):
    BASE_URL = "http://localhost:8000"

    def test_homepage_loads(self):
        """Smoke: Homepage returns 200"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)

    def test_api_health_check(self):
        """Smoke: API is responsive"""
        response = requests.get(f"{self.BASE_URL}/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')

    def test_database_connected(self):
        """Smoke: Database connection works"""
        response = requests.get(f"{self.BASE_URL}/api/health/db")
        self.assertEqual(response.json()['database'], 'connected')

    def test_login_page_accessible(self):
        """Smoke: Critical page loads"""
        response = requests.get(f"{self.BASE_URL}/login")
        self.assertEqual(response.status_code, 200)
```

---

## 7. Performance Testing

**What:** Test speed, scalability, and resource usage.

**Characteristics:**
- Measures response times
- Identifies bottlenecks
- Tools: locust, pytest-benchmark, JMeter

```python
# Performance Test using pytest-benchmark
import pytest

def test_search_performance(benchmark):
    """Search should complete in < 100ms"""
    database = load_test_data(10000)  # 10k records

    result = benchmark(lambda: database.search("query"))

    # Assert performance threshold
    assert benchmark.stats['mean'] < 0.1  # 100ms

# Performance Test using locust (load testing)
# File: locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_homepage(self):
        self.client.get("/")

    @task(1)
    def search(self):
        self.client.get("/search?q=test")

    @task(2)
    def view_product(self):
        self.client.get("/product/123")

# Run: locust -f locustfile.py --host=http://localhost:8000
```

---

## 8. Load Testing

**What:** Test system behavior under expected and peak load.

**Characteristics:**
- Simulates many concurrent users
- Finds breaking points
- Measures throughput

```python
# Load Test - Simulating concurrent users
import concurrent.futures
import requests
import time

def test_api_under_load():
    """API should handle 100 concurrent requests"""
    url = "http://localhost:8000/api/data"
    num_requests = 100
    results = []

    def make_request():
        start = time.time()
        response = requests.get(url)
        elapsed = time.time() - start
        return {'status': response.status_code, 'time': elapsed}

    # Execute 100 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [f.result() for f in futures]

    # Assert all succeeded
    success_count = sum(1 for r in results if r['status'] == 200)
    avg_time = sum(r['time'] for r in results) / len(results)

    assert success_count >= 95, f"Only {success_count}/100 requests succeeded"
    assert avg_time < 1.0, f"Average response time {avg_time}s exceeds 1s"
```

---

## 9. Security Testing

**What:** Test for vulnerabilities and security flaws.

**Characteristics:**
- SQL injection, XSS, CSRF
- Authentication/Authorization flaws
- Tools: OWASP ZAP, Bandit, Safety

```python
# Security Tests
import unittest

class TestSecurityVulnerabilities(unittest.TestCase):

    def test_sql_injection_prevented(self):
        """Ensure SQL injection is not possible"""
        malicious_input = "'; DROP TABLE users; --"

        # This should NOT execute the DROP TABLE
        result = user_service.search_users(malicious_input)

        # Table should still exist
        self.assertTrue(database.table_exists('users'))

    def test_xss_input_sanitized(self):
        """Ensure XSS scripts are escaped"""
        malicious_input = "<script>alert('hacked')</script>"

        user = user_service.create_user(name=malicious_input)

        # Script tags should be escaped
        self.assertNotIn("<script>", user.name)
        self.assertIn("&lt;script&gt;", user.name)

    def test_password_not_stored_plaintext(self):
        """Passwords must be hashed"""
        user = user_service.create_user(
            email="test@example.com",
            password="secret123"
        )

        # Password should be hashed, not plaintext
        self.assertNotEqual(user.password_hash, "secret123")
        self.assertTrue(len(user.password_hash) >= 60)  # bcrypt length

    def test_unauthorized_access_blocked(self):
        """Users cannot access other users' data"""
        user1 = create_user("user1@test.com")
        user2 = create_user("user2@test.com")

        # User1 trying to access User2's data
        with self.assertRaises(PermissionError):
            user_service.get_user_data(user_id=user2.id, requester=user1)
```

---

## 10. Acceptance Testing (UAT)

**What:** Verify system meets business requirements (user acceptance).

**Characteristics:**
- Written in business language
- Often uses BDD (Given-When-Then)
- Stakeholder sign-off
- Tools: Behave, pytest-bdd

```python
# Acceptance Test using pytest-bdd
# File: features/checkout.feature
"""
Feature: Shopping Cart Checkout
  As a customer
  I want to checkout my cart
  So that I can purchase items

  Scenario: Successful checkout with valid card
    Given I have items in my cart worth $50
    And I am logged in as "customer@test.com"
    When I enter valid payment details
    And I click checkout
    Then I should see "Order confirmed"
    And I should receive a confirmation email
    And my cart should be empty
"""

# File: test_checkout.py
from pytest_bdd import scenario, given, when, then

@scenario('features/checkout.feature', 'Successful checkout with valid card')
def test_successful_checkout():
    pass

@given('I have items in my cart worth $50')
def cart_with_items(cart):
    cart.add_item("Product", 50.00)
    return cart

@given('I am logged in as "customer@test.com"')
def logged_in_user():
    return login("customer@test.com")

@when('I enter valid payment details')
def enter_payment(checkout_page):
    checkout_page.enter_card("4111111111111111", "12/25", "123")

@when('I click checkout')
def click_checkout(checkout_page):
    checkout_page.submit()

@then('I should see "Order confirmed"')
def see_confirmation(checkout_page):
    assert "Order confirmed" in checkout_page.get_message()

@then('I should receive a confirmation email')
def check_email(email_mock):
    assert email_mock.was_sent_to("customer@test.com")

@then('my cart should be empty')
def cart_empty(cart):
    assert cart.item_count() == 0
```

---

## 11. Contract Testing

**What:** Test API contracts between services.

**Characteristics:**
- Ensures API producer/consumer agreement
- Prevents breaking changes
- Tools: Pact, Schemathesis

```python
# Contract Test - Verify API response matches expected schema
import unittest
from jsonschema import validate

class TestAPIContract(unittest.TestCase):

    USER_SCHEMA = {
        "type": "object",
        "required": ["id", "email", "name"],
        "properties": {
            "id": {"type": "integer"},
            "email": {"type": "string", "format": "email"},
            "name": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"}
        }
    }

    def test_get_user_matches_contract(self):
        """API response must match agreed schema"""
        response = api_client.get("/users/1")

        # Validate response matches contract
        validate(instance=response.json(), schema=self.USER_SCHEMA)

    def test_list_users_returns_array(self):
        """List endpoint must return array of users"""
        response = api_client.get("/users")

        self.assertIsInstance(response.json(), list)
        for user in response.json():
            validate(instance=user, schema=self.USER_SCHEMA)
```

---

## Summary Table

| Test Type | Question It Answers | Example |
|-----------|---------------------|---------|
| **Unit** | Does this function work? | `add(2,3) == 5` |
| **Integration** | Do these components work together? | Service + DB |
| **E2E** | Does the whole app work? | User login flow |
| **Functional** | Does it meet requirements? | Discount rules |
| **Regression** | Did we break anything? | Bug #123 still fixed? |
| **Smoke** | Does the app start? | Homepage loads |
| **Performance** | Is it fast enough? | Response < 100ms |
| **Load** | Can it handle traffic? | 1000 concurrent users |
| **Security** | Is it secure? | SQL injection blocked |
| **Acceptance** | Does customer accept it? | Feature sign-off |
| **Contract** | Do APIs match agreement? | Response schema |

---

## Which Tests to Write?

```
Start here:
    ↓
┌─────────────────────────────────────────────────┐
│  70% Unit Tests     - Fast, cheap, many         │
│  20% Integration    - Component interactions    │
│  10% E2E            - Critical user journeys    │
└─────────────────────────────────────────────────┘

Add as needed:
- Smoke tests → After deployments
- Regression → After bug fixes
- Performance → Before launch / after complaints
- Security → Always for auth, payments, user data
```
