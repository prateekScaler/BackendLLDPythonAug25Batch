# Design Patterns - Comprehensive Revision Guide

> Quick reference with UML, use cases, and gotchas for all patterns

---

## 1. Singleton Pattern

### UML Diagram
```
┌────────────────────────┐
│      Singleton         │
├────────────────────────┤
│ - _instance: Singleton │ ← static
├────────────────────────┤
│ - __init__()           │ ← private
│ + get_instance()       │ ← static
└────────────────────────┘
```

### Quick Code
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Real Use Cases
1. **Database Connection Pool** - One pool for entire app
2. **Logger** - Centralized logging
3. **Configuration Manager** - App-wide settings

### LLD Examples
- **Parking Lot:** Single `ParkingLotManager`
- **Cache System:** Single `CacheManager`
- **Rate Limiter:** Single `RateLimiterService`

### Gotchas ⚠️
- **Not thread-safe** without locking
- **Hard to test** (global state)
- **Inheritance issues** (shared _instance)

**Fix:** Use double-checked locking or decorator

---

## 2. Factory Method Pattern

### UML Diagram
```
┌─────────────────────┐
│  Creator (ABC)      │
├─────────────────────┤
│ + factory_method()  │ ← abstract
│ + operation()       │ ← template method
└──────────△──────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
ConcreteA     ConcreteB
```

### Quick Code
```python
class Creator(ABC):
    @abstractmethod
    def factory_method(self):
        pass
    
    def operation(self):
        product = self.factory_method()
        return product.use()
```

### Real Use Cases
1. **Payment Gateways** - Stripe, PayPal, Razorpay
2. **Notification Services** - Email, SMS, Push
3. **Document Exporters** - PDF, Excel, CSV

### LLD Examples
- **Ride Sharing:** `RideFactory` → Economy, Premium, Shared
- **Food Delivery:** `RestaurantFactory` → FastFood, FineDining
- **Hotel Booking:** `RoomFactory` → Standard, Deluxe, Suite

### Gotchas ⚠️
- **Requires abstract creator** - not just factory
- **Need template method** - factory alone isn't enough
- **Confuse with Simple Factory** - Factory Method uses inheritance

---

## 3. Abstract Factory Pattern

### UML Diagram
```
┌────────────────────────┐
│  AbstractFactory       │
├────────────────────────┤
│ + createProductA()     │
│ + createProductB()     │
└──────────△─────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
Factory1      Factory2
│  │           │  │
creates       creates
A1, B1        A2, B2
```

### Quick Code
```python
class UIFactory(ABC):
    @abstractmethod
    def create_button(self): pass
    
    @abstractmethod
    def create_textbox(self): pass

class WindowsFactory(UIFactory):
    def create_button(self): return WindowsButton()
    def create_textbox(self): return WindowsTextbox()
```

### Real Use Cases
1. **UI Themes** - Dark/Light with Button, Input, Modal
2. **Database Connectors** - MySQL/Postgres with Connection, Query, Transaction
3. **Document Exporters** - PDF/Word with Text, Image, Table renderers

### LLD Examples
- **Cloud Provider:** AWS, Azure, GCP (each creates VM, Storage, Network)
- **Game Platforms:** PC, Console, Mobile (each creates Graphics, Audio, Input)
- **Report System:** Web, Mobile, Print (each creates Header, Body, Footer)

### Gotchas ⚠️
- **Family consistency required** - all products must work together
- **Hard to add new product types** - must modify all factories
- **Overkill for simple cases** - use Factory Method instead

---

## 4. Builder Pattern

### Basic Builder (Most Common)

```
┌─────────────────┐         
│    Builder      │         ┌─────────────┐
├─────────────────┤ builds  │   Product   │
│ - _product      │────────►│             │
├─────────────────┤         └─────────────┘
│ + set_part_a()  │
│ + set_part_b()  │
│ + build()       │
└─────────────────┘
```

**Usage:**
```python
product = Builder()
    .set_part_a("value")
    .set_part_b("value")
    .build()
```

---

### Builder with Director (Advanced)

```
┌─────────────────┐
│    Director     │
├─────────────────┤
│ - builder       │
├─────────────────┤
│ + construct()   │──┐ uses
└─────────────────┘  │
                     ▼
┌─────────────────┐         ┌─────────────┐
│    Builder      │builds   │   Product   │
├─────────────────┤────────►│             │
│ + buildPart()   │         └─────────────┘
│ + getResult()   │
└────────△────────┘
         │
    ┌────┴────┐
ConcreteBuilder
```

**Usage:**
```python
builder = ConcreteBuilder()
director = Director(builder)
director.construct()
product = builder.get_result()
```

**Director:** Encapsulates common construction recipes

---

### Quick Code

**Basic Builder:**
```python
class Builder:
    def __init__(self):
        self._product = Product()
    
    def set_part_a(self, value):
        self._product.part_a = value
        return self  # ← Must return self!
    
    def set_part_b(self, value):
        self._product.part_b = value
        return self
    
    def build(self):
        return self._product

# Usage
product = Builder().set_part_a("A").set_part_b("B").build()
```

**With Director:**
```python
class Director:
    def __init__(self, builder):
        self._builder = builder
    
    def construct_recipe_1(self):
        return (self._builder
            .set_part_a("A")
            .set_part_b("B")
            .build())
    
    def construct_recipe_2(self):
        return (self._builder
            .set_part_a("X")
            .set_part_b("Y")
            .build())

# Usage
director = Director(Builder())
product1 = director.construct_recipe_1()
product2 = director.construct_recipe_2()
```

### Real Use Cases
1. **SQL Query Builder** - SELECT, WHERE, JOIN, ORDER BY
2. **HTTP Request Builder** - Headers, Body, Params
3. **Email Builder** - To, Subject, Body, Attachments

### LLD Examples
- **Trip Planner:** Flight + Hotel + Car rental builder
- **Meal Builder:** Burger customization (bun, patty, toppings)
- **Resume Builder:** Sections, formatting, export options

### Gotchas ⚠️
- **Forget `return self`** - breaks method chaining
- **Validation timing** - validate in `build()`, not setters
- **Director optional** - use only for common recipes

---

## 5. Prototype Pattern

### UML Diagram
```
┌─────────────────┐
│   Prototype     │
├─────────────────┤
│ + clone()       │
└────────△────────┘
         │
    ┌────┴────┐
    ▼         ▼
ConcreteA ConcreteB
```

### Quick Code
```python
import copy

class Prototype:
    def clone(self):
        return copy.deepcopy(self)  # Deep copy!
```

### Real Use Cases
1. **Game Characters** - Clone template with base stats
2. **Document Templates** - Newsletter, Invoice formatting
3. **Configuration Objects** - Server configs for different regions

### LLD Examples
- **Game Engine:** Enemy spawner (clone orcs, goblins)
- **Form Builder:** Clone form templates
- **Cloud Deployment:** Clone server configurations

### Gotchas ⚠️
- **Shallow vs Deep copy** - must use `deepcopy` for nested objects
- **When NOT to use** - all fields unique (no shared config)
- **Circular references** - `deepcopy` can handle, but be aware

**Prototype Registry:**
```python
class Registry:
    def __init__(self):
        self._prototypes = {}
    
    def register(self, name, prototype):
        self._prototypes[name] = prototype
    
    def create(self, name):
        return self._prototypes[name].clone()
```

---

## 6. Adapter Pattern

### UML Diagram
```
┌─────────┐       ┌─────────┐
│ Client  │──────►│ Target  │
└─────────┘       └────△────┘
                       │ implements
                 ┌─────┴─────┐
                 │  Adapter  │
                 ├───────────┤
                 │ - adaptee │───┐
                 └───────────┘   │ wraps
                                 ▼
                         ┌──────────┐
                         │ Adaptee  │
                         └──────────┘
```

### Quick Code
```python
class Adapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def request(self):
        return self.adaptee.specific_request()
```

### Real Use Cases
1. **Legacy System Integration** - Old API → New API
2. **Third-party Library Wrapper** - Celsius → Fahrenheit
3. **Data Format Conversion** - XML → JSON

### LLD Examples
- **Payment Integration:** Adapt different payment gateway APIs
- **Analytics Service:** Adapt Google Analytics, Mixpanel APIs
- **Cloud Storage:** Adapt AWS S3, Azure Blob, GCP Storage APIs

### Gotchas ⚠️
- **When NOT needed** - interfaces already compatible
- **Object vs Class adapter** - prefer composition (object adapter)
- **Two-way adapter** - can adapt bidirectionally if needed

---

## 7. Decorator Pattern

### UML Diagram
```
┌────────────┐
│ Component  │
└─────△──────┘
      │
  ┌───┴──────────┐
  ▼              ▼
Concrete    ┌──────────┐
Component   │Decorator │
            ├──────────┤
            │-component│◄─── wraps
            └─────△────┘
                  │
         ┌────────┴────────┐
         ▼                 ▼
    DecoratorA        DecoratorB
```

### Quick Code
```python
class Decorator(Component):
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return f"Decorated({self._component.operation()})"
```

### Real Use Cases
1. **Coffee Shop** - Base coffee + milk + sugar + whipped cream
2. **I/O Streams** - File → Buffer → Compression → Encryption
3. **Web Middleware** - Request → Auth → Logging → CORS

### LLD Examples
- **Notification System:** Base + SMS + Email + Slack decorators
- **Text Editor:** Text → Bold → Italic → Underline
- **Pizza Order:** Base pizza + cheese + pepperoni + olives

### Gotchas ⚠️
- **Order matters** - Tax before/after discount gives different results
- **Many small objects** - each decorator creates new object
- **Type checking fails** - `isinstance()` checks fail

---

## 8. Strategy Pattern

### UML Diagram
```
┌─────────────┐       ┌──────────────┐
│   Context   │──────►│  Strategy    │
│             │       └──────△───────┘
│ - strategy  │              │
└─────────────┘     ┌────────┴────────┐
                    ▼                 ▼
              StrategyA           StrategyB
```

### Quick Code
```python
class Context:
    def __init__(self):
        self._strategy = null
        
    def set_strategy(self, strategy):
        self._strategy = strategy
    
    def execute(self):
        return self._strategy.algorithm()
```

### Real Use Cases
1. **Route Planning** - Car, Bike, Walk, Transit algorithms
2. **Payment Processing** - Credit card, PayPal, Crypto
3. **Sorting** - QuickSort, MergeSort, HeapSort

### LLD Examples
- **Ride Pricing:** Standard, Surge, Pool pricing strategies
- **Discount System:** Percentage, BOGO, Seasonal discounts
- **File Compression:** ZIP, RAR, GZIP strategies

### Gotchas ⚠️
- **Strategy vs State** - Strategy swaps algorithms, State transitions
- **Client must know strategies** - needs to select which one
- **Overkill for 2-3 simple cases** - if-else might be simpler

---

## 9. Observer Pattern

### UML Diagram
```
┌─────────────┐         ┌──────────────┐
│  Subject    │◄────────│  Observer    │
│             │         └──────△───────┘
│ - observers │                │
│             │       ┌────────┴────────┐
│ + attach()  │       ▼                 ▼
│ + detach()  │   ObserverA         ObserverB
│ + notify()  │
└─────────────┘
```

### Quick Code
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, data):
        for obs in self._observers:
            obs.update(data)
```

### Real Use Cases
1. **Stock Ticker** - Price updates → Dashboard, Bot, Alerts
2. **Event System** - User action → Analytics, Logging, Notifications
3. **MVC** - Model changes → Multiple views update

### LLD Examples
- **Social Media:** Post → notify followers
- **E-commerce:** Order placed → Payment, Inventory, Shipping services
- **Monitoring:** Sensor reading → Alert, Log, Dashboard

### Gotchas ⚠️
- **Memory leaks** - forgot to detach observers
- **Notification storms** - too many rapid updates
- **Order not guaranteed** - observers notified in arbitrary order

---

## Pattern Comparison Table

| Pattern | Purpose | When to Use | Key Benefit |
|---------|---------|-------------|-------------|
| **Singleton** | One instance | Shared resource | Global access |
| **Factory Method** | Create via inheritance | Extensible creation | OCP compliant |
| **Abstract Factory** | Create families | Related objects | Consistency |
| **Builder** | Step-by-step construction | Complex objects | Readable |
| **Prototype** | Clone objects | Expensive creation | Performance |
| **Adapter** | Convert interface | Incompatible APIs | Integration |
| **Decorator** | Add responsibilities | Dynamic features | Flexible |
| **Strategy** | Swap algorithms | Runtime selection | Interchangeable |
| **Observer** | One-to-many notify | Event broadcasting | Loose coupling |

---

## Pattern Selection Guide

### Creation Patterns

**Need one instance globally?**
→ **Singleton**

**Complex object with many parameters?**
→ **Builder**

**Create objects without specifying class?**
→ **Factory Method** (if extensible) or **Simple Factory** (if fixed)

**Create families of related objects?**
→ **Abstract Factory**

**Expensive to create, want to clone?**
→ **Prototype**

---

### Structural Patterns

**Incompatible interfaces need to work together?**
→ **Adapter**

**Add responsibilities without subclassing?**
→ **Decorator**

---

### Behavioral Patterns

**Multiple algorithms, switch at runtime?**
→ **Strategy**

**One object changes, many need to know?**
→ **Observer**

---

## Common Anti-Patterns

### 1. Singleton Overuse
```python
# ❌ Don't make everything Singleton
class UtilityFunctions(Singleton):  # Bad!
    def add(self, a, b):
        return a + b

# ✅ Just use functions or modules
def add(a, b):
    return a + b
```

---

### 2. Factory for Everything
```python
# ❌ Don't use factory for simple objects
UserFactory.create()  # Overkill!

# ✅ Just use constructor
User()
```

---

### 3. Too Many Decorators
```python
# ❌ Confusing nesting
obj = D1(D2(D3(D4(D5(Base())))))

# ✅ Use builder or configuration
obj = ObjectBuilder().with_d1().with_d2().build()
```

---

## LLD Interview Cheat Sheet

| System | Patterns |
|--------|----------|
| **Parking Lot** | Singleton (manager), Factory (vehicle types), Strategy (pricing) |
| **Ride Sharing** | Factory Method (rides), Strategy (pricing), Observer (notifications) |
| **Food Delivery** | Factory (restaurants), Observer (order tracking), Strategy (delivery) |
| **Hotel Booking** | Builder (booking), Factory (rooms), Decorator (amenities) |
| **E-commerce** | Observer (order events), Strategy (discounts), Factory (products) |
| **Social Media** | Observer (followers), Singleton (feed), Factory (posts) |
| **Library System** | Singleton (catalog), Factory (media types), Observer (notifications) |
| **Movie Booking** | Factory (theaters), Strategy (pricing), Observer (bookings) |

---

## Quick Revision Checklist

- [ ] Can draw UML for each pattern
- [ ] Know when to use vs when NOT to use
- [ ] Understand gotchas for each
- [ ] Can code each pattern from memory
- [ ] Know 2-3 real examples per pattern
- [ ] Understand pattern relationships (Strategy vs State, Decorator vs Proxy)
- [ ] Can solve LLD problems using appropriate patterns

---

## Final Tips

1. **Don't force patterns** - solve problem first, pattern second
2. **Patterns can combine** - Singleton + Builder, Factory + Strategy
3. **UML is communication** - draw it clearly, explain it well
4. **Code readability** - patterns should make code clearer, not obscure
5. **Know trade-offs** - every pattern has pros/cons

**Remember:** Patterns are tools, not rules. Use them when they make sense!