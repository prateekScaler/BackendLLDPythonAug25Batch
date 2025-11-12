# SOLID Principles - Quick Reference

## 📋 Summary Table

| Principle | Definition | Key Benefit |
|-----------|-----------|-------------|
| **S**RP | One class, one reason to change | Easy to understand & maintain |
| **O**CP | Open for extension, closed for modification | Add features without breaking existing |
| **L**SP | Subtypes must be substitutable for base types | Polymorphism works correctly |
| **I**SP | Many specific interfaces > one general | Clients get only what they need |
| **D**IP | Depend on abstractions, not concretions | Flexible, decoupled, testable |

---

## 🎯 Quick Decision Guide

```
Adding new feature? 
  → Use OCP (extend, don't modify)

Class doing too much?
  → Apply SRP (split responsibilities)

Subclass breaking parent behavior?
  → Fix LSP (proper abstraction)

Forced to implement unused methods?
  → Apply ISP (split interface)

Hard to test or swap implementations?
  → Apply DIP (inject dependencies)
```

---

## 🚩 Violation Checklist

### SRP Violations:
- [ ] Class name has "Manager", "Handler", "Util"
- [ ] Methods do unrelated things
- [ ] Many import statements
- [ ] Long methods
- [ ] Multiple reasons to change

### OCP Violations:
- [ ] Growing if/elif chains
- [ ] Type checking (isinstance)
- [ ] Switch on type
- [ ] Must modify class to add feature

### LSP Violations:
- [ ] Subclass throws exceptions parent doesn't
- [ ] Empty/stub implementations
- [ ] Tightened preconditions
- [ ] Weakened postconditions
- [ ] Using isinstance to handle subclasses

### ISP Violations:
- [ ] Empty method implementations
- [ ] NotImplementedError in concrete class
- [ ] Clients use only part of interface
- [ ] Large interface with many methods

### DIP Violations:
- [ ] `new` in constructor
- [ ] Import concrete classes
- [ ] Hard-coded configurations
- [ ] Can't test with mocks

---

## ✅ Application Patterns

### SRP Pattern:
```python
# Bad: God class
class User:
    def validate(self): ...
    def save_to_db(self): ...
    def send_email(self): ...

# Good: Separated
class User: ...
class UserValidator: ...
class UserRepository: ...
class UserNotifier: ...
```

### OCP Pattern:
```python
# Bad: Modify for new types
def process(type):
    if type == "A": ...
    elif type == "B": ...

# Good: Extend with new classes
class Handler(ABC):
    @abstractmethod
    def process(self): pass

class HandlerA(Handler): ...
class HandlerB(Handler): ...
```

### LSP Pattern:
```python
# Bad: Square breaks Rectangle
class Rectangle:
    def set_width(self, w): ...

class Square(Rectangle):
    def set_width(self, w):
        # Breaks parent behavior
        self.width = self.height = w

# Good: Separate hierarchies
class Shape(ABC): ...
class Rectangle(Shape): ...
class Square(Shape): ...
```

### ISP Pattern:
```python
# Bad: Fat interface
class Worker(ABC):
    @abstractmethod
    def work(self): pass
    @abstractmethod
    def eat(self): pass

# Good: Segregated
class Workable(ABC):
    @abstractmethod
    def work(self): pass

class Eatable(ABC):
    @abstractmethod
    def eat(self): pass
```

### DIP Pattern:
```python
# Bad: Direct dependency
class Service:
    def __init__(self):
        self.db = MySQLDatabase()

# Good: Inject abstraction
class Service:
    def __init__(self, db: Database):
        self.db = db
```

---

## 🎓 When to Apply

| Principle | When | When Not |
|-----------|------|----------|
| **SRP** | Class has multiple concerns | Simple data classes |
| **OCP** | Variation points identified | Only 2 variations |
| **LSP** | Using inheritance | Composition is better |
| **ISP** | Large interfaces | Cohesive methods |
| **DIP** | External dependencies | Language built-ins |

---

## 🔧 Common Mistakes

1. **Over-engineering** - Don't apply SOLID to everything
2. **Premature abstraction** - Wait for actual variations
3. **Too many layers** - Balance with pragmatism
4. **Ignoring context** - Simple scripts don't need SOLID
5. **Following blindly** - Understand the "why"

---

## 💡 Key Principles

### The Goal:
- **Maintainable** - Easy to change
- **Testable** - Easy to verify
- **Flexible** - Easy to extend
- **Understandable** - Easy to read

### The Balance:
- Apply when building long-term systems
- Skip for throwaway code
- Start simple, refactor when needed
- Favor readability over perfection

---

## 🎯 Quick Tests

**SRP Test:** How many reasons to change?
- Answer should be: One

**OCP Test:** Can I add features without modifying?
- Answer should be: Yes

**LSP Test:** Can I replace parent with child?
- Answer should be: Yes, without breaking

**ISP Test:** Do clients use all methods?
- Answer should be: Yes

**DIP Test:** Can I test with mocks?
- Answer should be: Yes, easily

---

## 📚 Further Reading

- **Clean Architecture** by Robert C. Martin
- **Design Patterns** by Gang of Four
- **Refactoring** by Martin Fowler

---

## 🚀 Getting Started

1. **Start with SRP** - Break apart god classes
2. **Add OCP** - When variations emerge
3. **Check LSP** - When using inheritance
4. **Apply ISP** - When interfaces grow
5. **Use DIP** - For testability

**Remember:** SOLID is about managing complexity, not creating it!