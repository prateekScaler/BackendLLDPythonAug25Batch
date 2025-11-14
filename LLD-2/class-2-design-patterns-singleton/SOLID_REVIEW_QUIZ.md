# SOLID Review Quiz - ISP & DIP

## Quick Recap Quiz (5 Questions)

### Question 1: 

```python
class UserService:
    def create_user(self, data):
        # Validate
        if not data.get('email'):
            raise ValueError("Email required")
        
        # Hash password
        hashed = hashlib.sha256(data['password'].encode()).hexdigest()
        
        # Save to DB
        db.execute("INSERT INTO users VALUES (?, ?)", data['email'], hashed)
        
        # Send email
        smtp.send(data['email'], "Welcome!")
        
        # Log
        logger.info(f"User {data['email']} created")
```


**How many responsibilities does this class have?**
- A) 1  
- B) 2  
- C) 5  
- D) It's fine as-is
---
<details>
<summary>Answer</summary>

**- C) 5 responsibilities**

1. Validation
2. Password hashing
3. Database operations
4. Email notifications
5. Logging

**Fix:** Split into UserValidator, PasswordHasher, UserRepository, UserNotifier, Logger
</details>

---

### Question 2:

```python
class DiscountCalculator:
    def calculate(self, total, customer_type):
        if customer_type == "regular":
            return total
        elif customer_type == "premium":
            return total * 0.9
        elif customer_type == "vip":
            return total * 0.8
```

**What's the problem?**
- A) Too many if statements  
- B) Violates OCP - must modify to extend  
- C) Hard to read  
- D) Performance issue
---
<details>
<summary>Answer</summary>

**- B) Violates OCP - must modify to extend**

Every new customer type requires modifying this method.

**Fix:**
```python
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, total): pass

class RegularDiscount(DiscountStrategy):
    def calculate(self, total):
        return total

class PremiumDiscount(DiscountStrategy):
    def calculate(self, total):
        return total * 0.9

# Add new types without modifying existing code
```
</details>

---

### Question 3:

```python
class Bird:
    def fly(self):
        return "Flying..."

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")

def make_bird_fly(bird: Bird):
    return bird.fly()

make_bird_fly(Penguin())
```

**What's violated?**
- A) SRP  
- B) OCP  
- C) LSP - Penguin not substitutable for Bird  
- D) DIP
---
<details>
<summary>Answer</summary>

**- C) LSP - Penguin not substitutable for Bird**

Penguin breaks the contract of Bird.fly() by throwing exception.

**Fix:**
```python
class Bird(ABC):
    @abstractmethod
    def move(self): pass

class FlyingBird(Bird):
    def move(self):
        return "Flying..."

class Penguin(Bird):
    def move(self):
        return "Swimming..."
```
</details>

---
### Question 4A: Diamond Problem Basics

```python
class A:
    def speak(self): print("A")

class B(A):
    def speak(self): print("B")

class C(A):
    def speak(self): print("C")

class D(B, C):
    pass

d = D()
d.speak()
```

Which class’s method gets called first?
- A) A
- B) B
- C) C
- D) It will raise an error
---

<details>
<summary>Answer</summary>

**- B) B**

Python uses C3 Linearization (Consistent, monotonic, non-ambiguous MRO)  for method resolution order (MRO). 
In this case, D -> B -> C -> A.

</details>

---
### Question 4B: Interface Concepts in Python

**Which statement is TRUE about interfaces in Python?**

- A) Python has a built-in `interface` keyword  
- B) Python uses ABC (Abstract Base Class) for interfaces  
- C) Python doesn't support interfaces at all  
- D) Python interfaces require special syntax
---
<details>
<summary>Answer</summary>

**- B) Python uses ABC (Abstract Base Class) for interfaces**

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

# Cannot instantiate: PaymentMethod()
# Must inherit and implement: class CreditCard(PaymentMethod)
```

**Why no interface keyword?**
- Python is duck-typed ("if it walks like a duck...")
- ABC provides interface-like behavior
- Protocol (PEP 544) for structural typing
</details>

---

### Question 5: Interfaces in Python

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self): pass
    
    @abstractmethod
    def query(self): pass
    
    @abstractmethod
    def disconnect(self): pass

class ReadOnlyDB(Database):
    def connect(self): pass
    def query(self): pass
    
    def disconnect(self):
        pass  # Forced to implement even though not needed
```

**What principle is violated?**
- A) SRP  
- B) OCP  
- C) LSP  
- D) ISP - Interface too fat
---
<details>
<summary>Answer</summary>

**- D) ISP - Interface too fat**

ReadOnlyDB forced to implement disconnect even though it's not relevant.

**Fix:** Segregate interfaces
```python
class Connectable(ABC):
    @abstractmethod
    def connect(self): pass

class Queryable(ABC):
    @abstractmethod
    def query(self): pass

class Disconnectable(ABC):
    @abstractmethod
    def disconnect(self): pass

class ReadOnlyDB(Connectable, Queryable):
    # Only what's needed
    pass
```
</details>

---