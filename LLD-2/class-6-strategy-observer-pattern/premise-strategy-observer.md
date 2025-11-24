Here are 2 introductory quiz questions to set up Strategy and Observer patterns:

---

## Pre-Pattern Quiz: Identifying Code Smells

### Question 1: Navigation System - What's Wrong?

Look at this navigation code:

```python
class Navigator:
    def calculate_route(self, start, end, mode):
        if mode == "car":
            print("Calculating fastest car route...")
            # Use highways, avoid traffic, speed limits
        elif mode == "bike":
            print("Calculating bike route...")
            # Use bike lanes, avoid highways, elevation
        elif mode == "walk":
            print("Calculating walking route...")
            # Use sidewalks, shortest distance
        elif mode == "public":
            print("Calculating public transport...")
            # Use bus/train schedules, transfers

nav = Navigator()
nav.calculate_route("Home", "Office", "car")
```
---

**What happens when you need to add a new mode (scooter)?**

**Option A:**
```
Add another elif:
elif mode == "scooter":
    # scooter logic
```
- ✅ Easy to add
- ✅ No other changes needed

**Option B:**
```
Add another elif:
elif mode == "scooter":
    # scooter logic
```
- ❌ Must modify Navigator class
- ❌ Violates Open/Closed Principle
- ❌ Can't test scooter logic in isolation
- ❌ Risk breaking existing modes

**Option C:**
```
Create ScooterNavigator subclass
```
- ❌ Can't switch modes at runtime
- ❌ Must create new object

**Option D:**
```
Use string parameter "scooter_mode"
```
- ❌ Still requires modifying calculate_route()
- ❌ Runtime string errors possible

---

<details>
<summary>Answer</summary>

**B) Correctly identifies the problems**

---

**The Issues:**

```
┌──────────────────────────────┐
│      Navigator               │
│  ──────────────────────────  │
│  calculate_route(mode)       │
│    if car:      ← bloated    │
│    elif bike:   ← bloated    │
│    elif walk:   ← bloated    │
│    elif public: ← bloated    │
│    elif scooter: ← NEW       │
│    elif helicopter: ← NEW    │
└──────────────────────────────┘
```

**Problems:**
1. ❌ **Violates Open/Closed Principle** - Must modify existing code
2. ❌ **Hard to test** - Can't test routing algorithms separately
3. ❌ **Code duplication** - Similar validation logic repeated
4. ❌ **Runtime errors** - Typos in strings ("car" vs "cars")
5. ❌ **Grows infinitely** - More modes = bigger if-else chain

---

**What we need:**

```
Can we add new routing modes WITHOUT modifying Navigator?
Can we test each routing algorithm independently?
Can we switch algorithms at runtime?
```

**Answer:** Strategy Pattern! (Coming next...)

</details>

---

### Question 2: Stock Ticker - What's the Problem?

Look at this stock notification system:

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
---

**What's the main problem with this code?**

**Option A:**
```
Too many method calls
❌ Performance issue
```

**Option B:**
```
StockTicker knows about ALL components
❌ Tight coupling
❌ Must modify set_price() to add/remove listeners
❌ Can't disable notifications without code changes
❌ Hard to test StockTicker in isolation
❌ Circular dependencies possible
```

**Option C:**
```
Should use global variables instead
dashboard = None
mobile_app = None
```

**Option D:**
```
Should use inheritance
class DashboardTicker(StockTicker):
    pass
```

---

<details>
<summary>Answer</summary>

**B) Correctly identifies tight coupling problem**

---

**The Issues Visualized:**

```
┌─────────────────────────────────┐
│       StockTicker               │
│  ─────────────────────────────  │
│  set_price(price):              │
│    dashboard.update()      ←────┼─── Knows Dashboard
│    mobile_app.notify()     ←────┼─── Knows MobileApp
│    trading_bot.check()     ←────┼─── Knows TradingBot
│    email_service.alert()   ←────┼─── Knows EmailService
│    sms_service.send()      ←────┼─── NEW component
│    slack_bot.post()        ←────┼─── NEW component
└─────────────────────────────────┘
         TIGHT COUPLING!
```

---

**Problem 1: Must modify StockTicker for every change**

```python
# Add SMS alerts:
def set_price(self, price):
    # ... existing code ...
    email_service.send_alert(price)
    sms_service.send_sms(price)  # ← MODIFY existing method!

# Remove mobile notifications:
def set_price(self, price):
    dashboard.update(price)
    # mobile_app.push_notification(price)  ← COMMENT OUT
    trading_bot.check_price(price)
```

❌ Violates Open/Closed Principle
❌ Every listener change requires code modification
❌ Risky - might break existing functionality

---

**Problem 2: Can't disable components without code changes**

```python
# User disables mobile notifications
# Must MODIFY set_price() or use flags:

def set_price(self, price):
    dashboard.update(price)
    if mobile_enabled:  # ← Ugly conditional
        mobile_app.push_notification(price)
    # ...
```

❌ Code gets messy with flags
❌ Can't dynamically add/remove listeners

---

**Problem 3: Hard to test**

```python
# To test StockTicker, need ALL dependencies:
def test_stock_ticker():
    ticker = StockTicker()
    # Need: dashboard, mobile_app, trading_bot, email...
    ticker.set_price(100)  # Calls EVERYTHING!
```

❌ Can't test in isolation
❌ Must mock/stub all dependencies
❌ Slow tests

---

**Problem 4: Circular dependencies**

```python
# StockTicker → Dashboard
# Dashboard → StockTicker (to subscribe)
# 
# Result: Import hell! 💥
```

---

**What we need:**

```
✓ StockTicker doesn't know WHO is listening
✓ Add/remove listeners dynamically
✓ Listeners subscribe/unsubscribe themselves
✓ Easy to test
```

**Better approach:**

```
Current (Tight Coupling):
┌──────────────┐
│ StockTicker  │───► knows ───► Dashboard
│              │───► knows ───► MobileApp
│              │───► knows ───► TradingBot
└──────────────┘

Better (Observer Pattern):
┌──────────────┐
│ StockTicker  │───► notifies ───► ???
│              │                    (doesn't know who!)
└──────────────┘
         │
         └─── List of observers
              ├─ Dashboard  (subscribed)
              ├─ MobileApp  (subscribed)
              └─ TradingBot (subscribed)
```

---

**Real-world scenario:**

```python
# User story: "Add Slack notifications"

# Current approach:
def set_price(self, price):
    # ... 10 existing notifications ...
    slack_bot.post_update(price)  # ← MODIFY existing code! ❌

# What we want:
slack_observer = SlackObserver()
ticker.attach(slack_observer)  # ← Just add, don't modify! ✅
```

---

**Key Problems:**

| Issue | Impact |
|-------|--------|
| Tight coupling | Hard to change |
| Know all listeners | Violates SRP |
| Modify for changes | Violates OCP |
| Hard to test | Slow, brittle tests |
| Circular deps | Import problems |

**Answer:** Observer Pattern! (Coming next...)

</details>

---

This version clearly shows the **tight coupling** problem where StockTicker is hardcoded to know about every component it notifies!