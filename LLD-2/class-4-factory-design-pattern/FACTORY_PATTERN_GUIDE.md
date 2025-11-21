# Factory Design Pattern Family

> **Note for Students:** In the real world, many developers use "Factory Pattern" loosely without distinguishing between Simple Factory, Factory Method, and Abstract Factory. 
- You'll be perfectly fine knowing Simple Factory or Factory Method for most situations. Abstract Factory is more advanced and useful for specific scenarios. However, understanding all three will help you recognize them in codebases and interviews.

---

## 📖 Core Concept

**Factory Patterns centralize object creation logic, making code more flexible, maintainable, and testable.**

Instead of:
```python
# ❌ Creating objects directly everywhere
obj = ConcreteClass()
```

Do this:
```python
# ✅ Let a factory decide which object to create
obj = Factory.create()
```

---

## 🎯 The Evolution: Three Patterns

We'll build from the simplest to the most complex:

1. **Simple Factory** - Basic centralized creation
2. **Factory Method** - Extensible factory with inheritance
3. **Abstract Factory** - Families of related objects

Let's see how each solves different problems!

---

## 1. Simple Factory

### The Problem

```python
# Notification system - creating objects everywhere
def send_welcome_message(user, channel):
    if channel == "email":
        notif = EmailNotification(user.email)
    elif channel == "sms":
        notif = SMSNotification(user.phone)
    elif channel == "push":
        notif = PushNotification(user.device_id)
    
    notif.send("Welcome!")

def send_reminder(user, channel):
    # Same creation logic duplicated!
    if channel == "email":
        notif = EmailNotification(user.email)
    elif channel == "sms":
        notif = SMSNotification(user.phone)
    # ...

# Problems:
# ❌ Creation logic duplicated everywhere
# ❌ Hard to add new notification types
# ❌ Violates DRY (Don't Repeat Yourself)
```

### The Solution: Simple Factory

**Centralize object creation in one place.**

```python
# Step 1: Define common interface
class Notification:
    def send(self, message):
        raise NotImplementedError

# Step 2: Concrete implementations
class EmailNotification(Notification):
    def __init__(self, email):
        self.email = email
    
    def send(self, message):
        print(f"Email to {self.email}: {message}")

class SMSNotification(Notification):
    def __init__(self, phone):
        self.phone = phone
    
    def send(self, message):
        print(f"SMS to {self.phone}: {message}")

class PushNotification(Notification):
    def __init__(self, device_id):
        self.device_id = device_id
    
    def send(self, message):
        print(f"Push to {self.device_id}: {message}")

# Step 3: Simple Factory - centralized creation
class NotificationFactory:
    @staticmethod
    def create(channel: str, recipient: str) -> Notification:
        if channel == "email":
            return EmailNotification(recipient)
        elif channel == "sms":
            return SMSNotification(recipient)
        elif channel == "push":
            return PushNotification(recipient)
        else:
            raise ValueError(f"Unknown channel: {channel}")

# Usage - clean and simple!
def send_welcome_message(user, channel):
    notif = NotificationFactory.create(channel, user.email)
    notif.send("Welcome!")

def send_reminder(user, channel):
    notif = NotificationFactory.create(channel, user.email)
    notif.send("Reminder!")

# Benefits:
# ✅ Creation logic in one place
# ✅ Easy to maintain
# ✅ Consistent object creation
```

### Simple Factory Diagram

```
Client Code
    ↓
    calls create()
    ↓
┌─────────────────────┐
│ NotificationFactory │
│  (Simple Factory)   │
│                     │
│  + create(type)     │
└─────────────────────┘
    ↓ returns
    ↓
┌──────────────┐
│ Notification │ (interface)
└──────────────┘
    ↑ implements
    │
┌───────────┬─────────────┬──────────────┐
│   Email   │     SMS     │     Push     │
│Notification│Notification │Notification  │
└───────────┴─────────────┴──────────────┘
```

### When to Use Simple Factory

✅ **Use when:**
- Need centralized object creation
- Have multiple related classes to create
- Creation logic is straightforward (if-else is fine)
- Want to hide concrete class names from clients

❌ **Don't use when:**
- Need to extend with new types WITHOUT modifying factory
- Have complex inheritance hierarchies
- Need families of related objects

### Real-World Use Cases

1. **Database Connection Factory**
   - Input: "mysql", "postgresql", "mongodb"
   - Output: Appropriate database connection object

2. **File Parser Factory**
   - Input: ".json", ".xml", ".csv"
   - Output: Appropriate parser object

3. **Logger Factory**
   - Input: "file", "console", "syslog"
   - Output: Appropriate logger object

4. **Payment Gateway Factory**
   - Input: "stripe", "paypal", "square"
   - Output: Appropriate payment gateway object

---

## 2. Factory Method

### The Problem with Simple Factory

```python
# Simple Factory is great, but...
class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        if channel == "email":
            return EmailNotification()
        elif channel == "sms":
            return SMSNotification()
        # ...

# Problem: Want to add Discord notifications?
# Have to MODIFY the factory! Violates Open-Closed Principle
class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        if channel == "email":
            return EmailNotification()
        elif channel == "sms":
            return SMSNotification()
        elif channel == "discord":  # Modified existing code!
            return DiscordNotification()
```

### The Solution: Factory Method

**Let subclasses decide which object to create.**

```python
from abc import ABC, abstractmethod

# Step 1: Abstract creator with factory method
class NotificationFactory(ABC):
    """Abstract class with factory method"""
    
    @abstractmethod
    def create_notification(self) -> Notification:
        """Factory method - subclasses implement this"""
        pass
    
    def send_notification(self, message: str):
        """Template method using factory method"""
        notification = self.create_notification()
        notification.send(message)
        self.log(f"Sent via {notification.__class__.__name__}")
    
    def log(self, message: str):
        print(f"[LOG] {message}")

# Step 2: Concrete creators - each creates specific notification
class EmailNotificationFactory(NotificationFactory):
   
    def create_notification(self) -> Notification:
        return EmailNotification("user@example.com")

class SMSNotificationFactory(NotificationFactory):
   
    def create_notification(self) -> Notification:
        return SMSNotification("+1234567890")

class PushNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return PushNotification("device_123")

# Step 3: Want to add Discord? Just add new class!
class DiscordNotificationService(NotificationService):
    def create_notification(self) -> Notification:
        return DiscordNotification("server_xyz")
    # No need to modify existing code! ✅

# Usage
def notify_user(service: NotificationService, message: str):
    service.send_notification(message)

# Client code works with abstract service
email_service = EmailNotificationService()
sms_service = SMSNotificationService()
discord_service = DiscordNotificationService()  # New! No changes to existing code

notify_user(email_service, "Hello via Email")
notify_user(sms_service, "Hello via SMS")
notify_user(discord_service, "Hello via Discord")
```

### Factory Method Diagram

```
┌─────────────────────────┐
│  NotificationFactory   │ (Abstract Creator)
│  ─────────────────────  │
│  + send_notification()  │ (uses factory method)
│  # create_notification()│ (abstract factory method)
└─────────────────────────┘
           ↑ extends
           │
    ┌──────┴──────┬──────────────┬───────────────┐
    │             │              │               │
┌───────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐
│  Email    │ │   SMS   │ │   Push   │ │   Discord    │
│ Factory   │ │ Factory │ │ Factory  │ │   Factory    │
│           │ │         │ │          │ │              │
│ + create()│ │+ create()│ │+ create()│ │ + create()  │
└───────────┘ └─────────┘ └──────────┘ └──────────────┘
     │             │            │              │
     │creates      │creates     │creates       │creates
     ↓             ↓            ↓              ↓
┌───────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐
│   Email   │ │   SMS   │ │   Push   │ │   Discord    │
│Notification│ │Notification│ │Notification│ │Notification│
└───────────┘ └─────────┘ └──────────┘ └──────────────┘
```

### Simple Factory vs Factory Method

| Aspect | Simple Factory | Factory Method |
|--------|---------------|----------------|
| **Structure** | Single factory class | Abstract creator + concrete creators |
| **Extensibility** | Modify factory to add types | Add new subclass (Open-Closed) |
| **Complexity** | Simpler | More classes needed |
| **Use case** | Few types, rarely change | Many types, frequent additions |
| **Flexibility** | Less flexible | More flexible |

### When to Use Factory Method

✅ **Use when:**
- Need to extend with new types frequently
- Want to follow Open-Closed Principle strictly
- Subclasses should decide which object to create
- Have related business logic that varies by type

❌ **Don't use when:**
- Simple Factory is sufficient
- Creating single-level objects (no inheritance hierarchy)
- Over-engineering for simple cases

### Real-World Use Cases

1. **Document Generator**
   - PDFDocumentGenerator, WordDocumentGenerator, ExcelDocumentGenerator
   - Each knows how to create and format its document type

2. **Transport Logistics**
   - TruckLogistics, ShipLogistics, AirLogistics
   - Each creates appropriate transport vehicle and plans routes

3. **Game Character Creator**
   - WarriorCreator, MageCreator, ArcherCreator
   - Each creates character with specific attributes and abilities

4. **Export Service**
   - JSONExportService, XMLExportService, CSVExportService
   - Each creates appropriate formatter and handles export

---

## 3. Abstract Factory

### The Problem with Factory Method

```python
# Creating UI for different platforms
class WindowsButton:
    def render(self):
        print("Rendering Windows button")

class MacButton:
    def render(self):
        print("Rendering Mac button")

# Problem: Need to create FAMILIES of related objects
# Windows app needs: WindowsButton, WindowsCheckbox, WindowsMenu
# Mac app needs: MacButton, MacCheckbox, MacMenu

# Easy to mix them up!
button = WindowsButton()
checkbox = MacCheckbox()  # Oops! Mixed Windows and Mac
menu = WindowsMenu()
# Inconsistent UI! 💥
```

# Abstract Factory: Why Do We Need It?

## The Problem: Creating Families of Related Objects

When you need to create **multiple related objects** that should work together, you face a consistency problem.

### Example Scenario: Cross-Platform UI Components

You're building an application that runs on Windows, Mac, and Linux. Each platform needs:
- Button (styled for that platform)
- Checkbox (styled for that platform)  
- Menu (styled for that platform)

**The Challenge:** Ensure all components belong to the same platform (all Windows OR all Mac OR all Linux).

---

## ❌ Bad Design 1: Simple Factory (Can't Guarantee Consistency)

```python
# Simple Factory approach
class UIComponentFactory:
    @staticmethod
    def create_button(os_type: str):
        if os_type == "Windows":
            return WindowsButton()
        elif os_type == "Mac":
            return MacButton()
        elif os_type == "Linux":
            return LinuxButton()
    
    @staticmethod
    def create_checkbox(os_type: str):
        if os_type == "Windows":
            return WindowsCheckbox()
        elif os_type == "Mac":
            return MacCheckbox()
        elif os_type == "Linux":
            return LinuxCheckbox()
    
    @staticmethod
    def create_menu(os_type: str):
        if os_type == "Windows":
            return WindowsMenu()
        elif os_type == "Mac":
            return MacMenu()
        elif os_type == "Linux":
            return LinuxMenu()

# Client code - DANGEROUS!
class Application:
    def __init__(self, os_type: str):
        # ❌ Problem 1: Easy to pass DIFFERENT os_type by mistake!
        self.button = UIComponentFactory.create_button(os_type)
        self.checkbox = UIComponentFactory.create_checkbox("Mac")  # Oops! Typo!
        self.menu = UIComponentFactory.create_menu(os_type)
        
        # Result: Windows button + Mac checkbox + Windows menu
        # INCONSISTENT UI! 💥
    
    def render(self):
        self.button.render()
        self.checkbox.render()
        self.menu.render()

# Usage
app = Application("Windows")
app.render()
# Output:
# Rendering Windows-style button
# Rendering Mac-style checkbox      ← WRONG! Mixed platforms!
# Rendering Windows-style menu
```

**Problems with Simple Factory:**
1. ❌ **No consistency guarantee** - Each component created independently
2. ❌ **Easy to make mistakes** - Pass wrong os_type string
3. ❌ **No compile-time safety** - Bugs only appear at runtime
4. ❌ **Scattered string parameters** - os_type repeated everywhere
5. ❌ **Hard to track** - Can't ensure all components from same family

---

## ❌ Bad Design 2: Multiple Factory Methods (Still No Guarantee)

```python
# Using separate factories for each component
class ButtonFactory:
    @staticmethod
    def create(os_type: str):
        if os_type == "Windows":
            return WindowsButton()
        elif os_type == "Mac":
            return MacButton()
        elif os_type == "Linux":
            return LinuxButton()

class CheckboxFactory:
    @staticmethod
    def create(os_type: str):
        if os_type == "Windows":
            return WindowsCheckbox()
        elif os_type == "Mac":
            return MacCheckbox()
        elif os_type == "Linux":
            return LinuxCheckbox()

class MenuFactory:
    @staticmethod
    def create(os_type: str):
        if os_type == "Windows":
            return WindowsMenu()
        elif os_type == "Mac":
            return MacMenu()
        elif os_type == "Linux":
            return LinuxMenu()

# Client code - EVEN MORE DANGEROUS!
class Application:
    def __init__(self, button_os: str, checkbox_os: str, menu_os: str):
        # ❌ Problem: Now EACH component can be from different platform!
        self.button = ButtonFactory.create(button_os)
        self.checkbox = CheckboxFactory.create(checkbox_os)
        self.menu = MenuFactory.create(menu_os)
    
    def render(self):
        self.button.render()
        self.checkbox.render()
        self.menu.render()

# Usage - Complete chaos!
app = Application("Windows", "Mac", "Linux")  # All different platforms! 💥
app.render()
# Output:
# Rendering Windows-style button
# Rendering Mac-style checkbox
# Rendering Linux-style menu
# COMPLETELY INCONSISTENT UI! 💥

# Even "safe" usage is error-prone
def create_app(os_type: str):
    # Have to pass os_type to THREE different factories
    # Easy to make mistakes!
    button = ButtonFactory.create(os_type)
    checkbox = CheckboxFactory.create(os_type)  # Typo in os_type?
    menu = MenuFactory.create(os_type)          # Different variable?
    
    return Application(button, checkbox, menu)
```

**Problems with Multiple Factories:**
1. ❌ **Even worse consistency** - Each factory independent
2. ❌ **More parameters to manage** - One os_type per component
3. ❌ **More duplication** - Repeat os_type for each factory call
4. ❌ **More room for error** - Easy to mix up parameters
5. ❌ **No relationship** - Factories don't know about each other

---

## ✅ Good Design: Abstract Factory (Guarantees Consistency)

```python
from abc import ABC, abstractmethod

# Step 1: Abstract products
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass

class Menu(ABC):
    @abstractmethod
    def render(self):
        pass

# Step 2: Concrete products - Windows family
class WindowsButton(Button):
    def render(self):
        print("Rendering Windows-style button")

class WindowsCheckbox(Checkbox):
    def render(self):
        print("Rendering Windows-style checkbox")

class WindowsMenu(Menu):
    def render(self):
        print("Rendering Windows-style menu")

# Step 3: Concrete products - Mac family
class MacButton(Button):
    def render(self):
        print("Rendering Mac-style button")

class MacCheckbox(Checkbox):
    def render(self):
        print("Rendering Mac-style checkbox")

class MacMenu(Menu):
    def render(self):
        print("Rendering Mac-style menu")

# Step 4: Abstract Factory - defines interface for creating families
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
    
    @abstractmethod
    def create_menu(self) -> Menu:
        pass

# Step 5: Concrete Factories - each creates ONE complete family
class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()
    
    def create_menu(self) -> Menu:
        return WindowsMenu()

class MacUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
    
    def create_menu(self) -> Menu:
        return MacMenu()

# Step 6: Client code - works with any factory
class Application:
    def __init__(self, factory: UIFactory):
        # ✅ Single factory creates ALL components
        # ✅ Guaranteed to be consistent!
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()
        self.menu = factory.create_menu()
    
    def render(self):
        self.button.render()
        self.checkbox.render()
        self.menu.render()

# Usage - guaranteed consistent!
def create_app(os_type: str) -> Application:
    if os_type == "Windows":
        factory = WindowsUIFactory()
    elif os_type == "Mac":
        factory = MacUIFactory()
    else:
        raise ValueError(f"Unknown OS: {os_type}")
    
    # Pass ONE factory - all components from same family!
    return Application(factory)

# All Windows components - consistent!
windows_app = create_app("Windows")
windows_app.render()
# Output:
# Rendering Windows-style button
# Rendering Windows-style checkbox
# Rendering Windows-style menu

# All Mac components - consistent!
mac_app = create_app("Mac")
mac_app.render()
# Output:
# Rendering Mac-style button
# Rendering Mac-style checkbox
# Rendering Mac-style menu

# ✅ IMPOSSIBLE to mix platforms!
# ✅ ONE factory creates entire family
# ✅ Type-safe - factory guarantees consistency
```

### Abstract Factory Diagram

```
┌─────────────────────────────────────┐
│         UIFactory                   │ (Abstract Factory)
│  ─────────────────────────────────  │
│  + create_button(): Button          │
│  + create_checkbox(): Checkbox      │
│  + create_menu(): Menu              │
└─────────────────────────────────────┘
           ↑ implements
           │
    ┌──────┴──────┬────────────────┐
    │             │                │
┌───────────┐ ┌─────────┐ ┌──────────────┐
│  Windows  │ │   Mac   │ │    Linux     │
│ UIFactory │ │UIFactory│ │  UIFactory   │
└───────────┘ └─────────┘ └──────────────┘
     │             │              │
     │creates      │creates       │creates
     │family       │family        │family
     ↓             ↓              ↓
┌──────────┐  ┌─────────┐  ┌───────────┐
│ Windows  │  │   Mac   │  │   Linux   │
│ Button   │  │ Button  │  │  Button   │
│ Checkbox │  │ Checkbox│  │  Checkbox │
│ Menu     │  │ Menu    │  │  Menu     │
└──────────┘  └─────────┘  └───────────┘
```

### Factory Method vs Abstract Factory

| Aspect | Factory Method | Abstract Factory |
|--------|---------------|------------------|
| **Purpose** | Create ONE product | Create FAMILIES of related products |
| **Products** | Single product type | Multiple related products |
| **Focus** | Inheritance hierarchy | Product families/variants |
| **Example** | DocumentCreator → PDFDocument | WindowsUIFactory → Button+Checkbox+Menu |
| **Complexity** | Simpler | More complex |
| **Use case** | Varying single product | Ensuring product consistency |

### When to Use Abstract Factory

✅ **Use when:**
- Need to create families of related objects
- Want to ensure objects from same family are used together
- System should be independent of how products are created
- Products have multiple variants/themes

❌ **Don't use when:**
- Creating single products (use Factory Method)
- Products aren't related or don't need to be consistent
- Over-engineering simple scenarios

### Real-World Use Cases

1. **Cross-Platform UI Toolkit**
   - Windows/Mac/Linux factories
   - Each creates Button, Checkbox, TextField, Menu for that platform

2. **Database Access Layer**
   - MySQL/PostgreSQL/MongoDB factories
   - Each creates Connection, Command, DataReader for that database

3. **Game Theme System**
   - Medieval/SciFi/Fantasy factories
   - Each creates Weapons, Armor, Enemies, Environments matching theme

4. **Report Generation**
   - PDF/Excel/HTML factories
   - Each creates Table, Chart, Header, Footer in matching format

5. **Cloud Provider SDK**
   - AWS/Azure/GCP factories
   - Each creates Storage, Compute, Database, Network services

---

## 📊 Complete Comparison

### Pattern Selection Guide

```
┌─────────────────────────────────────────────────────────┐
│  Need to create objects?                                │
└─────────────────────────────────────────────────────────┘
                        │
                        ↓
        ┌───────────────┴───────────────┐
        │                               │
    Single type?                  Family of related types?
        │                               │
        ↓                               ↓
┌───────────────┐              ┌─────────────────┐
│ Few types?    │              │ ABSTRACT FACTORY│
│ Rarely change?│              │                 │
└───────────────┘              │ Example: UI Kit │
        │                      │ - Button        │
        ↓                      │ - Checkbox      │
    ┌──────────┐              │ - Menu          │
    │ Simple   │              │ All Windows OR  │
    │ Factory  │              │ All Mac         │
    └──────────┘              └─────────────────┘
        │
        ↓
┌──────────────┐
│ Many types?  │
│ Frequent add?│
└──────────────┘
        │
        ↓
┌──────────────┐
│   Factory    │
│   Method     │
│              │
│ Example:     │
│ Document Gen │
│ - PDF        │
│ - Word       │
│ - Excel      │
└──────────────┘
```

### Quick Reference

| Pattern | Object Count | Relationships | Extensibility | Complexity |
|---------|-------------|---------------|---------------|------------|
| **Simple Factory** | Single type | None | Modify factory | ⭐ Low |
| **Factory Method** | Single type | Inheritance | Add subclass | ⭐⭐ Medium |
| **Abstract Factory** | Product families | Related products | Add factory | ⭐⭐⭐ High |

---

## 💡 Practical Guidelines

### Start Simple, Evolve as Needed

```python
# Stage 1: Direct creation (OK for simple cases)
notification = EmailNotification()

# Stage 2: Growing complexity? Use Simple Factory
notification = NotificationFactory.create("email")

# Stage 3: Frequent additions? Use Factory Method
service = EmailNotificationService()
service.send_notification("Hello")

# Stage 4: Need families? Use Abstract Factory
factory = WindowsUIFactory()
app = Application(factory)
```

### Don't Over-Engineer!

```python
# ❌ Overkill for simple case
class PointFactory:  # Just to create Point(x, y)?
    @staticmethod
    def create(x, y):
        return Point(x, y)

# ✅ Just use constructor!
point = Point(10, 20)

# ✅ Use factory when you have ACTUAL complexity
notification = NotificationFactory.create("email")  # Many types
document = DocumentGenerator.create("pdf")  # Different logic
ui = UIFactory.create_button()  # Platform-specific
```

---

## 🎯 Key Takeaways

### Simple Factory
- **What:** Centralized object creation
- **When:** Basic creation logic, few types
- **Example:** NotificationFactory creating Email/SMS/Push

### Factory Method
- **What:** Subclasses decide which object to create
- **When:** Need extensibility, follow Open-Closed
- **Example:** DocumentService hierarchy creating different documents

### Abstract Factory
- **What:** Create families of related objects
- **When:** Need consistency across product families
- **Example:** UIFactory creating Button+Checkbox+Menu for each platform

### Remember
- Most real-world code uses Simple Factory or Factory Method
- Abstract Factory is for advanced scenarios
- Start simple, refactor when needed
- Don't over-engineer!

---

## 📚 Summary

**Factory Patterns solve one core problem: Decoupling object creation from object usage.**

Choose based on your needs:
- **Simple creation?** → Simple Factory
- **Extensible creation?** → Factory Method  
- **Related families?** → Abstract Factory

The goal isn't to use the most complex pattern, but to use the **right** pattern for your situation! 🚀