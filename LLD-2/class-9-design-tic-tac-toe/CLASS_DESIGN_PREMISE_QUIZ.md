# Low-Level Design Quiz: Class Design & Extensibility

## Question 1: Boolean vs Enum

**You're designing a payment system. Currently, payments can be "successful" or "failed". Which is better?**

**Option A:**
```python
class Payment:
    def __init__(self):
        self.is_successful = True  # Boolean
```

**Option B:**
```python
class PaymentStatus(Enum):
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"

class Payment:
    def __init__(self):
        self.status = PaymentStatus.SUCCESSFUL
```

**Your manager says: "Next quarter, we need PENDING and REFUNDED states."**

- A) Option A - booleans are simpler
- B) Option B - easier to extend
- C) Both are equally good
- D) Neither - use strings

---

<details>
<summary>Answer</summary>

**B) Option B - easier to extend**

**Problems with Boolean:**
- Adding new states requires multiple booleans → `is_successful`, `is_pending`, `is_refunded`
- Can have invalid states: `is_successful=True AND is_pending=True`
- Complex nested if-else logic
- No type safety

**Benefits of Enum:**
- ✅ Single source of truth
- ✅ Add new states without restructuring
- ✅ Type-safe - only valid values
- ✅ Self-documenting code
- ✅ No invalid state combinations

**Rule of Thumb:**
| Use Boolean | Use Enum |
|-------------|----------|
| Truly binary (is_deleted, is_active) | >2 states OR might expand |
| Will NEVER expand | Any business state |

</details>

---

## Question 2: Primitive Obsession

**Which design is better?**

**Option A:**
```python
class Order:
    def __init__(self, email: str, phone: str):
        self.customer_email = email
        self.customer_phone = phone
        self.shipping_email = email
        self.shipping_phone = phone
```

**Option B:**
```python
class Customer:
    def __init__(self, email: str, phone: str):
        self.email = email
        self.phone = phone

class Order:
    def __init__(self, customer: Customer):
        self.customer = customer
```

- A) Option A - fewer classes, simpler
- B) Option B - better encapsulation
- C) Both are equally good

---

<details>
<summary>Answer</summary>

**B) Option B - better encapsulation**

**Problems with Primitives:**
- ❌ No validation - `Order("invalid-email", "123")`
- ❌ Business logic scattered
- ❌ Duplicated concepts (customer email, shipping email)
- ❌ Adding fields requires changing multiple places

**Benefits of Separate Class:**
- ✅ Validation centralized in Customer
- ✅ Customer knows how to validate/notify itself
- ✅ Single concept - clear responsibility
- ✅ Extend Customer without touching Order

**When to Create Separate Class:**
| Keep Primitive | Create Class |
|----------------|--------------|
| Simple value (age: int) | Has validation rules |
| No behavior | Has methods/behavior |
| Used once | Used multiple places |
| Truly atomic | Domain concept |

**Example:**
```
❌ price: float, currency: str
✅ price: Money (with conversion logic)
```

</details>

---

## Question 3: Pen Design - Avoiding Code Duplication

**You're designing a pen system. Multiple pen types (Gel, Ball, Fountain) have similar `write()` logic. Which approach avoids duplication?**

**Option A: Copy logic in each subclass**
```python
class GelPen(Pen):
    def write(self):
        print("Gel Pen writes smoothly")

class BallPen(Pen):
    def write(self):
        print("Ball Pen writes smoothly")  # Duplicated!
```

**Option B: Strategy Pattern**
```python
class SmoothWritingStrategy:
    def write(self): print("Writing smoothly...")

class GelPen(Pen):
    def __init__(self):
        self.strategy = SmoothWritingStrategy()
    
    def write(self):
        self.strategy.write()
```

- A) Option A - simpler to understand
- B) Option B - reusable behavior
- C) Both are fine for small systems
- D) Use inheritance to share behavior

---

<details>
<summary>Answer</summary>

**B) Option B - reusable behavior**

**Problems with Duplication:**
- ❌ Same logic repeated across classes
- ❌ Changing behavior requires modifying multiple classes
- ❌ Inconsistent implementations over time
- ❌ Hard to test (test each class separately)

**Benefits of Strategy:**
- ✅ Behavior defined once, reused everywhere
- ✅ Easy to swap strategies at runtime
- ✅ Test strategies independently
- ✅ Add new behaviors without touching pen classes

**Example:**
```python
# Reuse strategies across pen types
gel_pen = GelPen(SmoothWritingStrategy())
fountain_pen = FountainPen(SmoothWritingStrategy())
ball_pen = BallPen(RoughWritingStrategy())

# Can even change at runtime
gel_pen.set_strategy(RoughWritingStrategy())
```

**When to Use Strategy:**
- Multiple classes share same behavior
- Behavior might change at runtime
- Want to test behavior independently
- Avoid code duplication

**Key Principle:** Encapsulate what varies. Make behaviors interchangeable.

</details>

---

## Question 4: Pen Design - LSP Violation

**You have `Pen` with `change_refill()` method. FountainPen doesn't use refills. Which design avoids LSP violation?**

**Option A: Make FountainPen throw exception**
```python
class Pen:
    def change_refill(self, refill): pass

class FountainPen(Pen):
    def change_refill(self, refill):
        raise Exception("Fountain pen has no refill!")
```

**Option B: Use Protocol/Interface**
```python
class RefillablePen(Protocol):
    def change_refill(self, refill): pass

class GelPen(Pen, RefillablePen):
    def change_refill(self, refill): 
        self.refill = refill

class FountainPen(Pen):
    # No change_refill method
    def change_ink(self, ink):
        self.ink = ink
```

- A) Option A - explicit error handling
- B) Option B - separate interfaces
- C) Both work equally well
- D) FountainPen shouldn't extend Pen

---

<details>
<summary>Answer</summary>

**B) Option B - separate interfaces**

**Problems with Exception Throwing:**
- ❌ Violates LSP - can't substitute FountainPen for Pen
- ❌ Runtime errors instead of compile-time safety
- ❌ Forces clients to handle exceptions
- ❌ False promise - method exists but can't be used

**Benefits of Separate Interface:**
- ✅ Type-safe - only refillable pens have `change_refill()`
- ✅ No invalid method calls possible
- ✅ Clear contracts - interfaces tell truth
- ✅ Flexible - compose interfaces as needed

**LSP (Liskov Substitution Principle):**
```
❌ BAD: Some Pen subclasses throw exceptions
✅ GOOD: Only pens that CAN refill implement RefillablePen
```

**Example Usage:**
```python
def refill_pen(pen: RefillablePen, new_refill):
    pen.change_refill(new_refill)  # ✅ Type-safe

gel = GelPen()
refill_pen(gel, new_refill)  # ✅ Works

fountain = FountainPen()
refill_pen(fountain, new_refill)  # ❌ Type error - caught early!
```

**When to Use Separate Interfaces:**
- Not all subclasses support all operations
- Want compile-time safety
- Avoid runtime exceptions
- Different objects have different capabilities

**Key Principle:** Don't force methods on classes that can't fulfill them. Use interfaces for capabilities.

</details>

---

## Question 5: Encapsulation - Direct Access vs Getters

**Which is better?**

**Option A:**
```python
class BankAccount:
    def __init__(self):
        self.balance = 0

account.balance = -1000  # Can go negative!
```

**Option B:**
```python
class BankAccount:
    def __init__(self):
        self._balance = 0
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
    
    def withdraw(self, amount):
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
```

- A) Option A - simpler
- B) Option B - better validation

---

<details>
<summary>Answer</summary>

**B) Option B - better validation and control**

**Problems with Direct Access:**
- ❌ No validation (`balance = -1000`)
- ❌ Can't track changes
- ❌ Can't enforce business rules
- ❌ Can't add logging/auditing later

**Benefits of Encapsulation:**
- ✅ Validation at entry point
- ✅ Enforce business rules (daily limit, minimum balance)
- ✅ Side effects (logging, notifications)
- ✅ Read-only access with `@property`

**When to Use Each:**
| Direct Access | Methods |
|---------------|---------|
| Simple data holder (DTO) | Business rules exist |
| No validation needed | Need validation |
| Internal class fields | Public API |
| No side effects | Logging/notification needed |

**Python's Middle Ground:**
```python
@property
def balance(self):
    return self._balance  # Read-only

# account.balance  ✅ Works
# account.balance = 100  ❌ Error
# account.deposit(100)  ✅ Must use method
```

**Key Principle:** Expose behavior, hide data. Objects manage their own state.

</details>

---

## Question 6: Null Object Pattern

**Which handles optional features better?**

**Option A: Null checks**
```python
class User:
    def __init__(self, premium=None):
        self.premium = premium
    
    def get_benefits(self):
        if self.premium is not None:
            return self.premium.get_benefits()
        return []
```

**Option B: Null Object**
```python
class NoPremium:
    def get_benefits(self): return []

class User:
    def __init__(self, premium=None):
        self.premium = premium or NoPremium()
    
    def get_benefits(self):
        return self.premium.get_benefits()  # No check!
```

- A) Option A - more explicit
- B) Option B - cleaner code

---

<details>
<summary>Answer</summary>

**B) Option B - cleaner code**

**Problems with Null Checks:**
- ❌ Scattered `if x is not None` everywhere
- ❌ Easy to forget → NoneType errors
- ❌ Repetitive boilerplate
- ❌ Clutters business logic

**Benefits of Null Object:**
- ✅ No null checks needed
- ✅ Polymorphic - same interface
- ✅ Impossible to get NoneType error
- ✅ Clean business logic

**Pattern Structure:**
```
Interface: MessageSender
  ├─ EmailSender (sends emails)
  ├─ SMSSender (sends SMS)
  └─ NoOpSender (does nothing) ← Null Object
```

**When to Use:**
| Use Null Checks | Use Null Object |
|-----------------|-----------------|
| Absence has meaning | Default "do nothing" behavior |
| Need to distinguish null | Optional collaborators |
| External input | Internal design |

**Examples:**
- Logger (NoOpLogger)
- Notifier (SilentNotifier)
- Strategy (NoStrategy)

**Key Principle:** "Tell, Don't Ask" - Don't ask if exists, just tell it to act

</details>

---

## Question 7: Strategy vs Enum for Behaviors

**Which is more extensible for "Buy 2 Get 30% off third" discount?**

**Option A: Enum**
```python
class DiscountType(Enum):
    PERCENTAGE = "PERCENTAGE"
    BOGO = "BOGO"

def apply_discount(type, value):
    if type == PERCENTAGE:
        return total * (1 - value/100)
    elif type == BOGO:
        # complex logic...
```

**Option B: Strategy**
```python
class DiscountStrategy(ABC):
    def calculate(self, order): pass

class Buy2Get30(DiscountStrategy):
    def calculate(self, order):
        # complex logic in separate class
```

- A) Option A - add enum value
- B) Option B - add new class

---

<details>
<summary>Answer</summary>

**B) Option B - add new strategy class**

**Problems with Enum + Logic:**
- ❌ Violates Open/Closed - must modify if-elif chain
- ❌ All logic in one method → grows huge
- ❌ Can't test independently
- ❌ Complex logic mixed with simple logic

**Benefits of Strategy:**
- ✅ Add new discount = add new class (no modification)
- ✅ Each strategy isolated
- ✅ Test independently
- ✅ Compose/combine strategies

**Comparison:**
| Enum with Logic | Strategy Pattern |
|-----------------|------------------|
| Modify if-elif | Add new class |
| Test entire method | Test each strategy |
| All logic centralized | Logic isolated |
| Violates OCP | Follows OCP |

**When to Use:**
| Enum | Strategy |
|------|----------|
| Trivial logic (<3 lines) | Complex logic |
| Rarely changes | Frequently extends |
| Simple identity | Complex behavior |

**Hybrid (Best):**
```python
enum DiscountType { PERCENTAGE, BOGO }  # Identity

DiscountFactory.create(PERCENTAGE) → PercentageStrategy  # Behavior
```

**Key Principle:** Enums for IDENTITY, Strategies for BEHAVIOR

</details>

---