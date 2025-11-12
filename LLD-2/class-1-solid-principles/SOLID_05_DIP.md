# Dependency Inversion Principle (DIP)

## 📖 Definition

**"High-level modules should not depend on low-level modules. Both should depend on abstractions."**

**Simple:** Depend on interfaces, not concrete implementations.

---

## 🎯 The Problem: Direct Dependencies

```python
class MySQLDatabase:
    def save(self, data):
        # MySQL-specific code
        return f"Saved to MySQL: {data}"


class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # Direct dependency!
    
    def create_order(self, order):
        # Business logic
        self.db.save(order)
        # Tightly coupled to MySQL!
```

**Problems:**
- Can't switch to PostgreSQL without changing OrderService
- Hard to test (needs real MySQL)
- High-level (business logic) depends on low-level (database)
- Violates DIP

---

## ✅ Solution: Depend on Abstraction

```python
from abc import ABC, abstractmethod

# Abstraction
class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass


# Low-level modules
class MySQLDatabase(Database):
    def save(self, data):
        return f"Saved to MySQL: {data}"


class PostgreSQLDatabase(Database):
    def save(self, data):
        return f"Saved to PostgreSQL: {data}"


# High-level module
class OrderService:
    def __init__(self, db: Database):  # Depends on abstraction!
        self.db = db
    
    def create_order(self, order):
        # Business logic
        self.db.save(order)
        # No dependency on specific database!


# Usage - inject dependency
mysql = MySQLDatabase()
service = OrderService(mysql)

# Easy to switch
postgres = PostgreSQLDatabase()
service = OrderService(postgres)

# Easy to test
class FakeDatabase(Database):
    def save(self, data):
        return "Saved to fake DB"

test_service = OrderService(FakeDatabase())
```

**Benefits:**
- Easy to switch implementations
- Testable with mocks
- Business logic independent of infrastructure
- Flexible architecture

---

## 🚩 Signs of Violation

### Red Flag 1: new in Constructor
```python
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # Creates dependency!
        self.email = SMTPEmailer()
        self.logger = FileLogger()
        # Tight coupling
```

### Red Flag 2: Import Concrete Classes
```python
from mysql_connector import MySQLDatabase  # Concrete!
from smtp_client import SMTPEmailer        # Concrete!

class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()
```

### Red Flag 3: Hard-coded Configurations
```python
class OrderService:
    def __init__(self):
        self.db_host = "mysql.prod.com"  # Hard-coded!
        self.db_port = 3306
        self.db = connect(self.db_host, self.db_port)
```

---

## 💡 How to Apply DIP

### Step 1: Identify Dependencies
```python
# OrderService depends on:
# - MySQLDatabase (storage)
# - SMTPEmailer (notifications)
# - FileLogger (logging)
```

### Step 2: Create Abstractions
```python
class Database(ABC):
    @abstractmethod
    def save(self, data): pass


class Notifier(ABC):
    @abstractmethod
    def send(self, message): pass


class Logger(ABC):
    @abstractmethod
    def log(self, message): pass
```

### Step 3: Inject Dependencies
```python
class OrderService:
    def __init__(self, db: Database, notifier: Notifier, logger: Logger):
        self.db = db
        self.notifier = notifier
        self.logger = logger
```

### Step 4: Wire at Application Root
```python
# main.py - composition root
def create_order_service():
    db = MySQLDatabase()
    notifier = EmailNotifier()
    logger = ConsoleLogger()
    return OrderService(db, notifier, logger)

service = create_order_service()
```

---

## 🎨 Practical Examples

### Example 1: Payment Processing

**❌ Bad (Depends on Concrete):**
```python
from stripe import StripeAPI

class PaymentProcessor:
    def __init__(self):
        self.stripe = StripeAPI(api_key="sk_...")  # Tight coupling!
    
    def process(self, amount):
        return self.stripe.charge(amount)
        # Can't switch to PayPal without rewriting
```

**✅ Good (Depends on Abstraction):**
```python
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount):
        pass


class StripeGateway(PaymentGateway):
    def __init__(self, api_key):
        self.api_key = api_key
    
    def charge(self, amount):
        return f"Stripe charged ${amount}"


class PayPalGateway(PaymentGateway):
    def __init__(self, client_id):
        self.client_id = client_id
    
    def charge(self, amount):
        return f"PayPal charged ${amount}"


class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    
    def process(self, amount):
        return self.gateway.charge(amount)


# Easy to switch
stripe = StripeGateway("sk_...")
processor = PaymentProcessor(stripe)

paypal = PayPalGateway("client_...")
processor = PaymentProcessor(paypal)
```

---

### Example 2: Notification System

**❌ Bad:**
```python
import smtplib

class UserService:
    def __init__(self):
        self.smtp = smtplib.SMTP('smtp.gmail.com')  # Concrete dependency!
    
    def register(self, user):
        # Save user
        # Send email
        self.smtp.send(user.email, "Welcome!")
        # Can't send SMS without changing code
```

**✅ Good:**
```python
class Notifier(ABC):
    @abstractmethod
    def send(self, recipient, message):
        pass


class EmailNotifier(Notifier):
    def __init__(self, smtp_server):
        self.smtp_server = smtp_server
    
    def send(self, recipient, message):
        return f"Email to {recipient}: {message}"


class SMSNotifier(Notifier):
    def __init__(self, twilio_client):
        self.twilio_client = twilio_client
    
    def send(self, recipient, message):
        return f"SMS to {recipient}: {message}"


class UserService:
    def __init__(self, notifiers: list[Notifier]):
        self.notifiers = notifiers
    
    def register(self, user):
        # Save user
        for notifier in self.notifiers:
            notifier.send(user.contact, "Welcome!")


# Flexible configuration
email = EmailNotifier("smtp.gmail.com")
sms = SMSNotifier(twilio_client)
service = UserService([email, sms])
```

---

### Example 3: Logging

**❌ Bad:**
```python
class OrderProcessor:
    def __init__(self):
        self.log_file = open("orders.log", "a")  # Concrete dependency!
    
    def process(self, order):
        self.log_file.write(f"Processing {order.id}\n")
        # Business logic
        # Stuck with file logging
```

**✅ Good:**
```python
class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass


class FileLogger(Logger):
    def __init__(self, filename):
        self.filename = filename
    
    def log(self, message):
        with open(self.filename, "a") as f:
            f.write(message + "\n")


class ConsoleLogger(Logger):
    def log(self, message):
        print(message)


class CloudLogger(Logger):
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
    
    def log(self, message):
        requests.post(self.api_endpoint, json={"log": message})


class OrderProcessor:
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def process(self, order):
        self.logger.log(f"Processing {order.id}")
        # Business logic


# Switch loggers easily
file_logger = FileLogger("orders.log")
processor = OrderProcessor(file_logger)

console_logger = ConsoleLogger()
processor = OrderProcessor(console_logger)
```

---

### Example 4: Complete Order System (DIP Applied)

```python
# Abstractions
class Database(ABC):
    @abstractmethod
    def save(self, data): pass


class Notifier(ABC):
    @abstractmethod
    def send(self, recipient, message): pass


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount): pass


# Concrete implementations
class MySQLDatabase(Database):
    def save(self, data):
        return "Saved to MySQL"


class EmailNotifier(Notifier):
    def send(self, recipient, message):
        return f"Email sent to {recipient}"


class StripeGateway(PaymentGateway):
    def charge(self, amount):
        return f"Charged ${amount} via Stripe"


# High-level business logic
class OrderService:
    def __init__(
        self,
        db: Database,
        notifier: Notifier,
        payment: PaymentGateway
    ):
        self.db = db
        self.notifier = notifier
        self.payment = payment
    
    def create_order(self, order):
        # Business logic (independent of infrastructure)
        self.payment.charge(order.total)
        self.db.save(order)
        self.notifier.send(order.customer_email, "Order confirmed!")


# Composition root
def configure_production():
    db = MySQLDatabase()
    notifier = EmailNotifier()
    payment = StripeGateway()
    return OrderService(db, notifier, payment)


def configure_test():
    db = FakeDatabase()
    notifier = FakeNotifier()
    payment = FakePayment()
    return OrderService(db, notifier, payment)
```

---

## ⚠️ When to Avoid DIP

### Don't abstract everything:

**❌ Over-abstraction:**
```python
# Overkill for Python built-ins
class StringManipulator(ABC):
    @abstractmethod
    def uppercase(self, text): pass

class PythonStringManipulator(StringManipulator):
    def uppercase(self, text):
        return text.upper()

# Just use: text.upper()
```

**✅ Reasonable:**
```python
# Abstract external dependencies, not language features
class Cache(ABC):
    @abstractmethod
    def get(self, key): pass
    
    @abstractmethod
    def set(self, key, value): pass

class RedisCache(Cache): ...
class MemoryCache(Cache): ...
```

**When to abstract:**
- External systems (databases, APIs)
- Third-party libraries
- Components likely to change
- Need for testing with mocks

**When not to abstract:**
- Language built-ins
- Stable standard library
- Simple, unlikely to change

---

## 🔧 Common Gotchas

### Gotcha 1: Leaky Abstractions
```python
# Bad - abstraction exposes implementation details
class Database(ABC):
    @abstractmethod
    def execute_sql(self, query):  # Assumes SQL!
        pass

# Good - implementation-agnostic
class Database(ABC):
    @abstractmethod
    def save(self, entity):
        pass
    
    @abstractmethod
    def find(self, id):
        pass
```

### Gotcha 2: Service Locator Anti-pattern
```python
# Bad - hidden dependencies
class ServiceLocator:
    services = {}

class OrderService:
    def create_order(self, order):
        db = ServiceLocator.get('database')  # Hidden dependency!
        db.save(order)

# Good - explicit dependencies
class OrderService:
    def __init__(self, db: Database):  # Clear dependency
        self.db = db
```

---

## ✅ Best Practices

1. **Inject dependencies** - Don't create them
2. **Program to interfaces** - Not implementations
3. **Composition root** - Wire dependencies at app entry
4. **Abstract boundaries** - External systems, not everything
5. **Test with fakes** - Leverage abstraction for testing

### Dependency Injection Patterns:

**Constructor Injection** (Preferred):
```python
class Service:
    def __init__(self, dep: Dependency):
        self.dep = dep
```

**Property Injection** (When needed):
```python
class Service:
    def set_dependency(self, dep: Dependency):
        self.dep = dep
```

**Method Injection** (Rare):
```python
class Service:
    def do_work(self, dep: Dependency):
        dep.execute()
```

---

## 🎯 Quick Checklist

- [ ] No `new` in constructors
- [ ] Dependencies injected
- [ ] Depends on abstractions (ABC/Protocol)
- [ ] Easy to swap implementations
- [ ] Testable with mocks

---

## 💡 Key Takeaway

**"Depend on abstractions, not concretions."**

High-level business logic should not depend on low-level implementation details. Both should depend on abstractions. This creates flexible, testable, maintainable systems where components can be easily swapped or mocked.

**Rule:** If you can't easily test it with fakes, you're violating DIP.