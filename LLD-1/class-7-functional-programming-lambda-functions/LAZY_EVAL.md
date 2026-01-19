## ⚡ Lazy Evaluation

### What is Lazy Evaluation?

**Computing values only when needed, not immediately**

```python
# List comprehension - EAGER (creates list immediately)
result = [x**2 for x in range(1000000)]  # Creates 1M element list NOW
# Memory: ~8MB allocated immediately

# map/filter - LAZY (creates iterator, computes on demand)
result = map(lambda x: x**2, range(1000000))  # Just an iterator
# Memory: ~60 bytes (just the iterator object)
```

### How It Works

```python
numbers = [1, 2, 3, 4, 5]

# Eager: Executes immediately
eager = [x**2 for x in numbers]  
print(eager)  # [1, 4, 9, 16, 25] - Already computed!

# Lazy: Defers execution
lazy = map(lambda x: x**2, numbers)
print(lazy)   #  - Nothing computed yet!

# Compute only when needed
print(list(lazy))  # [1, 4, 9, 16, 25] - Computed NOW
```

### Benefits of Lazy Evaluation

**1. Memory Efficiency**
```python
# Eager - Uses lots of memory
def process_eager():
    data = [x**2 for x in range(10_000_000)]  # ~80MB in memory
    first_five = data[:5]
    return first_five

# Lazy - Uses minimal memory
def process_lazy():
    data = map(lambda x: x**2, range(10_000_000))  # ~60 bytes
    first_five = list(itertools.islice(data, 5))
    return first_five

# Both return [0, 1, 4, 9, 16]
# But lazy version doesn't compute all 10M values!
```

**2. Performance - Short-Circuiting**
```python
import time

def slow_square(x):
    time.sleep(0.1)  # Simulate expensive operation
    return x ** 2

numbers = range(100)

# Eager - Processes ALL 100 (takes ~10 seconds)
eager = [slow_square(x) for x in numbers]
first_five = eager[:5]

# Lazy - Processes only FIRST 5 (takes ~0.5 seconds)
lazy = map(slow_square, numbers)
first_five = list(itertools.islice(lazy, 5))
```

**3. Infinite Sequences**
```python
# Eager - IMPOSSIBLE with infinite sequence
# Can't do: [x for x in count(0)]  # Never finishes!

# Lazy - Works fine!
from itertools import count, islice

infinite = map(lambda x: x**2, count(0))  # Infinite iterator
first_ten = list(islice(infinite, 10))    # [0,1,4,9,16,25,36,49,64,81]
```

**4. Composability Without Intermediate Lists**
```python
# Eager - Creates intermediate lists (memory waste)
numbers = range(1000000)
step1 = [x for x in numbers if x % 2 == 0]      # Intermediate list
step2 = [x**2 for x in step1]                    # Another intermediate list
step3 = [x for x in step2 if x > 1000]          # Final list
# Total: 3 full lists in memory!

# Lazy - No intermediate lists!
numbers = range(1000000)
step1 = filter(lambda x: x % 2 == 0, numbers)   # Just iterator
step2 = map(lambda x: x**2, step1)               # Chain iterator
step3 = filter(lambda x: x > 1000, step2)        # Chain iterator
result = list(step3)                             # Compute once, at the end
# Total: Only final result in memory!
```

### Practical Examples

**Example 1: Processing Large File**
```python
# Eager - Loads entire file into memory
def process_file_eager(filename):
    lines = [line.strip() for line in open(filename)]  # ALL lines in memory
    valid = [line for line in lines if len(line) > 0]
    upper = [line.upper() for line in valid]
    return upper[:10]  # Only need first 10!

# Lazy - Processes line by line
def process_file_lazy(filename):
    lines = (line.strip() for line in open(filename))  # Generator
    valid = filter(lambda x: len(x) > 0, lines)
    upper = map(str.upper, valid)
    return list(itertools.islice(upper, 10))  # Only processes first 10!
```

**Example 2: Finding First Match**
```python
# Eager - Checks ALL even if found early
def find_first_eager(numbers, target):
    results = [x for x in numbers if x > target]  # Processes ALL
    return results[0] if results else None

# Lazy - Stops at first match
def find_first_lazy(numbers, target):
    results = filter(lambda x: x > target, numbers)
    return next(results, None)  # Stops after first match!

# Example with large range
numbers = range(1_000_000)
find_first_eager(numbers, 10)   # Checks all 1M numbers
find_first_lazy(numbers, 10)    # Stops after 11th number!
```

**Example 3: Data Pipeline**
```python
import time

# Eager - All steps execute immediately
def pipeline_eager(data):
    print("Step 1: Filter")
    filtered = [x for x in data if x % 2 == 0]
    
    print("Step 2: Transform")
    transformed = [x**2 for x in filtered]
    
    print("Step 3: Filter again")
    result = [x for x in transformed if x > 100]
    
    return result[:5]

# Lazy - Nothing happens until list() is called
def pipeline_lazy(data):
    print("Building pipeline...")
    filtered = filter(lambda x: x % 2 == 0, data)
    transformed = map(lambda x: x**2, filtered)
    result = filter(lambda x: x > 100, transformed)
    
    print("Executing pipeline...")
    return list(itertools.islice(result, 5))

data = range(1000)
print("=== Eager ===")
pipeline_eager(data)

print("\n=== Lazy ===")
pipeline_lazy(data)
```

### Visualizing the Difference

```
EAGER (List Comprehension):
[1,2,3,4,5] → [square all] → [1,4,9,16,25] → [filter >5] → [9,16,25]
              └─ Create full list ─┘         └─ Create full list ─┘
              
LAZY (map/filter):
[1,2,3,4,5] → square → filter → [take 2] → [9,16]
              ↑        ↑         ↑
              Only computes what's needed!
              Stops after getting 2 results
```

### When to Use Lazy Evaluation

**✅ USE lazy (map/filter) when:**
- Working with large datasets
- Don't need all results
- Want to chain operations efficiently
- Processing infinite sequences
- Memory is constrained

**✅ USE eager (list comprehension) when:**
- Need to iterate multiple times
- Small datasets
- Want more readable code
- Need the full result immediately

### Practical Comparison

```python
from itertools import islice

# Scenario: Get first 5 squares of even numbers from large range
numbers = range(10_000_000)

# Eager - Computes 5 million squares!
result = [x**2 for x in numbers if x % 2 == 0][:5]
# Memory: ~40MB, Time: Several seconds

# Lazy - Computes only 5 squares!
result = list(islice(
    map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)),
    5
))
# Memory: ~60 bytes, Time: Microseconds
```

### Key Takeaways

1. **map/filter return iterators** (lazy, computed on demand)
2. **List comprehensions return lists** (eager, computed immediately)
3. **Lazy is memory efficient** (doesn't store intermediate results)
4. **Lazy enables short-circuiting** (stops when you have enough)
5. **Use list() to force evaluation** of lazy iterators
6. **Generator expressions** are lazy too: `(x**2 for x in numbers)`

```python
# Quick test to see if something is lazy:
result = map(lambda x: x**2, [1, 2, 3])
print(type(result))  #  - It's lazy!

result = [x**2 for x in [1, 2, 3]]
print(type(result))  #  - It's eager!
```

---