# Builder Design Pattern

## 📖 Definition

**"Separate the construction of a complex object from its representation so that the same construction process can create different representations."**

In simpler terms: Build complex objects step-by-step with a clean, readable API while keeping construction logic separate from the object itself.

---

## 🎯 The Problem (Recap from Prerequisites)

We've seen these issues with traditional object construction:

```python
# Problem 1: Too many parameters
pizza = Pizza("large", True, False, True, False, False, True, False, False, False)
# What does this even mean? 🤔

# Problem 2: Business logic in constructor
class Database:
    def __init__(self, host, port, username, password):
        if not self.is_host_reachable(host):  # Network call in constructor!
            raise Exception("Host not reachable")
        # ...

# Problem 3: Can't build incrementally
# All parameters needed upfront - no step-by-step construction
```

**The Builder Pattern solves all these problems!**

---

## 💡 The Solution

### Core Idea

Instead of:
```python
# Everything at once, unclear, error-prone
obj = ComplexObject(param1, param2, param3, param4, param5)
```

Do this:
```python
# Step-by-step, clear, flexible
obj = ComplexObject.builder()
    .param1(value1)
    .param2(value2)
    .param3(value3)
    .build()
```

---

## 🏗️ Implementation: Step-by-Step

Let's build a `Database` connection object using the Builder Pattern.

### Step 1: Create the Product Class (Simple Constructor)

```python
from dataclasses import dataclass

@dataclass
class Database:
    """The complex object we want to build"""
    host: str
    port: int
    username: str
    password: str
    
    def connect(self):
        print(f"Connecting to {self.host}:{self.port} as {self.username}")

# Note: Constructor is SIMPLE - just assigns values, no business logic!
```

### Step 2: Add Inner Builder Class

```python
@dataclass
class Database:
    host: str
    port: int
    username: str
    password: str
    
    @staticmethod
    def builder():
        """Factory method to create a builder"""
        return Database.Builder()
    
    class Builder:
        """Inner class that builds Database objects"""
        def __init__(self):
            # Initialize with None or defaults
            self._host = None
            self._port = None
            self._username = None
            self._password = None
```

**Why inner class?**
- Keeps builder close to the object it builds
- Encapsulates construction logic
- Clear relationship between Database and its builder

**Why `@staticmethod`?**
- Don't need a Database instance to create a builder
- Called on the class: `Database.builder()`
- Clean API for starting construction

### Step 3: Add Setter Methods with Method Chaining

```python
class Builder:
    def __init__(self):
        self._host = None
        self._port = None
        self._username = None
        self._password = None
    
    def set_host(self, host: str):
        """Set the database host"""
        self._host = host
        return self  # Return self for chaining!
    
    def set_port(self, port: int):
        """Set the database port"""
        self._port = port
        return self
    
    def set_username(self, username: str):
        """Set the username"""
        self._username = username
        return self
    
    def set_password(self, password: str):
        """Set the password"""
        self._password = password
        return self
```

**Why return `self`?**
- Enables method chaining
- Fluent, readable API
- Each method returns the builder for the next call

### Step 4: Add Build Method with Validation

```python
class Builder:
    # ... setter methods ...
    
    def build(self) -> Database:
        """Validate and create the Database object"""
        # Validation happens HERE, not in Database constructor!
        self._validate()
        
        return Database(
            host=self._host,
            port=self._port,
            username=self._username,
            password=self._password
        )
    
    def _validate(self):
        """Validate all required fields"""
        if not self._host:
            raise ValueError("Host is required")
        if not self._port:
            raise ValueError("Port is required")
        if not self._username:
            raise ValueError("Username is required")
        if not self._password:
            raise ValueError("Password is required")
        
        # Business logic validation
        if self._port < 1024 or self._port > 65535:
            raise ValueError("Port must be between 1024 and 65535")
```

**Key insight:** 
- Constructor stays simple (just assigns values)
- Builder handles validation and business logic
- Object creation fails gracefully with clear errors

### Complete Implementation

```python
from dataclasses import dataclass

@dataclass
class Database:
    host: str
    port: int
    username: str
    password: str
    
    def connect(self):
        print(f"Connecting to {self.host}:{self.port} as {self.username}")
    
    @staticmethod
    def builder():
        return Database.Builder()
    
    class Builder:
        def __init__(self):
            self._host = None
            self._port = None
            self._username = None
            self._password = None
        
        def set_host(self, host: str):
            self._host = host
            return self
        
        def set_port(self, port: int):
            self._port = port
            return self
        
        def set_username(self, username: str):
            self._username = username
            return self
        
        def set_password(self, password: str):
            self._password = password
            return self
        
        def build(self) -> Database:
            self._validate()
            return Database(
                host=self._host,
                port=self._port,
                username=self._username,
                password=self._password
            )
        
        def _validate(self):
            if not self._host:
                raise ValueError("Host is required")
            if not self._port:
                raise ValueError("Port is required")
            if not self._username:
                raise ValueError("Username is required")
            if not self._password:
                raise ValueError("Password is required")
            if self._port < 1024 or self._port > 65535:
                raise ValueError("Port must be between 1024 and 65535")
```

### Usage

```python
# Example 1: Valid database
db = Database.builder()
    .set_host("localhost")
    .set_port(3306)
    .set_username("admin")
    .set_password("secret123")
    .build()

db.connect()
# Output: Connecting to localhost:3306 as admin

# Example 2: Validation error
try:
    db = Database.builder()
        .set_host("localhost")
        .set_port(500)  # Invalid port!
        .set_username("admin")
        .set_password("secret")
        .build()
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Port must be between 1024 and 65535

# Example 3: Missing required field
try:
    db = Database.builder()
        .set_host("localhost")
        .set_port(3306)
        # Forgot username and password!
        .build()
except ValueError as e:
    print(f"Error: {e}")
    # Output: Error: Username is required
```

---

## 🍕 Example: Pizza Builder

A more complex example with optional parameters and list accumulation.

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Pizza:
    size: str
    crust: str
    cheese: str
    toppings: List[str]
    
    def __str__(self):
        toppings_str = ", ".join(self.toppings) if self.toppings else "cheese only"
        return f"{self.size} pizza with {self.crust} crust, {self.cheese}, toppings: {toppings_str}"

class PizzaBuilder:
    def __init__(self):
        # Defaults for optional parameters
        self._size = "medium"
        self._crust = "regular"
        self._cheese = "mozzarella"
        self._toppings = []
    
    def set_size(self, size: str):
        if size not in ["small", "medium", "large"]:
            raise ValueError(f"Invalid size: {size}")
        self._size = size
        return self
    
    def set_crust(self, crust: str):
        self._crust = crust
        return self
    
    def set_cheese(self, cheese: str):
        self._cheese = cheese
        return self
    
    def add_topping(self, topping: str):
        """Add a topping (can be called multiple times)"""
        self._toppings.append(topping)
        return self
    
    def build(self) -> Pizza:
        return Pizza(
            size=self._size,
            crust=self._crust,
            cheese=self._cheese,
            toppings=self._toppings
        )

# Usage examples
margherita = PizzaBuilder()
    .set_size("large")
    .set_crust("thin")
    .build()

print(margherita)
# Output: large pizza with thin crust, mozzarella, toppings: cheese only

meat_lovers = PizzaBuilder()
    .set_size("large")
    .add_topping("pepperoni")
    .add_topping("sausage")
    .add_topping("bacon")
    .build()

print(meat_lovers)
# Output: large pizza with regular crust, mozzarella, toppings: pepperoni, sausage, bacon
```

---

## 🎨 Pattern Variations

### Option 1: Builder as Inner Class (Recommended)

```python
class Database:
    # Product class
    
    @staticmethod
    def builder():
        return Database.Builder()
    
    class Builder:
        # Builder logic
        pass

# Usage
db = Database.builder().set_host("localhost").build()
```

**Pros:** Encapsulation, clear relationship, clean API

### Option 2: Separate Builder Class

```python
class Database:
    # Just the product
    pass

class DatabaseBuilder:
    # Builder in separate class
    def build(self) -> Database:
        return Database(...)

# Usage
db = DatabaseBuilder().set_host("localhost").build()
```

**Pros:** Separation of concerns, easier testing  
**Cons:** Less encapsulation, relationship not as clear

### Option 3: Director Pattern (for Presets)

```python
class DatabaseDirector:
    """Provides preset configurations"""
    
    @staticmethod
    def create_local():
        return Database.builder()
            .set_host("localhost")
            .set_port(3306)
            .set_username("root")
            .set_password("password")
            .build()
    
    @staticmethod
    def create_production(host: str):
        return Database.builder()
            .set_host(host)
            .set_port(5432)
            .set_username("prod_user")
            .set_password("secure_password")
            .build()

# Usage
local_db = DatabaseDirector.create_local()
prod_db = DatabaseDirector.create_production("prod.example.com")
```

**When to use:** Common configurations need names and presets

---

## ⚡ Key Concepts

### 1. Separation of Concerns

```python
# ✅ Product: Simple, just holds data
class Database:
    def __init__(self, host, port, username, password):
        self.host = host  # No validation here!
        self.port = port
        self.username = username
        self.password = password

# ✅ Builder: Handles construction logic
class Builder:
    def build(self):
        self._validate()  # Validation here!
        return Database(...)
```

### 2. Immutability

```python
# Product is immutable after creation
@dataclass(frozen=True)  # Can't modify after creation
class Database:
    host: str
    port: int
    username: str
    password: str

# Builder is mutable during construction
class Builder:
    def __init__(self):
        self._host = None  # Can modify
        # ...
    
    def host(self, host):
        self._host = host  # Mutable during building
        return self
```

### 3. Method Chaining (Fluent Interface)

```python
# Each method returns self
def set_host(self, host):
    self._host = host
    return self  # Enables chaining

# Allows fluent API
db = Database.builder()
    .set_host("localhost")     # Returns builder
    .set_port(3306)            # Returns builder
    .set_username("admin")     # Returns builder
    .set_password("secret")    # Returns builder
    .build()                   # Returns Database
```

---

## 💼 Real-World Use Cases

### 1. HTTP Request Builder

```python
class HttpRequest:
    def __init__(self, url, method, headers, body, timeout):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.timeout = timeout

class HttpRequestBuilder:
    def __init__(self):
        self._url = None
        self._method = "GET"
        self._headers = {}
        self._body = None
        self._timeout = 30
    
    def set_url(self, url):
        self._url = url
        return self
    
    def set_method(self, method):
        self._method = method
        return self
    
    def add_header(self, key, value):
        self._headers[key] = value
        return self
    
    def set_body(self, body):
        self._body = body
        return self
    
    def build(self):
        if not self._url:
            raise ValueError("URL is required")
        return HttpRequest(
            self._url, self._method, self._headers,
            self._body, self._timeout
        )

# Usage
request = HttpRequestBuilder()
    .set_url("https://api.example.com/users")
    .set_method("POST")
    .add_header("Content-Type", "application/json")
    .set_body({"name": "Alice"})
    .build()
```

### 2. Email Builder

```python
class Email:
    def __init__(self, to, subject, body, cc=None, attachments=None):
        self.to = to
        self.subject = subject
        self.body = body
        self.cc = cc or []
        self.attachments = attachments or []

class EmailBuilder:
    def __init__(self):
        self._to = []
        self._subject = ""
        self._body = ""
        self._cc = []
        self._attachments = []
    
    def add_to(self, *recipients):
        self._to.extend(recipients)
        return self
    
    def set_subject(self, subject):
        self._subject = subject
        return self
    
    def set_body(self, body):
        self._body = body
        return self
    
    def add_cc(self, *recipients):
        self._cc.extend(recipients)
        return self
    
    def add_attachment(self, filename):
        self._attachments.append(filename)
        return self
    
    def build(self):
        if not self._to:
            raise ValueError("At least one recipient required")
        return Email(self._to, self._subject, self._body,
                    self._cc, self._attachments)

# Usage
email = EmailBuilder()
    .add_to("alice@example.com", "bob@example.com")
    .set_subject("Meeting Reminder")
    .set_body("Don't forget about tomorrow's meeting")
    .add_cc("manager@example.com")
    .add_attachment("agenda.pdf")
    .build()
```

### 3. SQL Query Builder

```python
class Query:
    def __init__(self, select, from_table, where, order_by, limit):
        self.select = select
        self.from_table = from_table
        self.where = where
        self.order_by = order_by
        self.limit = limit
    
    def to_sql(self):
        sql = f"SELECT {self.select} FROM {self.from_table}"
        if self.where:
            sql += f" WHERE {self.where}"
        if self.order_by:
            sql += f" ORDER BY {self.order_by}"
        if self.limit:
            sql += f" LIMIT {self.limit}"
        return sql

class QueryBuilder:
    def __init__(self):
        self._select = "*"
        self._from_table = None
        self._where = None
        self._order_by = None
        self._limit = None
    
    def select(self, *columns):
        self._select = ", ".join(columns)
        return self
    
    def from_table(self, table):
        self._from_table = table
        return self
    
    def where(self, condition):
        self._where = condition
        return self
    
    def order_by(self, column):
        self._order_by = column
        return self
    
    def set_limit(self, count):
        self._limit = count
        return self
    
    def build(self):
        if not self._from_table:
            raise ValueError("Table is required")
        return Query(self._select, self._from_table,
                    self._where, self._order_by, self._limit)

# Usage
query = QueryBuilder()
    .select("name", "email", "age")
    .from_table("users")
    .where("age >= 18")
    .order_by("name")
    .set_limit(10)
    .build()

print(query.to_sql())
# Output: SELECT name, email, age FROM users WHERE age >= 18 ORDER BY name LIMIT 10
```

---

## ⚠️ Common Mistakes

### Mistake 1: Forgetting `return self`

```python
# ❌ Wrong
class Builder:
    def set_name(self, name):
        self._name = name
        # Forgot return self!

builder.set_name("Alice").set_age(25)  # 💥 Error!

# ✅ Correct
class Builder:
    def set_name(self, name):
        self._name = name
        return self  # ✅
```

### Mistake 2: No Validation in `build()`

```python
# ❌ Wrong - no validation
def build(self):
    return Database(self._host, self._port, ...)  # Could be invalid!

# ✅ Correct - validate before creating
def build(self):
    if not self._host:
        raise ValueError("Host is required")
    return Database(self._host, self._port, ...)
```

### Mistake 3: Reusing Builder Instances

```python
# ❌ Wrong - reusing builder
builder = Database.builder()

db1 = builder.set_host("host1").build()
db2 = builder.set_host("host2").build()  # db1 might be affected!

# ✅ Correct - new builder for each object
db1 = Database.builder().set_host("host1").build()
db2 = Database.builder().set_host("host2").build()
```

### Mistake 4: Business Logic in Product Constructor

```python
# ❌ Wrong - validation in constructor
class Database:
    def __init__(self, host, port):
        if not is_host_reachable(host):  # Network call!
            raise Exception("Host not reachable")
        self.host = host
        self.port = port

# ✅ Correct - validation in builder
class Builder:
    def build(self):
        if not self._is_host_reachable(self._host):
            raise Exception("Host not reachable")
        return Database(self._host, self._port)  # Simple constructor
```

---

## ✅ Best Practices

### 1. Keep Product Constructor Simple

```python
# ✅ Simple - just assigns values
class Database:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
```

### 2. Validate in `build()` Method

```python
def build(self):
    # All validation here
    self._validate()
    return Database(...)

def _validate(self):
    if not self._host:
        raise ValueError("Host is required")
    # ... more validation
```

### 3. Provide Sensible Defaults

```python
def __init__(self):
    self._timeout = 30        # Default timeout
    self._retry_count = 3     # Default retries
    self._method = "GET"      # Default HTTP method
    # User only overrides what they need
```

### 4. Use Descriptive Method Names

```python
# ✅ Clear and descriptive
.add_topping("pepperoni")
.remove_topping("olives")
.set_timeout(60)

# ❌ Generic and unclear
.set("topping", "pepperoni")
.configure("timeout", 60)
```

### 5. Make Required vs Optional Clear

```python
def build(self):
    # Clearly validate required fields
    if not self._url:
        raise ValueError("URL is required")
    
    # Optional fields have defaults in __init__
    return HttpRequest(
        url=self._url,           # Required
        method=self._method,     # Optional (has default)
        timeout=self._timeout    # Optional (has default)
    )
```

---

## 🎯 When to Use Builder Pattern

### ✅ Use Builder When:

1. **Many parameters** (especially optional ones)
   ```python
   # 10+ parameters? Use builder!
   Database(host, port, user, pass, ssl, timeout, pool_size, ...)
   ```

2. **Complex validation** needed
   ```python
   # Need to validate combinations or make network calls
   if ssl and port != 443:
       raise ValueError("SSL requires port 443")
   ```

3. **Want immutable objects** with flexible construction
   ```python
   @dataclass(frozen=True)  # Immutable product
   class Config:
       # Builder allows flexible construction
       pass
   ```

4. **Step-by-step construction** makes sense
   ```python
   # Build incrementally
   query = QueryBuilder()
       .select("*")
       .from_table("users")
       .where("age > 18")
       .build()
   ```

### ❌ Don't Use Builder When:

1. **Simple objects** (few parameters, all required)
   ```python
   # Just use constructor
   class Point:
       def __init__(self, x, y):
           self.x = x
           self.y = y
   ```

2. **Object created frequently** (performance matters)
   ```python
   # Builder has overhead - use simple constructor
   for i in range(1_000_000):
       point = Point(i, i)  # Fast
   ```

3. **All parameters required** with no validation
   ```python
   # Constructor is fine
   class User:
       def __init__(self, id, name, email):  # All required
           self.id = id
           self.name = name
           self.email = email
   ```

---

## 📝 Summary

### The Pattern in 4 Steps:

1. **Create Product** - Simple class with simple constructor
2. **Create Builder** - Inner class with mutable state
3. **Add Setters** - Methods that return `self` for chaining
4. **Add `build()`** - Validates and creates the product

### Key Benefits:

✅ **Readable** - Clear what each parameter does  
✅ **Flexible** - Only set what you need  
✅ **Safe** - Validation before object creation  
✅ **Maintainable** - Easy to add new parameters  
✅ **Testable** - Separate construction from business logic

### Remember:

- Product constructor: **simple** (just assigns values)
- Builder: **complex** (handles validation and logic)
- Method chaining: **return self**
- Validation: **in build() method**

---

## 🔗 Reading List

- [Telescoping Constructor Anti-pattern](https://www.vojtechruzicka.com/avoid-telescoping-constructor-pattern/)
- [Why Objects Should Be Immutable](https://octoperf.com/blog/2016/04/07/why-objects-must-be-immutable)
- [Builder Pattern - Python Patterns](https://python-patterns.guide/gang-of-four/builder/)
- [Gang of Four - Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns)