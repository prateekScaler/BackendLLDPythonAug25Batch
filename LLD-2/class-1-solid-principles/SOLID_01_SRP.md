# Single Responsibility Principle (SRP)

## 📖 Definition

**"A class should have one, and only one, reason to change."**

**Simple:** Each class does one thing well.

---

## 🎯 The Problem: God Class

```python
class Order:
    def __init__(self, items):
        self.items = items
        self.status = "pending"
    
    def process(self):
        # Responsibility 1: Calculate total
        total = sum(item.price * item.quantity for item in self.items)
        
        # Responsibility 2: Apply discount
        if total > 100:
            total *= 0.9
        
        # Responsibility 3: Save to database
        db.execute("INSERT INTO orders VALUES (?)", total)
        
        # Responsibility 4: Send notification
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.send(f"Order total: ${total}")
        
        # Responsibility 5: Log
        logging.info(f"Order processed: {total}")
        
        return total
```

**Why is this bad?**
- **5 reasons to change** (calculation, discount, DB, email, logging)
- Hard to test (needs real DB, SMTP)
- Can't reuse parts independently
- Changes ripple everywhere

---

## ✅ Solution: Separate Responsibilities

```python
# Responsibility 1: Order data and calculation
class Order:
    def __init__(self, items):
        self.items = items
        self.status = "pending"
    
    def calculate_total(self):
        return sum(item.price * item.quantity for item in self.items)


# Responsibility 2: Discount rules
class DiscountCalculator:
    def apply(self, total):
        if total > 100:
            return total * 0.9
        return total


# Responsibility 3: Database operations
class OrderRepository:
    def save(self, order):
        db.execute("INSERT INTO orders VALUES (?)", order)


# Responsibility 4: Notifications
class EmailNotifier:
    def send_confirmation(self, order, total):
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.send(f"Order total: ${total}")


# Responsibility 5: Logging
class OrderLogger:
    def log_processed(self, order_id, total):
        logging.info(f"Order {order_id} processed: ${total}")


# Orchestrator (single responsibility: coordinate)
class OrderProcessor:
    def __init__(self, repository, notifier, logger, discount):
        self.repository = repository
        self.notifier = notifier
        self.logger = logger
        self.discount = discount
    
    def process(self, order):
        total = order.calculate_total()
        total = self.discount.apply(total)
        self.repository.save(order)
        self.notifier.send_confirmation(order, total)
        self.logger.log_processed(order.id, total)
```

**Benefits:**
- Each class has **one reason to change**
- Easy to test (mock dependencies)
- Can reuse components
- Clear responsibilities

---

## 🚩 Signs of Violation

### Red Flags:
```python
class UserManager:
    def create_user(self):      # User management
        pass
    
    def send_email(self):       # Email handling
        pass
    
    def log_activity(self):     # Logging
        pass
    
    def validate_data(self):    # Validation
        pass
```

**Spot the violations:**
- Class name with "Manager", "Handler", "Service" (often god classes)
- Methods doing unrelated things
- Many import statements (uses many dependencies)
- Long methods (doing too much) - also called as monster methods
- If/elif chains for different responsibilities

### Quick Test:
**Ask:** "How many reasons would this class have to change?"
- Discount logic changes? → Change!
- Database changes? → Change!
- Email provider changes? → Change!

**If > 1, it violates SRP.**

---

## 💡 How to Apply SRP

### Step 1: Identify Responsibilities
```python
# List what the class does:
# 1. Calculate order total
# 2. Apply discounts
# 3. Save to database
# 4. Send email
# 5. Log events
```

### Step 2: Group Related Behaviors
```python
# Core domain: Order, Item
# Calculation: DiscountCalculator
# Persistence: OrderRepository
# Notification: EmailNotifier
# Infrastructure: Logger
```

### Step 3: Extract into Classes
```python
# One class per responsibility
class Order: ...
class DiscountCalculator: ...
class OrderRepository: ...
```

### Step 4: Use Dependency Injection
```python
class OrderProcessor:
    def __init__(self, repo, notifier, logger):
        self.repo = repo
        self.notifier = notifier
        self.logger = logger
```

---

## 🎨 Practical Examples

### Example 1: Report Generation

**❌ Bad:**
```python
class Report:
    def generate(self, data):
        # Fetch data
        data = db.query("SELECT * FROM sales")
        
        # Calculate metrics
        total = sum(row['amount'] for row in data)
        
        # Format report
        html = f"<h1>Total: ${total}</h1>"
        
        # Send email
        smtp.send(html)
        
        # Save to file
        with open("report.html", "w") as f:
            f.write(html)
```

**✅ Good:**
```python
class SalesDataFetcher:
    def fetch(self):
        return db.query("SELECT * FROM sales")


class SalesCalculator:
    def calculate_total(self, data):
        return sum(row['amount'] for row in data)


class ReportFormatter:
    def format_html(self, total):
        return f"<h1>Total: ${total}</h1>"


class ReportSender:
    def send_email(self, html):
        smtp.send(html)


class ReportSaver:
    def save_to_file(self, html, filename):
        with open(filename, "w") as f:
            f.write(html)


class ReportGenerator:
    def __init__(self, fetcher, calculator, formatter, sender, saver):
        self.fetcher = fetcher
        self.calculator = calculator
        self.formatter = formatter
        self.sender = sender
        self.saver = saver
    
    def generate(self):
        data = self.fetcher.fetch()
        total = self.calculator.calculate_total(data)
        html = self.formatter.format_html(total)
        self.sender.send_email(html)
        self.saver.save_to_file(html, "report.html")
```

---

## ⚠️ When to Avoid SRP

### Don't over-apply:

**❌ Too granular:**
```python
class UserFirstNameGetter:
    def get(self, user):
        return user.first_name

class UserLastNameGetter:
    def get(self, user):
        return user.last_name
```

**✅ Reasonable:**
```python
class User:
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
```

**Guidelines:**
- Don't split for the sake of splitting
- Keep cohesive behaviors together
- Balance with pragmatism

---

## 🔧 Common Gotchas

### Gotcha 1: Over-engineering Simple Code
```python
# Overkill for simple script
class DataReader: ...
class DataValidator: ...
class DataProcessor: ...
class DataWriter: ...

# Better for simple case
def process_data(filename):
    data = read_file(filename)
    result = calculate(data)
    write_file(result)
```

### Gotcha 2: Misunderstanding "Responsibility"
```python
# This is fine - cohesive responsibility
class Order:
    def add_item(self, item): ...
    def remove_item(self, item): ...
    def calculate_total(self): ...
```

**"Responsibility" = reason to change, not number of methods**

---

## ✅ Best Practices

1. **Ask "Why would this change?"** - If multiple reasons, split it
2. **Look at imports** - Many imports = doing too much
3. **Check method names** - Unrelated names = separate responsibilities
4. **Use dependency injection** - Makes responsibilities clear
5. **Start cohesive, split when needed** - Don't pre-optimize

---

## 🎯 Quick Checklist

- [ ] Class has one primary purpose
- [ ] Changes in one area don't affect others
- [ ] Can describe class in one sentence
- [ ] Easy to test in isolation
- [ ] Can reuse independently

---

## 💡 Key Takeaway

**"Do one thing, do it well."**

Each class should have a single, well-defined purpose. When requirements change, only the relevant class should need modification.