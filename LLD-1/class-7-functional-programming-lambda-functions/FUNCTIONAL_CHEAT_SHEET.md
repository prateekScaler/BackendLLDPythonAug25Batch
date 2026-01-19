# Functional Programming - Quick Reference Cheat Sheet

## 🎯 The Big Three

```
┌─────────────────────────────────────────────────────────┐
│                    map, filter, reduce                   │
└─────────────────────────────────────────────────────────┘

map     [1, 2, 3] → function → [2, 4, 6]
        Transform EACH element
        
filter  [1, 2, 3, 4] → condition → [2, 4]
        SELECT matching elements
        
reduce  [1, 2, 3, 4] → combine → 10
        COMBINE to single value
```

---

## 📝 Lambda Syntax Reminder

```python
lambda arguments: expression
   ↑       ↑          ↑
keyword  input     output

# Examples
lambda x: x * 2              # One arg
lambda x, y: x + y           # Two args
lambda x, y, z: x + y + z    # Three args
lambda: 42                   # No args
```

**Remember:** "Lambda X returns expression"

---

## 🗺️ map() - Transform Each

```python
map(function, iterable)
     ↓         ↓
  "what"   "to what"

# Pattern
result = list(map(lambda x: x * 2, [1, 2, 3]))
                    ↑ transform    ↑ input
# Output: [2, 4, 6]
```

### Common Uses
```python
map(str, [1, 2, 3])                    # Convert types
map(len, ["hi", "hello"])              # Get lengths
map(lambda x: x**2, numbers)           # Transform
map(lambda p: p.name, people)          # Extract attribute
map(lambda x, y: x+y, list1, list2)    # Two lists
```

---

## 🔍 filter() - Select Matching

```python
filter(predicate, iterable)
        ↓           ↓
    "condition"  "to what"

# Pattern
result = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
                       ↑ condition         ↑ input
# Output: [2, 4]
```

### Common Uses
```python
filter(lambda x: x > 0, numbers)       # Keep positives
filter(lambda x: x % 2 == 0, numbers)  # Keep evens
filter(lambda w: len(w) > 3, words)    # Keep long words
filter(lambda p: p.age >= 18, people)  # Filter by attribute
filter(None, [0, 1, '', 2, False])     # Remove falsy → [1, 2]
```

---

## 🔄 reduce() - Combine to One

```python
from functools import reduce  # ⚠️ Need import!

reduce(function, iterable, [initial])
        ↓          ↓           ↓
   "combiner"   "what"    "start value"

# Pattern
result = reduce(lambda x, y: x + y, [1, 2, 3, 4])
                 ↑ accumulator  ↑ current
# Output: 10
```

### How it Works
```
reduce(lambda x, y: x + y, [1, 2, 3, 4])

Step 1: x=1, y=2  →  3
Step 2: x=3, y=3  →  6
Step 3: x=6, y=4  →  10
Result: 10
```

### Common Uses
```python
reduce(lambda x, y: x + y, numbers)           # Sum
reduce(lambda x, y: x * y, numbers)           # Product
reduce(lambda x, y: x if x > y else y, nums)  # Max
reduce(lambda x, y: x + y, nested_lists)      # Flatten
```

---

## 🔗 Combining Operations

### Pattern 1: filter → map
```python
# Square only even numbers
result = list(map(
    lambda x: x**2,
    filter(lambda x: x % 2 == 0, numbers)
))
```

### Pattern 2: filter → map → reduce
```python
# Sum of squares of evens
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x**2,
        filter(lambda x: x % 2 == 0, numbers)
    )
)
```

### Pattern 3: map → reduce
```python
# Sum of all squares
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x**2, numbers)
)
```

---

## 🎓 vs List Comprehension

```python
numbers = [1, 2, 3, 4, 5, 6]

# Functional
result = list(map(
    lambda x: x**2,
    filter(lambda x: x % 2 == 0, numbers)
))

# List Comprehension (More Pythonic)
result = [x**2 for x in numbers if x % 2 == 0]

# Both give: [4, 16, 36]
```

**When to use which:**
- **List comp:** More readable, Pythonic ✅
- **Functional:** Composing operations, lazy eval

---

## ⚠️ Common Pitfalls

### 1. Forgot to convert to list
```python
# ❌ WRONG
result = map(lambda x: x * 2, [1, 2, 3])
print(result)  # <map object>

# ✅ RIGHT
result = list(map(lambda x: x * 2, [1, 2, 3]))
print(result)  # [2, 4, 6]
```

### 2. Forgot to import reduce
```python
# ❌ WRONG
reduce(lambda x, y: x + y, [1, 2, 3])  # NameError

# ✅ RIGHT
from functools import reduce
reduce(lambda x, y: x + y, [1, 2, 3])
```

### 3. Lambda with statements
```python
# ❌ WRONG - Can't use statements
lambda x: print(x)  # SyntaxError

# ✅ RIGHT - Use def
def print_value(x):
    print(x)
```

### 4. Too complex lambda
```python
# ❌ BAD - Unreadable
result = reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))

# ✅ GOOD - Readable steps
evens = filter(lambda x: x % 2 == 0, numbers)
squared = map(lambda x: x**2, evens)
result = reduce(lambda x, y: x + y, squared)
```

---

## 🎯 Mental Models

### map: "Do this to each"
```
[🔴, 🔴, 🔴]  →  paint blue  →  [🔵, 🔵, 🔵]
Each item transformed
```

### filter: "Keep only these"
```
[🔴, 🔵, 🔴, 🔵]  →  keep red  →  [🔴, 🔴]
Some items removed
```

### reduce: "Combine all into one"
```
[1, 2, 3, 4]  →  add all  →  10
Many become one
```

---

## 📊 Complexity Cheat Sheet

| Operation | Functional | List Comp | Loop |
|-----------|-----------|-----------|------|
| **Readability** | Medium | High | Medium |
| **Performance** | Same | Same | Same |
| **Lazy eval** | Yes | No | No |
| **Pythonic** | Medium | High | Low |

---

## 🔑 Quick Decision Tree

```
Need to process list?
│
├─ Transform each element?
│  └─ Use map() or [x*2 for x in list]
│
├─ Select some elements?
│  └─ Use filter() or [x for x in list if x > 5]
│
├─ Combine to single value?
│  └─ Use reduce() or sum()/max()/min()
│
└─ Multiple operations?
   └─ Chain: filter → map → reduce
```

---

## 💡 Memory Tricks

### Function Names
- **map** = "Map each item to new value"
- **filter** = "Filter out unwanted"
- **reduce** = "Reduce many to one"

### Syntax Pattern
```
function(lambda ..., iterable)
         ↑ what     ↑ to what
```

### Order Matters
```
filter → map → reduce
  ↓       ↓       ↓
 select  change  combine
```

---

## ✅ Best Practices Checklist

- [ ] Use lambda for simple, one-time operations
- [ ] Use def for complex logic
- [ ] Prefer list comprehensions when more readable
- [ ] Convert map/filter to list when needed
- [ ] Import reduce from functools
- [ ] Keep lambdas on one line
- [ ] Name intermediate steps for clarity
- [ ] Avoid deep nesting of operations

---

## 🚀 Practice Pattern

1. **Identify:** What needs to happen?
2. **Choose:** map, filter, or reduce?
3. **Write:** lambda or def?
4. **Convert:** to list if needed
5. **Test:** with simple data first

---

## 📝 Common Patterns Reference

```python
# Sum
sum(numbers)  # or reduce(lambda x,y: x+y, numbers)

# Product
reduce(lambda x, y: x * y, numbers)

# Max
max(numbers)  # or reduce(lambda x,y: x if x>y else y, numbers)

# Flatten
reduce(lambda x, y: x + y, nested_lists)

# Count matching
len(list(filter(condition, items)))

# Transform and sum
sum(map(transform, items))

# Filter and transform
list(map(transform, filter(condition, items)))
```

---

## 🎓 Interview Quick Answers

**Q: When to use lambda?**
A: Short, simple, one-time operations

**Q: map vs list comp?**
A: List comp more Pythonic, map for function composition

**Q: Pure function?**
A: Same input → same output, no side effects

**Q: Why functional?**
A: Easier testing, parallelization, reasoning about code