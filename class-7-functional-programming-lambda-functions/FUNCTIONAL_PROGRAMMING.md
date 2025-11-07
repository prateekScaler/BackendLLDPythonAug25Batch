# Functional Programming in Python

## 🎯 What is Functional Programming?

**Programming paradigm that treats computation as evaluation of mathematical functions**

```python
# Imperative/OOP style
total = 0
for num in [1, 2, 3, 4]:
    total += num
print(total)  # 10

# Functional style
from functools import reduce
total = reduce(lambda x, y: x + y, [1, 2, 3, 4])
print(total)  # 10
```

**Key Idea:** Functions are first-class citizens (can be passed around like data)

---

## 📊 OOP vs Functional Programming

```
Programming Paradigms
│
├── Object-Oriented (OOP)
│   ├── Objects + Methods
│   ├── Mutable State
│   └── Inheritance
│
└── Functional
    ├── Pure Functions
    ├── Immutable Data
    └── Function Composition
```

### Comparison Table

| Aspect | OOP | Functional |
|--------|-----|------------|
| **Building Block** | Objects & Classes | Functions |
| **State** | Mutable | Immutable |
| **Data + Behavior** | Encapsulated together | Separated |
| **Change** | Modify objects | Create new data |
| **Side Effects** | Common | Avoided |
| **Main Focus** | "What it is" | "What it does" |

### Example: Same Problem, Different Paradigms

**OOP Style:**
```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance  # Mutable state
    
    def deposit(self, amount):
        self.balance += amount  # Modifies state
        return self.balance

account = BankAccount(100)
account.deposit(50)  # Changes account
print(account.balance)  # 150
```

**Functional Style:**
```python
# Immutable, returns new value
def deposit(balance, amount):
    return balance + amount  # No mutation

balance = 100
new_balance = deposit(balance, 50)  # Creates new value
print(balance)      # 100 (unchanged)
print(new_balance)  # 150 (new value)
```

---

## 🏗️ Why Functional Programming Evolved?

### Historical Context

1. **1950s:** LISP invented (first FP language)
2. **Problem:** Managing complex state in large programs
3. **Insight:** Pure functions = easier to reason about
4. **Modern:** Concurrency/parallelism needs immutability

### Key Problems FP Solves

**Problem 1: Unpredictable State**
```python
# OOP - Hard to track
class Counter:
    count = 0  # Shared state
    def increment(self):
        self.count += 1  # Who changed it?

# FP - Predictable
def increment(count):
    return count + 1  # Clear input/output
```

**Problem 2: Side Effects**
```python
# OOP - Hidden side effects
def process(data):
    data.append(99)  # Modifies input!
    save_to_db(data)  # External side effect
    return data

# FP - Explicit
def process(data):
    new_data = data + [99]  # New data
    return new_data  # No side effects
```

**Problem 3: Testing Difficulty**
```python
# OOP - Needs setup
account = BankAccount(100)
account.deposit(50)
assert account.balance == 150

# FP - Simple
assert deposit(100, 50) == 150  # Just call function
```

---

## 🔑 Core Concepts

### 1. First-Class Functions

**Functions are values - can be assigned, passed, returned**

```python
# Assign function to variable
def greet(name):
    return f"Hello, {name}"

say_hello = greet  # Function as value
print(say_hello("Alice"))  # "Hello, Alice"

# Store functions in a dictionary
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

operations = {
    'add': add,
    'multiply': multiply
}

print(operations['add'](5, 3))  # 8
```

### 2. Higher-Order Functions

**Functions that take or return other functions**

```python
# Function takes function as parameter
def apply_twice(func, value):
    return func(func(value))

def double(x):
    return x * 2

result = apply_twice(double, 5)  # double(double(5))
print(result)  # 20

# Function returns function
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

times_three = make_multiplier(3)
print(times_three(10))  # 30
```

### 3. Pure Functions

**Same input → Same output, No side effects**

```python
# ✅ PURE - Predictable
def add(a, b):
    return a + b

print(add(2, 3))  # Always 5

# ❌ IMPURE - Unpredictable
total = 0
def add_to_total(x):
    global total
    total += x  # Side effect!
    return total

print(add_to_total(5))  # 5
print(add_to_total(5))  # 10 (different result!)
```

**Pure vs Impure Examples:**

| Pure ✅ | Impure ❌ |
|---------|-----------|
| `len([1,2,3])` | `print("hello")` |
| `sum([1,2,3])` | `list.append(4)` |
| `"hi".upper()` | `random.randint()` |
| `max(1, 2, 3)` | `file.write()` |

---

## 🔥 Lambda Functions

### What Are Lambdas?

**Anonymous functions - function without a name**

```python
# Regular function
def square(x):
    return x ** 2

# Lambda (anonymous)
square = lambda x: x ** 2

# Both work the same
print(square(5))  # 25
```

### Syntax: How to Remember

```
lambda arguments: expression
   ↑      ↑          ↑
 keyword  input    output (single expression)
```

**Pattern:**
```python
lambda x: x * 2           # One argument
lambda x, y: x + y        # Two arguments
lambda x, y, z: x+y+z     # Three arguments
lambda: 42                # No arguments
```

### When to Use Lambdas

**✅ USE when:**
- Short, simple operations
- One-time use (throwaway function)
- As argument to higher-order functions

```python
# Good use cases
numbers = [1, 2, 3, 4]
squared = map(lambda x: x**2, numbers)
even = filter(lambda x: x % 2 == 0, numbers)
sorted_words = sorted(words, key=lambda w: len(w))
```

**❌ DON'T USE when:**
- Complex logic (use def)
- Need multiple statements
- Reused multiple times
- Need docstring/name for clarity

```python
# ❌ BAD - Too complex
result = lambda x: x if x > 0 else -x if x < 0 else 0

# ✅ GOOD - Use def
def absolute_value(x):
    """Return absolute value of x"""
    if x > 0:
        return x
    elif x < 0:
        return -x
    else:
        return 0
```

### Lambda Limitations

```python
# ❌ Can't have statements
lambda x: print(x)  # SyntaxError

# ❌ Can't have multiple expressions
lambda x: x += 1    # SyntaxError

# ❌ Can't have assignments
lambda x: y = x + 1 # SyntaxError

# ✅ Only single expression
lambda x: x + 1     # OK
```

---

## 🛠️ Built-in Functional Tools

### map() - Transform Each Element

**Syntax:** `map(function, iterable)`

```python
# Without map (imperative)
numbers = [1, 2, 3, 4]
squared = []
for num in numbers:
    squared.append(num ** 2)

# With map (functional)
squared = map(lambda x: x ** 2, numbers)
print(list(squared))  # [1, 4, 9, 16]
```

**How to Remember:**
```
map(function, list) → applies function to EACH element
    ↓         ↓
  "what to do" + "to what"
```

**Common Patterns:**
```python
# Convert types
strings = map(str, [1, 2, 3])        # ['1', '2', '3']
ints = map(int, ['1', '2', '3'])     # [1, 2, 3]

# Extract attributes
names = map(lambda p: p.name, people)

# Multiple iterables
sums = map(lambda x, y: x + y, [1,2,3], [4,5,6])  # [5, 7, 9]
```

### filter() - Keep Elements That Match

**Syntax:** `filter(function, iterable)`

```python
# Without filter
numbers = [1, 2, 3, 4, 5, 6]
evens = []
for num in numbers:
    if num % 2 == 0:
        evens.append(num)

# With filter
evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))  # [2, 4, 6]
```

**How to Remember:**
```
filter(predicate, list) → keeps elements where predicate is TRUE
        ↓           ↓
   "condition" + "to what"
```

**Common Patterns:**
```python
# Filter by condition
adults = filter(lambda p: p.age >= 18, people)

# Remove None/empty
valid = filter(None, [0, 1, False, 2, '', 3])  # [1, 2, 3] 
## 0, False, '', None, and empty collections ([], {}, ()) are falsy, Everything else is truthy. 
## If you pass None as the function, Python treats it as the identity function — meaning it keeps only elements that are truthy.

# Filter by type
nums = filter(lambda x: isinstance(x, int), mixed_list)
```

### reduce() - Combine to Single Value

**Syntax:** `reduce(function, iterable, [initial])`

```python
from functools import reduce

# Without reduce
numbers = [1, 2, 3, 4]
total = 0
for num in numbers:
    total += num

# With reduce
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 10
```

**How to Remember:**
```
reduce(function, list) → combines all elements into ONE
        ↓          ↓
  "how to combine" + "what to combine"

Accumulator pattern:
reduce(lambda acc, curr: acc + curr, [1,2,3,4])
              ↑     ↑
         accumulator + current element
```

**Step-by-step visualization:**
```python
reduce(lambda x, y: x + y, [1, 2, 3, 4])

Step 1: x=1, y=2  → 1+2 = 3
Step 2: x=3, y=3  → 3+3 = 6
Step 3: x=6, y=4  → 6+4 = 10
Result: 10
```

**Common Patterns:**
```python
from functools import reduce

# Sum
total = reduce(lambda x, y: x + y, numbers)
# or just: sum(numbers)

# Product
product = reduce(lambda x, y: x * y, [1, 2, 3, 4])  # 24

# Maximum
max_val = reduce(lambda x, y: x if x > y else y, numbers)
# or just: max(numbers)

# Flatten lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda x, y: x + y, nested)  # [1,2,3,4,5,6]
```

---

## 🎓 Comparison: List Comprehension vs Functional

```python
numbers = [1, 2, 3, 4, 5, 6]

# List comprehension (Pythonic)
squared_evens = [x**2 for x in numbers if x % 2 == 0]

# Functional style
squared_evens = map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers))

# Both give: [4, 16, 36]
```

**When to use which?**
- **List comprehension:** More readable, Pythonic
- **Functional:** Composing operations, lazy evaluation

---

## 📝 Practice Examples

### Easy Level

**1. Double all numbers**
```python
numbers = [1, 2, 3, 4, 5]
# Expected: [2, 4, 6, 8, 10]

# Solution
result = list(map(lambda x: x * 2, numbers))
```

**2. Keep only positive numbers**
```python
numbers = [-2, -1, 0, 1, 2]
# Expected: [1, 2]

# Solution
result = list(filter(lambda x: x > 0, numbers))
```

**3. Sum all numbers**
```python
numbers = [1, 2, 3, 4, 5]
# Expected: 15

# Solution
from functools import reduce
result = reduce(lambda x, y: x + y, numbers)
```

### Medium Level

**4. Get lengths of all words**
```python
words = ["hi", "hello", "hey"]
# Expected: [2, 5, 3]

# Solution
result = list(map(lambda w: len(w), words))
# or: list(map(len, words))
```

**5. Filter words longer than 3 characters**
```python
words = ["hi", "hello", "hey", "python"]
# Expected: ['hello', 'python']

# Solution
result = list(filter(lambda w: len(w) > 3, words))
```

**6. Find maximum number**
```python
numbers = [3, 7, 2, 9, 1]
# Expected: 9

# Solution
from functools import reduce
result = reduce(lambda x, y: x if x > y else y, numbers)
# or: max(numbers)
```

### Advanced Level - Combinations

**7. Square even numbers**
```python
numbers = [1, 2, 3, 4, 5, 6]
# Expected: [4, 16, 36]

# Solution
result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
```

**8. Sum of squares**
```python
numbers = [1, 2, 3, 4]
# Expected: 30 (1+4+9+16)

# Solution
from functools import reduce
result = reduce(lambda x, y: x + y, map(lambda x: x**2, numbers))
```

**9. Count words starting with 'a'**
```python
words = ["apple", "banana", "apricot", "cherry"]
# Expected: 2

# Solution
result = len(list(filter(lambda w: w.startswith('a'), words)))
# or: reduce(lambda count, w: count + (1 if w.startswith('a') else 0), words, 0)
```

**10. Flatten and sum**
```python
nested = [[1, 2], [3, 4], [5, 6]]
# Expected: 21

# Solution
from functools import reduce
flat = reduce(lambda x, y: x + y, nested)
total = reduce(lambda x, y: x + y, flat)
# or: sum(sum(nested, []))
```

---

## 🎯 Memory Tricks

### map, filter, reduce

```
map    → TRANSFORM each element (1-to-1)
          "Map each item to new value"

filter → SELECT matching elements (many-to-fewer)
          "Filter out unwanted items"

reduce → COMBINE into single value (many-to-1)
          "Reduce many to one"
```

### Lambda Syntax

```
lambda x: x * 2
   ↑   ↑  ↑
  name in return
         expression
```

**Remember:** "Lambda takes X, returns expression"

---

## ⚠️ Common Pitfalls

### Pitfall 1: map/filter return iterators
```python
result = map(lambda x: x * 2, [1, 2, 3])
print(result)  # <map object> (not a list!)

# Must convert to list
print(list(result))  # [2, 4, 6]
```

### Pitfall 2: reduce needs import
```python
# ❌ WRONG
reduce(lambda x, y: x + y, [1, 2, 3])  # NameError

# ✅ RIGHT
from functools import reduce
reduce(lambda x, y: x + y, [1, 2, 3])
```

### Pitfall 3: Lambda can't have statements
```python
# ❌ WRONG
lambda x: print(x)  # SyntaxError

# ✅ RIGHT
def print_value(x):
    print(x)
```

### Pitfall 4: Overusing lambdas
```python
# ❌ BAD - Unreadable
result = reduce(lambda x, y: x + y, 
                map(lambda x: x**2, 
                    filter(lambda x: x % 2 == 0, numbers)))

# ✅ GOOD - Clear steps
evens = filter(lambda x: x % 2 == 0, numbers)
squared = map(lambda x: x**2, evens)
total = reduce(lambda x, y: x + y, squared)
```

---

## 🔑 Key Takeaways

1. **FP treats functions as data**
2. **Pure functions** = predictable, testable
3. **Immutability** = safer, easier to reason about
4. **Lambda** = anonymous, short functions
5. **map** = transform each
6. **filter** = keep matching
7. **reduce** = combine to one
8. **List comprehensions** often more Pythonic than map/filter

---

## ✅ Best Practices

**DO:**
- ✅ Use lambdas for simple, one-time operations
- ✅ Prefer list comprehensions for readability
- ✅ Keep functions pure when possible
- ✅ Use meaningful variable names even in lambdas

**DON'T:**
- ❌ Overuse lambdas (use def for complex logic)
- ❌ Create side effects in map/filter/reduce
- ❌ Nest too many functional operations
- ❌ Forget to convert map/filter to list when needed