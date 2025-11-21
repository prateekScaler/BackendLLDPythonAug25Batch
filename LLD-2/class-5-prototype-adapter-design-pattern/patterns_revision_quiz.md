# Design Patterns Revision Quiz

Quick revision of Singleton, Builder, Simple Factory, Factory Method, and Abstract Factory patterns.

---
## Question 1: Factory Pattern Selection
```python
# Scenario 1: Shipping Integration
# Need to create: FedExShipper, DHLShipper, UPSShipper, BlueDartShipper
# Requirement: Easy to add new shipping partners without modifying existing code

# Scenario 2: Game Character Creation
# Need to create: Warrior+Weapon+Armor OR Mage+Weapon+Armor OR Archer+Weapon+Armor
# Requirement: Ensure all equipment matches character class theme

# Scenario 3: Report Generator
# Need to create: SummaryReport, DetailedReport, ExecutiveReport
# Requirement: Centralize creation logic, limited report types
```

**Which pattern fits each scenario?**

- A) Scenario 1: Factory Method, Scenario 2: Abstract Factory, Scenario 3: Simple Factory
- B) Scenario 1: Simple Factory, Scenario 2: Factory Method, Scenario 3: Abstract Factory
- C) All should use Abstract Factory for consistency
- D) All should use Simple Factory for simplicity

---

<details>
<summary>Answer</summary>

**A) Scenario 1: Factory Method, Scenario 2: Abstract Factory, Scenario 3: Simple Factory**

**Scenario 1: Factory Method** (Shipping Integration)
```python
# Need: Easy to extend without modifying existing code

# ✅ Factory Method
class ShippingService(ABC):
    @abstractmethod
    def create_shipper(self) -> Shipper:
        pass
    
    def ship_order(self, package):
        shipper = self.create_shipper()
        return shipper.ship(package)

class FedExService(ShippingService):
    def create_shipper(self):
        return FedExShipper()

class DHLService(ShippingService):
    def create_shipper(self):
        return DHLShipper()

# Add new partner? Just create new subclass!
class BlueDartService(ShippingService):  # No modification to existing code
    def create_shipper(self):
        return BlueDartShipper()
```
---

**Scenario 2: Abstract Factory** (Game Character Creation)
```python
# Need: Ensure equipment matches character class theme

# ✅ Abstract Factory
class CharacterFactory(ABC):
    def create_weapon(self) -> Weapon:
        pass
    def create_armor(self) -> Armor:
        pass
    def create_skill(self) -> Skill:
        pass

class WarriorFactory(CharacterFactory):
    def create_weapon(self):
        return Sword()
    def create_armor(self):
        return HeavyArmor()
    def create_skill(self):
        return BattleCry()

class MageFactory(CharacterFactory):
    def create_weapon(self):
        return MagicStaff()
    def create_armor(self):
        return Robe()
    def create_skill(self):
        return Fireball()
```
---
```python
# Guaranteed consistent character build!
factory = WarriorFactory()
weapon = factory.create_weapon()  # Sword (warrior weapon)
armor = factory.create_armor()    # Heavy armor (warrior armor)
skill = factory.create_skill()    # Battle cry (warrior skill)
# Can't mix warrior sword with mage robe! ✅
```
---

**Scenario 3: Simple Factory** (Report Generator)
```python
# Need: Centralize creation, limited types, simple logic

# ✅ Simple Factory
class ReportFactory:
    @staticmethod
    def create(report_type: str) -> Report:
        if report_type == "summary":
            return SummaryReport()
        elif report_type == "detailed":
            return DetailedReport()
        elif report_type == "executive":
            return ExecutiveReport()
        else:
            raise ValueError(f"Unknown report type: {report_type}")

# Simple and sufficient for this case
report = ReportFactory.create("summary")
report.generate(data)
```
---
**Pattern Selection Guide:**

| Need | Pattern |
|------|---------|
| **Centralize creation** (few types) | Simple Factory |
| **Extend without modification** (many types) | Factory Method |
| **Families of related objects** (consistency) | Abstract Factory |

</details>

---

## Question 2: Pattern Combination Scenario

```python
# You're building a game engine with these requirements:

# 1. Game settings should be globally accessible (one instance)
# 2. Game settings have many optional configurations
# 3. Different game objects (enemies, weapons, items) need creation
# 4. UI elements must match the theme (dark/light mode)

# Which patterns would you use together?
```

**Best pattern combination:**

- A) Only Singleton for everything
- B) Singleton for settings, Builder for settings creation, Factory Method for game objects
- C) Singleton for settings, Builder for settings creation, Factory Method for game objects, Abstract Factory for themed UI
- D) Abstract Factory for everything

---

<details>
<summary>Answer</summary>

**C) Singleton for settings, Builder for settings creation, Factory Method for game objects, Abstract Factory for themed UI**

**Complete Implementation:**

```python
# 1. Singleton + Builder for Game Settings
class GameSettings:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            # Prevent re-initialization
            self.initialized = True
            self.difficulty = "normal"
            self.volume = 50
            self.resolution = (1920, 1080)
 ```
---
```python
class GameSettings:    
    @staticmethod
    def builder():
        return GameSettingsBuilder()

class GameSettingsBuilder:
    def __init__(self):
        self._difficulty = "normal"
        self._volume = 50
        self._resolution = (1920, 1080)
        self._graphics_quality = "high"
        self._vsync = True
    
    def set_difficulty(self, difficulty):
        self._difficulty = difficulty
        return self
    
    def set_resolution(self, width, height):
        self._resolution = (width, height)
        return self
    
    def build(self):
        settings = GameSettings()
        settings.difficulty = self._difficulty
        settings.volume = self._volume
        settings.resolution = self._resolution
        return settings

# Usage
settings = GameSettings.builder()
    .set_difficulty("hard")
    .set_volume(75)
    .set_resolution(2560, 1440)
    .build()
```
---
```python
# 2. Factory Method for Game Objects
class GameObjectFactory(ABC):
    @abstractmethod
    def create_object(self):
        pass
    
    def spawn(self, position):
        obj = self.create_object()
        obj.set_position(position)
        return obj

class EnemyFactory(GameObjectFactory):
    def create_object(self):
        return Enemy()

class WeaponFactory(GameObjectFactory):
    def create_object(self):
        return Weapon()

# Usage
enemy_factory = EnemyFactory()
enemy = enemy_factory.spawn((100, 200))
```
---

```python
# 3. Abstract Factory for Themed UI
class UIThemeFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass
    
    @abstractmethod
    def create_text(self):
        pass

class DarkThemeFactory(UIThemeFactory):
    def create_button(self):
        return DarkButton()
    
    def create_text(self):
        return DarkText()

class LightThemeFactory(UIThemeFactory):
    def create_button(self):
        return LightButton()
    
    def create_text(self):
        return LightText()
```
---
```python
# Usage
theme_factory = DarkThemeFactory()
button = theme_factory.create_button()
panel = theme_factory.create_text()
# All UI elements guaranteed to match theme!
```
---

**Why this combination works:**

```python
# Singleton: Global settings access
settings = GameSettings()  # Same instance everywhere
print(settings.difficulty)

# Builder: Complex settings configuration
GameSettings.builder()
    .set_difficulty("hard")
    .set_volume(75)
    .set_resolution(2560, 1440)
    .set_graphics_quality("ultra")
    .enable_vsync()
    .build()

# Factory Method: Extensible game object creation
class BossFactory(GameObjectFactory):  # Easy to add new types
    def create_object(self):
        return Boss()

# Abstract Factory: Consistent themed UI
theme = DarkThemeFactory()  # All dark theme elements
menu = Menu(theme)  # Menu gets consistent dark UI
```

**Key Insight:** Patterns complement each other! Use multiple patterns to solve different aspects of your system.

</details>
---

## 📝 Quiz Question

### Question: Method Memory Allocation

```python
class PaymentGateway:
    total_processed = 0
    
    def __init__(self, name):
        self.name = name
    
    def process(self, amount):  # Instance method
        return f"{self.name}: ${amount}"
    
    @classmethod
    def get_total(cls):  # Class method
        return cls.total_processed
    
    @staticmethod
    def validate_amount(amount):  # Static method
        return amount > 0

# Create 3 instances
stripe = PaymentGateway("Stripe")
paypal = PaymentGateway("PayPal")
square = PaymentGateway("Square")

# Each instance calls methods
stripe.validate_amount(100)
paypal.validate_amount(200)
square.validate_amount(300)

stripe.get_total()
paypal.get_total()
square.get_total()
```

**How many copies of `validate_amount()` and `get_total()` exist in memory?**

- A) 3 copies of each (one per instance)
- B) 1 copy of each (shared by all instances)
- C) 3 copies of `validate_amount`, 1 copy of `get_total`
- D) It depends on how many times they're called

---

<details>
<summary>Answer</summary>

**B) 1 copy of each (shared by all instances)**

### Explanation

# Static vs Class Method Memory Allocation

## 🧠 Quick Answer

**Both `@staticmethod` and `@classmethod` are stored ONCE in memory, regardless of how many instances call them.**

### Memory Diagram

```
┌────────────────────────────────────┐
│ Payment Class (1 copy in memory)  │
│                                    │
│ count = 0                          │
│ increment(cls) ←─── 1 copy only   │
│ validate(amount) ←─ 1 copy only   │
└────────────────────────────────────┘
         ↑    ↑    ↑
         │    │    │
      ┌──┘    │    └──┐
      │       │       │
   payment1 payment2 payment3
   (unique) (unique) (unique)
   
All instances share the SAME method code!
```

---
### Why This Matters

```python
import sys

class Payment:
    @staticmethod
    def validate(amount):
        return amount > 0
    
    @classmethod
    def create(cls, amount):
        return cls()

# Create instances
p1 = Payment()
p2 = Payment()
p3 = Payment()

# Check if methods are the same object
print(p1.validate == p2.validate)  # True (same method)
print(p1.create == p2.create)      # True (same method)

# Memory address
print(id(Payment.validate))        # Same address
print(id(p1.validate))             # Same address
print(id(p2.validate))             # Same address
```
---
### Comparison

| Method Type | Copies in Memory | Example |
|-------------|------------------|---------|
| `@staticmethod` | **1** (in class) | `validate_amount()` |
| `@classmethod` | **1** (in class) | `get_total()` |
| Instance method | **1** (in class) | `process()` |
| Instance data | **N** (per instance) | `self.name` |

---

## Summary

**Key Patterns Recap:**

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Singleton** | One instance globally | Loggers, configs, caches |
| **Builder** | Step-by-step construction | Many parameters, complex objects |
| **Simple Factory** | Centralized creation | Few types, simple logic |
| **Factory Method** | Extensible creation | Many types, frequent additions |
| **Abstract Factory** | Families of objects | Related objects must be consistent |

**Remember:**
- Patterns solve specific problems - don't force them!
- Multiple patterns can work together
- Start simple, add patterns as complexity grows

Ready to learn Prototype and Adapter patterns! 🚀
