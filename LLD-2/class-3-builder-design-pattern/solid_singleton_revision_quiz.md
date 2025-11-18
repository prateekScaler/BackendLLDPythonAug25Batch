# Design Patterns & SOLID - Revision Quiz

---
### Question 1: 

```python
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass

class RobotWorker(Worker):
    def work(self):
        print("Robot working")
    
    def eat(self):
        pass  # Robots don't eat!
    
    def sleep(self):
        pass  # Robots don't sleep!
```

**What's the problem?**
- A) SRP - Worker does too many things
- B) ISP - RobotWorker forced to implement unused methods
- C) LSP - Robot can't substitute Human
- D) OCP - Can't extend without modification

---
<details>
<summary>Answer</summary>

**B) ISP - RobotWorker forced to implement unnecessary methods**

**ISP says:** Don't force clients to depend on methods they don't use.

**The Problem:** Robot forced to implement `eat()` and `sleep()` with dummy implementations.

**The Fix - Segregate Interfaces:**
```python
class Workable(ABC):

class Eatable(ABC):


class Sleepable(ABC):

class HumanWorker(Workable, Eatable, Sleepable):

class RobotWorker(Workable):  # Only what it needs!
```

**Key Lesson:** Many small, specific interfaces > One large, general interface!

</details>

---

### Question 2: 

```python
class SMTPEmailSender:
    def send(self, message):
        print(f"Sending via SMTP: {message}")

class OrderService:
    def __init__(self):
        self.email_sender = SMTPEmailSender()  # Direct dependency!
    
    def place_order(self, order):
        self.email_sender.send("Order placed!")

service = OrderService()
```

**Company wants to switch to SendGrid. What's the problem?**
- A) No problem, change SMTPEmailSender to SendGridSender
- B) Must modify OrderService (violates OCP)
- C) OrderService depends on concrete implementation (violates DIP)
- D) Both B and C

---
<details>
<summary>Answer</summary>

**D) Both B and C**
**DIP says:** High-level modules shouldn't depend on low-level modules—both should depend on abstractions.
**The Fix - Dependency Injection:**
```python
from abc import ABC, abstractmethod

class EmailSender(ABC):
    @abstractmethod
    def send(self, message):
        pass
class SMTPEmailSender(EmailSender):
    def send(self, message):
        print(f"SMTP: {message}")
class SendGridEmailSender(EmailSender):
    def send(self, message):
        print(f"SendGrid: {message}")
class OrderService:
    def __init__(self, email_sender: EmailSender):  # Inject!
        self.email_sender = email_sender
    def place_order(self, order):
        self.email_sender.send("Order placed!")

# Easy to switch
service = OrderService(SendGridEmailSender())
```

**Key Lesson:** Inject dependencies, don't create them! Depend on abstractions!

</details>

---

## 🔹 Part B: Singleton Pattern (5 Questions)

---

### Question 1: The `__init__` Trap

```python
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        print("Initializing database connection")
        self.connection_count = 0
        self.connection_count += 1

db1 = Database()
db2 = Database()
db3 = Database()

print(db1.connection_count)
print(db2.connection_count)
print(db3.connection_count)
print(db1 is db2 is db3)
```

**What is the output?**

- A) `1, 1, 1, True`
- B) `3, 3, 3, True`
- C) `1, 2, 3, True`
- D) `1, 1, 1, False`
---
<details>
<summary>Answer</summary>

**A) `1, 1, 1, True`**

**Explanation:** `__new__` creates only ONE instance, but `__init__` runs EVERY time you call `Database()`. Each call resets `connection_count = 0`, then increments to 1. Since it's the same object, all references show `connection_count = 1`.

**The Fix:**
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
            self.connection_count = 0
            self._initialized = True
        self.connection_count += 1
```

**Key Takeaway:** Guard `__init__` to run initialization only once!

</details>

---

### Question 2: Inheritance Gotcha

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class DatabaseConnection(Singleton):
    pass

class CacheConnection(Singleton):
    pass

db = DatabaseConnection()
cache = CacheConnection()

print(type(db))
print(type(cache))
print(db is cache)
```

**What is the output?**

- A) `<class 'DatabaseConnection'>`, `<class 'CacheConnection'>`, `False`
- B) `<class 'Singleton'>`, `<class 'Singleton'>`, `True`
- C) `<class 'DatabaseConnection'>`, `<class 'DatabaseConnection'>`, `True`
- D) `<class 'CacheConnection'>`, `<class 'CacheConnection'>`, `True`
---
<details>
<summary>Answer</summary>

**C) `<class 'DatabaseConnection'>`, `<class 'DatabaseConnection'>`, `True`**

**Explanation:** `_instance` is shared across all subclasses! First call creates `DatabaseConnection`, second call returns the same instance.

**The Fix:**
```python
class Singleton:
    _instances = {}
    
    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
```

**Key Takeaway:** Use a dictionary to store instances per class, not globally!

</details>

---

### Question 3:

```python
import threading
import time

class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            time.sleep(0.001)
            cls._instance = super().__new__(cls)
        return cls._instance

instances = []

def create_instance():
    instances.append(Singleton())

threads = [threading.Thread(target=create_instance) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(len(instances))
print(len(set(id(i) for i in instances)))
```
---
**What is the likely output?**

- A) `10, 1` (10 instances created, all same object)
- B) `10, 10` (10 instances created, all different objects)
- C) `10, 2-5` (10 instances created, 2-5 unique objects due to race condition)
- D) The program crashes

---
<details>
<summary>Answer</summary>

**C) `10, 2-5` (race condition creates multiple instances)**

**Explanation:** Multiple threads pass the `if cls._instance is None` check simultaneously before any can create the instance. The `time.sleep()` makes this race condition more likely.

**The Fix - Double-Checked Locking:**
```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:           # First check (fast)
            with cls._lock:                  # Acquire lock
                if cls._instance is None:    # Second check (safe)
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Key Takeaway:** Use double-checked locking for thread safety!

</details>

---

### Question 5: Serialization Surprise

```python
import pickle

class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.value = "original"

s1 = Singleton()
s1.value = "modified"

serialized = pickle.dumps(s1)
s2 = pickle.loads(serialized)

print(s1.value)
print(s2.value)
print(s1 is s2)
```
---
**What is the output?**

- A) `modified`, `modified`, `True`
- B) `modified`, `original`, `True`
- C) `modified`, `modified`, `False`
- D) Error: cannot pickle Singleton

---

<details>
<summary>Answer</summary>

**C) `modified`, `modified`, `False`**

**Explanation:** `pickle.loads()` creates a NEW instance, bypassing `__new__`! This breaks the Singleton pattern.

**The Fix:**
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __reduce__(self):
        return (self.__class__, ())
    
    def __copy__(self):
        return self
    
    def __deepcopy__(self, memo):
        return self
```

**Key Takeaway:** Implement `__reduce__`, `__copy__`, and `__deepcopy__` to preserve Singleton!

</details>

---

## 📊 Quick Reference

### SOLID Principles Covered
| Principle | Question |
|-----------|----------|
| **ISP** | Forced to implement unused methods? |
| **DIP** | Depend on abstractions? |

### Singleton Pitfalls

1. **`__init__` runs every time** → Guard with `_initialized` flag
2. **Inheritance shares `_instance`** → Use `_instances = {}` dict
3. **Not thread-safe** → Use double-checked locking
4. **Constructor args ignored** → Validate or reject different args
5. **Serialization breaks pattern** → Implement `__reduce__`

**Bonus Tip:** Python modules are natural singletons! Often better than class-based Singletons.

---