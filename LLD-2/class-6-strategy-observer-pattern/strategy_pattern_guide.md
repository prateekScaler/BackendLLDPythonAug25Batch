# Strategy Pattern

> Define a family of algorithms, encapsulate each one, and make them interchangeable.

## Quick Start

```python
from strategy_demo import ShoppingCart, CreditCardStrategy, PayPalStrategy

cart = ShoppingCart()
cart.add_item("Book", 29.99)

# Switch strategies at runtime
cart.set_payment_strategy(CreditCardStrategy("1234...", "123"))
cart.checkout()

cart.set_payment_strategy(PayPalStrategy("user@email.com"))
cart.checkout()
```

## Structure

```
Context ────────► Strategy (interface)
                      │
           ┌─────────┼─────────┐
           ▼         ▼         ▼
      StrategyA  StrategyB  StrategyC
```

## When to Use

| Situation | Use Strategy? |
|-----------|---------------|
| Multiple algorithms, switch at runtime | ✅ Yes |
| Eliminate long if-else chains | ✅ Yes |
| Only 2 simple, fixed algorithms | ❌ Overkill |

# The Strategy Pattern

## Part 1: The Problem

You're building a navigation app. Different travel modes need different routing algorithms:

```python
class Navigator:
    def calculate_route(self, start, end, mode):
        if mode == "car":
            print("Calculating fastest car route...")
            # Use highways, avoid traffic
            # Consider speed limits
        elif mode == "bike":
            print("Calculating bike route...")
            # Use bike lanes, avoid highways
            # Consider elevation
        elif mode == "walk":
            print("Calculating walking route...")
            # Use sidewalks, shortest distance
            # Consider pedestrian paths
        elif mode == "public":
            print("Calculating public transport...")
            # Use bus/train schedules
            # Consider transfers

nav = Navigator()
nav.calculate_route("Home", "Office", "car")
```

**What's wrong?**

```
┌─────────────────────────────────────┐
│          Navigator                  │
│  ┌───────────────────────────────┐  │
│  │ if car...                    │  │
│  │ elif bike...                 │  │
│  │ elif walk...                 │  │
│  │ elif public...               │  │
│  │ elif scooter...   ← NEW      │  │
│  │ elif helicopter...← NEW      │  │
│  └───────────────────────────────┘  │
│         BLOATED CLASS!              │
└─────────────────────────────────────┘
```

**Problems:**
1. **Violates Open/Closed Principle** - Must modify class for new travel modes
2. **Hard to test** - Can't test routing algorithms in isolation
3. **Code duplication** - Each mode repeats distance/time calculations
4. **Runtime errors** - Typos in strings ("car" vs "cars")

---

## Part 2: First Attempt - Inheritance

"Let's use inheritance!"

```python
class RouteCalculatorStrategy:
    def calculate(self, start, end):
        raise NotImplementedError

class CarRouteCalculatorStrategy(RouteCalculatorStrategy):
    def calculate(self, start, end):
        print("Car route: Use highways")
        return ["Highway A", "Bridge", "Main St"]

class BikeRouteCalculatorStrategy(RouteCalculatorStrategy):
    def calculate(self, start, end):
        print("Bike route: Use bike lanes")
        return ["Bike Path", "Park Trail", "Side St"]
```

```
                     RouteCalculatorStrategy
                           │
    ┌──────────────────────┼─────────────────────────┐
    ▼                      ▼                         ▼
   Car                    Bike                      Walk
CalculatorStrategy  CalculatorStrategy           CalculatorStrategy
```

**Better, but new problem:** What if user needs to switch travel modes during navigation?

```python
# User selects car mode
calculator = CarRouteCalculator()
route = calculator.calculate("Home", "Office")

# User realizes bike is better (traffic jam!)
# Need to create NEW object!
calculator = BikeRouteCalculator()  # ← Wasteful!
route = calculator.calculate("Home", "Office")
```

**Flaw:** Travel mode is baked into the class. Can't change dynamically.

---

## Part 3: The Insight

**Separate what varies from what stays the same.**

- **Stays same:** Getting from A to B, calculating distance/time, showing route
- **Varies:** The algorithm to find the best route

**Solution:** Extract the varying algorithm into separate classes!

```
┌───────────────────────┐
│      Navigator        │
│    (the context)      │
│                       │
│   strategy ──────────────────► RouteStrategy
│                       │              │
│   calculate_route()   │       ┌──────┼──────┐
└───────────────────────┘       ▼      ▼      ▼
                              Car    Bike   Walk
                            Strategy Strategy Strategy
```

---

## Part 4: Strategy Pattern Implementation

### Step 1: Define the Strategy Interface

```python
from abc import ABC, abstractmethod

class RouteStrategy(ABC):
    @abstractmethod
    def calculate_route(self, start: str, end: str) -> dict:
        """Calculate route and return details (distance, time, path)."""
        pass
```

### Step 2: Implement Concrete Strategies

```python
class CarRouteStrategy(RouteStrategy):
    def calculate_route(self, start: str, end: str) -> dict:
        print("🚗 Calculating car route...")
        # Algorithm: Prefer highways, minimize time
        return {
            "path": [start, "Highway 101", "Bridge", end],
            "distance": "15 km",
            "time": "20 min",
            "details": "Via highways, avoid traffic"
        }

class BikeRouteStrategy(RouteStrategy):
    def calculate_route(self, start: str, end: str) -> dict:
        print("🚴 Calculating bike route...")
        # Algorithm: Use bike lanes, minimize elevation
        return {
            "path": [start, "Bike Lane A", "Park Trail", end],
            "distance": "12 km",
            "time": "45 min",
            "details": "Flat route with bike lanes"
        }

class WalkRouteStrategy(RouteStrategy):
    def calculate_route(self, start: str, end: str) -> dict:
        print("🚶 Calculating walking route...")
        # Algorithm: Use sidewalks, shortest distance
        return {
            "path": [start, "Main St", "Park", end],
            "distance": "8 km",
            "time": "90 min",
            "details": "Scenic pedestrian route"
        }

class PublicTransitStrategy(RouteStrategy):
    def calculate_route(self, start: str, end: str) -> dict:
        print("🚌 Calculating public transit route...")
        # Algorithm: Use bus/train schedules
        return {
            "path": [start, "Bus Stop A", "Metro Line 2", "Bus Stop B", end],
            "distance": "18 km",
            "time": "35 min",
            "details": "2 bus stops, 1 transfer"
        }
```

### Step 3: Create the Context

```python
class Navigator:
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
        self._route_strategy = None
    
    def set_strategy(self, strategy: RouteStrategy):
        """Change routing algorithm at runtime!"""
        self._route_strategy = strategy
    
    def calculate_route(self) -> dict:
        if not self._route_strategy:
            raise ValueError("No routing strategy selected!")
        
        print(f"\n📍 From: {self.start} → To: {self.end}")
        return self._route_strategy.calculate_route(self.start, self.end)
```

### Step 4: Use It!

```python
# Create navigator
nav = Navigator("Home", "Office")

# User selects Car mode
nav.set_strategy(CarRouteStrategy())
route = nav.calculate_route()
# Output:
# 📍 From: Home → To: Office
# 🚗 Calculating car route...
# {'path': [...], 'distance': '15 km', 'time': '20 min', ...}

# User switches to Bike (traffic jam!)
nav.set_strategy(BikeRouteStrategy())
route = nav.calculate_route()
# Output:
# 📍 From: Home → To: Office
# 🚴 Calculating bike route...
# {'path': [...], 'distance': '12 km', 'time': '45 min', ...}

# No new Navigator object needed - just swap the strategy!
```

---

## Part 5: Complete UML Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT                                   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────┐                        │
│  │           Navigator                 │                        │
│  │          (Context)                  │                        │
│  │  ─────────────────────────────────  │                        │
│  │  - start: str                       │                        │
│  │  - end: str                         │                        │
│  │  - _route_strategy: RouteStrategy   │────────┐               │
│  │  ─────────────────────────────────  │        │               │
│  │  + set_strategy(strategy)           │        │               │
│  │  + calculate_route()                │        │               │
│  └─────────────────────────────────────┘        │               │
│                                                  │               │
│                                                  ▼               │
│                            ┌──────────────────────────────┐     │
│                            │    <<interface>>             │     │
│                            │    RouteStrategy             │     │
│                            │  ─────────────────────────   │     │
│                            │  + calculate_route(): dict   │     │
│                            └──────────────────────────────┘     │
│                                        │                         │
│                  ┌─────────────────────┼─────────────────┐      │
│                  ▼                     ▼                 ▼      │
│  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────┐│
│  │CarRouteStrategy  │   │BikeRouteStrategy │   │WalkRouteStrategy│
│  │────────────────  │   │────────────────  │   │────────────────││
│  │+ calculate_route()│   │+ calculate_route()│   │+ calculate_route()│
│  │(highways, fast)  │   │(bike lanes, flat)│   │(sidewalks, short)│
│  └──────────────────┘   └──────────────────┘   └──────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Benefits

| Before (if-else) | After (Strategy) |
|------------------|------------------|
| Modify existing code | Add new class |
| Hard to test | Test each strategy in isolation |
| Runtime string errors | Compile-time type safety |
| One bloated class | Many focused classes |

**Open/Closed Principle:** Open for extension, closed for modification!

```python
# Adding new travel mode - NO CHANGES to existing code!
class ScooterRouteStrategy(RouteStrategy):
    def calculate_route(self, start: str, end: str) -> dict:
        print("🛴 Calculating scooter route...")
        return {
            "path": [start, "Scooter Path", end],
            "distance": "10 km",
            "time": "25 min",
            "details": "Smooth roads, no steep hills"
        }

# Just use it!
nav.set_strategy(ScooterRouteStrategy())
route = nav.calculate_route()
```

---

## Part 7: When to Use Strategy

**✅ Use when:**
- Multiple algorithms for same task
- Need to switch algorithms at runtime
- Want to avoid conditional statements
- Algorithm implementation details should be hidden

**❌ Don't use when:**
- Only 2-3 simple algorithms that won't change
- Algorithms don't share common interface
- Overkill for simple problems

---

## Part 8: Quick Reference

```python
# 1. Strategy Interface
class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

# 2. Concrete Strategies
class ConcreteStrategyA(Strategy):
    def execute(self, data):
        # Algorithm A
        pass

# 3. Context
class Context:
    def __init__(self):
        self._strategy = None
    
    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy
    
    def do_work(self, data):
        return self._strategy.execute(data)
```

**Key Point:** Strategy lets you define a family of algorithms, encapsulate each one, and make them interchangeable.

---
Here's the updated Strategy Pattern notes with real-world use cases:

---

## Part 9: Real-World Use Cases

### 🎯 LLD Interview Scenarios

#### 1. Payment Gateway Integration
```python
class PaymentProcessor:
    def __init__(self):
        self._payment_strategy = None
    
    def set_payment_method(self, strategy: PaymentStrategy):
        self._payment_strategy = strategy
    
    def process_payment(self, amount):
        return self._payment_strategy.pay(amount)

# Strategies: Stripe, PayPal, Razorpay, Square
# User can switch payment method at checkout
```

**Why Strategy?**
- Multiple payment gateways with different APIs
- Add new payment providers without modifying core code
- Switch providers based on region/currency/user preference

---

#### 2. Ride-Sharing Pricing Algorithm
```python
class RidePriceCalculator:
    def __init__(self):
        self._pricing_strategy = None
    
    def set_pricing_strategy(self, strategy: PricingStrategy):
        self._pricing_strategy = strategy
    
    def calculate_fare(self, distance, time, surge_multiplier):
        return self._pricing_strategy.calculate(distance, time, surge_multiplier)

# Strategies:
# - StandardPricing (base rate)
# - SurgePricing (peak hours)
# - PoolPricing (shared rides)
# - PremiumPricing (luxury cars)
```

**LLD Questions:**
- "Design Uber fare calculation system"
- "Implement dynamic pricing for ride-sharing"

---

#### 3. E-commerce Discount/Promotion System
```python
class ShoppingCart:
    def __init__(self):
        self._discount_strategy = None
    
    def apply_discount(self, strategy: DiscountStrategy):
        self._discount_strategy = strategy
    
    def calculate_total(self, items):
        subtotal = sum(item.price for item in items)
        discount = self._discount_strategy.calculate_discount(subtotal, items)
        return subtotal - discount

# Strategies:
# - PercentageDiscount (10% off)
# - BuyOneGetOne (BOGO)
# - SeasonalDiscount (Black Friday)
# - LoyaltyPointsDiscount
# - FirstTimeUserDiscount
```

**Interview Gold:**
- Easy to add new promotion types (Black Friday, Diwali sale)
- Combine multiple discounts (Strategy + Chain of Responsibility)

---

#### 4. File Compression Service
```python
class FileCompressor:
    def __init__(self, strategy: CompressionStrategy):
        self._compression_strategy = strategy
    
    def compress_file(self, file_path):
        return self._compression_strategy.compress(file_path)

# Strategies: ZIP, RAR, GZIP, BZIP2, 7Z
# Choose based on: file type, compression ratio needed, speed
```

**Real Interview Question:** "Design a cloud storage service with multiple compression algorithms"

---

### 💼 Software Engineering Use Cases

#### 1. Authentication/Authorization Systems
```python
class AuthenticationService:
    def __init__(self):
        self._auth_strategy = None
    
    def set_auth_method(self, strategy: AuthStrategy):
        self._auth_strategy = strategy
    
    def authenticate(self, credentials):
        return self._auth_strategy.authenticate(credentials)

# Strategies:
# - OAuth2Strategy (Google, Facebook login)
# - JWTStrategy (token-based)
# - BasicAuthStrategy (username/password)
# - BiometricStrategy (fingerprint, face ID)
# - SAMLStrategy (enterprise SSO)
```

**Real Use:**
- Microservices with different auth requirements
- Multi-tenant applications
- B2B vs B2C authentication

---

#### 2. Notification Delivery System
```python
class NotificationService:
    def send_notification(self, strategy: NotificationStrategy, message):
        return strategy.send(message)

# Strategies:
# - EmailNotification
# - SMSNotification
# - PushNotification
# - SlackNotification
# - WhatsAppNotification
```

**Production Scenario:**
```python
# User preferences determine strategy
if user.prefers_email:
    service.send_notification(EmailStrategy(), message)
elif user.prefers_sms:
    service.send_notification(SMSStrategy(), message)

# Fallback mechanism
for strategy in [PushStrategy(), EmailStrategy(), SMSStrategy()]:
    if strategy.send(message):
        break
```

---

#### 3. Data Export/Import (ETL Pipelines)
```python
class DataExporter:
    def __init__(self, strategy: ExportStrategy):
        self._export_strategy = strategy
    
    def export(self, data):
        return self._export_strategy.export(data)

# Strategies:
# - CSVExporter
# - JSONExporter
# - XMLExporter
# - ParquetExporter (big data)
# - AvroExporter (Kafka)
```

**Real-World:**
- Analytics dashboards (export reports in multiple formats)
- Data migration tools
- API response formatting

---

#### 4. Image Processing Pipeline
```python
class ImageProcessor:
    def process(self, image, strategy: FilterStrategy):
        return strategy.apply(image)

# Strategies:
# - GrayscaleFilter
# - BlurFilter
# - SharpenFilter
# - EdgeDetectionFilter
# - FaceDetectionFilter (ML-based)
```

**Production Use:**
- Instagram/Snapchat filters
- Medical imaging software
- Autonomous vehicles (image recognition)

---

#### 5. Caching Strategies
```python
class CacheManager:
    def __init__(self, strategy: CacheEvictionStrategy):
        self._eviction_strategy = strategy
    
    def evict(self, cache):
        return self._eviction_strategy.evict(cache)

# Strategies:
# - LRU (Least Recently Used)
# - LFU (Least Frequently Used)
# - FIFO (First In First Out)
# - TTL (Time To Live)
# - Random Eviction
```

**System Design:**
- Redis/Memcached configuration
- CDN caching policies
- Browser cache management

---

#### 6. Search/Sorting Algorithms (Academic → Real)
```python
class DataSorter:
    def sort(self, data, strategy: SortStrategy):
        return strategy.sort(data)

# Strategies:
# - QuickSort (general purpose)
# - MergeSort (stable, large datasets)
# - HeapSort (memory constrained)
# - TimSort (Python's default, nearly sorted data)
```

**Real Use:**
- Database query optimizers
- Search engines (ranking algorithms)
- E-commerce product sorting (price, rating, popularity)

---

### 🏢 Industry-Specific Examples

#### Banking/Finance
```python
# Interest calculation
class LoanCalculator:
    def calculate_interest(self, strategy: InterestStrategy):
        return strategy.calculate(principal, rate, time)

# Strategies: SimpleInterest, CompoundInterest, ReducingBalance
```

#### Gaming
```python
# AI behavior
class Enemy:
    def act(self, strategy: AIStrategy):
        return strategy.decide_action(self.state)

# Strategies: AggressiveAI, DefensiveAI, StealthAI
```

#### Healthcare
```python
# Diagnosis algorithm
class DiagnosisEngine:
    def diagnose(self, strategy: DiagnosisStrategy, symptoms):
        return strategy.analyze(symptoms)

# Strategies: RuleBased, MLBased, ExpertSystem
```

---

### 📊 When Strategy Pattern Shines

| Scenario | Why Strategy? |
|----------|---------------|
| **Multiple vendors** | Easy to switch (payment gateways, SMS providers) |
| **A/B testing** | Switch algorithms, measure results |
| **Runtime configuration** | User selects behavior (theme, language) |
| **Regional differences** | Different logic per country/region |
| **Algorithm evolution** | Replace old with new, keep both for comparison |

---

### 🎤 Interview Tips

**Question:** "Why not just use if-else?"

**Answer:**
```python
# Without Strategy (bad for 10+ algorithms):
def process(type):
    if type == "A": ...
    elif type == "B": ...
    # ... 50 more conditions

# With Strategy (scalable):
strategies = {
    "A": StrategyA(),
    "B": StrategyB()
}
strategies[type].execute()
```

**Benefits:**
- ✅ Each algorithm is a separate class (testable)
- ✅ Add new algorithm = add new class (OCP)
- ✅ No modification to existing code
- ✅ Runtime selection via config/database

---

### 🔥 Common Interview Follow-ups

**Q: "How do you choose which strategy to use at runtime?"**

```python
# 1. User selection
strategy = payment_strategies[user.preferred_method]

# 2. Configuration/feature flags
strategy = get_strategy_from_config("payment_method")

# 3. Context-based (location, time, load)
if peak_hours:
    strategy = SurgePricingStrategy()
else:
    strategy = StandardPricingStrategy()

# 4. Factory Pattern
strategy = StrategyFactory.create(strategy_type)
```

---

**Q: "Strategy vs State pattern?"**

| Strategy | State |
|----------|-------|
| Algorithms interchangeable | States transition |
| Client chooses strategy | Object changes state internally |
| Strategies independent | States know about each other |
| Example: Sorting algorithms | Example: Order (pending → shipped → delivered) |

---

**Key Takeaway for Interviews:**

> "Strategy pattern lets you define a family of algorithms, encapsulate each one, and make them interchangeable. It's perfect when you have multiple ways to accomplish the same task and want to switch between them at runtime without changing the client code."

**Mention OCP:** "This follows the Open/Closed Principle - open for extension (add new strategies), closed for modification (don't touch existing code)."