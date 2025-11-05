# Python Collections - Complete Guide

## 📊 Collections Overview

<pre>
Python Collections
├── Built-in
│   ├── list
│   ├── tuple
│   ├── dict
│   └── set
└── collections module
    ├── defaultdict
    ├── Counter
    ├── OrderedDict
    ├── deque
    ├── ChainMap
    └── namedtuple
</pre>

---

## 🔍 Quick Comparison

| Collection | Ordered | Mutable | Duplicates | Indexed | Use Case |
|------------|---------|---------|------------|---------|----------|
| **list** | ✅ | ✅ | ✅ | ✅       | General purpose |
| **tuple** | ✅ | ❌ | ✅ | ✅*      | Immutable data |
| **set** | ❌ | ✅ | ❌ | ❌       | Unique items |
| **dict** | ✅* | ✅ | ❌ keys | ❌       | Key-value pairs |

*Ordered since Python 3.7+

---

## 1️⃣ LIST - Dynamic Array

### Characteristics
```python
# Ordered, mutable, allows duplicates
numbers = [1, 2, 3, 2, 1]
```

### Common Operations
```python
# O(1) - Fast
lst.append(item)        # Add to end
lst[index]              # Access by index
len(lst)                # Get length

# O(n) - Slow
lst.insert(0, item)     # Insert at beginning
lst.remove(item)        # Remove first occurrence
item in lst             # Check membership
```

### Pitfalls

**Pitfall 1: List as default argument**
```python
# WRONG
def add_item(item, lst=[]):  # Mutable default!
    lst.append(item)
    return lst

result1 = add_item(1)  # [1]
result2 = add_item(2)  # [1, 2] 😱 Shared!

# RIGHT
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

**Pitfall 2: Modifying while iterating**
```python
# WRONG
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Skips elements!

# RIGHT
numbers = [num for num in numbers if num % 2 != 0]
```

**Pitfall 3: Shallow copy**
```python
list1 = [[1, 2], [3, 4]]
list2 = list1.copy()  # Shallow!

list2[0].append(99)
print(list1[0])  # [1, 2, 99] 😱
```

### Customization: Extending list
```python
class UniqueList(list):
    """List that only keeps unique items"""
    def append(self, item):
        if item not in self:
            super().append(item)

ul = UniqueList([1, 2, 3])
ul.append(2)  # Ignored
ul.append(4)  # Added
print(ul)  # [1, 2, 3, 4]
```

---

## 2️⃣ TUPLE - Immutable Sequence

### Characteristics
```python
# Ordered, immutable, allows duplicates
coords = (10, 20, 30)
```

### Use Cases
```python
# 1. Return multiple values
def get_stats():
    return (100, 85.5, "A")

# 2. Dictionary keys (hashable)
location_map = {
    (0, 0): "origin",
    (1, 1): "diagonal"
}

# 3. Unpacking
x, y, z = (1, 2, 3)
```

### Pitfalls

**Pitfall 1: Single element tuple**
```python
# WRONG
not_a_tuple = (1)      # This is int!
print(type(not_a_tuple))  # <class 'int'>

# RIGHT
is_a_tuple = (1,)      # Comma makes it tuple
print(type(is_a_tuple))   # <class 'tuple'>
```

**Pitfall 2: Immutability is shallow**
```python
t = ([1, 2], [3, 4])
t[0].append(99)  # Works! List inside is mutable
print(t)  # ([1, 2, 99], [3, 4])

# But can't replace tuple itself
t[0] = [5, 6]  # TypeError!
```

### Customization: namedtuple
```python
from collections import namedtuple

# Create a named tuple type
Point = namedtuple('Point', ['x', 'y'])

p = Point(10, 20)
print(p.x, p.y)  # 10 20
print(p[0])      # 10 (still indexable)

# More readable than regular tuple
```

---

## 3️⃣ SET - Unique Collection

### Characteristics
```python
# Unordered, mutable, no duplicates
unique_nums = {1, 2, 3, 2, 1}  # {1, 2, 3}
```

### Common Operations
```python
# O(1) - Fast
item in set             # Membership
set.add(item)           # Add item
set.remove(item)        # Remove (error if not found)
set.discard(item)       # Remove (no error)

# Example sets
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

# Set operations
set1 | set2             # Union → {1, 2, 3, 4, 5, 6}
set1 & set2             # Intersection → {3, 4}
set1 - set2             # Difference → {1, 2}
set1 ^ set2             # Symmetric difference → {1, 2, 5, 6}
```

### Pitfalls

**Pitfall 1: Empty set syntax**
```python
# WRONG
empty = {}  # This is a dict!

# RIGHT
empty = set()
```

**Pitfall 2: Set elements must be hashable**
```python
# WRONG ❌ - Mutable types are not hashable
s = {[1, 2], [3, 4]}           # TypeError: list is not hashable
s = {{'a': 1, 'b': 2}}         # TypeError: dict is not hashable
s = {{1, 2, 3}}                # TypeError: set is not hashable
s = {(1, [2, 3])}              # TypeError: list inside tuple is not hashable

# RIGHT ✅ - Immutable types are hashable
s = {(1, 2), (3, 4)}           # Tuples are hashable
s = {1, 3.14, "hello"}         # Numbers and strings are hashable
s = {frozenset([1, 2, 3])}     # frozenset is hashable (immutable version of set)
s = {(1, (2, 3))}              # Nested tuples are fine
s = {None, True, False}        # Immutable constants are fine

# Summary:
# ✅ Allowed in a set: int, float, str, bool, None, tuple*(Only stictly immutable tuples), frozenset
# ❌ Not allowed: list, dict, set, or any container that can change
```

**Pitfall 3: Sets are unordered**
```python
s = {3, 1, 2}
print(s)  # Order not guaranteed! Might be {1, 2, 3}

# Can't access by index
# s[0]  # TypeError!
```

### Customization: frozenset
```python
# Immutable set (hashable)
fs = frozenset([1, 2, 3])
fs.add(4)  # AttributeError (immutable)

# Can be used in sets and as dict keys
set_of_sets = {frozenset([1, 2]), frozenset([3, 4])}
```

---

## 4️⃣ DICT - Key-Value Mapping

### Characteristics
```python
# Ordered (3.7+), mutable, unique keys
user = {"name": "Alice", "age": 25}
```

### Common Operations
```python
# O(1) - Fast
dict[key]               # Access (KeyError if missing)
dict.get(key, default)  # Safe access
dict[key] = value       # Set value
key in dict             # Check key exists

# Iteration
dict.keys()             # Keys
dict.values()           # Values
dict.items()            # Key-value pairs
```

### Pitfalls

**Pitfall 1: Mutable default value**
```python
# WRONG
d = {"users": []}
d["users"].append("Alice")  # Modifies original!

# RIGHT
d = {"users": None}
if d["users"] is None:
    d["users"] = []
```

**Pitfall 2: Keys must be hashable**
```python
# WRONG ❌ - Mutable (unhashable) keys
d = {[1, 2]: "value"}              # TypeError: unhashable type: 'list'
d = {{1, 2, 3}: "value"}           # TypeError: unhashable type: 'set'
d = {{'a': 1}: "value"}            # TypeError: unhashable type: 'dict'
d = {(1, [2, 3]): "value"}         # TypeError: list inside tuple is not hashable

# RIGHT ✅ - Immutable (hashable) keys
d = {(1, 2): "value"}              # Tuple key is fine
d = {"name": "Alice"}              # String key is fine
d = {42: "Answer"}                 # Integers are fine
d = {3.14: "pi"}                   # Floats are fine
d = {True: "yes"}                  # Booleans are fine
d = {None: "empty"}                # None is fine
d = {frozenset([1, 2, 3]): "set"}  # frozenset is immutable, so fine
d = {(1, (2, 3)): "nested"}        # Tuple with tuple inside is fine

# Subtle example ⚠️
key = (1, [2, 3])  # tuple containing a mutable list
d = {key: "bad"}   # ❌ Fails, because list inside makes it unhashable

# Summary:
# ✅ Allowed keys: int, float, str, bool, None, tuple (of hashables), frozenset
# ❌ Not allowed: list, dict, set, or any object containing mutable parts
```

**Pitfall 3: Iteration order changed during iteration**
```python
# WRONG
d = {"a": 1, "b": 2, "c": 3}
for key in d:
    if key == "b":
        d["d"] = 4  # RuntimeError in some versions!

# RIGHT
for key in list(d.keys()):  # Iterate over copy
    if key == "b":
        d["d"] = 4
```

### Customization: UserDict
```python
from collections import UserDict

class DefaultDict(UserDict):
    """Dict with default value for missing keys"""
    def __init__(self, default_value):
        super().__init__()
        self.default_value = default_value
    
    def __getitem__(self, key):
        if key not in self.data:
            return self.default_value
        return self.data[key]

d = DefaultDict(0)
print(d["missing"])  # 0 (doesn't add to dict)
```

---

## 5️⃣ ADVANCED COLLECTIONS

### defaultdict
```python
from collections import defaultdict

# Auto-creates missing keys
dd = defaultdict(list)
dd["fruits"].append("apple")  # No KeyError!

# Common use: grouping
words = ["apple", "banana", "apricot", "berry"]
groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)
# {'a': ['apple', 'apricot'], 'b': ['banana', 'berry']}
```

### Counter
```python
from collections import Counter

# Count occurrences
words = ["apple", "banana", "apple", "cherry"]
counts = Counter(words)
# Counter({'apple': 2, 'banana': 1, 'cherry': 1})

print(counts.most_common(1))  # [('apple', 2)]

# Arithmetic operations
c1 = Counter(['a', 'b', 'c'])
c2 = Counter(['a', 'b', 'd'])
print(c1 + c2)  # Counter({'a': 2, 'b': 2, 'c': 1, 'd': 1})
```

### deque (Double-ended queue)
```python
from collections import deque

# O(1) operations at both ends
dq = deque([1, 2, 3])
dq.appendleft(0)   # [0, 1, 2, 3]
dq.append(4)       # [0, 1, 2, 3, 4]
dq.popleft()       # [1, 2, 3, 4]

# Maxlen - auto-removes from other end
recent = deque(maxlen=3)
recent.extend([1, 2, 3, 4])  # [2, 3, 4] (1 removed)
```

### ChainMap - Layered Dictionary Lookup
```python
from collections import ChainMap

# ============================================================
# ChainMap - Layer Multiple Dicts Without Merging
# ============================================================

# Basic: Priority lookup (first dict wins)
defaults = {"color": "blue", "size": "M", "theme": "light"}
custom = {"color": "red", "size": "L"}

config = ChainMap(custom, defaults)
print(config["color"])   # "red" (from custom, not defaults)
print(config["size"])    # "L" (from custom)
print(config["theme"])   # "light" (from defaults)

# Key: Looks up in ORDER, stops at first match
# custom → defaults → KeyError
```

**Why ChainMap? Memory Efficient!**
```python
# Regular merge - COPIES data
merged = {**defaults, **custom}  # New dict, duplicated data
    #print(merged) -> {'color': 'red', 'size': 'L', 'theme': 'light'} Rightmost dict wins
# ChainMap - NO COPY, just references
chained = ChainMap(custom, defaults)  # Points to originals

# Modify original, ChainMap sees it!
custom["color"] = "green"
print(config["color"])  # "green" (live reference!)
```

**Multiple Layers (3+ dicts)**
```python
system = {"font": "Arial", "size": "M"}
user = {"size": "L"}
session = {"color": "blue"}

config = ChainMap(session, user, system)
# Lookup order: session → user → system

print(config["color"])  # "blue" (session)
print(config["size"])   # "L" (user, not system)
print(config["font"])   # "Arial" (system)
```

**Mutations - Only Affect First Dict!**
```python
config["new_key"] = "value"
print(session)  # Has new_key
print(user)     # Doesn't have it

config["color"] = "red"
print(session["color"])  # Changed to "red"
```

**Use Case: Scope Resolution (like variable scope)**
```python
# Think: local → global → builtin
builtin = {"max_size": 100, "timeout": 30}
global_cfg = {"max_size": 200}
local_cfg = {"timeout": 5}

scope = ChainMap(local_cfg, global_cfg, builtin)
print(scope["timeout"])   # 5 (local overrides)
print(scope["max_size"])  # 200 (global overrides builtin)
```

**new_child() - Add Temporary Layer**
```python
base_config = {"db": "prod", "debug": False}
config = ChainMap(base_config)

# Temporarily override for function
with_debug = config.new_child({"debug": True})
print(config["debug"])      # False (original)
print(with_debug["debug"])  # True (temporary layer)
```

**Why Not Just Update Dict?**
```python
# Problem with update: permanent, can't easily undo
d = {"a": 1, "b": 2}
d.update({"a": 99})  # Overwrites! Original lost

# ChainMap: non-destructive, preserves layers
base = {"a": 1, "b": 2}
override = {"a": 99}
cm = ChainMap(override, base)
# base["a"] still 1, cm["a"] is 99
```

**Key Properties**
```python
# Access all dicts
print(config.maps)  # List of dicts [session, user, system]

# Remove first map
config = config.parents  # ChainMap(user, system)

# Add new first map
config = config.new_child({"new": "layer"})
```

**When to Use ChainMap vs Dict Merge**

| Use ChainMap when: | Use dict merge when: |
|-------------------|---------------------|
| ✅ Need layered lookups (config hierarchy) | ✅ Need single flat dict |
| ✅ Want to preserve original dicts | ✅ Want snapshot at point in time |
| ✅ Need to modify layers independently | ✅ Don't need layer separation |
| ✅ Memory matters (no copy) | ✅ Simpler logic needed |

**Real Example: Command Line Args + Config + Defaults**
```python
defaults = {"host": "localhost", "port": 8080, "debug": False}
config_file = {"port": 3000}
cli_args = {"debug": True}

# Priority: CLI > Config File > Defaults
final = ChainMap(cli_args, config_file, defaults)

print(final["host"])   # "localhost" (defaults)
print(final["port"])   # 3000 (config_file overrides defaults)
print(final["debug"])  # True (cli_args overrides all)
```

**Gotcha: Deletions Only Affect First Dict**
```python
cm = ChainMap({"a": 1}, {"a": 2, "b": 3})
del cm["a"]  # Removes from first dict only
print(cm["a"])  # 2 (from second dict!)
```

**Summary:**
- **No merge** - references original dicts
- **Lookup chain** - first match wins
- **Mutations** - only first dict affected
- **Use case** - layered configs, scope resolution
- **vs merge** - preserves layers, memory efficient

---

## 🎯 Decision Tree
```
Need a collection?
│
├── Does order matter?
│   │
│   ├── Yes → Mutable?
│   │       ├── Yes → ✅ list
│   │       └── No  → ✅ tuple
│   │
│   └── No → Unique items?
│           ├── Yes → ✅ set
│           └── No  → Key–value pairs?
│                     ├── Yes → ✅ dict
│                     └── No  → ✅ list
```

---

## 🎓 Interview Tricky Questions

### Q1: List Multiplication
```python
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)  # ?
```
**Answer:** `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]` (all rows share same list!)

### Q2: Dict Keys
```python
d = {}
d[[1, 2]] = "value"  # ?
```
**Answer:** TypeError (list not hashable)

### Q3: Set Operations
```python
s = {1, 2, 3}
s.remove(4)  # ?
```
**Answer:** KeyError

```python
s.discard(4)  # ?
```
**Answer:** No error (silent)

### Q4: Tuple Immutability
```python
t = ([1, 2], 3)
t[0].append(3)  # ?
t[0] = [4, 5]   # ?
```
**Answer:** First works, second raises TypeError

---

## ✅ Best Practices

1. **Choose right collection** for the use case
2. **Avoid mutable default arguments**
3. **Use tuple for immutable data**
4. **Use set for membership testing**
5. **Use dict.get() for safe access**
6. **Don't modify during iteration**
7. **Know the time complexity** of operations
8. **Use collections module** for specialized needs

---

## 🔑 Quick Reference

| Operation | list | tuple | set | dict |
|-----------|------|-------|-----|------|
| **Create** | `[1,2]` | `(1,2)` | `{1,2}` | `{"a":1}` |
| **Empty** | `[]` | `()` | `set()` | `{}` |
| **Add** | `.append()` | ❌ | `.add()` | `[key]=val` |
| **Remove** | `.remove()` | ❌ | `.remove()` | `del [key]` |
| **Access** | `[i]` | `[i]` | ❌ | `[key]` |
| **Test** | `in` O(n) | `in` O(n) | `in` O(1) | `in` O(1) |