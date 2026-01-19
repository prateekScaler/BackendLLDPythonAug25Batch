# Context Managers in Python

## What is a Context Manager?

**Simple Definition:** Automatic setup and cleanup for resources

**The Problem:**
```python
file = open("data.txt")
# Do something
file.close()  # ← Might forget this!
```

**The Solution:**
```python
with open("data.txt") as file:
    # Do something
# File automatically closed!
```

---

## Basic Syntax

```python
with resource as variable:
    # Use resource
# Resource automatically cleaned up
```

**What happens:**
1. `__enter__()` called → Setup
2. Your code runs
3. `__exit__()` called → Cleanup (ALWAYS, even on error!)

---

## Common Use Cases

### 1. File Operations
```python
# BAD - Manual close
file = open("data.txt")
data = file.read()
file.close()

# GOOD - Automatic close
with open("data.txt") as file:
    data = file.read()
```

### 2. Locks (Threading)
```python
from threading import Lock

lock = Lock()

# BAD - Manual release
lock.acquire()
# Do work
lock.release()

# GOOD - Automatic release
with lock:
    # Do work
```

### 3. Database Connections
```python
# BAD
connection = database.connect()
cursor = connection.cursor()
cursor.execute("SELECT * FROM users")
connection.close()

# GOOD
with database.connect() as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
```

### 4. Network Connections
```python
import socket

# GOOD
with socket.socket() as sock:
    sock.connect(('localhost', 8080))
    sock.send(b'Hello')
```

---

## Why Context Managers?

### Guarantee Cleanup
```python
with open("file.txt") as f:
    data = f.read()
    raise Exception("Error!")  # File STILL closes!
```

### Equivalent Without Context Manager
```python
f = open("file.txt")
try:
    data = f.read()
    raise Exception("Error!")
finally:
    f.close()  # Must manually ensure this
```

**Context manager = Automatic try-finally!**

---

## Creating Your Own Context Manager

### Method 1: Class-Based
```python
class MyResource:
    def __enter__(self):
        print("Setting up resource")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cleaning up resource")
        return False  # Don't suppress exceptions
    
    def do_something(self):
        print("Using resource")

# Usage
with MyResource() as resource:
    resource.do_something()
```

**Output:**
```
Setting up resource
Using resource
Cleaning up resource
```

### Method 2: Using @contextmanager Decorator
```python
from contextlib import contextmanager

@contextmanager
def my_resource():
    print("Setup")
    yield "resource"
    print("Cleanup")

# Usage
with my_resource() as r:
    print(f"Using {r}")
```

---

## Real Example: Timer

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    print(f"{name} started")
    yield
    end = time.time()
    print(f"{name} took {end - start:.2f}s")

# Usage
with timer("Database query"):
    time.sleep(2)  # Simulate query
```

**Output:**
```
Database query started
Database query took 2.00s
```

---

## Multiple Context Managers

### Stack Them
```python
with open("input.txt") as infile:
    with open("output.txt", "w") as outfile:
        outfile.write(infile.read())
```

### Or Use Comma (Python 3.1+)
```python
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read())
```

---

## Context Managers in Other Languages

### Java - try-with-resources
```java
// Similar concept
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
} // Automatically closed
```

### Go - defer
```go
// Different syntax, same idea
file, _ := os.Open("file.txt")
defer file.Close()  // Runs when function exits

// Use file
data, _ := ioutil.ReadAll(file)
```

### C# - using statement
```csharp
// Very similar to Python
using (StreamReader reader = new StreamReader("file.txt"))
{
    string content = reader.ReadToEnd();
} // Automatically disposed
```

### Rust - Drop trait
```rust
// Automatic cleanup when scope ends
{
    let file = File::open("file.txt")?;
    // Use file
} // file automatically closed here
```

---

## Common Python Context Managers

### Built-in
```python
# Files
with open("file.txt") as f:
    pass

# Locks
from threading import Lock
with Lock() as lock:
    pass

# Decimal context
from decimal import localcontext
with localcontext() as ctx:
    ctx.prec = 10
```

### From Libraries
```python
# Suppress exceptions
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove("file.txt")

# Change directory temporarily
import os
with os.scandir('/tmp') as entries:
    for entry in entries:
        print(entry.name)
```

---

## When to Create Your Own

**Create context manager when:**
- Need paired setup/cleanup operations
- Want to ensure cleanup always happens
- Managing a resource (connection, file, lock)
- Temporarily changing state

**Examples:**
- Database transactions
- Temporary directory creation
- Changing working directory
- Setting up test fixtures
- Timing code execution

---

## Advanced: Exception Handling

```python
class MyResource:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("No error")
        else:
            print(f"Error: {exc_val}")
        return False  # Don't suppress exception

with MyResource():
    raise ValueError("Oops!")
```

**Return values from `__exit__`:**
- `True` → Suppress exception
- `False` or `None` → Propagate exception

---

## Quick Reference

### Using Context Manager
```python
with resource as var:
    # use var
```

### Creating (Simple)
```python
from contextlib import contextmanager

@contextmanager
def my_context():
    # Setup
    yield value
    # Cleanup
```

### Creating (Class)
```python
class MyContext:
    def __enter__(self):
        # Setup
        return value
    
    def __exit__(self, *args):
        # Cleanup
        pass
```

---

## Common Patterns

### 1. Temporary State Change
```python
@contextmanager
def temporary_setting(value):
    old_value = get_setting()
    set_setting(value)
    yield
    set_setting(old_value)
```

### 2. Resource Acquisition
```python
@contextmanager
def database_connection():
    conn = acquire_connection()
    try:
        yield conn
    finally:
        conn.close()
```

### 3. Lock Pattern (Threading)
```python
@contextmanager
def lock_context(lock):
    lock.acquire()
    try:
        yield
    finally:
        lock.release()
```

---

## Remember

✓ Context managers = Automatic cleanup  
✓ Use `with` statement  
✓ Always prefer over manual try-finally  
✓ Create your own when managing resources  
✓ `__enter__` = setup, `__exit__` = cleanup  

---

## Summary

**Python:**
```python
with resource as r:
    use(r)
```

**Java:**
```java
try (Resource r = new Resource()) {
    use(r);
}
```

**Go:**
```go
defer cleanup()
use()
```

**C#:**
```csharp
using (var r = new Resource()) {
    use(r);
}
```

**All solve the same problem: Guaranteed cleanup!**