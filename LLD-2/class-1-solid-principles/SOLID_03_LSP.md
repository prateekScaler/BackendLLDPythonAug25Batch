# Liskov Substitution Principle (LSP)

## 📖 Definition

**"Objects of a superclass should be replaceable with objects of its subclasses without breaking the application."**

**Simple:** Subclasses must be usable wherever parent class is expected.

---

## 🎯 The Problem: Broken Substitution

```python
class Order:
    def __init__(self, items):
        self.items = items
        self.discount = 0
    
    def set_discount(self, percent):
        self.discount = percent
    
    def calculate_total(self):
        subtotal = sum(item.price for item in self.items)
        return subtotal * (1 - self.discount)


class FinalSaleOrder(Order):
    """Final sale orders can't have discounts"""
    
    def set_discount(self, percent):
        raise Exception("Final sale items can't be discounted!")
        # Breaks parent class contract!


# This works fine
def apply_promo(order: Order):
    order.set_discount(0.1)  # 10% off
    return order.calculate_total()

regular = Order([Item(100)])
print(apply_promo(regular))  # Works: $90

final_sale = FinalSaleOrder([Item(100)])
print(apply_promo(final_sale))  # Crashes! Violates LSP
```

**Problem:** `FinalSaleOrder` can't be used where `Order` is expected.

---

## ✅ Solution: Proper Abstraction

```python
from abc import ABC, abstractmethod

class Order(ABC):
    def __init__(self, items):
        self.items = items
    
    @abstractmethod
    def calculate_total(self):
        pass


class DiscountableOrder(Order):
    def __init__(self, items):
        super().__init__(items)
        self.discount = 0
    
    def set_discount(self, percent):
        self.discount = percent
    
    def calculate_total(self):
        subtotal = sum(item.price for item in self.items)
        return subtotal * (1 - self.discount)


class FinalSaleOrder(Order):
    def calculate_total(self):
        return sum(item.price for item in self.items)
        # No discount logic - and that's OK!


# Works with any Order
def get_total(order: Order):
    return order.calculate_total()

# Both work fine
discountable = DiscountableOrder([Item(100)])
discountable.set_discount(0.1)
print(get_total(discountable))  # $90

final_sale = FinalSaleOrder([Item(100)])
print(get_total(final_sale))  # $100

# Discounts only for discountable orders
if isinstance(order, DiscountableOrder):
    order.set_discount(0.1)
```

**Benefits:**
- Clear hierarchy
- No broken contracts
- Substitutable classes
- Type-safe

---

## 🚩 Signs of Violation

### Red Flag 1: Exception in Subclass
```python
class Bird:
    def fly(self):
        return "Flying..."

class Penguin(Bird):
    def fly(self):
        raise Exception("Can't fly!")  # Violates LSP
```

### Red Flag 2: Empty/No-op Implementation
```python
class Vehicle:
    def start_engine(self):
        return "Engine started"

class Bicycle(Vehicle):
    def start_engine(self):
        pass  # Does nothing - violates LSP
```

### Red Flag 3: Tightening Preconditions
```python
class User:
    def set_email(self, email):
        self.email = email  # Accepts any string

class AdminUser(User):
    def set_email(self, email):
        if not email.endswith("@company.com"):
            raise ValueError("Admin must use company email")
        # Tightens precondition - violates LSP
```

### Red Flag 4: Weakening Postconditions
```python
class Calculator:
    def divide(self, a, b):
        return a / b  # Returns float

class IntegerCalculator(Calculator):
    def divide(self, a, b):
        return int(a / b)  # Returns int - weakens postcondition
```

---

## 💡 LSP Rules

### 1. **Preconditions cannot be strengthened**
```python
# Bad
class Rectangle:
    def set_dimensions(self, width, height):
        pass  # Accepts any numbers

class Square(Rectangle):
    def set_dimensions(self, width, height):
        if width != height:
            raise ValueError("Square needs equal sides")
        # Strengthened precondition!
```

### 2. **Postconditions cannot be weakened**
```python
# Bad
class Account:
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError()
        self.balance -= amount
        # Guarantees exception if insufficient

class OverdraftAccount(Account):
    def withdraw(self, amount):
        self.balance -= amount  # No check!
        # Weakened postcondition - allows overdraft
```

### 3. **Invariants must be preserved**
```python
# Bad
class Stack:
    def __init__(self):
        self.items = []
    
    def size(self):
        return len(self.items)  # Always >= 0

class BrokenStack(Stack):
    def size(self):
        return -1  # Violates invariant!
```

---

## 🎨 Practical Examples

### Example 1: Rectangle-Square Problem

**❌ Classic Violation:**
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def set_width(self, width):
        self.width = width
        self.height = width  # Couples them!
    
    def set_height(self, height):
        self.width = height
        self.height = height


def test_rectangle(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20  # Fails for Square!
```

**✅ Correct Design:**
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
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2


# Both are shapes, but not in inheritance relationship
def calculate_area(shape: Shape):
    return shape.area()  # Works for both!
```

---

### Example 2: Payment Processing

**❌ Bad:**
```python
class PaymentProcessor:
    def process(self, amount, card_number):
        return f"Processed ${amount} with card {card_number}"


class CashPayment(PaymentProcessor):
    def process(self, amount, card_number):
        # Doesn't use card_number but signature forces it
        return f"Received ${amount} cash"
        # Violates LSP - unused parameter
```

**✅ Good:**
```python
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount):
        pass


class CardPayment(PaymentProcessor):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def process(self, amount):
        return f"Charged ${amount} to card {self.card_number}"


class CashPayment(PaymentProcessor):
    def process(self, amount):
        return f"Received ${amount} cash"


def checkout(processor: PaymentProcessor, amount):
    return processor.process(amount)  # Works for all!
```

---

### Example 3: Database Connection

**❌ Bad:**
```python
class Database:
    def connect(self):
        return "Connected"
    
    def disconnect(self):
        return "Disconnected"


class ReadOnlyDatabase(Database):
    def disconnect(self):
        raise Exception("Read-only DB can't disconnect!")
        # Violates LSP
```

**✅ Good:**
```python
class DataSource(ABC):
    @abstractmethod
    def query(self, sql):
        pass


class Database(DataSource):
    def connect(self):
        pass
    
    def disconnect(self):
        pass
    
    def query(self, sql):
        return self.execute(sql)


class ReadOnlyDatabase(DataSource):
    def query(self, sql):
        if sql.upper().startswith("SELECT"):
            return self.execute(sql)
        raise ValueError("Read-only database")


# Use based on actual capability
def fetch_data(source: DataSource, query):
    return source.query(query)  # Works for both
```

---

## ⚠️ When LSP Doesn't Apply

### Not Inheritance Issues:
```python
# This is fine - composition, not inheritance
class EmailService:
    def send(self, to, message):
        pass

class SMSService:
    def send(self, to, message):
        pass

# These aren't substitutable, and don't need to be
# They're different services, not parent-child
```

### Simple Data Classes:
```python
# This is fine - no behavior to substitute
@dataclass
class User:
    name: str
    email: str

@dataclass
class AdminUser:
    name: str
    email: str
    permissions: list[str]

# Not about substitution, just data structure
```

---

## 🔧 Common Gotchas

### Gotcha 1: "Is-a" vs "Behaves-like-a"
```python
# Penguin IS-A bird, but doesn't BEHAVE-LIKE-A bird (can't fly)
# Solution: Don't inherit based on "is-a" alone

class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class FlightlessBird(Bird):
    def move(self):
        return "Walking"
```

### Gotcha 2: Type Checking as Band-aid
```python
# Bad - using isinstance to fix LSP violation
def process(bird: Bird):
    if isinstance(bird, Penguin):
        bird.swim()
    else:
        bird.fly()

# Good - proper abstraction
def process(bird: Bird):
    bird.move()  # Each bird knows how to move
```

---

## ✅ Best Practices

1. **Design by contract** - Honor parent class contracts
2. **Test substitutability** - Can subclass replace parent in tests?
3. **Avoid type checking** - If using isinstance, LSP likely violated
4. **Favor composition** - When inheritance doesn't fit
5. **Keep hierarchies shallow** - Easier to maintain contracts

---

## 🎯 Quick Checklist

- [ ] Subclass doesn't throw unexpected exceptions
- [ ] Subclass accepts same or broader inputs
- [ ] Subclass returns same or more specific outputs
- [ ] Subclass preserves parent invariants
- [ ] No type checking (isinstance) needed

---

## 💡 Key Takeaway

**"Subtypes must be behaviorally substitutable."**

If you can't replace parent with child without breaking code, the hierarchy is wrong. Fix by proper abstraction, composition, or rethinking relationships.

**Test:** If client code needs `isinstance()` checks, LSP is violated.