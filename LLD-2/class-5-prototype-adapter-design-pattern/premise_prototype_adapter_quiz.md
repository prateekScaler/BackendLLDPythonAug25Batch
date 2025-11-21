# Prototype & Adapter Patterns - Pre-requisite Quiz

This quiz covers Copy Constructor concepts and introduces problems that Prototype and Adapter patterns solve.

---

## Section A: Copy Constructor & Cloning

### Question 1: Reference vs Copy

```python
class GameCharacter:
    def __init__(self, name, health, inventory):
        self.name = name
        self.health = health
        self.inventory = inventory  # List of items

# Scenario
hero = GameCharacter("Knight", 100, ["sword", "shield"])

option_a = hero
option_b = copy.copy(hero)
option_c = copy.deepcopy(hero)

option_a.health = 50
option_b.inventory.append("potion")
option_c.inventory.append("armor")

print(hero.health)      # ?
print(hero.inventory)   # ?
```

**What will be the output?**

- A) `100`, `['sword', 'shield']`
- B) `50`, `['sword', 'shield', 'potion']`
- C) `50`, `['sword', 'shield', 'potion', 'armor']`
- D) `100`, `['sword', 'shield', 'potion', 'armor']`

---

<details>
<summary>Answer</summary>

**B) `50`, `['sword', 'shield', 'potion']`**

**Step-by-step breakdown:**

```python
hero = GameCharacter("Knight", 100, ["sword", "shield"])

# Option A: Reference (same object)
option_a = hero  # Points to SAME object
option_a.health = 50
# hero.health is now 50! ✓

# Option B: Shallow copy (new object, shared nested objects)
option_b = copy.copy(hero)
# Different GameCharacter object
# BUT shares same inventory list
option_b.inventory.append("potion")
# hero.inventory also gets "potion"! ✓

# Option C: Deep copy (completely independent)
option_c = copy.deepcopy(hero)
# Different GameCharacter AND different inventory list
option_c.inventory.append("armor")
# hero.inventory NOT affected ✗

print(hero.health)      # 50 (changed by option_a)
print(hero.inventory)   # ['sword', 'shield', 'potion'] (changed by option_b)
```
---
**Visual representation:**

```
hero = GameCharacter("Knight", 100, ["sword", "shield"])
         │
         │
    ┌────┴────────────────────────┐
    │ GameCharacter               │
    │  name: "Knight"             │
    │  health: 100 → 50           │ ← option_a changes this
    │  inventory: ─────────┐      │
    └──────────────────────┼──────┘
                           │
                      ┌────▼────────────┐
                      │ List            │
                      │ ["sword",       │
                      │  "shield",      │
                      │  "potion"]      │ ← option_b adds this
                      └─────────────────┘
                           ▲
                           │
                    option_b shares this

option_c has its own list: ["sword", "shield", "armor"]
```

**Key takeaway:**
- **Reference** (`=`) → Same object
- **Shallow copy** → New object, shared nested objects
- **Deep copy** → Completely independent copy

</details>

---

### Question 2: 
```python
import copy
class Player:
    def __init__(self, name):
        self.name = name
        self.team = None
    
    def join_team(self, team):
        self.team = team
        team.members.append(self)

class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

# Setup
player1 = Player("Alice")
team = Team("Red Team")
player1.join_team(team)
# Try to copy
player2 = copy.deepcopy(player1)
```

**What happens and why?**

- A) Works fine - player2 is independent copy
- B) Circular reference error
- C) Works, but player2 and player1 share the same team
- D) Deep copy handles circular references automatically

---

<details>
<summary>Answer</summary>

**D) Deep copy handles circular references automatically**

**The circular reference:**

```python
player1 ──► team
            │
            ▼
         members: [player1]  ◄── Circular!

# player1.team → team
# team.members → [player1]
# player1 → ... → player1 (circular!)
```
---
**Deep copy handles this:**

```python
import copy

player2 = copy.deepcopy(player1)

# deepcopy uses a memo dictionary to track copied objects
# When it encounters player1 again (via team.members),
# it returns the already-copied player2, not creating infinite copies

print(player1 is player2)  # False - different players
print(player1.team is player2.team)  # False - different teams
print(player2 in player2.team.members)  # True - consistent!
```
---
**How it works internally:**

```python
# Simplified version of deepcopy behavior
def deepcopy(obj, memo=None):
    if memo is None:
        memo = {}  # Track already copied objects
    
    obj_id = id(obj)
    if obj_id in memo:
        return memo[obj_id]  # Already copied! Return existing copy
    
    # Create new object
    new_obj = obj.__class__.__new__(obj.__class__)
    memo[obj_id] = new_obj  # Remember it!
    
    # Copy attributes recursively
    for key, value in obj.__dict__.items():
        setattr(new_obj, key, deepcopy(value, memo))
    
    return new_obj
```
---
**Without memo (circular reference breaks):**

```python
# Infinite recursion!
copy player1
  → copy player1.team
    → copy player1.team.members[0]  # This is player1!
      → copy player1  # Again!
        → copy player1.team  # Again!
          → ... INFINITE! 💥
```

**Key insight:** `copy.deepcopy()` automatically handles circular references using a memo dictionary!

</details>

---

## Section B: Prototype Pattern Prerequisites

### Question 3: Creating Many Similar Objects

```python
# Game development scenario
class Enemy:
    def __init__(self, type, health, damage, speed, texture, ai_behavior):
        self.type = type
        self.health = health
        self.damage = damage
        self.speed = speed
        self.texture = self._load_texture(texture)  # Expensive!
        self.ai_behavior = ai_behavior
        self._initialize_ai()  # Expensive!
    
    def _load_texture(self, texture_path):
        # Load from disk - SLOW operation
        time.sleep(0.1)  # Simulating disk I/O
        return f"Texture({texture_path})"
    
    def _initialize_ai(self):
        # Complex AI initialization - SLOW
        time.sleep(0.1)
        pass
```
---
```python
# Need to spawn 100 zombies in game
zombies = []
for i in range(100):
    zombie = Enemy(
        type="zombie",
        health=50,
        damage=10,
        speed=2,
        texture="zombie.png",
        ai_behavior="chase_player"
    )
    zombies.append(zombie)
    # Each creation: 0.2 seconds
    # Total: 20 seconds! 💥
```
**What's the problem and how to solve it?**

- A) No problem - 20 seconds is acceptable
- B) Problem: Expensive initialization repeated. Solution: Create one template, clone it
- C) Problem: Too many parameters. Solution: Use Builder Pattern
- D) Problem: Different enemy types. Solution: Use Factory Pattern

---

<details>
<summary>Answer</summary>

**B) Problem: Expensive initialization repeated. Solution: Create one template, clone it**

**The Problem:**

```python
# Creating 100 zombies
for i in range(100):
    zombie = Enemy(...)
    # Each zombie:
    # - Loads texture from disk (0.1s) ← Wasteful!
    # - Initializes AI (0.1s) ← Wasteful!
    # All zombies are IDENTICAL!

# Total time: 100 × 0.2s = 20 seconds 💥
```
---
**Why this is wasteful:**

```python
# Zombie 1
texture = load_from_disk("zombie.png")  # 0.1s
ai = initialize_ai("chase_player")      # 0.1s

# Zombie 2
texture = load_from_disk("zombie.png")  # 0.1s ← SAME FILE!
ai = initialize_ai("chase_player")      # 0.1s ← SAME BEHAVIOR!

# Zombie 3
texture = load_from_disk("zombie.png")  # 0.1s ← AGAIN!
ai = initialize_ai("chase_player")      # 0.1s ← AGAIN!

# Doing the same expensive work 100 times! 💥
```
---
**Solution: Prototype Pattern (Clone template)**

```python
import copy

# Create ONE template zombie (0.2 seconds)
zombie_template = Enemy(
    type="zombie",
    health=50,
    damage=10,
    speed=2,
    texture="zombie.png",
    ai_behavior="chase_player"
)

# Clone template 100 times (near-instant!)
zombies = []
for i in range(100):
    zombie = copy.deepcopy(zombie_template)  # <0.001s per clone!
    zombies.append(zombie)
    # No texture loading!
    # No AI initialization!

# Total time: 0.2s + (100 × 0.001s) = ~0.3 seconds ✅
# 67x faster!
```
---
**Why cloning is faster:**

```python
# Constructor: Expensive
Enemy(...)
  → Load texture from disk (I/O) ← SLOW
  → Parse texture data ← SLOW
  → Initialize AI system ← SLOW
  → Allocate memory
  → Set attributes

# Clone: Fast
copy.deepcopy(template)
  → Copy memory ← FAST (just memory copy)
  → Done!

# Cloning just copies memory - no I/O, no initialization!
```
---
**When to use Prototype (cloning):**
- ✅ Creating many similar objects
- ✅ Object initialization is expensive
- ✅ Objects differ only slightly
- ✅ Want to avoid repeated expensive operations

**When NOT to use:**
- ❌ Objects are very different
- ❌ Initialization is cheap
- ❌ Need unique initialization each time

**This is the Prototype Pattern!** We'll learn more about it next.

</details>

---

## Section C: Adapter Pattern Prerequisites

### Question 4: Third-Party API Integration Problem

**The REALISTIC scenario:**
```python
# ALL payment gateways are third-party SDKs with different interfaces!

# Stripe SDK (third-party - can't modify)
class StripeSDK:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def create_charge(self, amount_cents: int, currency: str = "usd") -> StripeCharge:
        """Stripe's actual method"""
        return StripeCharge(
            id=f"ch_{amount_cents}",
            paid=True,
            amount=amount_cents
        )

class StripeCharge:
    def __init__(self, id: str, paid: bool, amount: int):
        self.id = id
        self.paid = paid
        self.amount = amount

```
---
```python
# PayPal SDK (third-party - can't modify)
class PayPalSDK:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def execute_payment(self, payment_data: dict) -> PayPalPayment:
        """PayPal's actual method"""
        return PayPalPayment(
            state="approved",
            payment_id=f"PAY-{payment_data['amount']}"
        )

class PayPalPayment:
    def __init__(self, state: str, payment_id: str):
        self.state = state
        self.payment_id = payment_id
```
---
```python
# Square SDK (third-party - can't modify)
class SquareSDK:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def charge_card(self, amount_in_cents: int, card_token: str) -> SquareResponse:
        """Square's actual method"""
        return SquareResponse(
            status="SUCCESS",
            transaction_id=f"sq_{amount_in_cents}"
        )

class SquareResponse:
    def __init__(self, status: str, transaction_id: str):
        self.status = status
        self.transaction_id = transaction_id
```

---

**Your application needs a UNIFIED interface:**
```python
# YOUR application's interface (what YOUR code expects)
class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> dict:
        """
        Standard interface for YOUR application
        - Takes amount in DOLLARS (float)
        - Returns dict with 'success' and 'transaction_id'
        """
        pass


# Your business logic expects THIS interface
def checkout(gateway: PaymentGateway, amount: float):
    """Your application code - expects PaymentGateway interface"""
    result = gateway.process_payment(amount)  # Expects this method!
    
    if result["success"]:  # Expects this dict format!
        print(f"✅ Payment successful: {result['transaction_id']}")
        send_confirmation_email(result)
        update_inventory()
    else:
        print("❌ Payment failed")
    
    return result
```

---

**Why can't you use the SDKs directly?**

**What's the problem?**

- A) Each SDK has different method names (create_charge, execute_payment, charge_card)
- B) Each SDK has different parameter formats (cents, dict, card_token)
- C) Each SDK returns different object types (StripeCharge, PayPalPayment, SquareResponse)
- D) All of the above - need adapters to make them work with YOUR interface!

---

<details>
<summary>Answer</summary>

**D) All of the above - need adapters!**

**The Real Problem:**

You can't modify the third-party SDKs, and your application code expects a consistent interface. Each SDK is incompatible with your `PaymentGateway` interface.
```python
# Your application expects:
class PaymentGateway(ABC):
    def process_payment(self, amount: float) -> dict:
        pass

# But you have:
# - StripeSDK.create_charge(amount_cents, currency) -> StripeCharge
# - PayPalSDK.execute_payment(payment_data) -> PayPalPayment  
# - SquareSDK.charge_card(amount_cents, card_token) -> SquareResponse
```

---
```python
# Try using Stripe SDK directly
stripe_sdk = StripeSDK("sk_test_123")
checkout(stripe_sdk, 100.00)  # 💥 FAILS!

# Problem 1: StripeSDK doesn't inherit from PaymentGateway
# Problem 2: No process_payment() method - has create_charge() instead
# Problem 3: Different parameters - needs cents, not dollars
# Problem 4: Returns StripeCharge object, not dict
# Problem 5: Success field is .paid, not result["success"]


# Try using PayPal SDK directly
paypal_sdk = PayPalSDK("client_123", "secret_456")
checkout(paypal_sdk, 100.00)  # 💥 FAILS!

# Problem 1: PayPalSDK doesn't inherit from PaymentGateway
# Problem 2: No process_payment() method - has execute_payment() instead
# Problem 3: Needs dict parameter, not float
# Problem 4: Returns PayPalPayment object, not dict
# Problem 5: Success field is .state == "approved", not result["success"]


# Try using Square SDK directly
square_sdk = SquareSDK("api_key_789")
checkout(square_sdk, 100.00)  # 💥 FAILS!

# Problem 1: SquareSDK doesn't inherit from PaymentGateway
# Problem 2: No process_payment() method - has charge_card() instead
# Problem 3: Needs cents AND card_token, not just dollars
# Problem 4: Returns SquareResponse object, not dict
# Problem 5: Success field is .status == "SUCCESS", not result["success"]
```
---

**Solution: Create Adapters**

Each adapter "wraps" the SDK and translates the interface:
```python
# Stripe Adapter
class StripeAdapter(PaymentGateway):
    def __init__(self, secret_key: str):
        self.sdk = StripeSDK(secret_key)  # Wrap the SDK
    
    def process_payment(self, amount: float) -> dict:
        # Translate YOUR interface → Stripe's interface
        amount_cents = int(amount * 100)  # Convert dollars to cents
        charge = self.sdk.create_charge(amount_cents)  # Call Stripe's method
        
        # Translate Stripe's response → YOUR format
        return {
            "success": charge.paid,
            "transaction_id": charge.id
        }
```
---
```python
# PayPal Adapter
class PayPalAdapter(PaymentGateway):
    def __init__(self, client_id: str, client_secret: str):
        self.sdk = PayPalSDK(client_id, client_secret)  # Wrap the SDK
    
    def process_payment(self, amount: float) -> dict:
        # Translate YOUR interface → PayPal's interface
        payment_data = {"amount": amount, "currency": "USD"}
        payment = self.sdk.execute_payment(payment_data)  # Call PayPal's method
        
        # Translate PayPal's response → YOUR format
        return {
            "success": payment.state == "approved",
            "transaction_id": payment.payment_id
        }
```
---

```python
# Square Adapter
class SquareAdapter(PaymentGateway):
    def __init__(self, api_key: str):
        self.sdk = SquareSDK(api_key)  # Wrap the SDK
    
    def process_payment(self, amount: float) -> dict:
        # Translate YOUR interface → Square's interface
        amount_cents = int(amount * 100)
        response = self.sdk.charge_card(amount_cents, "card_nonce_123")  # Call Square's method
        
        # Translate Square's response → YOUR format
        return {
            "success": response.status == "SUCCESS",
            "transaction_id": response.transaction_id
        }
```

---

**Now ALL SDKs work with your application code:**
```python
# Your business logic stays the same!
def checkout(gateway: PaymentGateway, amount: float):
    result = gateway.process_payment(amount)
    if result["success"]:
        print(f"✅ Payment successful: {result['transaction_id']}")
    return result


# Now they ALL work! ✅
stripe_gateway = StripeAdapter("sk_test_123")
checkout(stripe_gateway, 100.00)  # ✅ Works!

paypal_gateway = PayPalAdapter("client_123", "secret_456")
checkout(paypal_gateway, 100.00)  # ✅ Works!

square_gateway = SquareAdapter("api_key_789")
checkout(square_gateway, 100.00)  # ✅ Works!


# Your application code doesn't care which one!
def process_order(payment_method: str, amount: float):
    if payment_method == "stripe":
        gateway = StripeAdapter("sk_test_123")
    elif payment_method == "paypal":
        gateway = PayPalAdapter("client_123", "secret_456")
    elif payment_method == "square":
        gateway = SquareAdapter("api_key_789")
    
    return checkout(gateway, amount)  # Same interface for all!
```

---

**Why use Adapter Pattern?**

✅ **Can't modify third-party SDKs** - They're external libraries  
✅ **Each SDK has different interface** - Different methods, parameters, returns  
✅ **Your code needs consistency** - One interface for all payment processors  
✅ **Easy to add new processors** - Just create a new adapter  
✅ **Decouples your code from SDKs** - Change processors without changing business logic

**This is why we need the Adapter Pattern!**

</details>

---

**Key Insight:** In real applications, Stripe, PayPal, and Square are ALL third-party SDKs with incompatible interfaces. The Adapter Pattern lets you create a **unified interface** for your application while using their native SDKs under the hood.

### Question 5: Legacy Code Integration

```python
# Modern payment system
class ModernPaymentProcessor:
    def execute_payment(self, payment_details: PaymentDetails) -> PaymentResult:
        pass

class PaymentDetails:
    def __init__(self, amount, currency, customer_id, payment_method):
        self.amount = amount
        self.currency = currency
        self.customer_id = customer_id
        self.payment_method = payment_method

# Legacy system you must integrate with
class LegacyBillingSystem:
    def charge_customer(self, customer_number, dollar_amount):
        # Old system - different interface
        # Only supports USD
        # Returns 0 for success, error code otherwise
        return 0  # Success

# Your new code
def process_subscription(processor: ModernPaymentProcessor, amount, customer):
    details = PaymentDetails(
        amount=amount,
        currency="USD",
        customer_id=customer.id,
        payment_method="credit_card"
    )
    result = processor.execute_payment(details)
    return result.success
```

**How do you use LegacyBillingSystem with process_subscription()?**

- A) Modify LegacyBillingSystem to match ModernPaymentProcessor interface
- B) Modify process_subscription() to work with both systems
- C) Create an adapter that implements ModernPaymentProcessor and wraps LegacyBillingSystem
- D) Rewrite the entire legacy system

---

<details>
<summary>Answer</summary>

**C) Create an adapter that implements ModernPaymentProcessor and wraps LegacyBillingSystem**

**Why other options are bad:**

```python
# ❌ Option A: Modify LegacyBillingSystem
class LegacyBillingSystem:
    def execute_payment(self, payment_details):  # Changed!
        # Problem: This is a third-party library!
        # Can't modify external code!
        # Changes break on library update!
        pass

# ❌ Option B: Modify process_subscription
def process_subscription(processor, amount, customer):
    if isinstance(processor, ModernPaymentProcessor):
        # Modern way
        details = PaymentDetails(...)
        result = processor.execute_payment(details)
    elif isinstance(processor, LegacyBillingSystem):
        # Legacy way
        result_code = processor.charge_customer(customer.number, amount)
        result = result_code == 0
    # Problem: Violates Open-Closed Principle!
    # Every new system needs modification here!

# ❌ Option D: Rewrite legacy system
# Problem: Expensive, risky, time-consuming!
```
---

**✅ Option C: Adapter Pattern**

```python
class LegacyBillingAdapter(ModernPaymentProcessor):
    def __init__(self):
        self.legacy_system = LegacyBillingSystem()
    
    def execute_payment(self, payment_details: PaymentDetails) -> PaymentResult:
        # Translate modern interface → legacy interface
        result_code = self.legacy_system.charge_customer(
            customer_number=payment_details.customer_id,
            dollar_amount=payment_details.amount
        )
        
        # Translate legacy result → modern result
        return PaymentResult(success=(result_code == 0))

# Now legacy system works with modern code!
processor = LegacyBillingAdapter()
process_subscription(processor, 99.99, customer)  # ✅ Works!

# No modification to:
# - Legacy system (can't touch it)
# - Modern code (don't want to change it)
# - Just added an adapter!
```
---

**Benefits of Adapter:**

```python
# Clean separation
┌─────────────────────┐
│   Modern Code       │
│  (uses Modern API)  │
└──────────┬──────────┘
           │ expects ModernPaymentProcessor
           ↓
    ┌──────────────┐
    │   Adapter    │  ← Implements modern interface
    │   (Bridge)   │  ← Wraps legacy system
    └──────┬───────┘
           │ calls legacy methods
           ↓
┌─────────────────────┐
│   Legacy System     │
│  (old interface)    │
└─────────────────────┘

# Modern code doesn't know about legacy system
# Legacy system doesn't know about modern code
# Adapter translates between them!
```
---

**Real-world analogy:**

```
Power adapter for travel:
┌────────────────┐
│  US Device     │  (your modern code)
│  (2-pin plug)  │
└────────┬───────┘
         │
    ┌────┴────┐
    │ Adapter │  (adapter pattern)
    └────┬────┘
         │
┌────────┴───────┐
│  EU Socket     │  (legacy system)
│  (different)   │
└────────────────┘

Device doesn't change
Socket doesn't change
Adapter makes them work together!
```

**Key takeaway:** Adapter Pattern lets incompatible interfaces work together without modifying either side!

</details>

---

## Summary: What Problems Do These Patterns Solve?

### Prototype Pattern
**Problem:** Creating many similar objects with expensive initialization
**Solution:** Clone a pre-configured template instead of creating from scratch

**Use when:**
- Objects are expensive to create
- Need many similar objects
- Initialization involves I/O, complex computation, or resource loading

### Adapter Pattern
**Problem:** Incompatible interfaces between your code and third-party/legacy code
**Solution:** Create an adapter that translates one interface to another

**Use when:**
- Integrating third-party libraries
- Working with legacy code
- Interfaces don't match
- Can't modify the incompatible code

**Ready to dive into these patterns!** 🚀
