# Builder Pattern Revision & Factory Design Pattern - Pre-requisite Quiz

This quiz covers Builder Pattern revision and introduces problems that Factory Pattern solves.

---

## Section A: Builder Pattern Revision

### Question 1: Builder Pattern - Core Principle

```python
# Approach A
class Database:
    def __init__(self, host, port, username, password):
        if not self._validate_host(host):
            raise ValueError("Invalid host")
        if port < 1024:
            raise ValueError("Invalid port")
        self.host = host
        self.port = port
        self.username = username
        self.password = password

# Approach B
class Database:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    class Builder:
        def build(self):
            self._validate()
            return Database(...)
```

**What's the main advantage of Approach B (Builder Pattern)?**

- A) Faster object creation
- B) Separates validation logic from object construction
- C) Uses less memory
- D) Allows multiple constructors

---

<details>
<summary>Answer</summary>

**B) Separates validation logic from object construction**

**Key principle of Builder Pattern:**

```python
# Product constructor: SIMPLE - just assigns values
class Database:
    def __init__(self, host, port, username, password):
        self.host = host        # No validation
        self.port = port        # No business logic
        self.username = username
        self.password = password

# Builder: COMPLEX - handles validation and business logic
class Builder:
    def build(self):
        self._validate()         # All validation here
        self._check_connection() # Business logic here
        return Database(...)     # Simple object creation
```

**Why this matters:**
- Constructor stays simple and focused
- Easy to test validation separately
- Business logic doesn't pollute the data class
- Object is guaranteed valid when created

</details>

---

### Question 2: Builder Pattern - When NOT to Use

You're building a simple application. Which class should NOT use Builder Pattern?

```python
# Option A
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Option B
class HttpRequest:
    def __init__(self, url, method, headers, body, timeout, 
                 retry_count, verify_ssl, cookies, auth):
        # ... 9 parameters
        pass

# Option C
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Option D
class EmailMessage:
    def __init__(self, to, cc, bcc, subject, body, 
                 attachments, priority, read_receipt):
        # ... 8 parameters with validation
        pass
```
---
**Which options should NOT use Builder Pattern?**

- A) A and C only
- B) B and D only
- C) A, B, and C
- D) Only A

---

<details>
<summary>Answer</summary>

**A) A and C only**

**Don't use Builder when:**

```python
# ❌ Too simple - Builder is overkill
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

point = Point(10, 20)  # Simple constructor is fine!

# ❌ Few parameters, all required
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

user = User("Nitin", "Nitin@scaler.com")  # No need for builder!
```
---
**Use Builder when:**

```python
# ✅ Many parameters (especially optional ones)
class HttpRequest:
    # 9 parameters - builder makes sense!
    pass

request = HttpRequest.builder()
    .set_url("https://api.com")
    .set_method("POST")
    .set_timeout(60)
    .build()

# ✅ Complex validation and multiple optional configurations
class EmailMessage:
    # 8 parameters with complex validation - builder helps!
    pass

email = EmailMessage.builder()
    .add_to("alice@example.com")
    .set_subject("Hello")
    .add_attachment("file.pdf")
    .build()
```

**Rule of thumb:**
- **2-3 required parameters, no validation** → Simple constructor
- **4+ parameters OR optional parameters OR complex validation** → Builder Pattern

</details>

---

### Question 3: Builder Pattern - Tricky Scenario

```python
class ReportBuilder:
    def __init__(self):
        self._title = None
        self._data = []
        self._format = "PDF"
    
    def set_title(self, title):
        self._title = title
        return self
    
    def add_data(self, data):
        self._data.append(data)
        return self
    
    def set_format(self, format):
        self._format = format
        return self
    
    def build(self):
        return Report(self._title, self._data, self._format)

# Usage
builder = ReportBuilder()

report1 = builder.set_title("Q1 Report").add_data([1, 2, 3]).build()
report2 = builder.set_title("Q2 Report").add_data([4, 5, 6]).build()

print(report1.data)  # What will this print?
```
---

**What's the output and what's the problem?**

- A) `[1, 2, 3]` - No problem
- B) `[1, 2, 3, 4, 5, 6]` - Builder state is shared!
- C) `Error` - Can't reuse builder
- D) `None` - Data not set properly

---

<details>
<summary>Answer</summary>

**B) `[1, 2, 3, 4, 5, 6]` - Builder state is shared!**

**The Problem:**

```python
builder = ReportBuilder()  # Single builder instance

# First build
report1 = builder
    .set_title("Q1 Report")
    .add_data([1, 2, 3])    # builder._data = [1, 2, 3]
    .build()

# Second build - REUSES the same builder!
report2 = builder
    .set_title("Q2 Report")
    .add_data([4, 5, 6])    # builder._data = [1, 2, 3, 4, 5, 6] ⚠️
    .build()

print(report1.data)  # [1, 2, 3, 4, 5, 6] - WRONG!
print(report2.data)  # [1, 2, 3, 4, 5, 6] - If passing by reference
```
---

**Solution:**

```python
# ✅ Create NEW builder for each object
report1 = ReportBuilder()
    .set_title("Q1 Report")
    .add_data([1, 2, 3])
    .build()

report2 = ReportBuilder()  # NEW builder instance
    .set_title("Q2 Report")
    .add_data([4, 5, 6])
    .build()

print(report1.data)  # [1, 2, 3] ✓
print(report2.data)  # [4, 5, 6] ✓
```

**Key lesson:** Never reuse builder instances! Each object needs a fresh builder.

</details>

---

## Question 5: Understanding `@staticmethod`

```python
class Database:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    # Option A: Instance method
    def create_helper(self):
        return Helper(self.host)
    
    # Option B: Static method
    @staticmethod
    def create_helper_static():
        return Helper()
    
    # Option C: Class method
    @classmethod
    def create_helper_class(cls):
        return Helper()

class Helper:
    def __init__(self, host=None):
        self.host = host
```

**When should you use `@staticmethod`?**

- A) When you need access to instance data (`self`)
- B) When you don't need `self` or `cls` - just a utility function
- C) When you need to access the class itself (`cls`)
- D) Always use it for better performance

---

<details>
<summary>Answer</summary>

**B) When you don't need `self` or `cls` - just a utility function**

**Understanding the differences:**

```python
class MathUtils:
    pi = 3.14159
    
    # Instance method - needs self
    def get_circle_area(self, radius):
        return self.pi * radius * radius  # Uses self.pi
    
    # Static method - doesn't need self or cls
    @staticmethod
    def add(a, b):
        return a + b  # Just a utility function
    
    # Class method - needs cls
    @classmethod
    def get_pi(cls):
        return cls.pi  # Uses cls.pi

# Usage
utils = MathUtils()
area = utils.get_circle_area(5)  # Need instance

result = MathUtils.add(2, 3)  # No instance needed
pi = MathUtils.get_pi()  # No instance needed, but uses class
```
---
**When to use each:**

| Method Type | Has `self`? | Has `cls`? | Use When |
|-------------|-------------|------------|----------|
| Instance method | ✅ | ❌ | Need instance data |
| Static method | ❌ | ❌ | Utility function, no instance/class needed |
| Class method | ❌ | ✅ | Need class itself (factory methods) |

**Key point:** Use `@staticmethod` when the method doesn't need access to instance or class - it's logically related to the class but operates independently.

</details>

---

## Question 6: Understanding `@staticmethod` and Builder Creation

Look at this builder implementation:

```python
class Database:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    @staticmethod
    def builder():
        return Database.Builder()
    
    class Builder:
        def __init__(self):
            self._host = None
            self._port = None
            self._username = None
            self._password = None
        
        def set_host(self, host):
            self._host = host
            return self
        
        def build(self):
            return Database(self._host, self._port, 
                          self._username, self._password)
```

**Why is `@staticmethod` used instead of a regular method?**

- A) `@staticmethod` makes the method faster
- B) We don't need access to the instance (`self`) to create a Builder
- C) `@staticmethod` is required for inner classes
- D) Regular methods can't return objects

---

<details>
<summary>Answer</summary>

**B) We don't need access to the instance (`self`) to create a Builder**

### Why Static Works Best:

```python
# Scenario: Building a database connection
# We DON'T have a database yet - we're trying to CREATE one!

# ❌ Instance method doesn't make sense
# db = Database(???)  # We don't know the parameters yet!
# builder = db.builder()  # Circular logic!

# ✅ Static method makes perfect sense
builder = Database.builder()  # Start building
builder.set_host("localhost")
builder.set_port(3306)
database = builder.build()  # NOW we have a database!
```
---
### Comparison Table:

| Method Type | Has `self`? | Has `cls`? | When to Use |
|-------------|-------------|------------|-------------|
| **Instance method** | ✅ Yes | ❌ No | Need instance data |
| **Class method** | ❌ No | ✅ Yes | Factory methods, inheritance |
| **Static method** | ❌ No | ❌ No | Utility, doesn't need class/instance |
---

### Why Not @classmethod?

```python
# You COULD use @classmethod:
class Database:
    @classmethod
    def builder(cls):
        return Database.Builder()

# But it's unnecessary!
# We don't need 'cls' because:
# 1. We're explicitly using Database.Builder() anyway
# 2. Builder is tied to Database, not inherited classes

# @staticmethod is clearer about intent:
# "This method is just a utility that returns a Builder"
```
---
### Key Takeaways:

1. **`@staticmethod`** is used for `builder()` because:
   - We don't have a Database instance yet
   - We don't need instance data (`self`)
   - It's a factory/utility function
   
2. **Purpose of `builder()`:**
   - Starting point for building a new object
   - Called on the class, not an instance
   - Returns a new Builder to configure

3. **Why not just call `Database.Builder()` directly?**
   - Less intuitive API
   - Can't change implementation easily
   - Breaks encapsulation

**The pattern:** Use `@staticmethod` when the method doesn't need access to instance or class data - it's just a utility or factory function!

</details>

---

## Question 7: Method Chaining

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.grade = None
    
    def set_age(self, age):
        self.age = age
        return self  # What does this do?
    
    def set_grade(self, grade):
        self.grade = grade
        return self

# Usage
student = Student("Alice").set_age(20).set_grade("A")
```

**Why does this pattern work?**

- A) Because `return self` allows chaining method calls
- B) Python automatically returns `self` from methods
- C) It's a special syntax for Student class
- D) Methods are called in parallel

---

<details>
<summary>Answer</summary>

**A) Because `return self` allows chaining method calls**

### How it works:

```python
# Without method chaining
student = Student("Alice")
student.set_age(20)      # Returns None normally
student.set_grade("A")   # Returns None

# With method chaining (return self)
student = Student("Alice").set_age(20).set_grade("A")

# Step by step:
# 1. Student("Alice")           → returns student object
# 2. student.set_age(20)        → returns self (same student)
# 3. student.set_grade("A")     → returns self (same student)
```
---
### The pattern:

```python
class FluentAPI:
    def method1(self):
        # do something
        return self  # Key: return self
    
    def method2(self):
        # do something
        return self
    
    def method3(self):
        # do something
        return self

# Now you can chain
obj = FluentAPI().method1().method2().method3()
```
---
### Benefits:
- **Readability:** Reads like natural language
- **Concise:** No intermediate variables
- **Fluent:** Smooth, flowing API

### Builder Pattern uses this extensively!

```python
# Builder pattern preview
pizza = PizzaBuilder()
    .set_size("large")
    .add_cheese()
    .add_pepperoni()
    .build()
```
---
### Real-world parallel:

Think of ordering at Subway:
- ❌ Bad: "I want a sandwich with wheat bread, turkey, cheddar, lettuce, tomatoes, onions, pickles, mustard, mayo, no olives, no jalapeños, toasted"
- ✅ Good: "Wheat bread" → "Turkey" → "Cheddar" → "Lettuce, tomatoes, onions" → "Mustard and mayo" → "Toast it"

Step-by-step is clearer than one giant sentence!

</details>

---

## Section B: Factory Pattern Prerequisites

### Question 4: Object Creation Problem

```python
def send_notification(notification_type, user, message):
    """Send different types of notifications"""
    if notification_type == "email":
        # Email needs host, port, credentials
        notification = EmailNotification(
            recipient=user.email,
            smtp_host="smtp.gmail.com",
            smtp_port=587,
            username="noreply@company.com",
            password="secret123"
        )
        notification.send(message)
    
    elif notification_type == "sms":
        # SMS needs API key, phone validation
        notification = SMSNotification(
            phone=user.phone,
            api_key="twilio_key_xyz",
            country_code=user.country_code
        )
        notification.send(message)
    
    else:
        raise ValueError(f"Unknown notification type: {notification_type}")

```

**What are the problems with this approach?**

- A) Complex creation logic mixed with business logic
- B) Each notification type has different parameters - hard to manage
- C) Have to duplicate this complex creation logic everywhere
- D) All of the above

---

<details>
<summary>Answer</summary>

**D) All of the above**

**Problems illustrated:**


# Problem 1: Creation logic is COMPLEX, not just simple if-else
 Each notification type needs:
- Different parameters
- Different configuration
- Different credentials
- Different validation

# This complexity shouldn't be in business logic!
---
# Problem 2: Duplication nightmare
```python
def send_welcome_email(user):
    # Need to remember all Email parameters again!
    notification = EmailNotification(
        recipient=user.email,
        smtp_host="smtp.gmail.com",  # Duplicate config
        smtp_port=587,
        username="noreply@company.com",
        password="secret123"
    )
    notification.send("Welcome!")

def send_reminder_email(user):
    # Same parameters duplicated AGAIN!
    notification = EmailNotification(
        recipient=user.email,
        smtp_host="smtp.gmail.com",  # Still duplicating
        smtp_port=587,
        username="noreply@company.com",
        password="secret123"
    )
    notification.send("Reminder!")
```
---

# Problem 3: Easy to make mistakes
```python
def send_sms(user):
    notification = SMSNotification(
        phone=user.phone,
        api_key="wrong_key",        # Oops! Wrong key
        country_code="+91"           # Hardcoded instead of user.country_code
    )
    # Inconsistent creation!
```
---

# Problem 4: Configuration changes = update everywhere
- SMTP host changes? Update in 50 places! 💥
- API key rotates? Update everywhere! 💥

# Problem 5: Adding new notification type
```python
def send_notification(notification_type, user, message):
    if notification_type == "email":
        # 5 lines of email setup
    elif notification_type == "sms":
        # 4 lines of SMS setup
    elif notification_type == "push":
        # 4 lines of push setup
    elif notification_type == "slack":
        # 4 lines of slack setup
    elif notification_type == "discord":  # New type!
        # 5 more lines of discord setup
        notification = DiscordNotification(
            webhook_url="https://discord.com/...",
            channel_id=user.discord_channel,
            bot_token="discord_bot_token"
        )
        notification.send(message)
    # Function keeps growing! 💥
```
---

**What we need:**
- **Centralized complex creation logic** - all parameters in one place
- **Hide complexity** - business logic shouldn't know about SMTP hosts, API keys, etc.
- **Easy to maintain** - change configuration in one place
- **Consistent object creation** - same parameters used everywhere
- **Separate concerns** - creation logic separate from business logic

**This is where Factory Pattern helps!**

With Factory Pattern:
```python
# Business logic - simple and clean!
def send_notification(notification_type, user, message):
    notification = NotificationFactory.create(notification_type, user)
    notification.send(message)
    # No complex parameters!
    # No configuration details!
    # Just create and use!
```

**Key insight:** When object creation itself is complex (multiple parameters, configuration, validation), keeping it in business logic makes code:
- Hard to read
- Hard to maintain  
- Error-prone
- Difficult to test

Factory Pattern solves this by encapsulating the complexity!

</details>

---

---

### Question 5: From Simple Factory to Factory Method

```python
# Payment gateway interface
class PaymentGateway:
    def charge(self, amount):
        raise NotImplementedError

class StripeGateway(PaymentGateway):
    def charge(self, amount):
        print(f"Charging ${amount} via Stripe")
        return {"success": True}

class PayPalGateway(PaymentGateway):
    def charge(self, amount):
        print(f"Charging ${amount} via PayPal")
        return {"success": True}

# Simple Factory approach
class PaymentGatewayFactory:
    @staticmethod
    def create(gateway_type: str) -> PaymentGateway:
        if gateway_type == "stripe":
            return StripeGateway()
        elif gateway_type == "paypal":
            return PayPalGateway()
        else:
            raise ValueError(f"Unknown gateway: {gateway_type}")
```
---
```python
class OrderProcessor:
    def __init__(self):
        # Using factory to create gateway
        self.payment_gateway = PaymentGatewayFactory.create("stripe")
    
    def process_order(self, order):
        result = self.payment_gateway.charge(order.amount)
        if result["success"]:
            print("Order processed!")

```

**What problems still exist with this Simple Factory approach?**

- A) Works perfectly - no problems!
- B) Factory violates Open-Closed Principle (must modify to add new gateways)
- C) OrderProcessor violates Dependency Inversion Principle (depends on factory, and tightly coupled with stripe)
- D) B and C - still has design issues

---

<details>
<summary>Answer</summary>

**D) B and C - still has design issues**

**Problem 1: Factory violates Open-Closed Principle (OCP)**

```python
class PaymentGatewayFactory:
    @staticmethod
    def create(gateway_type: str) -> PaymentGateway:
        if gateway_type == "stripe":
            return StripeGateway()
        elif gateway_type == "paypal":
            return PayPalGateway()
        # Want to add Square gateway?
        elif gateway_type == "square":  # MUST MODIFY existing factory! ❌
            return SquareGateway()
        # Want to add Razorpay?
        elif gateway_type == "razorpay":  # MODIFY again! ❌
            return RazorpayGateway()
        
        # Every new gateway = modify this class
        # Violates OCP: Should be open for extension, closed for modification
```
---
**Problem 2: OrderProcessor violates Dependency Inversion Principle (DIP)**

```python
class OrderProcessor:
    def __init__(self):
        # Depends on concrete factory and string type
        self.payment_gateway = PaymentGatewayFactory.create("stripe")
        # ❌ High-level module (OrderProcessor) depends on low-level module (Factory, stripe)
        # ❌ Depends on implementation detail (string gateway_type)
    
    def process_order(self, order):
        result = self.payment_gateway.charge(order.amount)
        if result["success"]:
            print("Order processed!")

# Problems:
# - Can't easily mock the factory for testing
# - OrderProcessor knows about factory implementation
# - Hard to change how gateways are created
```
---
**Problem 3: Testing is still difficult**

```python
# ❌ Hard to test - factory is called inside constructor
class OrderProcessorTest:
    def test_process_order(self):
        # How do we inject a mock gateway?
        # Factory.create() is called in __init__
        # Can't easily control what gets created
        processor = OrderProcessor()  # Creates real Stripe gateway!
```
---
**Better approach: Factory Method Pattern**

```python
from abc import ABC, abstractmethod

# Abstract creator with factory method
class OrderProcessor(ABC):
    def __init__(self):
        self.payment_gateway = self.create_payment_gateway()
    
    @abstractmethod
    def create_payment_gateway(self) -> PaymentGateway:
        """Factory method - subclasses implement this"""
        pass
    
    def process_order(self, order):
        result = self.payment_gateway.charge(order.amount)
        if result["success"]:
            print("Order processed!")

# Concrete creators - each creates specific gateway
class StripeOrderProcessor(OrderProcessor):
    def create_payment_gateway(self) -> PaymentGateway:
        return StripeGateway()

class PayPalOrderProcessor(OrderProcessor):
    def create_payment_gateway(self) -> PaymentGateway:
        return PayPalGateway()

# Want to add Square? Just create new class! ✅
class SquareOrderProcessor(OrderProcessor):
    def create_payment_gateway(self) -> PaymentGateway:
        return SquareGateway()
    # No modification to existing code! Follows OCP ✅
```
---

# Usage
```python
stripe_processor = StripeOrderProcessor()
paypal_processor = PayPalOrderProcessor()
square_processor = SquareOrderProcessor()  # New gateway - no changes to existing code!

# Testing is easy now!
class MockOrderProcessor(OrderProcessor):
    def create_payment_gateway(self) -> PaymentGateway:
        return MockPaymentGateway()  # Inject mock for testing!

test_processor = MockOrderProcessor()  # Easy to test ✅
```
---

**Key improvements with Factory Method:**

✅ **Follows Open-Closed Principle:**
- Add new gateways by creating new subclasses
- No modification to existing code

✅ **Follows Dependency Inversion Principle:**
- High-level module (OrderProcessor) defines interface
- Low-level modules (concrete processors) implement it
- Both depend on abstraction (PaymentGateway interface)

✅ **Easy to test:**
- Create MockOrderProcessor for testing
- No need to modify production code

✅ **Better separation of concerns:**
- Each processor knows how to create its own gateway
- Creation logic distributed to appropriate classes

**Summary:**
- **Simple Factory** = Centralized creation, but violates OCP
- **Factory Method** = Distributed creation, follows OCP and DIP
- Use Factory Method when you need extensibility without modifying existing code

</details>
---

### Question 6: Platform-Specific Object Creation

```python
import platform

class Application:
    def __init__(self):
        # Detect OS and create appropriate UI elements
        os_type = platform.system()
        
        if os_type == "Windows":
            self.button = WindowsButton()
            self.checkbox = WindowsCheckbox()
            self.menu = WindowsMenu()
        elif os_type == "Darwin":  # macOS
            self.button = MacButton()
            self.checkbox = MacCheckbox()
            self.menu = MacMenu()
        elif os_type == "Linux":
            self.button = LinuxButton()
            self.checkbox = LinuxCheckbox()
            self.menu = LinuxMenu()
    
    def render(self):
        self.button.render()
        self.checkbox.render()
        self.menu.render()
```

**What problems do you see with this approach?**

- A) Need to remember to create all platform-specific components together
- B) Easy to mix Windows button with Mac checkbox by mistake
- C) Hard to add support for a new platform
- D) All of the above

---

<details>
<summary>Answer</summary>

**D) All of the above**

**Problems illustrated:**

```python
# Problem 1: Easy to create inconsistent UI
if os_type == "Windows":
    self.button = WindowsButton()
    self.checkbox = MacCheckbox()      # Oops! Wrong OS!
    self.menu = WindowsMenu()
# Windows app with Mac checkbox? 💥
# Problem 2: Adding new platform means modifying many places
# Want to add Android support?
if os_type == "Windows":
    # ...
elif os_type == "Darwin":
    # ...
elif os_type == "Linux":
    # ...
elif os_type == "Android":  # Add here
    self.button = AndroidButton()
    self.checkbox = AndroidCheckbox()
    self.menu = AndroidMenu()
# Have to modify every component creation!
```
---
```python
# Problem 3: Components must be created together
# Can't just create a button - need entire family
# But easy to forget one:
if os_type == "Windows":
    self.button = WindowsButton()
    self.checkbox = WindowsCheckbox()
    # Forgot menu! 💥

# Problem 4: Duplication
class LoginDialog:
    def __init__(self):
        # Same OS detection logic duplicated!
        if os_type == "Windows":
            self.button = WindowsButton()
            # ...

class SettingsDialog:
    def __init__(self):
        # Duplicated again!
        if os_type == "Windows":
            self.button = WindowsButton()
            # ...
```
---
**What we need:**
- Ensure all components belong to the same family (all Windows or all Mac)
- Easy way to add new platforms without modifying existing code
- Centralized logic for creating related objects
- **This is where Abstract Factory Pattern helps!**

**Hint:** Abstract Factory creates **families** of related objects, ensuring they're compatible.

</details>

---

## Summary: What Problems Do Factory Patterns Solve?

After these questions, you should understand:

### From Builder Pattern:
✅ Separate construction logic from the object  
✅ Handle complex object creation step-by-step  
✅ Use when many parameters or complex validation needed

### New Problems (Factory Pattern Territory):
❌ **Object creation scattered everywhere** → Need centralized creation  
❌ **Hard to switch implementations** → Need flexible creation  
❌ **Tight coupling to concrete classes** → Need abstraction  
❌ **Creating families of related objects** → Need to ensure consistency

**Factory Patterns solve these problems!** Let's learn how. 🚀