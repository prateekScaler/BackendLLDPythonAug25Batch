# Open/Closed Principle (OCP)

## 📖 Definition

**"Software entities should be open for extension, but closed for modification."**

**Simple:** Add new features without changing existing code.

---

## 🎯 The Problem: Modifying Existing Code

```python
class DiscountCalculator:
    def apply(self, order, discount_type):
        total = order.calculate_total()
        
        if discount_type == "percentage":
            return total * 0.9
        elif discount_type == "fixed":
            return total - 10
        elif discount_type == "seasonal":
            return total * 0.85
        # Add new discount? Modify this method!
```

**Problems:**
- Must modify existing code for new discounts
- Risk breaking existing functionality
- Growing if/elif chain
- Violates OCP

---

## ✅ Solution: Extension Through Abstraction

```python
from abc import ABC, abstractmethod

# Closed for modification
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, total):
        pass

# Open for extension - add new strategies
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent):
        self.percent = percent
    
    def calculate(self, total):
        return total * (1 - self.percent)

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount):
        self.amount = amount
    
    def calculate(self, total):
        return total - self.amount

class SeasonalDiscount(DiscountStrategy):
    def __init__(self, season_percent):
        self.season_percent = season_percent
    
    def calculate(self, total):
        return total * (1 - self.season_percent)

# Add new discount? Just create new class!
class BuyOneGetOneDiscount(DiscountStrategy):
    def calculate(self, total):
        return total * 0.5

# Calculator doesn't change
class DiscountCalculator:
    def apply(self, order, strategy: DiscountStrategy):
        total = order.calculate_total()
        return strategy.calculate(total)
```

**Benefits:**
- Add discounts without changing existing code
- Each discount is independent
- Easy to test
- No if/elif chains

---

## 🚩 Signs of Violation

### Red Flags:
```python
# Growing if/elif chains
def process_payment(method):
    if method == "credit_card":
        ...
    elif method == "paypal":
        ...
    elif method == "crypto":
        ...
    # Add new method? Modify this!

# Type checking
def calculate(shape):
    if isinstance(shape, Circle):
        return math.pi * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    # Add new shape? Modify this!

# Switch statements on type
def serialize(obj):
    if obj.type == "json":
        return json.dumps(obj)
    elif obj.type == "xml":
        return to_xml(obj)
```

**Pattern:** Adding features requires modifying existing code.

---

## 💡 How to Apply OCP

### Strategy Pattern (Behavior Selection)

```python
# Bad: Modification required
class PaymentProcessor:
    def process(self, amount, method):
        if method == "card":
            # Process card
            pass
        elif method == "paypal":
            # Process PayPal
            pass

# Good: Extension through new classes
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        return f"Charging ${amount} to credit card"

class PayPalPayment(PaymentMethod):
    def process(self, amount):
        return f"Charging ${amount} via PayPal"

class PaymentProcessor:
    def process(self, amount, method: PaymentMethod):
        return method.process(amount)
```

### Template Method (Algorithm Steps)

```python
# Bad: Different methods for each type
class ReportGenerator:
    def generate_pdf(self):
        data = self.fetch_data()
        # PDF-specific formatting
        pass
    
    def generate_html(self):
        data = self.fetch_data()
        # HTML-specific formatting
        pass

# Good: Extension through inheritance
class ReportGenerator(ABC):
    def generate(self):
        data = self.fetch_data()
        formatted = self.format_data(data)
        self.save(formatted)
    
    def fetch_data(self):
        return db.query("SELECT * FROM reports")
    
    @abstractmethod
    def format_data(self, data):
        pass
    
    @abstractmethod
    def save(self, formatted):
        pass

class PDFReport(ReportGenerator):
    def format_data(self, data):
        return f"PDF: {data}"
    
    def save(self, formatted):
        write_file("report.pdf", formatted)

class HTMLReport(ReportGenerator):
    def format_data(self, data):
        return f"<html>{data}</html>"
    
    def save(self, formatted):
        write_file("report.html", formatted)
```

---

## 🎨 Practical Examples

### Example 1: Notification System

**❌ Bad (Modification Required):**
```python
class NotificationService:
    def send(self, user, message, channel):
        if channel == "email":
            smtp.send(user.email, message)
        elif channel == "sms":
            twilio.send(user.phone, message)
        elif channel == "push":
            firebase.send(user.device_id, message)
        # Add Slack? Modify this method!
```

**✅ Good (Open for Extension):**
```python
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, user, message):
        pass

class EmailChannel(NotificationChannel):
    def send(self, user, message):
        smtp.send(user.email, message)

class SMSChannel(NotificationChannel):
    def send(self, user, message):
        twilio.send(user.phone, message)

class PushChannel(NotificationChannel):
    def send(self, user, message):
        firebase.send(user.device_id, message)

class SlackChannel(NotificationChannel):  # New! No modifications needed
    def send(self, user, message):
        slack.send(user.slack_id, message)

class NotificationService:
    def __init__(self, channels: list[NotificationChannel]):
        self.channels = channels
    
    def notify(self, user, message):
        for channel in self.channels:
            channel.send(user, message)
```

---

### Example 2: Logging System

**❌ Bad:**
```python
class Logger:
    def log(self, message, destination):
        if destination == "file":
            with open("log.txt", "a") as f:
                f.write(message)
        elif destination == "console":
            print(message)
        elif destination == "database":
            db.execute("INSERT INTO logs VALUES (?)", message)
```

**✅ Good:**
```python
class LogHandler(ABC):
    @abstractmethod
    def write(self, message):
        pass

class FileHandler(LogHandler):
    def __init__(self, filename):
        self.filename = filename
    
    def write(self, message):
        with open(self.filename, "a") as f:
            f.write(message + "\n")

class ConsoleHandler(LogHandler):
    def write(self, message):
        print(message)

class DatabaseHandler(LogHandler):
    def write(self, message):
        db.execute("INSERT INTO logs VALUES (?)", message)

class CloudHandler(LogHandler):  # New handler!
    def write(self, message):
        requests.post("https://logs.cloud.com", json={"msg": message})

class Logger:
    def __init__(self, handlers: list[LogHandler]):
        self.handlers = handlers
    
    def log(self, message):
        for handler in self.handlers:
            handler.write(message)
```

---

### Example 3: Validation Rules

**❌ Bad:**
```python
class UserValidator:
    def validate(self, user):
        errors = []
        
        if not user.email or "@" not in user.email:
            errors.append("Invalid email")
        
        if not user.password or len(user.password) < 8:
            errors.append("Password too short")
        
        # Add new rule? Modify this method!
        
        return errors
```

**✅ Good:**
```python
class ValidationRule(ABC):
    @abstractmethod
    def validate(self, value):
        pass

class EmailRule(ValidationRule):
    def validate(self, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email")

class PasswordLengthRule(ValidationRule):
    def __init__(self, min_length):
        self.min_length = min_length
    
    def validate(self, password):
        if len(password) < self.min_length:
            raise ValueError(f"Password must be at least {self.min_length} chars")

class PasswordStrengthRule(ValidationRule):  # New rule!
    def validate(self, password):
        if not any(c.isupper() for c in password):
            raise ValueError("Password needs uppercase letter")

class UserValidator:
    def __init__(self, rules: list[ValidationRule]):
        self.rules = rules
    
    def validate(self, user):
        errors = []
        for rule in self.rules:
            try:
                rule.validate(user)
            except ValueError as e:
                errors.append(str(e))
        return errors
```

---

## ⚠️ When to Avoid OCP

### Don't over-engineer:

**❌ Too abstract for simple cases:**
```python
# Overkill for two options
class OutputFormat(ABC):
    @abstractmethod
    def format(self, text): pass

class UppercaseFormat(OutputFormat):
    def format(self, text): return text.upper()

class LowercaseFormat(OutputFormat):
    def format(self, text): return text.lower()

# Better: Simple function
def format_text(text, uppercase=True):
    return text.upper() if uppercase else text.lower()
```

**When abstraction isn't worth it:**
- Only 2-3 variations
- Variations unlikely to change
- Simple logic
- Throwaway code

---

## 🔧 Common Gotchas

### Gotcha 1: Predicting Wrong Abstractions
```python
# Bad: Abstract too early based on wrong assumptions
class Animal(ABC):
    @abstractmethod
    def fly(self): pass  # Not all animals fly!

# Better: Wait for actual variations
class Bird:
    def fly(self): pass

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly")
```

**Rule:** Wait for 2-3 concrete cases before abstracting.

### Gotcha 2: Over-abstraction
```python
# Too many layers
class DataSource(ABC): pass
class DatabaseDataSource(DataSource): pass
class PostgresDatabaseDataSource(DatabaseDataSource): pass
class PostgresV14DatabaseDataSource(PostgresDatabaseDataSource): pass

# Simpler
class DatabaseSource(ABC): pass
class PostgresSource(DatabaseSource): pass
```

---

## ✅ Best Practices

1. **Identify variation points** - What's likely to change?
2. **Create abstractions** - Use ABC or Protocol
3. **Implement variations** - Each as separate class
4. **Inject dependencies** - Pass concrete implementations
5. **Test each variation** - Independent unit tests

### Good Candidates for OCP:
- Payment methods
- Notification channels
- Report formats
- Validation rules
- Logging destinations
- Data sources

---

## 🎯 Quick Checklist

- [ ] New features don't modify existing classes
- [ ] Behavior varies through new classes
- [ ] No growing if/elif chains
- [ ] Easy to add new variations
- [ ] Existing code stays stable

---

## 💡 Key Takeaway

**"Extend, don't modify."**

Design for extension by using abstractions. When requirements change, add new classes instead of modifying existing ones. Existing code should be closed (stable), while system is open (extensible).