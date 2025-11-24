# Observer Pattern

> Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

## Quick Start

```python
from observer_demo import StockTicker, DashboardDisplay, TradingBot

# Create subject
stock = StockTicker("AAPL")

# Create and attach observers
stock.attach(DashboardDisplay())
stock.attach(TradingBot(buy_threshold=140, sell_threshold=160))

# Change triggers notification to all observers
stock.price = 155.00
```

## Structure

```
Subject ──────┬──────► Observer (interface)
              │              │
              │       ┌──────┼──────┐
              │       ▼      ▼      ▼
              │   Observer Observer Observer
              │       A        B       C
              │
        attach()
        detach()
        notify()
```

## When to Use

| Situation | Use Observer? |
|-----------|---------------|
| One-to-many state changes | ✅ Yes |
| Loose coupling needed | ✅ Yes |
| Simple 1:1 communication | ❌ Overkill |
| Order of updates matters | ⚠️ Consider alternatives |

## Key Insight

**Publish-Subscribe** - Subject publishes changes, observers subscribe to receive them. Neither knows details about the other.

# The Observer Pattern

## Part 1: The Problem

You're building a stock trading app. When stock prices change, multiple components need updates:

```python
class StockTicker:
    def __init__(self):
        self.price = 0
    
    def set_price(self, price):
        self.price = price
        # Now what? Who needs to know?
        
        # Dashboard needs update
        dashboard.update(price)
        
        # Mobile app needs notification
        mobile_app.push_notification(price)
        
        # Trading bot needs to check
        trading_bot.check_price(price)
        
        # Email alerts
        email_service.send_alert(price)
        
        # More and more components...
```

**What's wrong?**

```
┌─────────────────────────────────────┐
│          StockTicker                │
│  ─────────────────────────────────  │
│  set_price():                       │
│    dashboard.update()      ← TIGHT  │
│    mobile_app.notify()     ← COUPLING│
│    trading_bot.check()     ← TO     │
│    email_service.alert()   ← EVERYTHING│
│    sms_service.send()      ← NEW    │
│    slack_bot.post()        ← NEW    │
└─────────────────────────────────────┘
```

**Problems:**
1. **Tight coupling** - StockTicker knows about ALL dependent components
2. **Hard to extend** - Adding new listeners requires modifying StockTicker
3. **Hard to remove** - Removing a listener requires code changes
4. **Circular dependencies** - Everything depends on everything

---

## Part 2: First Attempt - Callback List

"Let's just keep a list of callbacks!"

```python
class StockTicker:
    def __init__(self):
        self.price = 0
        self.callbacks = []  # List of functions
    
    def register(self, callback):
        self.callbacks.append(callback)
    
    def set_price(self, price):
        self.price = price
        for callback in self.callbacks:
            callback(price)

# Usage
ticker = StockTicker()
ticker.register(lambda p: print(f"Dashboard: ${p}"))
ticker.register(lambda p: print(f"Mobile: ${p}"))
ticker.set_price(150.50)
```

**Better!** But problems remain:

```python
# Problem 1: How to unregister?
def my_handler(price):
    print(f"Price: {price}")

ticker.register(my_handler)
# Later...
ticker.callbacks.remove(my_handler)  # Works, but messy

# Problem 2: No structure - just raw functions
# Can't add methods like pause(), get_state(), etc.

# Problem 3: Lambda can't be removed
ticker.register(lambda p: print(p))  # Can't remove this!
```

**Flaw:** No proper interface for observers. Just raw functions.

---

## Part 3: The Insight

**Define a contract between Subject and Observers.**

```
Subject (Publisher)          Observer (Subscriber)
────────────────────         ─────────────────────
- Maintains observer list    - Has update() method
- Notifies all observers     - Reacts to notifications
- Doesn't know WHO they are  - Can subscribe/unsubscribe
```

**Key Principle:** Subject doesn't care WHAT observers do - just that they have an `update()` method.

```
           ┌─────────────┐
           │  Subject    │
           │  (Stock)    │
           └──────┬──────┘
                  │ notifies
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │Dashboard│ │ Mobile  │ │  Bot    │
   │Observer │ │Observer │ │Observer │
   └─────────┘ └─────────┘ └─────────┘
   
   All implement: update(data)
```

---

## Part 4: Observer Pattern Implementation

### Step 1: Define the Observer Interface

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, data: dict) -> None:
        """Called when subject state changes."""
        pass
```

### Step 2: Define the Subject Interface

```python
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Subscribe an observer."""
        pass
    
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Unsubscribe an observer."""
        pass
    
    @abstractmethod
    def notify(self) -> None:
        """Notify all observers."""
        pass
```

### Step 3: Implement Concrete Subject

```python
class StockTicker(Subject):
    def __init__(self, symbol: str):
        self.symbol = symbol
        self._price = 0.0
        self._observers: list[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"📎 {observer.__class__.__name__} subscribed to {self.symbol}")
    
    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"📌 {observer.__class__.__name__} unsubscribed from {self.symbol}")
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update({
                "symbol": self.symbol,
                "price": self._price
            })
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, value: float):
        old_price = self._price
        self._price = value
        print(f"\n📈 {self.symbol}: ${old_price:.2f} → ${value:.2f}")
        self.notify()  # Automatically notify on change!
```

### Step 4: Implement Concrete Observers

```python
class DashboardDisplay(Observer):
    def update(self, data: dict) -> None:
        print(f"  🖥️  Dashboard: {data['symbol']} is now ${data['price']:.2f}")


class MobileApp(Observer):
    def update(self, data: dict) -> None:
        print(f"  📱 Mobile Push: {data['symbol']} price changed to ${data['price']:.2f}")


class TradingBot(Observer):
    def __init__(self, buy_threshold: float, sell_threshold: float):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
    
    def update(self, data: dict) -> None:
        price = data['price']
        symbol = data['symbol']
        
        if price < self.buy_threshold:
            print(f"  🤖 Bot: BUY {symbol} at ${price:.2f} (below ${self.buy_threshold})")
        elif price > self.sell_threshold:
            print(f"  🤖 Bot: SELL {symbol} at ${price:.2f} (above ${self.sell_threshold})")
        else:
            print(f"  🤖 Bot: HOLD {symbol} at ${price:.2f}")


class EmailAlert(Observer):
    def __init__(self, email: str, threshold: float):
        self.email = email
        self.threshold = threshold
    
    def update(self, data: dict) -> None:
        if data['price'] > self.threshold:
            print(f"  📧 Email to {self.email}: {data['symbol']} exceeded ${self.threshold}!")
```

### Step 5: Use It!

```python
# Create subject
apple_stock = StockTicker("AAPL")

# Create observers
dashboard = DashboardDisplay()
mobile = MobileApp()
bot = TradingBot(buy_threshold=140, sell_threshold=160)
alert = EmailAlert("trader@email.com", threshold=155)

# Subscribe
apple_stock.attach(dashboard)
apple_stock.attach(mobile)
apple_stock.attach(bot)
apple_stock.attach(alert)

# Price changes - all observers notified automatically!
apple_stock.price = 145.00
apple_stock.price = 158.00
apple_stock.price = 162.00

# Unsubscribe mobile (user disabled notifications)
apple_stock.detach(mobile)

apple_stock.price = 138.00  # Mobile won't receive this
```

---

## Part 5: Complete UML Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│    ┌────────────────────────┐         ┌────────────────────────┐   │
│    │    <<interface>>       │         │    <<interface>>       │   │
│    │       Subject          │         │       Observer         │   │
│    │ ────────────────────── │         │ ────────────────────── │   │
│    │ + attach(observer)     │◄────────│ + update(data)         │   │
│    │ + detach(observer)     │         └────────────────────────┘   │
│    │ + notify()             │                    △                  │
│    └────────────────────────┘                    │                  │
│               △                                   │                  │
│               │                     ┌────────────┼────────────┐    │
│               │                     │            │            │    │
│    ┌──────────────────────┐   ┌─────────┐  ┌─────────┐  ┌─────────┐│
│    │     StockTicker      │   │Dashboard│  │ Mobile  │  │  Bot    ││
│    │ ──────────────────── │   │ Display │  │   App   │  │         ││
│    │ - symbol: str        │   │─────────│  │─────────│  │─────────││
│    │ - price: float       │   │+update()│  │+update()│  │+update()││
│    │ - observers: list    │   └─────────┘  └─────────┘  └─────────┘│
│    │ ──────────────────── │                                         │
│    │ + attach(observer)   │                                         │
│    │ + detach(observer)   │                                         │
│    │ + notify()           │                                         │
│    └──────────────────────┘                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Push vs Pull Model

### Push Model (what we implemented)
Subject sends data TO observers:

```python
def notify(self):
    for observer in self._observers:
        observer.update({"symbol": self.symbol, "price": self._price})
        #              ↑ Data pushed to observer
```

### Pull Model
Subject notifies, observer fetches what it needs:

```python
# Subject
def notify(self):
    for observer in self._observers:
        observer.update(self)  # Pass self reference
        #              ↑ Observer pulls data from subject

# Observer
def update(self, subject: StockTicker):
    price = subject.price  # Pull only what you need
    symbol = subject.symbol
```

**When to use which:**

| Push | Pull |
|------|------|
| Observers need same data | Observers need different data |
| Simple, direct | More flexible |
| Subject controls data | Observer controls data |

---

## Part 7: Benefits

```
BEFORE (Tight Coupling)          AFTER (Observer Pattern)
─────────────────────────        ─────────────────────────
Subject knows all observers      Subject knows only interface
Hard to add new observers        Add observers dynamically
Hard to remove observers         Remove observers anytime
Circular dependencies            One-way dependency
```

**Real-World Examples:**
- Event listeners in JavaScript
- Django signals
- React state management
- Message queues (Pub/Sub)

---

## Part 8: When to Use Observer

**✅ Use when:**
- Changes in one object require changing others
- You don't know how many objects need to change
- An object should notify others without knowing who
- You need loose coupling

**❌ Don't use when:**
- Simple one-to-one communication
- Order of notification matters
- Observers need guaranteed delivery

---

## Part 9: Quick Reference

```python
# 1. Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

# 2. Subject Interface
class Subject(ABC):
    @abstractmethod
    def attach(self, observer): pass
    
    @abstractmethod
    def detach(self, observer): pass
    
    @abstractmethod
    def notify(self): pass

# 3. Concrete Subject
class ConcreteSubject(Subject):
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for obs in self._observers:
            obs.update(self._state)

# 4. Concrete Observer
class ConcreteObserver(Observer):
    def update(self, data):
        # React to change
        pass
```

**Key Point:** Observer defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified automatically.


Here are the concise real-world use cases for Observer Pattern:

---

## Part 11: Real-World Use Cases

### 🎯 LLD Interview Scenarios

#### 1. Stock Trading Platform
```python
class StockExchange:
    def __init__(self):
        self._observers = []
        self._stocks = {}
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def update_stock_price(self, symbol, price):
        self._stocks[symbol] = price
        self.notify(symbol, price)

# Observers: TradingBot, PriceAlert, Portfolio, Chart, NewsService
# When price changes → all observers notified automatically
```

**Why Observer?**
- Multiple components need real-time price updates
- Loose coupling - StockExchange doesn't know who's watching
- Easy to add new observers (analytics, ML models)

**Interview Gold:** "Design a real-time stock ticker system"

---

#### 2. Notification System (Push Notifications)
```python
class User:
    def __init__(self):
        self._observers = []  # Email, SMS, Push, Slack
    
    def notify_followers(self, event):
        for observer in self._observers:
            observer.update(event)

# Use Case: Social Media
# User posts → followers get notifications
# User goes live → subscribers alerted
```

**LLD Questions:**
- "Design Instagram notification system"
- "Implement Twitter follower feed updates"

---

#### 3. Event-Driven Microservices
```python
class OrderService:
    def place_order(self, order):
        # Process order
        self.notify_observers("ORDER_PLACED", order)

# Observers:
# - PaymentService → processes payment
# - InventoryService → updates stock
# - ShippingService → prepares shipment
# - NotificationService → emails customer
# - AnalyticsService → tracks metrics
```

**Real Interview:** "Design event-driven e-commerce system"

---

#### 4. Weather Monitoring System
```python
class WeatherStation:
    def __init__(self):
        self._observers = []
        self._temperature = 0
    
    def set_temperature(self, temp):
        self._temperature = temp
        self.notify()

# Observers:
# - PhoneDisplay (current conditions)
# - WebDisplay (forecast)
# - StatsDisplay (historical data)
# - AlertService (extreme weather warnings)
```

**Classic GoF Example** - Often asked in interviews

---

### 💼 Software Engineering Use Cases

#### 1. UI Event Handling (Frontend)
```python
class Button:
    def __init__(self):
        self._click_listeners = []
    
    def on_click(self, listener):
        self._click_listeners.append(listener)
    
    def click(self):
        for listener in self._click_listeners:
            listener.handle_click()

# JavaScript equivalent: addEventListener
button.addEventListener('click', handler1)
button.addEventListener('click', handler2)
```

**Real Use:**
- React state management (Redux, MobX)
- Angular/Vue reactive data binding
- Event-driven JavaScript

---

#### 2. Log Aggregation System
```python
class LogManager:
    def __init__(self):
        self._handlers = []
    
    def add_handler(self, handler: LogHandler):
        self._handlers.append(handler)
    
    def log(self, level, message):
        for handler in self._handlers:
            handler.handle(level, message)

# Handlers:
# - ConsoleHandler (dev environment)
# - FileHandler (production logs)
# - ElasticsearchHandler (centralized logging)
# - SlackHandler (critical errors)
# - SentryHandler (error tracking)
```

**Production Scenario:**
```python
logger = LogManager()
logger.add_handler(ConsoleHandler())
logger.add_handler(FileHandler("/var/log/app.log"))
logger.add_handler(SentryHandler())

logger.log("ERROR", "Database connection failed")
# All handlers notified → console, file, Sentry
```

---

#### 3. Model-View-Controller (MVC)
```python
class Model:
    def __init__(self):
        self._views = []  # Observers
        self._data = None
    
    def set_data(self, data):
        self._data = data
        self.notify_views()  # All views update automatically

# Views: WebView, MobileView, DashboardView, APIResponse
```

**Framework Examples:**
- Django signals
- Spring Framework events
- Android LiveData/ViewModel

---

#### 4. Chat Application
```python
class ChatRoom:
    def __init__(self):
        self._participants = []  # Observers
    
    def join(self, user):
        self._participants.append(user)
    
    def send_message(self, sender, message):
        for user in self._participants:
            if user != sender:
                user.receive_message(sender, message)

# Observers: User1, User2, User3, ... UserN
# One sends → all others notified
```

**Real Apps:** Slack, Discord, WhatsApp group chats

---

#### 5. Game Development
```python
class GameEventManager:
    def __init__(self):
        self._listeners = {}
    
    def subscribe(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
    
    def publish(self, event_type, data):
        for listener in self._listeners.get(event_type, []):
            listener.on_event(data)

# Events: PLAYER_DIED, LEVEL_UP, ITEM_COLLECTED, BOSS_DEFEATED
# Observers: ScoreSystem, AchievementSystem, UIManager, SoundManager
```

**Use Case:**
```python
game.subscribe("PLAYER_DIED", RespawnSystem())
game.subscribe("PLAYER_DIED", DeathSoundEffect())
game.subscribe("PLAYER_DIED", StatisticsTracker())

game.publish("PLAYER_DIED", player_data)
# All systems react to death event
```

---

#### 6. CI/CD Pipeline
```python
class BuildPipeline:
    def __init__(self):
        self._observers = []
    
    def run_build(self):
        result = self.compile_and_test()
        self.notify("BUILD_COMPLETE", result)

# Observers:
# - SlackNotifier → posts to #builds channel
# - EmailNotifier → emails team
# - JiraIntegration → updates tickets
# - DeploymentService → auto-deploys if tests pass
```

**Real Tools:** Jenkins, GitLab CI, GitHub Actions

---

### 🏢 Industry-Specific Examples

#### E-commerce
```python
class Inventory:
    def update_stock(self, product_id, quantity):
        # Update database
        self.notify("STOCK_CHANGED", product_id, quantity)

# Observers:
# - WebsiteDisplay → shows "Out of Stock"
# - WishlistService → notifies waiting customers
# - AnalyticsService → tracks demand
# - ReorderService → triggers supplier order
```

#### IoT/Smart Home
```python
class TemperatureSensor:
    def set_temperature(self, temp):
        self._temperature = temp
        self.notify(temp)

# Observers:
# - Thermostat → adjusts heating/cooling
# - MobileApp → updates dashboard
# - AlertService → warns if too hot/cold
# - DataLogger → stores for analysis
```

#### Financial Systems
```python
class Account:
    def withdraw(self, amount):
        self._balance -= amount
        self.notify("TRANSACTION", amount)

# Observers:
# - FraudDetection → checks for suspicious activity
# - NotificationService → SMS/email confirmation
# - AccountingSystem → updates ledger
# - TaxCalculator → tracks taxable transactions
```

---

### 📊 When Observer Pattern Shines

| Scenario | Why Observer? |
|----------|---------------|
| **One-to-Many Updates** | One change affects multiple components |
| **Event Broadcasting** | Publish events, subscribers react |
| **Loose Coupling** | Subject doesn't know observers |
| **Dynamic Subscriptions** | Add/remove observers at runtime |
| **Reactive Systems** | Real-time updates (dashboards, feeds) |

---

### 🎤 Interview Tips

**Question:** "How is Observer different from Pub/Sub?"

**Answer:**
```
Observer Pattern:
Subject ──directly──► Observers
(subject knows observer interface)

Pub/Sub Pattern:
Publisher ──► MessageBroker ──► Subscribers
           (completely decoupled)
```

**Observer:** Subject maintains list of observers
**Pub/Sub:** Message broker (Kafka, RabbitMQ) handles routing

---

**Question:** "What are the drawbacks of Observer?"

**Answer:**
1. **Memory Leaks** - Forgot to unsubscribe
```python
observer = PriceAlert()
ticker.attach(observer)
# Later: forget to detach → memory leak
```

2. **Unpredictable Order** - No guarantee which observer runs first
```python
# Both observers modify shared state - race condition!
ticker.attach(observer1)
ticker.attach(observer2)
```

3. **Notification Storms** - Too many updates
```python
# Price updates 1000 times/sec → 1000 notifications!
for i in range(1000):
    ticker.set_price(i)  # Each triggers all observers
```

**Solutions:**
- Use weak references (Python: `weakref`)
- Implement update batching/debouncing
- Priority-based observer ordering

---

### 🔥 Common Interview Variations

#### 1. Push vs Pull Model

**Push (what we've seen):**
```python
def notify(self, data):
    for observer in self._observers:
        observer.update(data)  # Push data to observer
```

**Pull:**
```python
def notify(self):
    for observer in self._observers:
        observer.update(self)  # Observer pulls what it needs

class Observer:
    def update(self, subject):
        data = subject.get_data()  # Pull data
```

**When to use:**
- Push: Observers need same data
- Pull: Observers need different data

---

#### 2. Event Types

```python
class EventManager:
    def __init__(self):
        self._subscribers = {}
    
    def subscribe(self, event_type, observer):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(observer)
    
    def publish(self, event_type, data):
        for observer in self._subscribers.get(event_type, []):
            observer.update(data)

# Subscribe to specific events
manager.subscribe("ORDER_PLACED", email_service)
manager.subscribe("ORDER_PLACED", inventory_service)
manager.subscribe("PAYMENT_FAILED", alert_service)
```

---

### 🎯 Quick Comparison

| Pattern | Use Case |
|---------|----------|
| **Observer** | Stock price updates |
| **Strategy** | Sorting algorithms |
| **Factory** | Create payment objects |
| **Singleton** | Database connection |
| **Adapter** | Legacy API integration |

---

**Key Takeaway for Interviews:**

> "Observer pattern defines a one-to-many dependency where when one object (subject) changes state, all its dependents (observers) are notified automatically. It's perfect for event-driven systems, real-time updates, and when you need loose coupling between components."

**Mention Real Examples:** "Like how React uses observers for state management, or how message queues like Kafka implement pub/sub using observer pattern principles."