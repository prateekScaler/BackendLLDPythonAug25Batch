# Iterators in Python

## 🎯 What is an Iterator?

**An object that lets you traverse through a collection one item at a time**

```python
# Lists are iterable
numbers = [1, 2, 3]

# Get iterator from iterable
iterator = iter(numbers)

# Get items one by one
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
print(next(iterator))  # StopIteration exception
```

**Key:** Iterator = object with `__iter__()` and `__next__()` methods

---

## 🔍 Iterable vs Iterator

### Iterable → Iterator Flow

**Iterable**
- When you call `iter()` on an iterable, you get an **Iterator**.

**Iterator**
- The iterator produces items one by one using `next()`:
  1. `next()` → **Item 1**
  2. `next()` → **Item 2**
  3. `next()` → **Item 3**
  4. `next()` → **StopIteration** (signals the end)

---

| Object     | Action | Result         |
|-------------|---------|----------------|
| Iterable    | `iter()` | Iterator       |
| Iterator    | `next()` | Item 1         |
| Iterator    | `next()` | Item 2         |
| Iterator    | `next()` | Item 3         |
| Iterator    | `next()` | StopIteration  |


**Iterable:** Can be looped over (list, string, dict)

**Iterator:** Does the actual looping

## Common Iterable Types

| Category | Examples |
|-----------|-----------|
| **Sequences** | `list`, `tuple`, `str`, `range`, `bytes`, `bytearray` |
| **Collections** | `dict` (keys, values, items), `set`, `frozenset` |
| **Generators** | Generator functions (`yield`), generator expressions |
| **File Objects** | Objects returned by `open()` (iterate over lines) |
| **Iterator-returning built-ins** | `zip()`, `map()`, `filter()`, `enumerate()`, `re.finditer()`, `os.scandir()`, `pathlib.Path.glob()` |
| **Custom Classes** | Any class implementing `__iter__()` or `__getitem__()` |

## Quick Check
```python
from collections.abc import Iterable
isinstance(obj, Iterable)

```python
# Iterable - can be iterated multiple times
numbers = [1, 2, 3]
for n in numbers:
    print(n)
for n in numbers:  # Works again
    print(n)

# Iterator - consumed after one use
iterator = iter(numbers)
for n in iterator:
    print(n)
for n in iterator:  # Empty! Already consumed
    print(n)
```

---

## 🛠️ How Iterators Work

### Behind the Scenes of for Loop

```python
# What you write
for item in [1, 2, 3]:
    print(item)

# What Python does
iterator = iter([1, 2, 3])
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```

---

## 🎨 Creating Custom Iterator

## Implementing Dunder Methods

```python
class Counter:
    def __init__(self, max_count):
        self.max_count = max_count
        self.current = 0
    
    def __iter__(self):
        return self  # Iterator returns itself
    
    def __next__(self):
        if self.current >= self.max_count:
            raise StopIteration
        
        self.current += 1
        return self.current

# Usage
counter = Counter(3)
for num in counter:
    print(num)  # 1, 2, 3
```

### Practical Example: Range-like Iterator

```python
class MyRange:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        
        value = self.current
        self.current += 1
        return value

# Usage
for i in MyRange(1, 5):
    print(i)  # 1, 2, 3, 4
```

---

## 💡 Why Use Iterators?

### 1. Memory Efficiency
```python
# List - stores all items in memory
numbers = [x**2 for x in range(1000000)]  # ~8MB

## Above expression is just a syntax sugar for:
numbers = []
for x in range(1000000):
    numbers.append(x**2)

# Iterator - computes on demand
numbers = (x**2 for x in range(1000000))  # ~200 bytes

## Above expression is just a syntax sugar for:
def generate_squares():
    for x in range(1000000):
        yield x**2
```

### 2. Lazy Evaluation
```python
# Eager - computes all immediately
def process_eager():
    results = []
    for i in range(1000000):
        results.append(expensive_operation(i))
    return results[:10]  # Only need 10, computed 1M!

# Lazy - computes only what's needed
def process_lazy():
    iterator = (expensive_operation(i) for i in range(1000000))
    return list(itertools.islice(iterator, 10))  # Computed 10
```

### 3. Infinite Sequences
```python
from itertools import count

# Impossible with list
# numbers = [x for x in count()]  # Never finishes!

# Works with iterator
infinite = count(0)
for i, num in enumerate(infinite):
    print(num)
    if i >= 5:
        break  # 0, 1, 2, 3, 4, 5
```

---

## 🔑 Built-in Iterator Tools

```python
from itertools import *

# count - infinite counting
for i in islice(count(10), 3):
    print(i)  # 10, 11, 12

# cycle - repeat forever
colors = cycle(['red', 'green', 'blue'])
for i, color in enumerate(colors):
    print(color)
    if i >= 5:
        break  # red, green, blue, red, green, blue

# repeat - repeat item
for item in islice(repeat('A'), 3):
    print(item)  # A, A, A

# chain - combine iterators
for item in chain([1, 2], [3, 4]):
    print(item)  # 1, 2, 3, 4
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Iterator exhaustion
```python
iterator = iter([1, 2, 3])
print(list(iterator))  # [1, 2, 3]
print(list(iterator))  # [] - exhausted!
```

### Pitfall 2: Modifying during iteration
```python
# BAD - modifying while iterating
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Skips elements!

# GOOD - iterate over copy
for num in list(numbers):
    if num % 2 == 0:
        numbers.remove(num)
```

---

## ✅ Key Takeaways

1. **Iterator** = object that implements `__iter__()` and `__next__()`
2. **Iterable** = object that returns iterator via `iter()`
3. **Memory efficient** - doesn't store all items
4. **Lazy evaluation** - computes on demand
5. **One-time use** - exhausted after iteration
6. **for loops** use iterators behind the scenes

---

## 🎓 Quick Reference

```python
# Get iterator
iterator = iter([1, 2, 3])

# Get next item
item = next(iterator)

# Check if iterable
from collections.abc import Iterable
isinstance([1, 2, 3], Iterable)  # True

# Check if iterator
from collections.abc import Iterator
isinstance(iter([1, 2, 3]), Iterator)  # True
```