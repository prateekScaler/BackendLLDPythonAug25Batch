# ChainMap & Functional Programming Quiz 🧠
## Advanced Concepts & Gotchas

---

## SECTION 1: ChainMap Challenges

### Question 1: ChainMap Mutation

```python
from collections import ChainMap

defaults = {"a": 1, "b": 2}
overrides = {"b": 3}

config = ChainMap(overrides, defaults)
config["c"] = 4

print(defaults)
print(overrides)
```

**What's in each dict?**
- A) defaults: `{"a":1, "b":2}`, overrides: `{"b":3, "c":4}`
- B) defaults: `{"a":1, "b":2, "c":4}`, overrides: `{"b":3}`
- C) defaults: `{"a":1, "b":2, "c":4}`, overrides: `{"b":3, "c":4}`
- D) Both unchanged
---

<details>
<summary>Answer</summary>

**A) defaults unchanged, overrides gets "c"**

**Explanation:** ChainMap mutations (inserts, updates) only affect the FIRST dict in the chain.

```python
defaults = {"a": 1, "b": 2}
overrides = {"b": 3}
# Only overrides is modified!
```

**Rule:** Writes go to first map only, reads search all maps.
</details>

---

### Question 2: ChainMap Deletion

```python
from collections import ChainMap

d1 = {"a": 1, "b": 2}
d2 = {"a": 10, "c": 3}

cm = ChainMap(d1, d2)
del cm["a"]

print(cm["a"])
```

**What happens?**
- A) KeyError
- B) Prints `10`
- C) Prints `1`
- D) Prints `None`
---
<details>
<summary>Answer</summary>

**B) Prints `10`**

**Explanation:** Delete only removes from FIRST dict. ChainMap then finds "a" in second dict!

```python
d1 = {"b": 2}      # "a" removed
d2 = {"a": 10, "c": 3}  # "a" still here
cm["a"]  # Returns 10 from d2
```

**Gotcha:** Deletion doesn't remove from all dicts, just first one.
</details>

---

## SECTION 2: Lazy Evaluation

### Question 3: Memory Mystery

```python
# Version A
result_a = [x**2 for x in range(1000000)]
first = result_a[0]

# Version B
result_b = map(lambda x: x**2, range(1000000))
first = next(iter(result_b))
```

**Which uses less memory?**
- A) Version A
- B) Version B
- C) Same memory
- D) Depends on Python version
---
<details>
<summary>Answer</summary>

**B) Version B (map is lazy)**

**Memory:**
- List comprehension: ~8MB (stores all 1M items)
- map: ~60 bytes (just iterator object)

**Explanation:** map() returns iterator that computes values on demand. List comprehension creates entire list immediately.

**Rule:** Use map/filter for memory efficiency with large datasets.
</details>

---

### Question 4: Iterator Exhaustion

```python
from functools import reduce

numbers = map(lambda x: x * 2, [1, 2, 3])

result1 = reduce(lambda x, y: x + y, numbers)
result2 = reduce(lambda x, y: x + y, numbers)

print(result2)
```

**What's result2?**
- A) `12`
- B) `0`
- C) `TypeError`
- D) `None`
---
<details>
<summary>Answer</summary>

**C) TypeError: reduce() of empty sequence**

**Explanation:** map() returns iterator (lazy). After first reduce() consumes it, iterator is exhausted. Second reduce() gets empty iterator.

```python
numbers = map(...)  # Iterator
result1 = reduce(..., numbers)  # Consumes iterator
result2 = reduce(..., numbers)  # Empty! TypeError
```

**Rule:** Iterators are one-time use. Convert to list if reusing: `list(numbers)`.
</details>

---

## SECTION 3: Lambda & Higher-Order Functions

### Question 5: Lambda Closure Trap

```python
funcs = [lambda x: x * i for i in range(3)]

results = [f(10) for f in funcs]
print(results)
```

**What's the output?**
- A) `[0, 10, 20]`
- B) `[20, 20, 20]`
- C) `[10, 10, 10]`
- D) `SyntaxError`
---
<details>
<summary>Answer</summary>

**B) `[20, 20, 20]`**

**Explanation:** Lambda captures variable `i` by reference, not value. When lambdas execute, loop finished and `i = 2` for all.

```python
# All lambdas reference same i
# When called, i = 2 (final loop value)
# 10 * 2 = 20 for all
```

**Fix:**
```python
funcs = [lambda x, i=i: x * i for i in range(3)]
#                 ↑ captures value
```

**Gotcha:** Late binding in closures.
</details>

---

### Question 6A: reduce Short-Circuit?

```python
from functools import reduce

def expensive(x, y):
    print(f"Computing {x} + {y}")
    return x + y

numbers = [1, 2, 3, 4, 5]
result = reduce(expensive, numbers)
```

**How many times does expensive() run?**
- A) 5 times
- B) 4 times
- C) 1 time
- D) 10 times
---
<details>
<summary>Answer</summary>

**B) 4 times**

**Explanation:** reduce() needs n-1 operations to combine n elements:

```
Step 1: 1 + 2 = 3
Step 2: 3 + 3 = 6
Step 3: 6 + 4 = 10
Step 4: 10 + 5 = 15
```

**Key:** reduce() doesn't short-circuit - always processes entire sequence.

Compare to filter/map which can stop early with islice.
</details>

---
### Question 6B: reduce() with Initializer

```python
from functools import reduce

def combine(x, y):
    print(f"Combining {x} and {y}")
    return x + y

numbers = [1, 2, 3]
result = reduce(combine, numbers, 10)
print("Result:", result)
```
**How many times does combine() run?**
- A) 2 times
- B) 3 times
- C) 4 times
- D) 1 time

---

<details>
<summary>Answer</summary>

**B) 3 times**

**Explanation:** With initializer, reduce() starts with that value and processes all elements:

``` 
Step 1: combine(10, 1) -> 11
Step 2: combine(11, 2) -> 13
Step 3: combine(13, 3) -> 16
```

---

### Question 7: map Multiple Iterables

```python
result = list(map(lambda x, y: x + y, [1, 2, 3], [10, 20]))

print(result)
print(len(result))
```

**What's the output?**
- A) `[11, 22, 3]`, length 3
- B) `[11, 22, 13]`, length 3
- C) `[11, 22]`, length 2
- D) `ValueError`

---

<details>
<summary>Answer</summary>

**C) `[11, 22]`, length 2**

**Explanation:** map() with multiple iterables stops at SHORTEST iterable.

```python
[1, 2, 3]    # Length 3
[10, 20]     # Length 2 (stops here)

Results: [1+10, 2+20] = [11, 22]
3 is never processed!
```

**Rule:** map() stops at shortest input.
</details>

---

## SECTION 4: Complex Scenarios

### Question 8: Pipeline Order

```python
from functools import reduce

numbers = range(10)

result = reduce(
    lambda x, y: x + y,
    map(lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers)
    )
)

print(result)
```

**What's the result?**
- A) 120
- B) 165
- C) 285
- D) 0

---

<details>
<summary>Answer</summary>

**A) 120**

**Step-by-step:**
```python
range(10)          # [0,1,2,3,4,5,6,7,8,9]
filter(even)       # [0,2,4,6,8]
map(square)        # [0,4,16,36,64]
reduce(sum)        # 0+4+16+36+64 = 120
```

**Order:** filter → map → reduce (inside-out)
</details>

---

## Question 9: Lambda Syntax Rules
Which of these lambda expressions will cause SyntaxError?

```python

# Option 1
f1 = lambda x: x + 1

# Option 2  
f2 = lambda x: x = x + 1

# Option 3
f3 = lambda x: print(x)

# Option 4
f4 = lambda x: x if x > 0 else -x
```

**Which options will cause SyntaxError?**
- A) Only Option 2
- B) Options 2 and 3
- C) Only Option 3
- D) Options 1 and 4

---

<details>
<summary>Answer</summary>


**A) Only Option 2**
**Explanation:**
**Option 1 ✅ Valid**
```python
lambda x: x + 1
# Single expression - works fine
```
**Option 2 ❌ SyntaxError**
```python
lambda x: x = x + 1
# Can't use assignment statement (=) in lambda
# SyntaxError: invalid syntax
```

**Option 3 ✅ Valid (but problematic)**
```python
lambda x: print(x)
# Syntactically correct
# But returns None (print's return value)
```

**Option 4 ✅ Valid**
```python
lambda x: x if x > 0 else -x
# Ternary expression is allowed
```

**Key Rules:**
- ❌ Can't use assignment statements (`x = value`)
- ❌ Can't use multiple statements
- ✅ Can use single expressions
- ✅ Ternary operator is one expression

</details>

---

## 🔑 Lambda Limitations Summary

### ❌ INVALID - Statements Not Allowed

```python
# Assignment
lambda x: x = x + 1        # SyntaxError

# Multiple expressions
lambda x: x + 1; x * 2     # SyntaxError

# Assignment with different variable
lambda x: y = x + 1        # SyntaxError
```

### ✅ VALID - Single Expressions Only

```python
# Simple expression
lambda x: x + 1            # OK

# Function call (even if returns None)
lambda x: print(x)         # OK (but returns None)

# Ternary operator
lambda x: x if x > 0 else -x    # OK

# Complex expression
lambda x, y: x * 2 + y * 3      # OK
```

---

## 🎯 Remember

**Statement vs Expression:**
- **Statement:** Does something (assignment, print, if, for, while)
- **Expression:** Returns a value (x + 1, x > 0, function calls)

**Lambda Rule:**
```
Lambda can ONLY contain a single EXPRESSION
(no statements allowed)
```

**When you need statements, use `def`:**
```python
# ❌ Can't do this with lambda
lambda x: x = x + 1

# ✅ Use def instead
def increment(x):
    x = x + 1
    return x
```

---

## 💡 Quick Test

**Is it valid in lambda?**
- `x + 1` → ✅ Expression
- `x = 1` → ❌ Statement
- `x > 0` → ✅ Expression
- `return x` → ❌ Statement
- `x if x > 0 else -x` → ✅ Expression
- `print(x)` → ✅ Expression (function call)

**If in doubt: Can you put it on the right side of `=`?**
- `result = x + 1` → Yes, it's an expression ✅
- `result = x = 1` → No, can't assign to assignment ❌

---

### Question 10: Generator Exhaustion Gotcha

```python
def process():
    data = (x * 2 for x in range(5))
    print(sum(data))
    print(sum(data))

process()
```

**What prints?**
- A) `20` then `20`
- B) `20` then `0`
- C) Error on second sum
- D) `20` then `None`


---


<details>
<summary>Answer</summary>

**B) `20` then `0`**

**Explanation:** Generator expressions are iterators (one-time use).

```python
data = (x * 2 for x in range(5))  # [0,2,4,6,8]
sum(data)  # Consumes: 0+2+4+6+8 = 20
sum(data)  # Empty iterator: 0
```

**Note:** sum() of empty iterator returns 0 (not error).

**Fix:** Convert to list: `data = [x * 2 for x in range(5)]`
</details>

---

## 🔑 Concepts Tested

### ChainMap:
1. Mutations affect first dict only
2. Deletion doesn't remove from all dicts
3. Lookup searches all dicts in order

### Functional Programming:
4. Lazy evaluation (map/filter are iterators)
5. Iterator exhaustion (one-time use)
6. Lambda closure trap (late binding)
7. reduce always processes entire sequence
8. map stops at shortest iterable
9. Pipeline execution order
10. Generator exhaustion

---