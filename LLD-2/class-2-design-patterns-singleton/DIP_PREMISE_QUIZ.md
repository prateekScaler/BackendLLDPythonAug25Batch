### Question 1:

```python
class EmailService:
    def send_email(self, to, message):
        print(f"Sending email to {to}: {message}")

class UserService:
    def __init__(self):
        self.email_service = EmailService()  # Created here!
    
    def register_user(self, user):
        # Save user logic
        self.email_service.send_email(user.email, "Welcome!")
```

**What's the problem with this code?**

- A) EmailService should be private  
- B) UserService is tightly coupled to EmailService  
- C) register_user method is too long  
- D) No problem, this is good design
---
<details>
<summary>Answer</summary>

**- B) UserService is tightly coupled to EmailService**

**Problems:**
- Can't swap EmailService for SMSService without modifying UserService
- Can't test UserService without real EmailService
- Hard to change notification method
- High-level (UserService) depends on low-level (EmailService)

**What if requirements change?**
```python
# Now need SMS instead - must modify UserService!
class UserService:
    def __init__(self):
        self.sms_service = SMSService()  # Changed here
    
    def register_user(self, user):
        self.sms_service.send_sms(user.phone, "Welcome!")  # Changed here
```

**Key insight:** Direct instantiation (`new`) creates tight coupling!
</details>

---

### Question 2: Testability Challenge

```python
import mysql.connector

class OrderRepository:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="prod-db.company.com",
            user="admin",
            password="secret123"
        )
    
    def save_order(self, order):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO orders VALUES (?)", order)

class OrderService:
    def __init__(self):
        self.repo = OrderRepository()  # Direct dependency!
    
    def create_order(self, order):
        # Business logic
        self.repo.save_order(order)
```

**How would you write a unit test for `OrderService.create_order()`?**

- A) Easy - just call create_order()  
- B) Need to connect to production database  
- C) Need to mock mysql.connector globally  
- D) Very difficult without refactoring
---
<details>
<summary>Answer</summary>

**- D) Very difficult without refactoring**

**Problems with testing:**

**Why so hard?**
- OrderService creates OrderRepository internally
- OrderRepository creates MySQL connection internally
- No way to inject a fake repository
- No abstraction to mock against

**Better approach preview:**
```python
# With dependency injection (DIP)
class OrderService:
    def __init__(self, repo):  # Injected!
        self.repo = repo

# Easy to test
def test_create_order():
    fake_repo = FakeRepository()
    service = OrderService(fake_repo)  # Inject fake!
    service.create_order(order)
    # No database needed!
```

**Key insight:** Direct dependencies make testing painful!
</details>

---

### Question 3: Change Propagation

```python
class MySQLDatabase:
    def connect(self):
        return "Connected to MySQL"
    
    def execute_query(self, query):
        return f"MySQL: {query}"

class PostgreSQLDatabase:
    def connect(self):
        return "Connected to PostgreSQL"
    
    def run_query(self, sql):  # Different method name!
        return f"PostgreSQL: {sql}"

class ReportGenerator:
    def __init__(self):
        self.db = MySQLDatabase()
    
    def generate(self):
        self.db.connect()
        data = self.db.execute_query("SELECT * FROM sales")
        return f"Report: {data}"
```

**What happens if you need to switch from MySQL to PostgreSQL?**

- A) Just change `MySQLDatabase()` to `PostgreSQLDatabase()`  
- B) Must change ReportGenerator code (method names differ)  
- C) No changes needed  
- D) Only change database configuration
---
<details>
<summary>Answer</summary>

**- B) Must change ReportGenerator code (method names differ)**


**Ripple effect:**
- Change database type → Must change ReportGenerator
- Different interface → Must update all method calls
- What if used in 20 places?
- Every place needs modification!

**Why this happens:**
- ReportGenerator depends on concrete MySQL class
- PostgreSQL has different interface
- No abstraction to program against

**Better approach:**
```python
from abc import ABC, abstractmethod

class Database(ABC):  # Abstraction!
    @abstractmethod
    def connect(self): pass
    
    @abstractmethod
    def query(self, sql): pass  # Unified interface

class MySQLDatabase(Database):
    def connect(self):
        return "Connected to MySQL"
    
    def query(self, sql):
        return f"MySQL: {sql}"

class PostgreSQLDatabase(Database):
    def connect(self):
        return "Connected to PostgreSQL"
    
    def query(self, sql):
        return f"PostgreSQL: {sql}"

class ReportGenerator:
    def __init__(self, db: Database):  # Depend on abstraction!
        self.db = db
    
    def generate(self):
        self.db.connect()
        data = self.db.query("SELECT * FROM sales")
        return f"Report: {data}"

# Easy to switch!
mysql_gen = ReportGenerator(MySQLDatabase())
postgres_gen = ReportGenerator(PostgreSQLDatabase())
# No code changes in ReportGenerator!
```

**Key insight:** Depending on concrete classes makes changes ripple everywhere!
</details>

---

## 🎯 Key Problems Identified

From these questions, we see three major issues:

### 1. **Tight Coupling**
```python
# BAD: Creates dependency internally
class Service:
    def __init__(self):
        self.dep = ConcreteDependency()  # Tight coupling!
```

**Problems:**
- Can't swap implementations
- Modification required for changes
- Inflexible design

---

### 2. **Testing Difficulty**
```python
# BAD: Need real database, SMTP, etc.
class Service:
    def __init__(self):
        self.db = MySQL()
        self.email = SMTP()
```

**Problems:**
- Can't use test doubles
- Need real infrastructure
- Slow tests
- Fragile tests

---

### 3. **Change Propagation**
```python
# BAD: Switch database → change everywhere
class Service:
    def process(self):
        result = self.mysql.execute_query()  # MySQL-specific!
```

**Problems:**
- Changes ripple through codebase
- Must update many files
- Breaks existing code
- Violates Open/Closed

---

## ✅ Solution Preview: Dependency Inversion

**Principle:** "Depend on abstractions, not concretions"

### Pattern to Learn:

**Instead of:**
```python
class HighLevel:
    def __init__(self):
        self.low_level = ConcreteLowLevel()  # BAD!
```

**Do this:**
```python
class LowLevelInterface(ABC):  # Abstraction
    @abstractmethod
    def operation(self): pass

class HighLevel:
    def __init__(self, low_level: LowLevelInterface):  # GOOD!
        self.low_level = low_level
```

**Benefits:**
- ✅ Easy to swap implementations
- ✅ Testable with mocks
- ✅ Changes don't propagate
- ✅ Flexible architecture

---

## 💡 Key Insights

**From Question 1:** Direct instantiation = tight coupling  
**From Question 2:** Tight coupling = hard to test  
**From Question 3:** Concrete dependencies = changes ripple

**Solution:**
1. Create abstractions (interfaces)
2. Inject dependencies (don't create them)
3. Program to interfaces, not implementations

---

## 🚀 You're Ready for DIP!

These problems motivate the **Dependency Inversion Principle**:

> "High-level modules should not depend on low-level modules.  
> Both should depend on abstractions."

Let's learn how to solve these problems! 🎯