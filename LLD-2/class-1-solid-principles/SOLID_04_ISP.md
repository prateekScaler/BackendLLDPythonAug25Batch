# Interface Segregation Principle (ISP)

## 📖 Definition

**"No client should be forced to depend on methods it does not use."**

**Simple:** Many small, specific interfaces better than one large, general interface.

---

## 🎯 The Problem: Fat Interface

```python
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass


class HumanWorker(Worker):
    def work(self):
        return "Working..."
    
    def eat(self):
        return "Eating lunch..."
    
    def sleep(self):
        return "Sleeping..."


class RobotWorker(Worker):
    def work(self):
        return "Working..."
    
    def eat(self):
        pass  # Robots don't eat!
    
    def sleep(self):
        pass  # Robots don't sleep!
    # Forced to implement unused methods!
```

**Problems:**
- Robot forced to implement eat/sleep
- Interface too broad
- Clients depend on methods they don't use
- Violates ISP

---

## ✅ Solution: Segregated Interfaces

```python
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass


class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass


class Sleepable(ABC):
    @abstractmethod
    def sleep(self):
        pass


class HumanWorker(Workable, Eatable, Sleepable):
    def work(self):
        return "Working..."
    
    def eat(self):
        return "Eating..."
    
    def sleep(self):
        return "Sleeping..."


class RobotWorker(Workable):
    def work(self):
        return "Working..."
    # Only implements what it needs!


# Clients depend only on what they use
def manage_work(worker: Workable):
    worker.work()

def manage_break(worker: Eatable):
    worker.eat()
```

**Benefits:**
- Clients use only needed interfaces
- No forced implementations
- Clear responsibilities
- Easier to maintain

---

## 🚩 Signs of Violation

### Red Flag 1: Empty/Stub Implementations
```python
class Printer(ABC):
    @abstractmethod
    def print(self): pass
    
    @abstractmethod
    def scan(self): pass
    
    @abstractmethod
    def fax(self): pass

class SimplePrinter(Printer):
    def print(self):
        return "Printing..."
    
    def scan(self):
        raise NotImplementedError  # Don't have scanner!
    
    def fax(self):
        raise NotImplementedError  # Don't have fax!
```

### Red Flag 2: Large Interface with Many Methods
```python
class OrderService(ABC):
    @abstractmethod
    def create_order(self): pass
    
    @abstractmethod
    def cancel_order(self): pass
    
    @abstractmethod
    def ship_order(self): pass
    
    @abstractmethod
    def generate_invoice(self): pass
    
    @abstractmethod
    def send_confirmation(self): pass
    
    @abstractmethod
    def process_refund(self): pass
    # Too many responsibilities!
```

### Red Flag 3: Clients Using Only Part of Interface
```python
# Client only needs one method but gets forced to depend on all
def process_payment(service: OrderService):
    service.process_refund()
    # Doesn't use other 5 methods
```

---

## 💡 How to Apply ISP

### Step 1: Identify Client Needs
```python
# What does each client actually use?
# Warehouse: ship_order
# Accounting: generate_invoice, process_refund
# Customer: create_order, cancel_order
```

### Step 2: Create Role-Based Interfaces
```python
class OrderCreation(ABC):
    @abstractmethod
    def create_order(self): pass
    
    @abstractmethod
    def cancel_order(self): pass


class OrderShipping(ABC):
    @abstractmethod
    def ship_order(self): pass


class OrderAccounting(ABC):
    @abstractmethod
    def generate_invoice(self): pass
    
    @abstractmethod
    def process_refund(self): pass
```

### Step 3: Implement as Needed
```python
class OrderService(OrderCreation, OrderShipping, OrderAccounting):
    def create_order(self): pass
    def cancel_order(self): pass
    def ship_order(self): pass
    def generate_invoice(self): pass
    def process_refund(self): pass


# Clients depend only on what they need
def customer_portal(service: OrderCreation):
    service.create_order()

def warehouse_system(service: OrderShipping):
    service.ship_order()

def accounting_system(service: OrderAccounting):
    service.generate_invoice()
```

---

## 🎨 Practical Examples

### Example 1: Document System

**❌ Bad (Fat Interface):**
```python
class Document(ABC):
    @abstractmethod
    def open(self): pass
    
    @abstractmethod
    def save(self): pass
    
    @abstractmethod
    def print(self): pass
    
    @abstractmethod
    def close(self): pass


class ReadOnlyDocument(Document):
    def open(self): pass
    def close(self): pass
    
    def save(self):
        raise Exception("Read-only!")  # Forced to implement
    
    def print(self):
        raise Exception("Can't print!")  # Forced to implement
```

**✅ Good (Segregated):**
```python
class Openable(ABC):
    @abstractmethod
    def open(self): pass
    
    @abstractmethod
    def close(self): pass


class Saveable(ABC):
    @abstractmethod
    def save(self): pass


class Printable(ABC):
    @abstractmethod
    def print(self): pass


class EditableDocument(Openable, Saveable, Printable):
    def open(self): pass
    def close(self): pass
    def save(self): pass
    def print(self): pass


class ReadOnlyDocument(Openable):
    def open(self): pass
    def close(self): pass
    # Only what it needs!


# Clients use specific interfaces
def view_document(doc: Openable):
    doc.open()

def edit_document(doc: Saveable):
    doc.save()

def print_document(doc: Printable):
    doc.print()
```

---

### Example 2: Database Operations

**❌ Bad:**
```python
class Database(ABC):
    @abstractmethod
    def connect(self): pass
    
    @abstractmethod
    def disconnect(self): pass
    
    @abstractmethod
    def read(self, query): pass
    
    @abstractmethod
    def write(self, query): pass
    
    @abstractmethod
    def backup(self): pass
    
    @abstractmethod
    def restore(self): pass


class ReadOnlyDB(Database):
    def read(self, query): pass
    
    # Forced to implement methods it doesn't support
    def write(self, query):
        raise NotImplementedError
    
    def backup(self):
        raise NotImplementedError
    
    def restore(self):
        raise NotImplementedError
```

**✅ Good:**
```python
class Connectable(ABC):
    @abstractmethod
    def connect(self): pass
    
    @abstractmethod
    def disconnect(self): pass


class Readable(ABC):
    @abstractmethod
    def read(self, query): pass


class Writable(ABC):
    @abstractmethod
    def write(self, query): pass


class Backupable(ABC):
    @abstractmethod
    def backup(self): pass
    
    @abstractmethod
    def restore(self): pass


class FullDatabase(Connectable, Readable, Writable, Backupable):
    def connect(self): pass
    def disconnect(self): pass
    def read(self, query): pass
    def write(self, query): pass
    def backup(self): pass
    def restore(self): pass


class ReadOnlyDatabase(Connectable, Readable):
    def connect(self): pass
    def disconnect(self): pass
    def read(self, query): pass


# Clients use only what they need
def query_data(db: Readable):
    return db.read("SELECT * FROM users")

def update_data(db: Writable):
    db.write("UPDATE users SET ...")

def maintain_db(db: Backupable):
    db.backup()
```

---

### Example 3: Authentication System

**❌ Bad:**
```python
class AuthService(ABC):
    @abstractmethod
    def login(self): pass
    
    @abstractmethod
    def logout(self): pass
    
    @abstractmethod
    def register(self): pass
    
    @abstractmethod
    def reset_password(self): pass
    
    @abstractmethod
    def verify_email(self): pass
    
    @abstractmethod
    def enable_2fa(self): pass


# Read-only client forced to depend on all methods
def check_auth_status(auth: AuthService):
    # Only needs login, but depends on 6 methods!
    pass
```

**✅ Good:**
```python
class LoginService(ABC):
    @abstractmethod
    def login(self, username, password): pass
    
    @abstractmethod
    def logout(self): pass


class RegistrationService(ABC):
    @abstractmethod
    def register(self, user_data): pass
    
    @abstractmethod
    def verify_email(self, token): pass


class PasswordService(ABC):
    @abstractmethod
    def reset_password(self, email): pass


class TwoFactorService(ABC):
    @abstractmethod
    def enable_2fa(self): pass
    
    @abstractmethod
    def verify_2fa(self, code): pass


class AuthSystem(LoginService, RegistrationService, PasswordService, TwoFactorService):
    # Implements all
    pass


# Clients use specific interfaces
def authenticate(service: LoginService):
    service.login("user", "pass")

def register_user(service: RegistrationService):
    service.register(user_data)

def recover_account(service: PasswordService):
    service.reset_password("email@example.com")
```

---

## ⚠️ When to Avoid ISP

### Don't over-segregate:

**❌ Too granular:**
```python
class Nameable(ABC):
    @abstractmethod
    def get_name(self): pass

class Ageable(ABC):
    @abstractmethod
    def get_age(self): pass

class Emailable(ABC):
    @abstractmethod
    def get_email(self): pass

# Too many tiny interfaces!
```

**✅ Reasonable grouping:**
```python
class UserInfo(ABC):
    @abstractmethod
    def get_name(self): pass
    
    @abstractmethod
    def get_age(self): pass
    
    @abstractmethod
    def get_email(self): pass

# Cohesive group of related methods
```

**Guidelines:**
- Group related methods
- Consider actual client usage
- Balance with pragmatism

---

## 🔧 Common Gotchas

### Gotcha 1: Premature Segregation
```python
# Don't split before seeing actual need
# Wait for 2-3 concrete implementations
```

### Gotcha 2: Mixing Concerns
```python
# Bad - mixing authentication and authorization
class SecurityService(ABC):
    @abstractmethod
    def login(self): pass
    
    @abstractmethod
    def check_permission(self): pass

# Good - separate concerns
class Authentication(ABC):
    @abstractmethod
    def login(self): pass

class Authorization(ABC):
    @abstractmethod
    def check_permission(self): pass
```

---

## ✅ Best Practices

1. **Role-based interfaces** - Design per client role
2. **Cohesive methods** - Group related operations
3. **Client-first design** - Start from client needs
4. **Avoid marker interfaces** - Empty interfaces are red flag
5. **Composition over fat interfaces** - Multiple small > one large

---

## 🎯 Quick Checklist

- [ ] No empty/stub method implementations
- [ ] Clients use all methods they depend on
- [ ] Interfaces focused on single role
- [ ] Easy to add new implementations
- [ ] No NotImplementedError in concrete classes

---

## 💡 Key Takeaway

**"Clients shouldn't see what they don't need."**

Design interfaces based on client needs, not provider capabilities. Many small, focused interfaces are better than one large, general interface. This makes systems more flexible, maintainable, and easier to test.

**Rule of thumb:** If a client only uses 1-2 methods of a 10-method interface, split it.