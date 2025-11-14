# The Singleton Pattern:

## Part 1: Foundation - Quick Python Refresher

Before we dive into Singleton, let's quickly revisit some Python fundamentals we'll need.

### Class Variables vs Instance Variables

```python
class Counter:
    total_count = 0  # Class variable - shared across ALL instances
    
    def __init__(self, name):
        self.name = name  # Instance variable - unique to each instance
        Counter.total_count += 1

c1 = Counter("First")
c2 = Counter("Second")

print(c1.name)           # "First" - different for each instance
print(c2.name)           # "Second"
print(Counter.total_count)  # 2 - shared across all instances
```

**Key Point:** Class variables are shared; instance variables are not.

---

### Static Methods vs Class Methods

```python
class MathUtils:
    pi = 3.14159  # Class variable
    
    @staticmethod
    def add(a, b):
        return a + b  # No access to class or instance
    
    @classmethod
    def get_pi(cls):
        return cls.pi  # Can access class variables via 'cls'

print(MathUtils.add(2, 3))  # 5
print(MathUtils.get_pi())   # 3.14159
```

**Key Point:** Static methods are just namespaced functions. Class methods can access/modify class state.

---

### Encapsulation in Python

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # "Private" by convention (single underscore)
    
    def get_balance(self):
        return self._balance

# Python doesn't enforce privacy - it's based on trust
account = BankAccount(1000)
print(account._balance)  # 1000 - accessible but discouraged
```

**Key Point:** Python doesn't have true private members. We use conventions (`_variable`) and raise errors when needed.

---

## Part 2: The Singleton Problem

Imagine you're building an application that needs a database connection. Let's see what happens without Singleton:

```python
class Database:
    def __init__(self):
        print("Creating expensive database connection...")
        self.connection = "Connected to PostgreSQL"

# Somewhere in your code
db1 = Database()  # "Creating expensive database connection..."
db2 = Database()  # "Creating expensive database connection..." again!

print(db1 is db2)  # False - Two different objects!
```

**Problems:**
- Memory waste (duplicate connections)
- Resource exhaustion (too many DB connections)
- Inconsistent state (different configurations)

**What we need:** Ensure only ONE instance exists, and everyone uses that same instance.

---

## Part 3: First Attempt - The `__init__` Trap

You might think: "Let's make the constructor private!"

```python
class Database:
    _instance = None
    
    def __init__(self):
        raise RuntimeError("Use get_instance() instead!")

```

**The Problem:** If `__init__` raises an error, we can never create an instance at all. We're stuck!

**The Realization:** We need to separate *object creation* from *object initialization*.

---

## Part 4: Enter `__new__` - The Real Constructor

Python has a secret: before `__init__` runs, `__new__` creates the object!

```python
class Example:
    def __new__(cls):
        print("1. __new__ called - creating object")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self):
        print("2. __init__ called - initializing object")

obj = Example()
# Output:
# 1. __new__ called - creating object
# 2. __init__ called - initializing object
```

**The Flow:** 
1. `__new__` creates the raw object
2. `__new__` returns the object
3. `__init__` initializes it

**The Insight:** We can control creation in `__new__` and return the same instance every time!

---

## Part 5: Classic Singleton with `__new__`

Now we can implement our Singleton properly:

```python
class Database:
    _instance = None  # Class variable to store the single instance
    
    def __new__(cls):
        if cls._instance is None:
            print("Creating first (and only) instance")
            cls._instance = super().__new__(cls)
        else:
            print("Returning existing instance")
        return cls._instance
    
    def __init__(self):
        print("__init__ called")

# Let's test it
db1 = Database()
# Output:
# Creating first (and only) instance
# __init__ called

db2 = Database()
# Output:
# Returning existing instance
# __init__ called (Oops! This runs again!)

print(db1 is db2)  # True - Same object!
```

**Success!** We have a single instance.

**Gotcha:** Notice `__init__` runs every time, even though we return the same object. We need to handle this:

```python
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            print("Initializing database connection")
            self.connection = "Connected to PostgreSQL"
            self._initialized = True
        else:
            print("Already initialized, skipping")

db1 = Database()  # "Initializing database connection"
db2 = Database()  # "Already initialized, skipping"
```

**This works!** But is it thread-safe?

---

## Part 6: The Multithreading Problem

Imagine two threads creating a Database instance simultaneously:

```python
# Thread 1                           # Thread 2
if cls._instance is None:           # Checks at the same time
                                     if cls._instance is None:
    cls._instance = super().__new__(cls)
                                     # Also creates an instance!
                                     cls._instance = super().__new__(cls)
```

**Result:** Two instances might be created! Race condition.

**Visualization:**
```
Time →
Thread A: [Check None] ─→ [Create Instance A] ─→ [Return A]
Thread B:      [Check None] ─→ [Create Instance B] ─→ [Return B]
                  ↑
                  Both see None!
```

---

## Part 7: Solution - Thread Lock (Simple but Slow)

Let's make it thread-safe with a lock:

```python
import threading

class Database:
    _instance = None
    _lock = threading.Lock()  # Create a lock
    
    def __new__(cls):
        with cls._lock:  # Acquire lock - only one thread can enter
            if cls._instance is None:
                print(f"Thread {threading.current_thread().name} creating instance")
                cls._instance = super().__new__(cls)
            return cls._instance

# Test with multiple threads
import time

def create_db():
    db = Database()
    print(f"Thread {threading.current_thread().name} got instance {id(db)}")

threads = [threading.Thread(target=create_db, name=f"T{i}") for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Output:
# Thread T0 creating instance
# Thread T0 got instance 140234567890
# Thread T1 got instance 140234567890  (same!)
# Thread T2 got instance 140234567890  (same!)
# ...
```

**Success:** Thread-safe!

**Problem:** Every single access acquires the lock, even after the instance is created. This is slow!

**Scenario:**
```python
# After first creation, the instance exists
# But EVERY call still acquires the expensive lock:
db1 = Database()  # Acquires lock (needed - creates instance)
db2 = Database()  # Acquires lock (unnecessary - instance exists)
db3 = Database()  # Acquires lock (unnecessary - instance exists)
# ... thousands of times
```

---

## Part 8: Double-Checked Locking (Fast and Safe)

The optimization: **check before locking**!

```python
import threading

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        # FIRST CHECK - fast, no lock needed
        if cls._instance is None:
            # Only acquire lock if instance doesn't exist
            with cls._lock:
                # SECOND CHECK - inside lock to be safe
                if cls._instance is None:
                    print(f"Thread {threading.current_thread().name} creating instance")
                    cls._instance = super().__new__(cls)
        
        return cls._instance

db1 = Database()  # First check fails → acquire lock → second check fails → create
db2 = Database()  # First check passes → return immediately (no lock!)
db3 = Database()  # First check passes → return immediately (no lock!)
```

**How it works:**

1. **First Check (outside lock):** Fast check - if instance exists, return immediately
2. **Lock Acquisition:** Only if first check fails (instance doesn't exist)
3. **Second Check (inside lock):** Ensures only one thread creates instance

**Why two checks?**

```
Thread A: [Check 1: None] ─→ [Acquire Lock] ─→ [Check 2: None] ─→ [Create] ─→ [Release]
Thread B:      [Check 1: None] ─→ [Wait for Lock] ─→ [Check 2: Exists!] ─→ [Return]
```

Without the second check, Thread B would create another instance!

**Performance:**
- **First creation:** Slight overhead from double-check
- **All subsequent calls:** Fast path (no lock)

---

## Part 9: Alternative Approaches

### Approach 1: Decorator Pattern

Instead of modifying the class, wrap it with a decorator:

```python
def singleton(cls):
    instances = {}  # Store instances per class
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Database initialized")
        self.connection = "Connected"

db1 = Database()  # "Database initialized"
db2 = Database()  # Returns existing instance
print(db1 is db2)  # True
```

**Benefits:**
- Clean class definition (no Singleton logic inside)
- Reusable for multiple classes
- More Pythonic

**When to use:** When you want to keep your class clean and apply Singleton pattern flexibly.

---

### Approach 2: Metaclass (Advanced)

A metaclass controls how classes are created. We can use it to control instance creation:

```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        # __call__ is invoked when you do ClassName()
        if cls not in cls._instances:
            # Create instance using parent's __call__
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("Database initialized")
        self.connection = "Connected"

db1 = Database()  # "Database initialized"
db2 = Database()  # Returns existing instance
print(db1 is db2)  # True
```

**How it works:**
1. When you write `Database()`, Python calls `SingletonMeta.__call__()`
2. The metaclass checks if an instance exists
3. Creates one if needed, or returns existing one

**Benefits:**
- Transparent to class users
- Works with inheritance
- Can handle multiple Singleton classes

**When to use:** When you need inheritance or want ultimate control.

---

**Thread-safe version:**

```python
import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:  # First check
            with cls._lock:
                if cls not in cls._instances:  # Second check
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"
```

---

### Approach 3: Module-Level Instance (Most Pythonic!)

Python modules are singletons by nature!

```python
# database.py
class _Database:
    def __init__(self):
        print("Database initialized")
        self.connection = "Connected"
    
    def query(self, sql):
        return f"Executing: {sql}"

# Create single instance at module level
database = _Database()
```

```python
# app.py
from database import database

# Everyone imports the same instance
database.query("SELECT * FROM users")
```

**Why this works:**
- Python imports a module only once
- Subsequent imports reuse the cached module
- The instance is created once when module loads

**Benefits:**
- Simple and clean
- No special Singleton code needed
- Pythonic idiom
- Thread-safe by default (module import is thread-safe)

**When to use:** For most Python applications - this is the recommended approach!

---

## Part 10: Practical Examples

### Example 1: Configuration Manager

```python
class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        self.db_host = "localhost"
        self.db_port = 5432
        self.api_key = "secret_key_123"
        self.debug = True

# Anywhere in your app
config = Config()
print(config.db_host)  # "localhost"

# Another file
config2 = Config()
print(config2.db_host)  # Same "localhost"
print(config is config2)  # True
```

**Why Singleton:** Single source of truth for application settings.

---

### Example 2: Logger

```python
class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.file = open("app.log", "a")
            self._initialized = True
    
    def log(self, level, message):
        self.file.write(f"[{level}] {message}\n")
        self.file.flush()

# Different modules can log to the same file
logger1 = Logger()
logger1.log("INFO", "Application started")

logger2 = Logger()
logger2.log("ERROR", "Something went wrong")

# Both write to the same file
print(logger1 is logger2)  # True
```

**Why Singleton:** Coordinate writes to single log file, prevent file conflicts.

---

### Example 3: Database Connection Pool

```python
class ConnectionPool:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.max_connections = 10
            self.active_connections = []
            self._initialized = True
    
    def get_connection(self):
        if len(self.active_connections) < self.max_connections:
            conn = f"Connection-{len(self.active_connections) + 1}"
            self.active_connections.append(conn)
            return conn
        else:
            return None  # Pool exhausted

# All parts of app share the same pool
pool = ConnectionPool()
conn1 = pool.get_connection()  # "Connection-1"
conn2 = pool.get_connection()  # "Connection-2"

# Another module
pool2 = ConnectionPool()
print(pool is pool2)  # True - same pool
print(pool2.active_connections)  # Shows both connections
```

**Why Singleton:** Control total number of connections across entire application.

---

## Part 11: When NOT to Use Singleton

### ❌ Anti-Pattern 1: God Object

```python
# DON'T DO THIS!
@singleton
class Utils:
    def format_date(self, date):
        pass
    
    def send_email(self, to, subject):
        pass
    
    def calculate_tax(self, amount):
        pass
    
    def resize_image(self, image):
        pass

# These are unrelated functions - just use modules!
```

**Better:** Use separate modules or simple functions.

---

### ❌ Anti-Pattern 2: Hidden Dependencies

```python
# BAD: Hidden dependency
class OrderService:
    def create_order(self, items):
        logger = Logger()  # Hidden! Hard to test
        logger.log("INFO", "Creating order")
        # ...

# GOOD: Explicit dependency
class OrderService:
    def __init__(self, logger):
        self.logger = logger  # Clear! Easy to test
    
    def create_order(self, items):
        self.logger.log("INFO", "Creating order")
        # ...
```

**Why better:** Easier to test, dependencies are explicit.

---

### ❌ Anti-Pattern 3: Domain Objects

```python
# DON'T make domain objects Singletons!
@singleton
class User:
    pass

# This makes no sense - you need multiple users!
```

**Remember:** Singleton is for infrastructure, not domain objects.

---

## Part 12: Comparison Table

| Approach | Complexity | Pythonic | Thread-Safe | Best For |
|----------|-----------|----------|-------------|----------|
| Module-level | ⭐ Simple | ⭐⭐⭐ Very | ✅ Yes | **Most cases** |
| `__new__` | ⭐⭐ Medium | ⭐⭐ Moderate | ❌ No (needs lock) | Learning, control |
| Decorator | ⭐⭐ Medium | ⭐⭐⭐ Very | ❌ No (needs lock) | Multiple singletons |
| Metaclass | ⭐⭐⭐ Complex | ⭐⭐ Moderate | ❌ No (needs lock) | Advanced needs |

**Add double-checked locking to any approach for thread safety!**

---

## Part 13: Key Takeaways

### ✅ Use Singleton for:
- Configuration objects
- Loggers
- Connection pools
- Caches
- Resource managers

### ❌ Avoid Singleton for:
- Domain objects (User, Order, Product)
- Stateless utilities (use functions instead)
- When you need multiple instances
- When testability is critical (prefer dependency injection)

### 🎯 Best Practices:
1. **Prefer module-level instances** (most Pythonic)
2. **Use double-checked locking** for thread safety
3. **Handle `__init__` carefully** (use initialization flag)
4. **Document why** you're using Singleton
5. **Consider alternatives** (dependency injection, context managers)

### 🔑 Remember:
- **Singleton = One instance per class**
- **Python modules are natural singletons**
- **Thread safety matters in concurrent applications**
- **It's a pattern, not a rule** - use when appropriate!

---

## Quick Decision Guide

```
Do you need exactly one instance?
├─ Simple case? → Use module-level instance ⭐
├─ Need thread safety? → Add double-checked locking
├─ Multiple singleton classes? → Use decorator
├─ Need inheritance/advanced control? → Use metaclass
└─ Just learning? → Start with __new__ method
```

---

**Final Wisdom:** The best Singleton in Python is often just a module-level instance. Keep it simple!