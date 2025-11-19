# Builder Pattern - Pre-requisite Questions

These questions help you understand why we need the Builder Pattern before diving into the implementation.

---

## Question 1: Constructor Complexity Problem

```python
class Pizza:
    def __init__(self, size, cheese, pepperoni, mushrooms, onions, 
                 bacon, olives, chicken, extra_cheese, stuffed_crust):
        self.size = size
        self.cheese = cheese
        self.pepperoni = pepperoni
        self.mushrooms = mushrooms
        self.onions = onions
        self.bacon = bacon
        self.olives = olives
        self.chicken = chicken
        self.extra_cheese = extra_cheese
        self.stuffed_crust = stuffed_crust

# Creating a simple margherita pizza
margherita = Pizza("large", True, False, False, False, 
                   False, False, False, False, False)
```

**What are the problems with this approach?**

- A) Hard to remember parameter order
- B) Unclear what `False, False, False` means
- C) Can't make some parameters optional easily
- D) All of the above

---
<details>
<summary>Answer</summary>

**D) All of the above**

**Problems illustrated:**

```python
# Problem 1: Parameter order confusion
pizza1 = Pizza("large", True, False, True, False, False, False, False, False, False)
# Which is mushrooms? Which is olives? 🤔

# Problem 2: Boolean hell - no clarity
pizza2 = Pizza("medium", True, False, False, False, False, False, False, False, False)
# What does this pizza have? Need to count positions!

# Problem 3: All parameters required, even defaults
simple_pizza = Pizza("small", True, False, False, False, False, False, False, False, False)
# Just want cheese pizza, but need to pass 10 parameters!

# Problem 4: Easy to make mistakes
wrong_pizza = Pizza("large", True, True, False, False, False, True, False, False, False)
# Accidentally put olives instead of onions? Good luck debugging!
```

**This is where Builder Pattern helps!**

</details>

---

## Question 2: Immutability and Object Construction

```python
# Option A: Mutable construction
class User:
    def __init__(self):
        self.name = None
        self.email = None
    
    def set_name(self, name):
        self.name = name
    
    def set_email(self, email):
        self.email = email

user = User()
user.set_name("Alice")
user.set_email("alice@example.com")

# Option B: Immutable construction
class User2:
    def __init__(self, name, email):
        self._name = name
        self._email = email
    
    @property
    def name(self):
        return self._name

user2 = User2("Alice", "alice@example.com")
```

**What's a problem with Option A in a multi-threaded environment?**

- A) Object can be used before it's fully initialized
- B) State can change unexpectedly during construction
- C) Thread A might see partially constructed object
- D) All of the above

---
<details>
<summary>Answer</summary>

**D) All of the above**

**The dangers of mutable construction:**

```python
# Thread 1
user = User()
user.set_name("Alice")
# -- Thread 1 paused here --
validate_user(user)  # Oops! Email is None!

# Thread 2 (executes while Thread 1 is paused)
user.set_email("alice@example.com")
```
---
**Problem scenarios:**

```python
# Scenario 1: Incomplete object used
user = User()
user.set_name("Alice")
send_email(user)  # 💥 Email is None! Crash!

# Scenario 2: Object passed before ready
def process_users(users):
    for user in users:
        print(f"{user.name}: {user.email}")

user = User()
users_list.append(user)  # Added to list but not initialized!
user.set_name("Bob")     # Set later
# Another thread processes list → sees None values

# Scenario 3: Validation nightmare
user = User()
if validate_user(user):  # How to validate? Some fields None!
    save_to_database(user)
user.set_name("Alice")   # Set after validation!
user.set_email("alice@example.com")
```
---
**Why immutability helps:**

```python
# Good: All or nothing
user = User2("Alice", "alice@example.com")
# Object is complete and valid from moment of creation
# Cannot change after creation
# Thread-safe by default
```
---
**Builder Pattern solution:**

```python
# Builder ensures complete object before creation
user = UserBuilder()
    .set_name("Alice")
    .set_email("alice@example.com")
    .build()  # Only here is the immutable User created
            # Validation happens in build()
            # Object is complete and immutable
```

**Key insight:**
- **Mutable construction** = risky, especially in concurrent code
- **Immutable object** = safe, but needs all data upfront
- **Builder Pattern** = best of both worlds (fluent construction → immutable result)

</details>

---

## Question 3: Telescoping Constructor Anti-Pattern

```python
class HttpRequest:
    # Constructor 1: Just URL
    def __init__(self, url):
        self.url = url
        self.method = "GET"
        self.headers = {}
        self.body = None
        self.timeout = 30
    
    # Constructor 2: URL + method
    def __init__(self, url, method):
        self.url = url
        self.method = method
        self.headers = {}
        self.body = None
        self.timeout = 30
    
    # Constructor 3: URL + method + headers
    def __init__(self, url, method, headers):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = None
        self.timeout = 30
    
    # ... more constructors ...
```

**What's wrong with this approach?**

- A) Python doesn't support method overloading like this
- B) Code duplication in every constructor
- C) Combinatorial explosion (too many constructors needed)
- D) All of the above

---
<details>
<summary>Answer</summary>

**D) All of the above**

**Problem 1: Python doesn't allow multiple `__init__` methods**

```python
class HttpRequest:
    def __init__(self, url):
        pass
    
    def __init__(self, url, method):  # This OVERWRITES the first one!
        pass

# Only the last __init__ exists
request = HttpRequest("https://api.com")  # 💥 TypeError: missing argument 'method'
```
---
**Problem 2: Even if Python supported it, combinatorial explosion**

```python
# How many constructors do you need?
__init__(url)
__init__(url, method)
__init__(url, method, headers)
__init__(url, method, headers, body)
__init__(url, method, headers, body, timeout)
__init__(url, method, headers, timeout)  # Skip body
__init__(url, method, body)  # Skip headers
__init__(url, method, timeout)  # Skip headers and body
__init__(url, headers)  # Skip method
__init__(url, body)  # Skip method and headers
# ... and so on

# With 5 optional parameters, you'd need 2^5 = 32 constructors! 🤯
```
---
**Problem 3: Code duplication**

```python
class HttpRequest:
    def __init__(self, url, method="GET", headers=None, body=None, timeout=30):
        self.url = url
        self.method = method
        self.headers = headers or {}
        self.body = body
        self.timeout = timeout

# Better, but still problems:
# 1. Easy to mix up parameter order
request = HttpRequest("url", "POST", None, "body", 60)
# What's None? What's the body? Confusing!

# 2. Can't skip middle parameters easily
request = HttpRequest("url", "POST", ???, "body")  # Want to skip headers
# Have to pass None explicitly

# 3. All parameters in one line gets messy
request = HttpRequest("https://api.com/users", "POST", 
                     {"Authorization": "Bearer token"}, 
                     {"name": "Alice"}, 60)
# Hard to read!
```
---
**Builder Pattern solution:**

```python
request = HttpRequestBuilder()
    .set_url("https://api.com/users")
    .set_method("POST")
    .add_header("Authorization", "Bearer token")
    .set_body({"name": "Alice"})
    .set_timeout(60)
    .build()

# Or just what you need
simple_request = HttpRequestBuilder()
    .set_url("https://api.com")
    .build()  # Uses defaults for everything else

# Benefits:
# ✅ Clear what each value is
# ✅ Only set what you need
# ✅ Readable and maintainable
# ✅ Can add new options without breaking existing code
```

</details>

---

## Question 4: Business Logic in Constructor

```python
class Database:
    def __init__(self, host, port, username, password):
        # Validation in constructor
        if not self.is_host_reachable(host):
            raise Exception("Host is not reachable")
        
        if port < 1024:
            raise Exception("Invalid port")
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def is_host_reachable(self, host):
        # Network call to check if host is reachable
        return True

# Creating a database makes network calls!
db = Database("localhost", 3306, "admin", "secret")
```

**What's the problem with this approach?**

- A) Constructor does too much (validation + network calls + construction)
- B) Hard to test without hitting the network
- C) Can't build the object step-by-step
- D) All of the above

---

<details>
<summary>Answer</summary>

**D) All of the above**

**The Problems:**

```python
# Problem 1: Can't test without side effects
db = Database("localhost", 3306, "user", "pass")  # Makes network call!

# Problem 2: Constructor failure = no object at all
try:
    db = Database("unreachable-host", 3306, "user", "pass")
except Exception:
    # Can't inspect what went wrong
    pass

# Problem 3: Constructor keeps growing with more features
class Database:
    def __init__(self, host, port, username, password,
                 ssl=False, timeout=30, pool_size=10):
        # Validation logic grows
        # More parameters = more complexity
        pass
```

**Key insight:** Constructor should ideally just assign values, not contain complex business logic or validation. We need a better way to separate construction from validation.

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

### Understanding @staticmethod:

```python
# What's the difference?

class Database:
    # Regular instance method
    def get_info(self):
        # Has access to 'self' (the Database instance)
        return f"Host: {self.host}, Port: {self.port}"
    
    # Static method
    @staticmethod
    def builder():
        # No access to 'self'
        # Just returns a new Builder
        return Database.Builder()
    
    # Class method
    @classmethod
    def from_url(cls, url):
        # Has access to 'cls' (the Database class itself)
        # Can create instances using cls()
        return cls(host, port, user, pass)
```
---
### Why Static Method for `builder()`?

```python
# ❌ If we used a regular instance method:
class Database:
    def builder(self):  # Needs 'self'
        return Database.Builder()

# Problem: Need an existing Database instance first!
db = Database("localhost", 3306, "user", "pass")  # Must create Database first
builder = db.builder()  # Then get builder from it
# This defeats the purpose! We're using builder to CREATE databases!

# ✅ With static method:
class Database:
    @staticmethod
    def builder():  # No 'self' needed
        return Database.Builder()

# Can call without any Database instance
builder = Database.builder()  # Just call it on the class!
database = builder.set_host("localhost").build()  # Now create the database
```
---
### When to Use Each Type:

```python
class Database:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection_count = 0
    
    # ✅ Instance method - needs existing instance data
    def get_connection_info(self):
        return f"{self.host}:{self.port} ({self.connection_count} connections)"
    
    # ✅ Static method - doesn't need instance or class
    @staticmethod
    def builder():
        return Database.Builder()
    
    @staticmethod
    def validate_port(port):
        return 1024 <= port <= 65535
    
    # ✅ Class method - needs the class itself (for inheritance)
    @classmethod
    def create_local(cls):
        return cls("localhost", 3306)
    
    @classmethod
    def from_config(cls, config):
        return cls(config['host'], config['port'])
```
---

### Real Example - Why Static Works Best:

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

## Summary: Why Do We Need Builder Pattern?

After these questions, you should see these problems:

1. **Too many constructor parameters** → Hard to use, error-prone
2. **Telescoping constructors** → Code duplication, maintenance nightmare
3. **Mutable construction** → Thread-unsafe, can use incomplete objects
4. **Boolean parameters** → Unclear meaning (`true, false, false, true` - what?)
5. **Optional parameters** → Hard to handle elegantly
6. **Named parameters with business logic** → Constructor becomes bloated, hard to maintain
7. **Direct builder instantiation** → Exposes implementation, less flexible
8. **Need for static factory method** → Better encapsulation and API design

**Builder Pattern solves all of these!**
