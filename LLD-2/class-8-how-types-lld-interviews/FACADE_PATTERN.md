# Facade Pattern - Concise Guide

## Intent
**Provide a simplified, unified interface to a complex subsystem, making it easier to use.**

Facade means "face" in French. It is a front-facing building that is the main entrance to a building. The facade is the first thing that a visitor sees when they enter a building. The facade hides the complexity of the building from the visitor. The facade provides a simple interface to the building. The facade is a single point of entry to the building.

---

## Problem Statement
A system has many interconnected components with complex interactions. Clients need to perform common tasks but shouldn't deal with the complexity of multiple subsystems, their APIs, and initialization sequences.

**Example:** Booking a movie ticket requires interacting with seat selection, payment gateway, notification service, and inventory management - too complex for client code.

---

## Generic UML

```
┌──────────────────────┐
│       Facade         │ ← Simple, unified interface
├──────────────────────┤
│- subsystem1          │
│- subsystem2          │
│- subsystem3          │
├──────────────────────┤
│+ simplified_method() │ ← High-level operations
└──────────────────────┘
           │
           │ coordinates
           ▼
    ┌──────┴──────┬────────────┬──────────┐
    │             │            │          │
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Subsystem│ │Subsystem│ │Subsystem│ │Subsystem│
│   A     │ │   B     │ │   C     │ │   D     │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
    ↑ Complex subsystems (hidden from client)

┌──────────────────────┐
│       Client         │
└──────────────────────┘
           │
           │ uses simple interface
           ▼
┌──────────────────────┐
│       Facade         │
└──────────────────────┘
```

**Key Concepts:**
- **Facade**: Simple interface that delegates to subsystems
- **Subsystems**: Complex components doing actual work
- **Client**: Uses facade, unaware of subsystem complexity
- **Coordination**: Facade orchestrates multiple subsystems

---

## Example 1: Home Theater System

**Problem:** Watching a movie requires coordinating DVD player, projector, sound system, lights

```python
# Without Facade - Complex client code
class DVDPlayer:
    def on(self): print("DVD on")
    def play(self, movie): print(f"Playing {movie}")
    def stop(self): print("DVD stop")
    def off(self): print("DVD off")

class Projector:
    def on(self): print("Projector on")
    def wide_screen_mode(self): print("Wide screen mode")
    def off(self): print("Projector off")

class SoundSystem:
    def on(self): print("Sound on")
    def set_volume(self, level): print(f"Volume: {level}")
    def off(self): print("Sound off")

class Lights:
    def dim(self, level): print(f"Lights dimmed to {level}%")

# Client must know all subsystems and correct sequence!
dvd = DVDPlayer()
projector = Projector()
sound = SoundSystem()
lights = Lights()

# To watch a movie - 10+ steps!
lights.dim(10)
projector.on()
projector.wide_screen_mode()
sound.on()
sound.set_volume(50)
dvd.on()
dvd.play("Inception")
# Error-prone, repetitive!
```

```python
# With Facade - Simple interface
class HomeTheaterFacade:
    def __init__(self):
        self._dvd = DVDPlayer()
        self._projector = Projector()
        self._sound = SoundSystem()
        self._lights = Lights()
    
    def watch_movie(self, movie):
        """Simplified method - one call does everything"""
        print("🎬 Get ready to watch movie...")
        self._lights.dim(10)
        self._projector.on()
        self._projector.wide_screen_mode()
        self._sound.on()
        self._sound.set_volume(50)
        self._dvd.on()
        self._dvd.play(movie)
    
    def end_movie(self):
        """Simplified cleanup"""
        print("🎬 Shutting down theater...")
        self._dvd.stop()
        self._dvd.off()
        self._sound.off()
        self._projector.off()
        self._lights.dim(100)

# Client code - Clean and simple!
theater = HomeTheaterFacade()
theater.watch_movie("Inception")  # One call!
# ... watch movie ...
theater.end_movie()  # One call!
```

**UML:**
```
┌──────────────────────┐
│ HomeTheaterFacade    │ ← Facade
├──────────────────────┤
│- dvd: DVDPlayer      │
│- projector: Projector│
│- sound: SoundSystem  │
│- lights: Lights      │
├──────────────────────┤
│+ watch_movie(movie)  │ ← Simple interface
│+ end_movie()         │
└──────────────────────┘
           │
           │ coordinates
           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│   DVD   │ │Projector│ │  Sound  │ │ Lights  │
│ Player  │ │         │ │ System  │ │         │
└─────────┘ └─────────┘ └─────────┘ └─────────┘

Client → theater.watch_movie() → Facade coordinates all 4 subsystems
```

---

## Example 2: E-Commerce Order Processing

**Problem:** Placing an order involves inventory, payment, shipping, notifications

```python
# Subsystems (complex)
class InventorySystem:
    def check_stock(self, product_id):
        return True
    
    def reserve_item(self, product_id):
        print(f"✓ Reserved product {product_id}")

class PaymentGateway:
    def validate_card(self, card):
        return True
    
    def charge(self, amount, card):
        print(f"✓ Charged ${amount}")
        return "TXN123"

class ShippingService:
    def calculate_shipping(self, address):
        return 5.99
    
    def create_shipment(self, order_id, address):
        print(f"✓ Shipment created for order {order_id}")

class NotificationService:
    def send_confirmation_email(self, email, order_id):
        print(f"✓ Email sent to {email}")
    
    def send_sms(self, phone, message):
        print(f"✓ SMS sent to {phone}")

# Facade - Simplified interface
class OrderFacade:
    def __init__(self):
        self._inventory = InventorySystem()
        self._payment = PaymentGateway()
        self._shipping = ShippingService()
        self._notification = NotificationService()
    
    def place_order(self, product_id, card, address, email, phone):
        """One method to place entire order"""
        print("🛒 Processing order...")
        
        # Step 1: Check inventory
        if not self._inventory.check_stock(product_id):
            return {"success": False, "error": "Out of stock"}
        
        # Step 2: Calculate total
        shipping_cost = self._shipping.calculate_shipping(address)
        total = 99.99 + shipping_cost
        
        # Step 3: Process payment
        if not self._payment.validate_card(card):
            return {"success": False, "error": "Invalid card"}
        
        txn_id = self._payment.charge(total, card)
        
        # Step 4: Reserve inventory
        self._inventory.reserve_item(product_id)
        
        # Step 5: Create shipment
        order_id = f"ORD-{txn_id}"
        self._shipping.create_shipment(order_id, address)
        
        # Step 6: Send notifications
        self._notification.send_confirmation_email(email, order_id)
        self._notification.send_sms(phone, "Order confirmed!")
        
        return {"success": True, "order_id": order_id}

# Client - Simple usage
order_facade = OrderFacade()
result = order_facade.place_order(
    product_id="P123",
    card="4111-1111-1111-1111",
    address="123 Main St",
    email="user@example.com",
    phone="+1234567890"
)
# Output:
# 🛒 Processing order...
# ✓ Charged $105.98
# ✓ Reserved product P123
# ✓ Shipment created for order ORD-TXN123
# ✓ Email sent to user@example.com
# ✓ SMS sent to +1234567890
```

**UML:**
```
┌──────────────────────┐
│    OrderFacade       │ ← Facade
├──────────────────────┤
│- inventory           │
│- payment             │
│- shipping            │
│- notification        │
├──────────────────────┤
│+ place_order(...)    │ ← One simple method
└──────────────────────┘
           │
           │ orchestrates
           ▼
┌──────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐
│Inventory │ │ Payment │ │Shipping │ │Notification │
│  System  │ │ Gateway │ │ Service │ │   Service   │
└──────────┘ └─────────┘ └─────────┘ └─────────────┘
```

---

## Example 3: Data Analysis Pipeline

**Problem:** Running analysis requires data loading, preprocessing, multiple algorithms, visualization

```python
# Subsystems
class DataLoader:
    def load_csv(self, file):
        print(f"✓ Loaded {file}")
        return {"data": [1, 2, 3]}

class DataPreprocessor:
    def clean_data(self, data):
        print("✓ Data cleaned")
        return data
    
    def normalize(self, data):
        print("✓ Data normalized")
        return data

class AnalysisEngine:
    def statistical_analysis(self, data):
        print("✓ Stats computed")
        return {"mean": 2.0, "std": 0.8}
    
    def ml_analysis(self, data):
        print("✓ ML model trained")
        return {"accuracy": 0.95}

class Visualizer:
    def plot_results(self, results):
        print("✓ Plots generated")

class ReportGenerator:
    def create_pdf(self, results):
        print("✓ PDF report created")
        return "report.pdf"

# Facade
class DataAnalysisFacade:
    def __init__(self):
        self._loader = DataLoader()
        self._preprocessor = DataPreprocessor()
        self._engine = AnalysisEngine()
        self._visualizer = Visualizer()
        self._reporter = ReportGenerator()
    
    def run_full_analysis(self, csv_file):
        """One method for complete analysis pipeline"""
        print("📊 Starting analysis pipeline...")
        
        # Load
        data = self._loader.load_csv(csv_file)
        
        # Preprocess
        data = self._preprocessor.clean_data(data)
        data = self._preprocessor.normalize(data)
        
        # Analyze
        stats = self._engine.statistical_analysis(data)
        ml_results = self._engine.ml_analysis(data)
        
        # Visualize
        self._visualizer.plot_results({**stats, **ml_results})
        
        # Report
        report = self._reporter.create_pdf({**stats, **ml_results})
        
        return report

# Client - One simple call
facade = DataAnalysisFacade()
report = facade.run_full_analysis("sales_data.csv")
print(f"Report ready: {report}")
```

**UML:**
```
┌──────────────────────┐
│DataAnalysisFacade    │
├──────────────────────┤
│+ run_full_analysis() │ ← One method
└──────────────────────┘
           │
           │ coordinates pipeline
           ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Loader │→│Prepro│→│Analysis│→│Visual- │→│Report  │
│        │ │cessor│ │ Engine │ │  izer  │ │  Gen   │
└────────┘ └──────┘ └────────┘ └────────┘ └────────┘
```

---

## Where Facade is Used

### Real-World Applications:

1. **Frameworks & Libraries**
   - jQuery (simplifies DOM manipulation)
   - Express.js (simplifies HTTP server)
   - Requests library (simplifies HTTP in Python)

2. **Operating Systems**
   - File system API (hides disk, cache, permissions)
   - Network stack (hides TCP/IP layers)

3. **Enterprise Systems**
   - Order processing systems
   - Banking transaction systems
   - Booking engines (travel, events)

4. **Development Tools**
   - Build tools (Maven, Gradle)
   - ORMs (SQLAlchemy, Hibernate)
   - Cloud SDKs (AWS SDK, Azure SDK)

5. **Hardware**
   - Device drivers
   - Graphics APIs (OpenGL, DirectX)
   - Camera APIs (single method to capture photo)

### Libraries Using Facade:

- **Python**: `requests` library (facade over `urllib`)
- **Java**: JDBC (facade over database drivers)
- **JavaScript**: jQuery (facade over DOM API)
- **C++**: SFML (facade over OpenGL/audio/input)

---

## Facade vs Related Patterns

| Aspect | Facade | Adapter | Decorator |
|--------|--------|---------|-----------|
| **Purpose** | Simplify complex system | Convert interface | Add behavior |
| **Interface** | New simplified interface | Match existing interface | Same interface |
| **Subsystems** | Multiple subsystems | One incompatible class | One component |
| **Wrapping** | Optional (can bypass) | Must use adapter | Must use decorator |
| **Complexity** | Reduces complexity | Converts compatibility | Adds functionality |

### Code Comparison:

```python
# FACADE - Simplifies multiple subsystems
class HomeTheaterFacade:
    def watch_movie(self):
        self._dvd.play()
        self._projector.on()
        self._sound.on()
        # Coordinates multiple subsystems

# ADAPTER - Converts one interface
class PowerAdapter:
    def __init__(self, us_plug):
        self._us_plug = us_plug
    
    def connect_to_eu_socket(self):
        # Converts US plug to EU socket
        return self._us_plug.connect()

# DECORATOR - Adds behavior
class LoggingDecorator:
    def __init__(self, api):
        self._api = api
    
    def request(self):
        print("Log: Request")
        return self._api.request()  # Adds logging
```

### Visual Difference:

```
FACADE - Simplifies many
Client → Facade → [SubsystemA, SubsystemB, SubsystemC]
         (one simple interface to many complex systems)

ADAPTER - Converts one
Client → Adapter → IncompatibleClass
         (makes interface compatible)

DECORATOR - Wraps one
Client → Decorator → Component
         (same interface, added behavior)
```

### When to Use Which:

**Use Facade when:**
- ✅ System has many interconnected components
- ✅ Need simple interface for common tasks
- ✅ Want to decouple client from subsystems
- ✅ Subsystems are complex to use directly

**Use Adapter when:**
- ✅ Need to integrate incompatible interface
- ✅ Working with third-party code
- ✅ Converting one interface to another

**Use Decorator when:**
- ✅ Adding responsibilities dynamically
- ✅ Need to extend behavior
- ✅ Want to stack multiple enhancements

---

## Key Takeaways

### Facade Pattern:
1. **Provides simple interface** to complex subsystem
2. **Doesn't hide subsystems** - clients can still access directly if needed
3. **Reduces coupling** between client and subsystems
4. **Coordinates subsystems** for common operations

### Benefits:
```
Without Facade:
Client knows about 10 classes, 50 methods
Client code: 50 lines for one operation

With Facade:
Client knows about 1 class, 3 methods
Client code: 1 line for one operation
Complexity hidden, ease of use increased
```

### Design Principles:
- **Principle of Least Knowledge**: Talk only to close friends
- **Loose Coupling**: Client doesn't depend on subsystems
- **Encapsulation**: Hide complexity behind simple interface

---

## Implementation Checklist

- [ ] Identify complex subsystems client interacts with
- [ ] Define common high-level operations
- [ ] Create facade class with simple methods
- [ ] Facade coordinates subsystem calls
- [ ] Client uses facade instead of subsystems directly
- [ ] Optional: Allow direct subsystem access if needed

---

## Quick Reference

**Pattern Type:** Structural  
**Problem:** Complex subsystem with many interactions  
**Solution:** Unified, simplified interface that coordinates subsystems  
**When to use:** Simplify complex system, reduce coupling, provide easy-to-use API  
**Related patterns:** Adapter (converts interface), Mediator (coordinates), Abstract Factory (creates subsystems)

---

## Real Example: Python's `requests` Library

```python
# Without Facade (using urllib - complex)
import urllib.request
import urllib.parse
import json

url = "https://api.example.com/users"
data = json.dumps({"name": "John"}).encode('utf-8')
headers = {'Content-Type': 'application/json'}
req = urllib.request.Request(url, data=data, headers=headers, method='POST')
response = urllib.request.urlopen(req)
result = json.loads(response.read().decode('utf-8'))

# With Facade (requests library - simple)
import requests

result = requests.post(
    "https://api.example.com/users",
    json={"name": "John"}
).json()

# requests is a FACADE over urllib!
```

**Key insight:** Good facades make complex tasks simple while still allowing access to underlying complexity when needed.