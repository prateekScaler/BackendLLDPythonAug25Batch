# Template Method Pattern - Quick Guide

> Define the skeleton of an algorithm, letting subclasses override specific steps without changing the algorithm's structure.

---

## The Problem

```python
class PDFReport:
    def generate(self):
        self.open_file()
        self.add_header()
        self.add_content()
        self.add_footer()
        self.save()

class ExcelReport:
    def generate(self):
        self.open_file()      # Same!
        self.add_header()     # Same!
        self.add_content()    # Different
        self.add_footer()     # Same!
        self.save()           # Same!
```

❌ Duplicate algorithm structure in every class
❌ Hard to maintain consistent flow

---

## The Solution

```python
class Report(ABC):
    def generate(self):  # ← Template Method
        self.open_file()
        self.add_header()
        self.add_content()      # ← Hook (varies)
        self.add_footer()
        self.save()
    
    def open_file(self):
        print("Opening file...")
    
    def add_header(self):
        print("Adding header...")
    
    @abstractmethod
    def add_content(self):  # ← Must override
        pass
    
    def add_footer(self):
        print("Adding footer...")
    
    def save(self):
        print("Saving file...")

class PDFReport(Report):
    def add_content(self):
        print("Adding PDF content...")

class ExcelReport(Report):
    def add_content(self):
        print("Adding Excel content...")
```

---

## Structure

```
┌─────────────────────────────┐
│    AbstractClass            │
│  ─────────────────────────  │
│  + templateMethod()         │◄─── Algorithm skeleton (final)
│    ├─ step1()               │
│    ├─ step2() [abstract]    │◄─── Varies by subclass
│    └─ step3()               │
│  ─────────────────────────  │
│  # step1()                  │◄─── Common implementation
│  # step2() [abstract]       │
│  # step3()                  │◄─── Common implementation
└─────────────────────────────┘
         △
    ┌────┴────┐
    ▼         ▼
ConcreteA  ConcreteB
override   override
step2()    step2()
```

---

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Template Method** | Defines algorithm skeleton | `generate()` |
| **Primitive Operations** | Steps that vary | `add_content()` |
| **Hook Methods** | Optional override points | `before_save()` |
| **Common Operations** | Shared steps | `add_header()` |

---

## Template Method in Other Patterns

### 1. Factory Method ⭐ Most Common

```python
class NotificationService(ABC):
    @abstractmethod
    def create_notification(self):  # ← Factory (varies)
        pass
    
    def send(self, message):  # ← Template Method
        notif = self.create_notification()
        notif.validate()
        notif.deliver(message)
        notif.log()

# Structure:
Template: send()
├─ create_notification() [varies]
├─ validate() [common]
├─ deliver() [common]
└─ log() [common]
```

**Why:** Template defines notification flow, factory provides the notification type

---

### 2. Strategy Pattern (Inverse Relationship)

```python
# Strategy: Algorithm varies, context stays same
class Context:
    def execute(self):
        result = self.strategy.algorithm()  # ← Strategy varies
        return result

# Template: Structure fixed, steps vary
class Algorithm(ABC):
    def execute(self):  # ← Template (fixed)
        self.step1()
        self.step2()  # ← Step varies
```

**Difference:**
- **Template:** Skeleton fixed, steps vary (inheritance)
- **Strategy:** Entire algorithm varies (composition)

---

### 3. Builder Pattern

```python
class DocumentBuilder(ABC):
    def build(self):  # ← Template Method
        self.create_document()
        self.add_header()
        self.add_content()  # ← Varies
        self.add_footer()
        return self.document
    
    @abstractmethod
    def add_content(self):
        pass

# Structure:
Template: build()
├─ create_document() [common]
├─ add_header() [common]
├─ add_content() [varies]
└─ add_footer() [common]
```

**Why:** Template ensures consistent build sequence

---

## Comparison Table

| Pattern | Uses Template? | How? |
|---------|---------------|------|
| **Factory Method** | ✅ Always | Template orchestrates, factory creates |
| **Builder** | ✅ Often | Template defines build sequence |
| **Strategy** | ❌ Opposite | Strategy IS the algorithm, not skeleton |
| **Abstract Factory** | ⚠️ Sometimes | Template coordinates multiple factories |
| **Adapter** | ❌ No | Just converts interface |
| **Prototype** | ❌ No | Just clones objects |
| **Singleton** | ❌ No | Just controls instantiation |

---

## Real-World Examples

### 1. Testing Framework

```python
class TestCase(ABC):
    def run(self):  # ← Template
        self.setUp()
        try:
            self.test()  # ← Varies
        finally:
            self.tearDown()
    
    def setUp(self):
        pass  # Hook
    
    @abstractmethod
    def test(self):
        pass
    
    def tearDown(self):
        pass  # Hook
```

---

### 2. Game AI

```python
class AIController(ABC):
    def take_turn(self):  # ← Template
        self.assess_situation()
        action = self.choose_action()  # ← Varies
        self.execute_action(action)
        self.update_state()
    
    @abstractmethod
    def choose_action(self):
        pass
```

---

### 3. Data Processing Pipeline

```python
class DataProcessor(ABC):
    def process(self, data):  # ← Template
        loaded = self.load(data)
        validated = self.validate(loaded)
        transformed = self.transform(validated)  # ← Varies
        self.save(transformed)
    
    @abstractmethod
    def transform(self, data):
        pass
```

---

## When to Use Template Method

✅ **Use when:**
- Multiple classes share same algorithm structure
- Want to avoid code duplication
- Need to enforce algorithm steps
- Want to control which steps can vary

❌ **Don't use when:**
- Each class needs completely different algorithm
- Only one concrete implementation
- Steps are too granular (too many hooks)

---

## Template vs Strategy - Quick Decision

```
Do subclasses share algorithm STRUCTURE?
│
├─ Yes → Template Method
│         (inherit, override steps)
│
└─ No → Strategy
        (compose, swap algorithms)
```

**Example:**

```python
# Template: Structure same, steps vary
class Sorter(ABC):
    def sort(self, data):
        self.prepare(data)
        self.do_sort(data)  # ← Varies (quicksort, mergesort)
        self.cleanup(data)

# Strategy: Entire algorithm varies
class Sorter:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def sort(self, data):
        return self.strategy.sort(data)  # ← Entire algorithm
```

---

## Quick Reference

```python
# Template Method Pattern
class AbstractClass(ABC):
    def template_method(self):       # Public, called by client
        self.common_step1()
        self.required_step()         # Subclass must implement
        self.hook()                  # Subclass may override
        self.common_step2()
    
    def common_step1(self):
        pass  # Default implementation
    
    @abstractmethod
    def required_step(self):
        pass  # Must override
    
    def hook(self):
        pass  # Optional override
    
    def common_step2(self):
        pass  # Default implementation
```

---

## Key Principles

1. **Hollywood Principle:** "Don't call us, we'll call you"
   - Parent calls child's methods, not vice versa

2. **Inversion of Control:**
   - Framework controls flow, not subclass

3. **Open/Closed:**
   - Algorithm open for extension (override steps)
   - Algorithm closed for modification (skeleton fixed)

---

## Summary

**Template Method is the skeleton behind:**
- ✅ Factory Method (always)
- ✅ Builder (often)
- ⚠️ Abstract Factory (sometimes)
- ❌ Strategy (opposite concept)

**Key Insight:** Template Method + Factory Method = Most common creational pattern combo