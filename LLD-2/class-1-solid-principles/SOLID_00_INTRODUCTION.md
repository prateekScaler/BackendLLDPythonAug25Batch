# SOLID Principles in Python

## 📜 Brief History

**Created by:** Robert C. Martin (Uncle Bob) in early 2000s  
**Published in:** "Design Principles and Design Patterns" (2000)  
**Acronym coined by:** Michael Feathers

**Why SOLID?** Software was becoming unmaintainable - changes broke everything, testing was hard, code was rigid.

**Goal:** Create flexible, maintainable, testable code that handles change gracefully.

---

## 🎯 What is SOLID?

Five design principles for object-oriented programming:

- **S** - Single Responsibility Principle
- **O** - Open/Closed Principle
- **L** - Liskov Substitution Principle
- **I** - Interface Segregation Principle
- **D** - Dependency Inversion Principle

---

## ❓ Setting the Premise - Design Quiz

### Question 1: User Notification System

**Which design is better?**

**Option A:**
```python
class UserManager:
    def create_user(self, email, password):
        # Validate email
        if "@" not in email:
            raise ValueError("Invalid email")
        
        # Hash password
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        # Save to database
        db.execute("INSERT INTO users VALUES (?, ?)", email, hashed)
        
        # Send welcome email
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.send_message(f"Welcome {email}!")
        
        # Log activity
        logging.info(f"User {email} created")
```

**Option B:**
```python
class UserManager:
    def __init__(self, db, emailer, logger):
        self.db = db
        self.emailer = emailer
        self.logger = logger
    
    def create_user(self, email, password):
        user = User(email, password)
        self.db.save(user)
        self.emailer.send_welcome(user)
        self.logger.log(f"User {email} created")
```

<details>
<summary>Answer</summary>

**Option B is better**

**Why:**
- Separated concerns (validation, storage, notification)
- Dependencies injected (testable)
- Easy to change email provider or database
- Clear responsibilities

**Option A problems:**
- Does too much (validation, hashing, DB, email, logging)
- Hard to test (needs real SMTP, DB)
- Can't change email provider without modifying class
- Violates Single Responsibility Principle
</details>

---

### Question 2: Payment Processing

**Which design is better?**

**Option A:**
```python
class PaymentProcessor:
    def process(self, amount, method):
        if method == "credit_card":
            # Process credit card
            return self._process_credit_card(amount)
        elif method == "paypal":
            # Process PayPal
            return self._process_paypal(amount)
        elif method == "crypto":
            # Process crypto
            return self._process_crypto(amount)
        # Add new payment method? Modify this class!
```

**Option B:**
```python
class PaymentProcessor:
    def process(self, payment_method, amount):
        return payment_method.process(amount)

class CreditCardPayment:
    def process(self, amount):
        # Process credit card
        pass

class PayPalPayment:
    def process(self, amount):
        # Process PayPal
        pass

# Add new payment? Just create new class!
```

<details>
<summary>Answer</summary>

**Option B is better**

**Why:**
- Open for extension (add new payment methods)
- Closed for modification (no need to change existing code)
- Each payment method independent
- Easy to add crypto, bank transfer, etc.

**Option A problems:**
- Must modify class to add new payment method
- Growing if/elif chain
- Violates Open/Closed Principle
</details>

---

### Question 3: Shape Area Calculator

**Which design is better?**

**Option A:**
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)
    
    def set_width(self, width):
        self.width = width
        self.height = width  # Couple width and height
    
    def set_height(self, height):
        self.width = height
        self.height = height

def process(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.width * rect.height == 20  # Fails for Square!
```

**Option B:**
```python
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, size):
        self.size = size
    
    def area(self):
        return self.size * self.size
```

<details>
<summary>Answer</summary>

**Option B is better**

**Why:**
- Square doesn't pretend to be a Rectangle
- Each shape handles its own area calculation
- Can substitute any Shape without breaking
- No unexpected behavior

**Option A problems:**
- Square breaks Rectangle's behavior
- Caller can't trust parent class behavior
- Violates Liskov Substitution Principle
</details>

---

## 🎯 The Evolving Example: E-commerce Order System

We'll use an **order processing system** that evolves through each SOLID principle.

### Initial Problem (Bad Design)

```python
class Order:
    def __init__(self, items):
        self.items = items
        self.status = "pending"
    
    def calculate_total(self):
        total = sum(item.price for item in self.items)
        
        # Apply discount
        if len(self.items) > 5:
            total *= 0.9
        
        # Add tax
        total *= 1.1
        
        # Save to database
        db.execute("UPDATE orders SET total=?", total)
        
        # Send email
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.send(f"Order total: ${total}")
        
        # Log
        print(f"Order processed: ${total}")
        
        return total
```

**Problems:**
- Does too much (calculation, DB, email, logging)
- Hard to test
- Can't change email provider
- Can't add new discount rules
- Tightly coupled

**We'll fix this step-by-step with SOLID principles!**

---

## 📋 SOLID Principles Overview

| Principle | Purpose | Key Benefit |
|-----------|---------|-------------|
| **SRP** | One class, one reason to change | Easy to understand & maintain |
| **OCP** | Open for extension, closed for modification | Add features without breaking existing |
| **LSP** | Subtypes must be substitutable | Polymorphism works correctly |
| **ISP** | Many specific interfaces > one general | Clients get only what they need |
| **DIP** | Depend on abstractions, not concrete | Flexible, decoupled architecture |

---

## 🔑 Key Concepts

### Before SOLID:
- ❌ God classes (do everything)
- ❌ Rigid (hard to change)
- ❌ Fragile (changes break things)
- ❌ Immobile (can't reuse)
- ❌ Hard to test

### After SOLID:
- ✅ Small, focused classes
- ✅ Flexible (easy to change)
- ✅ Robust (changes isolated)
- ✅ Reusable (components work independently)
- ✅ Testable (mock dependencies)

---

## 🎓 Learning Path

1. **Single Responsibility** - Break apart god classes
2. **Open/Closed** - Make code extensible
3. **Liskov Substitution** - Ensure inheritance works
4. **Interface Segregation** - Split fat interfaces
5. **Dependency Inversion** - Invert dependencies

Each principle builds on the previous one!

---

## 💡 When to Apply SOLID?

**Do apply when:**
- Code will change over time
- Multiple developers involved
- Building libraries/frameworks
- Long-term projects

**Don't over-apply when:**
- Simple scripts
- Proof of concepts
- Throwaway code
- Premature optimization

**Remember:** SOLID is about managing complexity, not creating it!

---

## 🚀 Next Steps

We'll refactor our Order system through each principle:
1. **SRP** → Separate concerns
2. **OCP** → Make extensible
3. **LSP** → Fix inheritance
4. **ISP** → Split interfaces
5. **DIP** → Invert dependencies

Let's begin! 🎯