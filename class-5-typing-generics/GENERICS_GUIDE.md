# Generics in Python

## What are Generics?

**Write code that works with ANY type, while maintaining type safety**

```python
# Without generics - need separate functions
def get_first_int(items: list[int]) -> int:
    return items[0]

def get_first_str(items: list[str]) -> str:
    return items[0]

# With generics - one function for all types!
from typing import TypeVar

T = TypeVar('T')

def get_first(items: list[T]) -> T:
    return items[0]

# Works with any type!
num = get_first([1, 2, 3])      # T = int
name = get_first(["a", "b"])    # T = str
```

---

## Why Generics?

### 1. **Code Reusability**
```python
# Without generics - duplicate code
class IntStack:
    def push(self, item: int): ...
    def pop(self) -> int: ...

class StrStack:
    def push(self, item: str): ...
    def pop(self) -> str: ...

# With generics - one class!
class Stack[T]:
    def push(self, item: T): ...
    def pop(self) -> T: ...
```

### 2. **Type Safety**
```python
from typing import TypeVar

T = TypeVar('T')

def get_first(items: list[T]) -> T:
    return items[0]

# mypy knows return type matches input!
num: int = get_first([1, 2, 3])        # ✓ OK
name: str = get_first(["a", "b"])      # ✓ OK
wrong: int = get_first(["a", "b"])     # ✗ mypy error!
```

### 3. **Flexibility**
```python
# Same function works for any type
data = get_first([1, 2, 3])              # int
person = get_first([user1, user2])       # User object
config = get_first([{"key": "val"}])     # dict
```

---

## Python Generics Evolution

### Old Way (Python < 3.12)
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value
```

### New Way (Python 3.12+)
```python
class Box[T]:
    def __init__(self, value: T):
        self.value = value
```

**We'll show both syntaxes!**

---

## TypeVar Basics

```python
from typing import TypeVar

# Simple TypeVar
T = TypeVar('T')  # Can be any type

# Multiple TypeVars
T = TypeVar('T')
U = TypeVar('U')

def pair(first: T, second: U) -> tuple[T, U]:
    return (first, second)

result = pair(1, "hello")  # tuple[int, str]
```

---

## Generic Functions

### Example 1: Identity Function
```python
from typing import TypeVar

T = TypeVar('T')

def identity(value: T) -> T:
    return value

# T inferred from usage
x = identity(42)        # T = int
y = identity("hello")   # T = str
z = identity([1, 2])    # T = list[int]
```

### Example 2: Get First Element
```python
T = TypeVar('T')

def get_first(items: list[T]) -> T:
    return items[0]

num = get_first([1, 2, 3])        # int
name = get_first(["a", "b"])      # str
```

### Example 3: Swap Function
```python
T = TypeVar('T')

def swap(pair: tuple[T, T]) -> tuple[T, T]:
    return (pair[1], pair[0])

result = swap((1, 2))           # tuple[int, int]
result = swap(("a", "b"))       # tuple[str, str]
```

---

## Generic Classes

### Example 1: Simple Box (Python 3.12+)
```python
class Box[T]:
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value

# Usage
int_box = Box(42)
int_box = Box[int](42)     # Explicit type
num = int_box.get()        # num is int

str_box = Box("hello")
text = str_box.get()       # text is str
```

### Example 2: Stack (Python 3.12+)
```python
class Stack[T]:
    def __init__(self):
        self.items: list[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()
    
    def is_empty(self) -> bool:
        return len(self.items) == 0

# Usage
int_stack = Stack[int]()
int_stack.push(1)
int_stack.push(2)
num = int_stack.pop()  # num is int

str_stack = Stack[str]()
str_stack.push("hello")
text = str_stack.pop()  # text is str
```

### Example 3: Old Syntax (Python < 3.12)
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value
```

---

## Bounded TypeVars (Constraints)

### Example 1: Numeric Only
```python
from typing import TypeVar

# Only int or float allowed
NumT = TypeVar('NumT', int, float)

def add(a: NumT, b: NumT) -> NumT:
    return a + b

result1 = add(1, 2)          # ✓ int
result2 = add(1.5, 2.5)      # ✓ float
# result3 = add("a", "b")    # ✗ mypy error!
```

### Example 2: Upper Bound
```python
from typing import TypeVar

class Animal:
    def speak(self): ...

class Dog(Animal):
    def speak(self): print("Woof")

class Cat(Animal):
    def speak(self): print("Meow")

# T must be Animal or subclass
T = TypeVar('T', bound=Animal)

def make_speak(animal: T) -> T:
    animal.speak()
    return animal

dog = make_speak(Dog())     # ✓ OK
cat = make_speak(Cat())     # ✓ OK
# make_speak("hello")       # ✗ str is not Animal
```

---

## Multiple Type Parameters

```python
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

class Pair[K, V]:
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value
    
    def get_key(self) -> K:
        return self.key
    
    def get_value(self) -> V:
        return self.value

# Usage
pair1 = Pair(1, "one")           # K=int, V=str
pair2 = Pair("name", 42)         # K=str, V=int
pair3 = Pair[str, int]("age", 25)  # Explicit types
```

---

## Generic Functions with Multiple Types

```python
T = TypeVar('T')
U = TypeVar('U')

def map_values(items: list[T], func: Callable[[T], U]) -> list[U]:
    return [func(item) for item in items]

# Usage
nums = [1, 2, 3]
strs = map_values(nums, str)  # list[int] -> list[str]
doubled = map_values(nums, lambda x: x * 2)  # list[int] -> list[int]
```

---

## Comparison with Other Languages

### Java
```java
// Generic class
public class Box<T> {
    private T value;
    
    public Box(T value) {
        this.value = value;
    }
    
    public T get() {
        return value;
    }
}

// Usage
Box<Integer> intBox = new Box<>(42);
Box<String> strBox = new Box<>("hello");
```

### TypeScript
```typescript
// Generic function
function identity<T>(value: T): T {
    return value;
}

// Generic class
class Box<T> {
    constructor(private value: T) {}
    
    get(): T {
        return this.value;
    }
}

// Usage
const intBox = new Box<number>(42);
const strBox = new Box<string>("hello");
```

### C++
```cpp
// Template (C++ generics)
template<typename T>
class Box {
    T value;
public:
    Box(T v) : value(v) {}
    T get() { return value; }
};

// Usage
Box<int> intBox(42);
Box<string> strBox("hello");
```

---

## When to Use Generics

✅ **DO use generics when:**
- Building collections (Stack, Queue, Tree)
- Creating reusable data structures
- Writing utility functions (map, filter, reduce)
- Building frameworks/libraries
- Type varies but behavior same

❌ **DON'T use generics when:**
- Only one type needed
- Different types need different logic
- Over-complicating simple code

---

## Common Patterns

### Pattern 1: Container
```python
class Container[T]:
    def __init__(self):
        self.items: list[T] = []
    
    def add(self, item: T): ...
    def get(self, index: int) -> T: ...
```

### Pattern 2: Result Type
```python
class Result[T, E]:
    def __init__(self, value: T | None, error: E | None):
        self.value = value
        self.error = error
    
    def is_ok(self) -> bool:
        return self.error is None
```

### Pattern 3: Builder
```python
class Builder[T]:
    def __init__(self):
        self.result: T | None = None
    
    def build(self) -> T:
        return self.result
```

---

## Summary

| Feature | Without Generics | With Generics |
|---------|-----------------|---------------|
| Reusability | Low (duplicate code) | High |
| Type Safety | Weak | Strong |
| Flexibility | Limited | High |
| Complexity | Simple | Medium |

**Key Points:**
- Generics = type-safe reusable code
- TypeVar for generic types
- Python 3.12+ has cleaner syntax
- mypy enforces generic constraints
- Similar to Java/C++/TypeScript generics