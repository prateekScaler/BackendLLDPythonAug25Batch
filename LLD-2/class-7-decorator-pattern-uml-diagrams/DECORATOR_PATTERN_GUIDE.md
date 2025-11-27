# The Decorator Pattern

> Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

---

## Part 1: The Real Problem - Coffee Shop Example

You're building a POS system for a coffee shop. Let's see how the problem evolves:

### Day 1: Simple Menu

```python
class Coffee:
    def cost(self):
        return 5.0
    
    def description(self):
        return "Coffee"

# Works fine!
coffee = Coffee()
print(f"{coffee.description()}: ${coffee.cost()}")
```

✅ Simple and clean

---

### Day 2: Add Milk Option

```python
class Coffee:
    def cost(self):
        return 5.0

class CoffeeWithMilk:
    def cost(self):
        return 5.0 + 1.5  # Coffee + Milk

# Now we need 2 classes!
```

⚠️ Starting to duplicate code

---

### Day 3: Add Sugar, Whipped Cream...

```python
class Coffee:
    def cost(self): return 5.0

class CoffeeWithMilk:
    def cost(self): return 6.5

class CoffeeWithSugar:
    def cost(self): return 5.5

class CoffeeWithMilkAndSugar:
    def cost(self): return 7.0

class CoffeeWithMilkAndSugarAndWhippedCream:
    def cost(self): return 9.0

# EXPLOSION OF CLASSES! 💥
```

**The Problem:**
- 3 add-ons = 8 combinations (2³)
- 5 add-ons = 32 combinations (2⁵)
- **Class explosion!**

---

### Attempt 1: Boolean Flags 🤔

"Let's use flags instead!"

```python
class Coffee:
    def __init__(self, has_milk=False, has_sugar=False, 
                 has_whipped=False, has_caramel=False):
        self.has_milk = has_milk
        self.has_sugar = has_sugar
        self.has_whipped = has_whipped
        self.has_caramel = has_caramel
    
    def cost(self):
        total = 5.0
        if self.has_milk:
            total += 1.5
        if self.has_sugar:
            total += 0.5
        if self.has_whipped:
            total += 2.0
        if self.has_caramel:
            total += 1.0
        return total
    
    def description(self):
        desc = "Coffee"
        if self.has_milk: desc += " with Milk"
        if self.has_sugar: desc += " with Sugar"
        # ... more conditionals
        return desc
```

**Problems with flags:**
- ❌ Constructor becomes massive with 10+ add-ons
- ❌ Can't add same add-on twice (double shot espresso?)
- ❌ Violates Open/Closed Principle
- ❌ Hard to price dynamically (seasonal prices)

```python
# Want double milk? Can't do it!
coffee = Coffee(has_milk=True, has_milk=True)  # ❌ Can't repeat

# Want to add new add-on? Modify class!
class Coffee:
    def __init__(self, ..., has_vanilla=False):  # ❌ Modify existing class
```

---

### Attempt 2: Inheritance 🤔

"Let's use inheritance for combinations!"

```python
class Coffee:
    def cost(self): return 5.0

class MilkCoffee(Coffee):
    def cost(self): return super().cost() + 1.5

class SugarMilkCoffee(MilkCoffee):
    def cost(self): return super().cost() + 0.5

# Still need classes for every combination!
```

**Problems:**
- ❌ Still class explosion
- ❌ Static - can't add/remove at runtime
- ❌ Rigid inheritance hierarchy

---

## Part 2: The Insight 💡

**What if we could "wrap" objects with behavior?**

```
Coffee
  └─ wrapped by Milk
      └─ wrapped by Sugar
          └─ wrapped by Whipped Cream

Like [Russian nesting dolls! 🪆](https://www.youtube.com/shorts/SNzAmwOVVTY)
```

**Key Idea:** Each wrapper adds its own cost/description, then delegates to the wrapped object.

---

## Part 3: Decorator Pattern Solution

### Step 1: Component Interface

```python
from abc import ABC, abstractmethod

class Beverage(ABC):
    """Component - the interface"""
    
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass
```

---

### Step 2: Concrete Component

```python
class Coffee(Beverage):
    """Concrete Component - the base object"""
    
    def cost(self) -> float:
        return 5.0
    
    def description(self) -> str:
        return "Coffee"
```

---

### Step 3: Decorator Base Class

```python
class AddOnDecorator(Beverage):
    """Decorator - wraps a Beverage"""
    
    def __init__(self, beverage: Beverage):
        self._beverage = beverage  # Wrap the component
    
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass
```

---

### Step 4: Concrete Decorators

```python
class Milk(AddOnDecorator):
    def cost(self) -> float:
        return self._beverage.cost() + 1.5  # Add milk cost
    
    def description(self) -> str:
        return self._beverage.description() + " + Milk"


class Sugar(AddOnDecorator):
    def cost(self) -> float:
        return self._beverage.cost() + 0.5
    
    def description(self) -> str:
        return self._beverage.description() + " + Sugar"


class WhippedCream(AddOnDecorator):
    def cost(self) -> float:
        return self._beverage.cost() + 2.0
    
    def description(self) -> str:
        return self._beverage.description() + " + Whipped Cream"


class Caramel(AddOnDecorator):
    def cost(self) -> float:
        return self._beverage.cost() + 1.0
    
    def description(self) -> str:
        return self._beverage.description() + " + Caramel"
```

---

### Step 5: Usage - The Magic! ✨

```python
# Simple coffee
coffee = Coffee()
print(f"{coffee.description()}: ${coffee.cost()}")
# Coffee: $5.0

# Coffee with milk
coffee = Coffee()
coffee = Milk(coffee)  # Wrap with Milk
print(f"{coffee.description()}: ${coffee.cost()}")
# Coffee + Milk: $6.5

# Coffee with milk and sugar
coffee = Coffee()
coffee = Milk(coffee)
coffee = Sugar(coffee)  # Wrap again!
print(f"{coffee.description()}: ${coffee.cost()}")
# Coffee + Milk + Sugar: $7.0

# Double milk! (not possible with flags)
coffee = Coffee()
coffee = Milk(coffee)
coffee = Milk(coffee)  # Wrap twice!
print(f"{coffee.description()}: ${coffee.cost()}")
# Coffee + Milk + Milk: $8.0

# Full customization
coffee = Coffee()
coffee = Milk(coffee)
coffee = Sugar(coffee)
coffee = WhippedCream(coffee)
coffee = Caramel(coffee)
print(f"{coffee.description()}: ${coffee.cost()}")
# Coffee + Milk + Sugar + Whipped Cream + Caramel: $10.0
```

**How it works:**

```
coffee.cost() call chain:
Caramel.cost()
  └─ WhippedCream.cost() + 1.0
      └─ Sugar.cost() + 2.0
          └─ Milk.cost() + 0.5
              └─ Coffee.cost() + 1.5
                  └─ return 5.0

5.0 → 6.5 → 7.0 → 9.0 → 10.0 ✅
```

---

## Part 4: UML Diagram

```
┌──────────────────────┐
│   <<interface>>      │
│      Beverage        │
├──────────────────────┤
│ + cost()             │
│ + description()      │
└──────────△───────────┘
           │
    ┌──────┴──────────────────────┐
    │                             │
    ▼                             ▼
┌──────────┐         ┌──────────────────────┐
│  Coffee  │         │   AddOnDecorator     │
├──────────┤         │   (abstract)         │
│+ cost()  │         ├──────────────────────┤
│+ desc()  │         │ - _beverage: Beverage│◄─── Wraps
└──────────┘         │ + cost()             │
                     │ + description()      │
                     └──────────△───────────┘
                                │
                     ┌──────────┼──────────┐
                     ▼          ▼          ▼
              ┌──────────┐ ┌──────────┐ ┌────────┐
              │   Milk   │ │  Sugar   │ │ Whipped│
              ├──────────┤ ├──────────┤ ├────────┤
              │+ cost()  │ │+ cost()  │ │+ cost()│
              └──────────┘ └──────────┘ └────────┘
```

---

## Part 5: Benefits vs Problems

### ✅ Benefits

**1. Open/Closed Principle**
```python
# Add new add-on without modifying existing code
class Vanilla(AddOnDecorator):
    def cost(self):
        return self._beverage.cost() + 0.75
    
    def description(self):
        return self._beverage.description() + " + Vanilla"

# Just use it - no modifications needed!
```

**2. Flexible Combinations**
```python
# Any combination possible
coffee = Coffee()
coffee = Milk(coffee)
coffee = Milk(coffee)  # Double milk
coffee = Sugar(coffee)
coffee = Vanilla(coffee)
# Infinite flexibility!
```

**3. Runtime Composition**
```python
# Build order based on user selection
order = Coffee()
if user.wants_milk:
    order = Milk(order)
if user.wants_sugar:
    order = Sugar(order)
```

**4. Single Responsibility**
```python
# Each decorator does ONE thing
class Milk(AddOnDecorator):
    def cost(self):
        return self._beverage.cost() + 1.5  # Only knows milk price
```

---

### ⚠️ Potential Issues

**1. Many Small Objects**
```python
coffee = Caramel(WhippedCream(Sugar(Milk(Coffee()))))
# Creates 5 objects for one coffee!
```

**2. Order Matters (Sometimes)**
```python
# Discounts before or after tax?
price = Tax(Discount(Item()))     # Different from
price = Discount(Tax(Item()))     # this!
```

**3. Identity Checks Fail**
```python
coffee = Coffee()
decorated = Milk(coffee)

isinstance(decorated, Coffee)  # False! It's Milk
# Decorator hides the original type
```

---

## Part 6: Real-World Use Cases

### 1. I/O Streams (Classic Example)

```python
# Python file handling
file = open("data.txt")                    # Base
file = BufferedReader(file)                # Add buffering
file = GzipDecompressor(file)              # Add decompression
file = CharacterDecoder(file, "utf-8")     # Add decoding

# Each layer adds functionality!
```

**Java equivalent:**
```java
InputStream file = new FileInputStream("data.txt");
file = new BufferedInputStream(file);
file = new GZIPInputStream(file);
```

---

### 2. Web Request/Response Middleware

```python
class HttpHandler:
    def handle(self, request):
        return "Response"

class LoggingDecorator(HttpHandler):
    def __init__(self, handler):
        self._handler = handler
    
    def handle(self, request):
        print(f"Request: {request}")
        response = self._handler.handle(request)
        print(f"Response: {response}")
        return response

class AuthDecorator(HttpHandler):
    def __init__(self, handler):
        self._handler = handler
    
    def handle(self, request):
        if not request.is_authenticated():
            return "401 Unauthorized"
        return self._handler.handle(request)

# Stack decorators
handler = HttpHandler()
handler = AuthDecorator(handler)
handler = LoggingDecorator(handler)
handler.handle(request)
```

**Real frameworks:**
- Express.js middleware
- Django middleware
- Flask decorators

---

### 3. Text Formatting

```python
class Text:
    def __init__(self, content):
        self.content = content
    
    def render(self):
        return self.content

class BoldDecorator:
    def __init__(self, text):
        self._text = text
    
    def render(self):
        return f"<b>{self._text.render()}</b>"

class ItalicDecorator:
    def __init__(self, text):
        self._text = text
    
    def render(self):
        return f"<i>{self._text.render()}</i>"

# Usage
text = Text("Hello")
text = BoldDecorator(text)
text = ItalicDecorator(text)
print(text.render())  # <i><b>Hello</b></i>
```

---

### 4. Notification System

```python
class Notifier:
    def send(self, message):
        print(f"Sending: {message}")

class SMSDecorator:
    def __init__(self, notifier):
        self._notifier = notifier
    
    def send(self, message):
        self._notifier.send(message)
        print(f"SMS: {message}")

class EmailDecorator:
    def __init__(self, notifier):
        self._notifier = notifier
    
    def send(self, message):
        self._notifier.send(message)
        print(f"Email: {message}")

class SlackDecorator:
    def __init__(self, notifier):
        self._notifier = notifier
    
    def send(self, message):
        self._notifier.send(message)
        print(f"Slack: {message}")

# Multi-channel notification
notifier = Notifier()
notifier = SMSDecorator(notifier)
notifier = EmailDecorator(notifier)
notifier = SlackDecorator(notifier)
notifier.send("Server down!")
# Sends via SMS, Email, and Slack!
```

---

### 5. Caching & Performance

```python
class DataSource:
    def get_data(self):
        # Expensive database call
        return fetch_from_db()

class CachingDecorator:
    def __init__(self, source):
        self._source = source
        self._cache = {}
    
    def get_data(self):
        if "data" not in self._cache:
            self._cache["data"] = self._source.get_data()
        return self._cache["data"]

class LoggingDecorator:
    def __init__(self, source):
        self._source = source
    
    def get_data(self):
        print("Fetching data...")
        data = self._source.get_data()
        print(f"Got {len(data)} records")
        return data

# Add caching and logging
source = DataSource()
source = CachingDecorator(source)
source = LoggingDecorator(source)
```

---

## Part 7: Python-Specific - @decorator

Python's `@decorator` syntax is Decorator pattern!

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    return wrapper

@log_calls
def greet(name):
    print(f"Hello, {name}")

# Equivalent to:
# greet = log_calls(greet)

greet("Alice")
# Calling greet
# Hello, Alice
# Done greet
```

**Function decorators ARE the Decorator pattern!**

---

## Part 8: When to Use Decorator

### ✅ Use Decorator When:

| Situation | Example |
|-----------|---------|
| Add responsibilities dynamically | Logging, caching |
| Multiple optional features | Coffee add-ons, text formatting |
| Avoid subclass explosion | N features = 2ᴺ subclasses |
| Compose behavior at runtime | User-selected options |
| Single Responsibility Principle | Each decorator does one thing |

---

### ❌ Don't Use When:

| Situation | Use Instead |
|-----------|-------------|
| Need to remove decorators | Strategy (swap algorithm) |
| Order doesn't matter | Separate objects |
| Few combinations (2-3) | Simple inheritance |
| Need type checking | Inheritance |

---

## Part 9: Decorator vs Similar Patterns

### Decorator vs Proxy

**Decorator:** Adds behavior
```python
original = RealObject()
decorated = Decorator(original)  # Adds logging, caching
```

**Proxy:** Controls access
```python
original = RealObject()
proxy = Proxy(original)  # Access control, lazy loading
```

---

### Decorator vs Strategy

**Decorator:** Stacks (multiple wrappers)
```python
obj = Component()
obj = DecoratorA(obj)
obj = DecoratorB(obj)  # Stack them!
```

**Strategy:** Swaps (one algorithm)
```python
obj = Context()
obj.set_strategy(StrategyA())  # Choose one
obj.set_strategy(StrategyB())  # Swap
```

---

### Decorator vs Adapter

**Decorator:** Same interface
```python
class Coffee:
    def cost(self): pass

class Milk(Coffee):  # Same interface
    def cost(self): pass
```

**Adapter:** Different interfaces
```python
class OldAPI:
    def old_method(self): pass

class Adapter:
    def new_method(self):  # Different interface
        self.old_api.old_method()
```

---

## Part 10: Quick Reference

```python
# Pattern Structure
class Component(ABC):
    @abstractmethod
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        return "Base"

class Decorator(Component):
    def __init__(self, component):
        self._component = component
    
    @abstractmethod
    def operation(self):
        pass

class ConcreteDecorator(Decorator):
    def operation(self):
        return f"Decorated({self._component.operation()})"

# Usage
obj = ConcreteComponent()
obj = ConcreteDecorator(obj)
obj.operation()  # "Decorated(Base)"
```

---

## Summary

**The Journey:**
1. Started with class explosion
2. Tried flags → rigid
3. Tried inheritance → still explosion
4. **Decorator:** Wrap objects dynamically ✅

**Key Insight:** Composition over inheritance - build functionality by wrapping, not subclassing.

**Real Power:** Add/remove responsibilities at runtime without modifying code.

**Remember:** Like Russian nesting dolls 🪆 - each layer adds something, then delegates to the inner doll!