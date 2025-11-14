# Singleton Pattern - Prerequisite Quiz

### Question 1: Class-Level Members

```python
class Counter:
    count = 0  # What kind of variable is this?
    
    def __init__(self):
        self.instance_count = 0
    
    def increment(self):
        Counter.count += 1
        self.instance_count += 1

c1 = Counter()
c2 = Counter()
c1.increment()
c2.increment()

print(Counter.count)        # ?
print(c1.instance_count)    # ?
print(c2.instance_count)    # ?
```

**What are the outputs?**
- A) 2, 1, 1  
- B) 1, 1, 1  
- C) 2, 2, 2  
- D) 0, 1, 1
---
<details>
<summary>Answer</summary>

**- A) 2, 1, 1**

- `Counter.count` is a **class variable** (shared across all instances)
- `self.instance_count` is an **instance variable** (separate per instance)

**Key Concept:**
```python
class MyClass:
    class_var = 0      # Shared by ALL instances
    
    def __init__(self):
        self.instance_var = 0  # Separate per instance
```
</details>

---

### Question 2: Encapsulation in Python

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance      # Single underscore
        self.__secret = "12345"      # Double underscore
    
    def get_balance(self):
        return self._balance

account = BankAccount(1000)

print(account._balance)      # Works?
print(account.__secret)      # Works?
print(account._BankAccount__secret)  # Works?
```

**Which statements are TRUE?**
- A) `_balance` is private, cannot access  
- B) `__secret` is name-mangled to `_BankAccount__secret`  
- C) Python has true private members  
- D) Both A and B
---
<details>
<summary>Answer</summary>

**- B) `__secret` is name-mangled to `_BankAccount__secret`**

```python
account._balance           # ✅ Works (convention: protected)
account.__secret          # ❌ AttributeError
account._BankAccount__secret  # ✅ Works (name mangling exposed)
```

**Python Encapsulation:**
- `_single`: Convention for "protected" (developer hint)
- `__double`: Name mangling (harder to access)
- **No true private** - Python trusts developers

</details>

---

### Question 3: Object Creation Process

```python
class MyClass:
    def __new__(cls):
        print("__new__ called")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self):
        print("__init__ called")

obj = MyClass()
```

**What's the output and order?**
- A) `__init__ called` then `__new__ called`  
- B) `__new__ called` then `__init__ called`  
- C) Only `__new__ called`  
- D) Only `__init__ called`
---
<details>
<summary>Answer</summary>

**- B) `__new__ called` then `__init__ called`**

**Object creation flow:**
```
1. __new__(cls)     → Creates the instance (memory allocation)
2. __init__(self)   → Initializes the instance (setup)
```

**Key differences:**
- `__new__`: Class method, creates object, must return instance
- `__init__`: Instance method, initializes object, returns None

</details>

---

**Key differences:**

| Aspect | `__new__` | `__init__` |
|--------|----------|-----------|
| Purpose | Create instance | Initialize instance |
| First param | `cls` (class) | `self` (instance) |
| Return | Instance | None |
| When used | Rare | Common (setup) |

---

### Question 4: When Single Instance Makes Sense

**Which scenario REQUIRES only one instance?**

- A) Database connection pool manager  
- B) User objects in a web app  
- C) Shopping cart items  
- D) Blog post objects
---
<details>
<summary>Answer</summary>

**- A) Database connection pool manager**

**Why single instance needed:**
```python
# BAD: Multiple connection pools
pool1 = ConnectionPool(max_connections=10)
pool2 = ConnectionPool(max_connections=10)
# Now you have 20 connections total! Resource waste!

# GOOD: Single connection pool
pool = ConnectionPool.get_instance()  # Always same pool
# Controlled resource management
```

**Other examples needing Singleton:**
- Configuration manager (one config for entire app)
- Logger (single logging destination)
- Cache manager (shared cache)
- Thread pool (controlled thread count)

**Not Singleton:**
- User objects - multiple users exist
- Shopping carts - one per user
- Blog posts - many posts exist
</details>
---
