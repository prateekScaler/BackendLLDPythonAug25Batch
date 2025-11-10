# Generators in Python

## 🎯 What is a Generator?

**A simple way to create iterators using `yield` keyword**

```python
# Regular function - returns once
def regular():
    return 1

# Generator function - yields multiple times
def generator():
    yield 1
    yield 2
    yield 3

# Usage
gen = generator()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

**Key:** Generator = easy iterator creation with `yield`

---

### 🧠 Context: Generators vs Functional Tools (`map`, `filter`, `reduce`)

Python gives you multiple ways to process data lazily.  
Functions like `map()`, `filter()`, and `reduce()` (from `functools`) are perfect when your logic is short and can be expressed in a **single functional expression** — often with a `lambda`. They are already **lazy iterators**, so they don’t build lists in memory.

However, when your logic becomes more complex — involving multiple conditions, branching, error handling, or multi-step transformations — **generators** are the better choice. They maintain the same laziness but give you the full control of normal Python syntax (`if`, `for`, `try/except`, etc.).

---

### Example: Simple Transformation → Use `map` / `filter`

```python
from functools import reduce

# Square even numbers and find their sum
numbers = range(10)
result = reduce(
    lambda acc, x: acc + x,
    map(lambda x: x**2, filter(lambda n: n % 2 == 0, numbers)),
    0
)
print(result)  # 120
```

### Example: Complex Logic → Use a Generator
```python
def process_numbers(nums):
    """Filter, transform, and handle errors lazily."""
    for n in nums:
        try:
            if n % 2 == 0:
                yield n**2
            elif n < 0:
                raise ValueError("Negative value encountered")
        except ValueError as e:
            print(f"Skipping: {e}")

# Usage
for val in process_numbers(range(-2, 5)):
    print(val)
```

---

## 🔍 Function vs Generator

```python
# Regular function - returns list
def get_numbers():
    return [1, 2, 3]

result = get_numbers()
print(result)  # [1, 2, 3] - all at once

# Generator - yields one at a time
def get_numbers_gen():
    yield 1
    yield 2
    yield 3

gen = get_numbers_gen()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
```

---

## 💡 Why Use Generators?

### 1. Memory Efficient

```python
# List - all in memory
def squares_list(n):
    return [x**2 for x in range(n)]

numbers = squares_list(1000000)  # ~8MB in memory

# Syntactical sugar would have been:
squares_list = [x**2 for x in range(5)]


# Generator - one at a time
def squares_gen(n):
    for x in range(n):
        yield x**2

numbers = squares_gen(1000000)  # ~200 bytes

# Syntactical sugar would have been:
squares_gen = (x**2 for x in range(5))
```

### 2. Lazy Computation

```python
# Computes all first 1M, then takes 10
def first_10_eager():
    numbers = [x**2 for x in range(1000000)]
    return numbers[:10]

# Computes only 10
def first_10_lazy():
    def gen():
        for x in range(1000000):
            yield x**2
    
    result = []
    for i, num in enumerate(gen()):
        result.append(num)
        if len(result) >= 10:
            break
    return result
```

### 3. Infinite Sequences

```python
def infinite_count():
    num = 0
    while True:
        yield num
        num += 1

# Can work with infinite generator
counter = infinite_count()
print(next(counter))  # 0
print(next(counter))  # 1
print(next(counter))  # 2
```

---

## 🎨 Creating Generators

### Method 1: Generator Function

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

### Method 2: Generator Expression

```python
# List comprehension - eager
squares_list = [x**2 for x in range(5)]

# Generator expression - lazy
squares_gen = (x**2 for x in range(5))

print(list(squares_gen))  # [0, 1, 4, 9, 16]
```

---

## 🛠️ Practical Examples

### Example 1: File Reading

```python
# BAD - loads entire file
def read_file_bad(filename):
    with open(filename) as f:
        return f.readlines()  # All lines in memory

# GOOD - reads line by line
def read_file_good(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Usage - only processes needed lines
for i, line in enumerate(read_file_good("large_file.txt")):
    print(line)
    if i >= 10:
        break  # Only read 10 lines
```

### Example 2: Fibonacci

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci()
for _ in range(10):
    print(next(fib))
```

### Example 3: Data Pipeline

```python
def read_data():
    """Read from source"""
    for i in range(100):
        yield {"id": i, "value": i * 2}

def filter_data(data):
    """Filter valid items"""
    for item in data:
        if item["value"] > 50:
            yield item

def transform_data(data):
    """Transform items"""
    for item in data:
        yield {"id": item["id"], "result": item["value"] * 2}

# Pipeline - memory efficient
pipeline = transform_data(filter_data(read_data()))
for item in pipeline:
    print(item)
```

### Example 4: Batch Processing

```python
def batch_items(items, batch_size):
    """Yield items in batches"""
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    
    # Yield remaining items
    if batch:
        yield batch

# Usage
data = range(25)
for batch in batch_items(data, 10):
    print(batch)  # [0-9], [10-19], [20-24]
```

---

## 🔄 Generator Methods

### send() - Send value to generator

```python
def echo():
    while True:
        value = yield
        print(f"Received: {value}")

gen = echo()
next(gen)  # Prime the generator
gen.send("Hello")  # Received: Hello
gen.send("World")  # Received: World
```

### close() - Stop generator

```python
def counter():
    n = 0
    while True:
        yield n
        n += 1

gen = counter()
print(next(gen))  # 0
print(next(gen))  # 1
gen.close()
# print(next(gen))  # StopIteration
```

### throw() - Throw exception

```python
def error_handler():
    try:
        while True:
            value = yield
            print(f"Processing: {value}")
    except ValueError:
        print("ValueError caught!")

gen = error_handler()
next(gen)
gen.send(10)
gen.throw(ValueError)
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Exhausted generator

```python
gen = (x**2 for x in range(3))
print(list(gen))  # [0, 1, 4]
print(list(gen))  # [] - exhausted!

# Must create new generator
gen = (x**2 for x in range(3))
print(list(gen))  # [0, 1, 4]
```

### Pitfall 2: Early termination

```python
def cleanup_gen():
    try:
        yield 1
        yield 2
        yield 3
    finally:
        print("Cleanup!")

gen = cleanup_gen()
print(next(gen))  # 1
# Breaks early - finally still runs
```

---

## 🔗 Generator vs List Comprehension

```python
# List comprehension - eager, all in memory
list_comp = [x**2 for x in range(1000)]
print(type(list_comp))  # <class 'list'>

# Generator expression - lazy, on demand
gen_exp = (x**2 for x in range(1000))
print(type(gen_exp))  # <class 'generator'>
```

**Use list when:**
- Need to iterate multiple times
- Small dataset
- Need list operations (indexing, slicing)

**Use generator when:**
- Large dataset
- Single pass iteration
- Memory constrained
- Pipeline processing

---

## ✅ Key Takeaways

1. **Generators** are functions that use `yield`
2. **Memory efficient** - produces items on demand
3. **Lazy evaluation** - computes only when needed
4. **One-time use** - exhausted after iteration
5. **Simpler than iterators** - no need for `__iter__` and `__next__`
6. **Great for pipelines** - chain transformations
7. **Can be infinite** - yield forever

---

## 🎓 Quick Reference

```python
# Generator function
def gen():
    yield 1
    yield 2

# Generator expression
gen = (x for x in range(10))

# Get next value
next(gen)

# Convert to list
list(gen)

# Use in for loop
for item in gen:
    print(item)
```

---

## 📊 Comparison Summary

| Feature | List | Iterator | Generator |
|---------|------|----------|-----------|
| **Memory** | All items | Minimal | Minimal |
| **Reusable** | Yes | No | No |
| **Create** | `[]` | Class | `yield` |
| **When** | Small data | Manual control | Large/infinite data |