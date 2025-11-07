# 🧠 Python Collections Quiz
## Test Your Knowledge!

---

## Question 1: The Empty Set 🕳️

```python
a = {}
b = set()

print(type(a))
print(type(b))
```

**Q: What types are a and b?**

A) Both are sets

B) Both are dicts

C) a is dict, b is set

D) a is set, b is dict

---

## Answer 1: C 📚

```
a is dict
b is set
```

**Key Rule:**
```python
{}      # Empty DICT!
set()   # Empty SET

{1, 2}  # Set (has elements)
```

**Remember:** `{}` makes dict by default!

---

## Question 2: Tuple Tricks 🎭

```python
t = (1)
print(len(t))
```

**Q: What happens?**

A) `1`

B) TypeError: object of type 'int' has no len()

C) `0`

D) `(1,)`

---

## Answer 2: B 💥

**Explanation:**
```python
t = (1)   # This is int 1, not tuple!
# Parentheses are just for grouping

t = (1,)  # Comma makes it tuple
print(len(t))  # 1 ✓
```

**Single element tuple needs comma!**

---

## Question 3: Set Membership 🔍

```python
s = {1, 2, 3}
print(s[0])
```

**Q: What's the output?**

A) `1`

B) `2`

C) `3`

D) TypeError

---

## Answer 3: D ❌

```
TypeError: 'set' object is not subscriptable
```

**Sets are:**
- ✓ Unordered
- ✓ No indexing
- ✓ No slicing

**Can only:**
```python
1 in s        # True (membership)
for x in s:   # Iterate
```

---

## Question 4: Dict Key Types 🔑

```python
d = {}
d[(1, 2)] = "a"
d[[1, 2]] = "b"
```

**Q: What happens?**

A) Both work fine

B) First works, second TypeError

C) First TypeError, second works

D) Both TypeError

---

## Answer 4: B 🎯

```
First: ✓ Works
Second: TypeError: unhashable type: 'list'
```

**Dict keys must be hashable:**
```python
# Hashable (immutable)
d[(1, 2)] = "a"     # ✓ Tuple
d["key"] = "b"      # ✓ String
d[42] = "c"         # ✓ Number

# Not hashable (mutable)
d[[1, 2]] = "d"     # ✗ List
d[{1: 2}] = "e"     # ✗ Dict
d[{1, 2}] = "f"     # ✗ Set
```

---

## Question 5: Remove vs Discard 🗑️

```python
s = {1, 2, 3}
s.remove(4)
print("A")
s.discard(4)
print("B")
```

**Q: What prints?**

A) A and B

B) Only A

C) Only B

D) Nothing (error on line 2)

---

## Answer 5: D 💥

```
KeyError on line 2 (nothing prints)
```

**Difference:**
```python
s.remove(4)   # KeyError if not found
s.discard(4)  # Silent if not found

# If 4 doesn't exist:
remove()  → Crash
discard() → Nothing
```

**Use discard() for safe removal**

---

## Question 6: Shallow Copy Gotcha 🪞

```python
list1 = [[1, 2], [3, 4]]
list2 = list1.copy()

list2[0].append(99)
print(list1[0])
```

**Q: What's list1[0]?**

A) `[1, 2]`

B) `[1, 2, 99]`

C) `[99, 1, 2]`

D) `[[1, 2], [3, 4]]`

---

## Answer 6: B 😱

```
[1, 2, 99]
```

**Shallow copy copies references!**
```python
list1 = [[1, 2], [3, 4]]
list2 = list1.copy()  # New list, same nested lists!

# Both share same inner lists
list2[0] is list1[0]  # True
```

**Fix with deep copy:**
```python
import copy
list2 = copy.deepcopy(list1)
```

---

## Question 7: Iteration Modification 🔄

```python
numbers = [1, 2, 4, 5, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)

print(numbers)
```

**Q: What's the final list?**

A) `[1, 5]`

B) `[1, 2, 4, 5, 5]`

C) `[1, 4, 5, 5]`

D) `[]`

---

## Answer 7: C 🤔

```
[1, 4, 5, 5]
```

**Why? Iterator skips elements!**
```python
# Step by step:
[1, 2, 4, 5, 5]  i=0
    ↑ 2 is even, remove it

[1, 4, 5, 5]     i=1
       ↑ Iterator moved, skips 4!
       Check 5 (odd), do not remove

[1, 4, 5, 5]  # Wrong! 4 got skipped
```

**Never modify during iteration!**

---

## Question 8: Tuple Mutability 🧬

```python
t = ([1, 2], 3)
t[0].append(3)
t[0] = [4, 5]
```

**Q: Which line(s) work?**

A) Both work

B) First works, second fails

C) First fails, second works

D) Both fail

---

## Answer 8: B ✅❌

```
Line 1: ✓ Works
Line 2: ✗ TypeError
```

**Immutability is shallow:**
```python
t = ([1, 2], 3)

t[0].append(3)  # ✓ Modifying list inside
                # Tuple still has same list object

t[0] = [4, 5]   # ✗ Replacing tuple element
                # Can't change tuple itself!
```

---

## Question 9: defaultdict Magic 🎩

```python
from collections import defaultdict

d = defaultdict(int)
print(d["missing"])
print(len(d))
```

**Q: What's len(d)?**

A) `0`

B) `1`

C) `2`

D) KeyError

---

## Answer 9: B 🪄

```
len(d) is 1
```

**defaultdict creates missing keys!**
```python
d = defaultdict(int)

d["missing"]  # Creates key with default (0)
# d = {"missing": 0}

len(d)  # 1
```

**Regular dict:**
```python
d = {}
d["missing"]  # KeyError!
```

---

## Question 10: Counter Arithmetic 🧮

```python
from collections import Counter

c1 = Counter(['a', 'b', 'b'])
c2 = Counter(['b', 'c'])

result = c1 + c2
print(result['b'])
```

**Q: What's result['b']?**

A) `2`

B) `3`

C) `1`

D) `4`

---

## Answer 10: B ✨

```
result['b'] is 3
```

**Counter adds counts:**
```python
c1 = Counter(['a', 'b', 'b'])
# {'a': 1, 'b': 2}

c2 = Counter(['b', 'c'])
# {'b': 1, 'c': 1}

c1 + c2
# {'a': 1, 'b': 3, 'c': 1}
#         ↑ 2 + 1
```

---

## 🔑 Key Takeaways

✅ `{}` is dict, not set!

✅ Never use mutable defaults

✅ Single element tuple needs comma

✅ Sets can't be indexed

✅ Dict keys must be hashable

✅ `.remove()` errors, `.discard()` silent

✅ `.copy()` is shallow

✅ Don't modify during iteration

✅ Tuple immutability is shallow

✅ defaultdict auto-creates keys

---

## 📊 Collection Pitfalls Summary

| Collection | Pitfall | Fix |
|------------|---------|-----|
| list | Mutable default | Use `None` |
| list | Modify while iterating | List comprehension |
| tuple | Single element | Add comma |
| set | Empty `{}` | Use `set()` |
| dict | Mutable keys | Use immutables |
| all | Shallow copy | Use `deepcopy` |
