# Design Patterns - Introduction

## 📜 What are Design Patterns?

**Definition:** Proven solutions to recurring design problems in software.

**Created by:** Gang of Four (GoF) - 1994 book "Design Patterns"

**Not:** Code to copy-paste  
**But:** Templates for solving common problems

---

## 🎯 Why Design Patterns?

### Without Patterns:
```python
# Reinventing the wheel every time
# Inconsistent solutions
# Hard to communicate designs
# No shared vocabulary
```

### With Patterns:
```python
# Proven solutions
# Common vocabulary ("Let's use a Singleton")
# Best practices encoded
# Easier maintenance
```

---

## 📚 Three Types of Patterns

### 1. **Creational Patterns** - Object Creation
**Problem:** How to create objects flexibly?

| Pattern | Purpose | Example |
|---------|---------|---------|
| **Singleton** | One instance only | Database connection pool |
| Factory | Create objects without specifying exact class | Different database drivers |
| Builder | Construct complex objects step-by-step | Query builder |
| Prototype | Clone existing objects | Copy configurations |

**Common thread:** Control and flexibility in object creation

---

### 2. **Structural Patterns** - Object Composition
**Problem:** How to compose objects into larger structures?

| Pattern | Purpose | Example |
|---------|---------|---------|
| Adapter | Make incompatible interfaces work together | Legacy API wrapper |
| Decorator | Add behavior without modifying | Logging, caching |
| Facade | Simplified interface to complex system | Library wrapper |
| Proxy | Control access to object | Lazy loading, access control |

**Common thread:** Relationships between objects

---

### 3. **Behavioral Patterns** - Object Interaction
**Problem:** How should objects communicate and distribute responsibility?

| Pattern | Purpose | Example |
|---------|---------|---------|
| Strategy | Swap algorithms at runtime | Payment methods |
| Observer | Notify multiple objects of changes | Event system |
| Command | Encapsulate request as object | Undo/redo |
| Iterator | Sequential access without exposing structure | Custom collections |

**Common thread:** Communication between objects

---

## 🎯 Quick Comparison

```
Creational:  "How do I CREATE this?"
Structural:  "How do I COMPOSE this?"
Behavioral:  "How do these COMMUNICATE?"
```

---

## 💡 When to Use Patterns?

### ✅ Use when:
- Problem is common and well-understood
- Pattern fits naturally
- Team knows the pattern
- Long-term maintainability matters

### ❌ Don't use when:
- Simple problem doesn't need it
- Forcing pattern where it doesn't fit
- Team unfamiliar (adds complexity)
- Over-engineering

**Remember:** Patterns are tools, not rules!

---

## 🚀 Learning Path

**Today:** Singleton (Creational)
- Most commonly used
- Simplest to understand
- Good introduction to patterns

**Next:** Other patterns as needed in projects

---

## 📊 Pattern Frequency (Real-world)

```
Most Used:
  ★★★★★ Singleton, Factory, Observer, Strategy
  ★★★★☆ Decorator, Adapter
  ★★★☆☆ Builder, Command
  ★★☆☆☆ Others

Start with the most common!
```

---

## 🎓 Key Takeaway

**Design patterns are:**
- Vocabulary for developers
- Proven solutions
- Not code, but concepts
- Tools, not dogma

**Let's start with Singleton! 🎯**