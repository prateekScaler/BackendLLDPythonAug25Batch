# Copy Constructors in Python

## 🎯 What is a Copy Constructor?

**A method that creates a new object as a copy of an existing object**

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    # Copy constructor
    def __init__(self, other):
        self.name = other.name
        self.age = other.age
```

**Problem:** Python doesn't have multiple constructors!

---

## ❌ What is NOT a Copy

```python
person1 = Person("Alice", 25)
person2 = person1  # NOT a copy! Same object, different name

person2.age = 30
print(person1.age)  # 30 (both changed!)

# Both point to same object in memory
print(id(person1) == id(person2))  # True
```

**Key:** Assignment creates a **reference**, not a copy

---

## 📊 Types of Copying

```
┌─────────────────────────────────────┐
│         Original Object             │
│  ┌─────────┐      ┌──────────┐    │
│  │  name   │      │  address │──┐  │
│  │ "Alice" │      │  (obj)   │  │  │
│  └─────────┘      └──────────┘  │  │
└──────────────────────────────────┼──┘
                                   │
┌──────────────────────────────────▼──┐
│            Address Object            │
│  ┌─────────┐      ┌──────────┐     │
│  │  city   │      │  "NYC"   │     │
│  └─────────┘      └──────────┘     │
└─────────────────────────────────────┘

Reference:      Both variables → Same object
Shallow Copy:   New object → Same nested objects
Deep Copy:      New object → New nested objects (all levels)
```

---

## 🔴 The Problem: Mutable Objects

```python
class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades  # List is mutable!

student1 = Student("Alice", [90, 85, 95])
student2 = student1  # Reference

student2.grades.append(100)
print(student1.grades)  # [90, 85, 95, 100] 😱
# student1 affected!
```

**Issue:** Shared mutable state leads to bugs

---

## 🟡 Shallow Copy

**Creates new object, but copies references to nested objects**

```python
import copy

class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades

student1 = Student("Alice", [90, 85, 95])
student2 = copy.copy(student1)  # Shallow copy

# Different objects
print(id(student1) == id(student2))  # False

# But share same list!
student2.grades.append(100)
print(student1.grades)  # [90, 85, 95, 100] 😱
```

**Problem:** Nested mutable objects still shared

---

## 🟢 Deep Copy

**Creates new object AND recursively copies all nested objects**

```python
import copy

student1 = Student("Alice", [90, 85, 95])
student2 = copy.deepcopy(student1)  # Deep copy

# Different objects
print(id(student1) == id(student2))  # False

# Different lists!
print(id(student1.grades) == id(student2.grades))  # False

student2.grades.append(100)
print(student1.grades)  # [90, 85, 95] ✅
print(student2.grades)  # [90, 85, 95, 100] ✅
```

**Solution:** Complete independence

---

## 🔧 Implementing Copy Methods

### Method 1: Using `copy` module

```python
import copy

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def shallow_copy(self):
        return copy.copy(self)
    
    def deep_copy(self):
        return copy.deepcopy(self)
```

### Method 2: Manual `__copy__` and `__deepcopy__`

```python
import copy

class Person:
    def __init__(self, name, friends):
        self.name = name
        self.friends = friends
    
    def __copy__(self):
        """Called by copy.copy()"""
        return Person(self.name, self.friends)  # Shallow
    
    def __deepcopy__(self, memo):
        """Called by copy.deepcopy()"""
        return Person(
            copy.deepcopy(self.name, memo),
            copy.deepcopy(self.friends, memo)
        )
```

### Method 3: Custom Copy Constructor Pattern

```python
class Person:
    def __init__(self, name=None, age=None, other=None):
        if other:  # Copy constructor
            self.name = other.name
            self.age = other.age
            self.friends = other.friends.copy()  # Shallow copy list
        else:  # Normal constructor
            self.name = name
            self.age = age
            self.friends = []
    
    @classmethod
    def from_person(cls, other):
        """Alternative: class method"""
        new = cls(other.name, other.age)
        new.friends = other.friends.copy()
        return new
```

---

## 💣 Common Pitfalls

### Pitfall 1: Forgetting Nested Objects

```python
class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members
    
    def copy(self):
        # WRONG: Shares members list!
        return Team(self.name, self.members)
    
    def correct_copy(self):
        # RIGHT: Copies list
        return Team(self.name, self.members.copy())
```

### Pitfall 2: Circular References

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# Circular reference
node1 = Node(1)
node2 = Node(2)
node1.next = node2
node2.next = node1  # Circular!

# copy.copy() works fine
# copy.deepcopy() handles this automatically!
node1_copy = copy.deepcopy(node1)  # Uses memo dict
```

### Pitfall 3: Copying Singleton Objects

```python
class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __deepcopy__(self, memo):
        # Return same instance (don't copy singleton!)
        return self
```

---

## 🎯 When to Use Each

```
┌─────────────────────────────────────────────┐
│           Decision Tree                      │
└─────────────────────────────────────────────┘

Need independent copy?
├─ No  → Use reference (obj2 = obj1)
└─ Yes → Has nested mutable objects?
         ├─ No  → Shallow copy (copy.copy())
         └─ Yes → Want nested objects independent?
                  ├─ No  → Shallow copy
                  └─ Yes → Deep copy (copy.deepcopy())
```

| Scenario | Use |
|----------|-----|
| **Just a reference** | `obj2 = obj1` |
| **Simple objects** | `copy.copy()` |
| **Nested mutables** | `copy.deepcopy()` |
| **Custom logic** | Implement `__copy__` |

---

## 📝 Real-World Examples

### Example 1: Game Character

```python
import copy

class Character:
    def __init__(self, name, health, inventory):
        self.name = name
        self.health = health
        self.inventory = inventory  # List of items
    
    def save_state(self):
        """Save game state"""
        return copy.deepcopy(self)  # Complete copy
    
    def restore_state(self, saved):
        """Load game state"""
        self.__dict__ = copy.deepcopy(saved.__dict__)

# Usage
player = Character("Hero", 100, ["sword", "potion"])
checkpoint = player.save_state()

player.health = 10  # Player takes damage
player.inventory.remove("potion")

player.restore_state(checkpoint)  # Restore!
```

### Example 2: Configuration Object

```python
class Config:
    def __init__(self):
        self.settings = {
            "theme": "dark",
            "notifications": True,
            "plugins": ["spellcheck", "format"]
        }
    
    def get_test_config(self):
        """Get config for testing without affecting original"""
        test_config = copy.deepcopy(self)
        test_config.settings["database"] = "test_db"
        return test_config
```

### Example 3: Undo/Redo System

```python
class Document:
    def __init__(self, content):
        self.content = content
        self.history = []
    
    def save_state(self):
        """Save for undo"""
        self.history.append(copy.deepcopy(self.content))
    
    def undo(self):
        if self.history:
            self.content = self.history.pop()
```

---

## 🎓 Interview Questions

### Q1: What's the output?

```python
class Box:
    def __init__(self, items):
        self.items = items

box1 = Box([1, 2, 3])
box2 = box1
box3 = copy.copy(box1)

box2.items.append(4)
box3.items.append(5)

print(box1.items)  # ?
```

**Answer:** `[1, 2, 3, 4, 5]`
- box2 is reference (same object)
- box3 is shallow copy (shares items list)

### Q2: Deep vs Shallow?

```python
import copy

x = [[1, 2], [3, 4]]
y = copy.copy(x)
z = copy.deepcopy(x)

y[0].append(99)
z[0].append(88)

print(x[0])  # ?
```

**Answer:** `[1, 2, 99]`
- y is shallow (shares nested lists)
- z is deep (independent nested lists)

### Q3: Custom __copy__

```python
class Person:
    def __init__(self, name):
        self.name = name
        self.friends = []
    
    def __copy__(self):
        new = Person(self.name)
        new.friends = self.friends  # Reference!
        return new

p1 = Person("Alice")
p1.friends.append("Bob")
p2 = copy.copy(p1)
p2.friends.append("Charlie")

print(len(p1.friends))  # ?
```

**Answer:** `2` (Both share friends list)

---

## ✅ Best Practices

1. **Default to deepcopy** for safety with nested objects
2. **Implement `__copy__` and `__deepcopy__`** for custom behavior
3. **Document** whether methods modify in-place or return copies
4. **Test** copying behavior in unit tests
5. **Be aware** of performance (deepcopy is expensive)
6. **Handle** circular references with memo dict
7. **Consider** immutable objects (don't need copying)

---

## 🔑 Key Takeaways

- **Assignment** = Reference (same object)
- **Shallow Copy** = New object, shared nested objects
- **Deep Copy** = Completely independent copy
- **Use** `copy.copy()` for shallow, `copy.deepcopy()` for deep
- **Implement** `__copy__` and `__deepcopy__` for custom logic
- **Beware** of mutable nested objects
- **Test** copying behavior to avoid bugs