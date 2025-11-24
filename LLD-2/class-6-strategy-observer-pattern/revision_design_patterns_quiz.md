# Design Patterns Quiz 1

---
## Question 2: Builder Pattern - Common Mistake

Which Builder implementation will cause a runtime error?

**Option A:**
```python
class QueryBuilder:
    def select(self, fields):
        self._fields = fields
    
    def where(self, condition):
        self._condition = condition
        return self
    
    def build(self):
        return Query(self._fields, self._condition)
```

**Option B:**
```python
class QueryBuilder:
    def select(self, fields):
        self._fields = fields
        return self
    
    def where(self, condition):
        self._condition = condition
        return self
    
    def build(self):
        return Query(self._fields, self._condition)

```

---

<details>
<summary>Answer</summary>

**A) will cause AttributeError at runtime**

**The Problem:**
```python
class QueryBuilder:
    def select(self, fields):
        self._fields = fields
        # Forgot return self! ← BUG

query = QueryBuilder().select(["name", "age"]).where("age > 18")
#                                              ↑
#                     None.where() → AttributeError!
```

Without `return self`, method returns `None`
Next method call fails: `None.where(...)` → Error

---

**Option B - Correct:**
```python
def select(self, fields):
    self._fields = fields
    return self  # ✅ Enables chaining

# Works!
query = QueryBuilder()
    .select(["name"])
    .where("age > 18")
    .build()
```

---


**Complete Builder Pattern:**

```python
class Query:
    def __init__(self, fields, condition):
        self.fields = fields
        self.condition = condition

class QueryBuilder:
    def __init__(self):
        self._fields = []
        self._condition = None
    
    def select(self, fields):
        self._fields = fields
        return self  # Critical!
    
    def where(self, condition):
        self._condition = condition
        return self  # Critical!
    
    def build(self) -> Query:
        return Query(self._fields, self._condition)

# Usage
query = (QueryBuilder()
    .select(["id", "name"])
    .where("active = true")
    .build())
```

---

**UML Diagram:**

```
┌─────────────────────┐
│   QueryBuilder      │
│  ─────────────────  │
│  - _fields: list    │
│  - _condition: str  │
│  ─────────────────  │
│  + select(fields)   │──► returns self
│  + where(cond)      │──► returns self
│  + build(): Query   │──► returns Product
└─────────────────────┘
         │
         │ builds
         ▼
┌─────────────────────┐
│      Query          │
│  ─────────────────  │
│  + fields           │
│  + condition        │
└─────────────────────┘
```

**Key Mistake:** Forgetting `return self` breaks method chaining!

</details>


---

## Question 3: Prototype Pattern - When NOT to Use

Which scenario should NOT use Prototype pattern?

**Option A:**
```python
# Configuration: Pre-configured server settings
prod_config = ServerConfig(
    host="prod.db.com",
    port=5432,
    max_connections=100,
    ssl=True,
    timeout=30
)
# Clone for different regions
us_server = prod_config.clone()
eu_server = prod_config.clone()
eu_server.host = "eu.db.com"
```

**Option B:**
```python
# User profiles: Each user has unique data
user_template = User()
user1 = user_template.clone()
user1.name = "Alice"
user1.email = "alice@example.com"
user1.id = generate_unique_id()
user1.preferences = {...}
```
---

**Option C:**
```python
registry = NewsletterRegistry()
registry.register("weekly", Newsletter(
    styles={"font": "Arial", "size": 12},
    header="Weekly Update",
    footer="© 2024"
))
registry.register("monthly", Newsletter(
    styles={"font": "Arial", "size": 14},
    header="Monthly Digest",
    footer="© 2024"
))

# Clone from registry based on type
weekly = registry.create("weekly")
weekly.content = "This week's news..."

monthly = registry.create("monthly")
monthly.content = "This month's highlights..."
```

---

<details>
<summary>Answer</summary>

**B) User profiles - Should NOT use Prototype**

---

**Quick Visual:**

```
A) ServerConfig        B) User             C) Newsletter Registry
   ├─ host             ├─ name             ├─ "weekly" template
   ├─ port             ├─ email            │   └─ clone()
   ├─ ssl              ├─ id               ├─ "monthly" template
   └─ timeout          └─ preferences      │   └─ clone()
   ✅ 90% same         ❌ 100% different   ✅ Registry + variants
```

---

**Why B is wrong:**

```python
user_template = User()  # Empty template?
user1 = user_template.clone()
user1.name = "Alice"          # Everything set AFTER clone
user1.email = "alice@..."
user1.id = generate_unique_id()
user1.preferences = {...}
```

❌ No shared state - template is empty
❌ All fields unique - no benefit from cloning
❌ Just `clone()` + fill = overcomplicated constructor

**Better:**
```python
user1 = User("Alice", "alice@...", generate_unique_id(), {...})
```

---

**Why A is correct:**

```python
# Expensive setup done once
prod_config = ServerConfig(
    host="prod.db.com",
    port=5432,
    max_connections=100,
    ssl=True,
    timeout=30
)

# Quick clones with small tweaks
us_server = prod_config.clone()  # Inherits all settings

eu_server = prod_config.clone()
eu_server.host = "eu.db.com"     # Only change host
```

- ✅ 90% shared configuration
- ✅ Only host varies
- ✅ Clone faster than rebuilding

---

**Why C is correct (Prototype Registry):**

```python
# Registry stores multiple templates
registry.register("weekly", Newsletter(...))
registry.register("monthly", Newsletter(...))
registry.register("special", Newsletter(...))

# Clone appropriate template
weekly = registry.create("weekly")
monthly = registry.create("monthly")
```

- ✅ Centralized template management
- ✅ Different newsletter types with variations
- ✅ Clone from registry based on type
- ✅ **Registry Pattern + Prototype** = powerful combo

**Use Case:**
```
Marketing team needs newsletter
├─ "What type?" → "weekly"
├─ Registry: clone("weekly") template
└─ Set content → Ready!
```

---

**Prototype Registry Structure:**

```
┌──────────────────────────┐
│  NewsletterRegistry      │
│  ──────────────────────  │
│  - templates: dict       │
│  ──────────────────────  │
│  + register(name, proto) │
│  + create(name): clone() │
└──────────────────────────┘
         │
         ├─ "weekly" → Newsletter (template)
         ├─ "monthly" → Newsletter (template)
         └─ "special" → Newsletter (template)
```

---

**Decision Guide:**

```
Is there shared configuration?
│
├─ Yes, substantial → ✅ Use Prototype
│   └─ Many templates? → Use Registry
│
└─ No shared state → ❌ Use Constructor
    └─ All fields unique → Direct instantiation
```

---

**When to use Registry:**

```python
# WITHOUT Registry
weekly = NewsletterTemplate1().clone()
monthly = NewsletterTemplate2().clone()
special = NewsletterTemplate3().clone()

# WITH Registry
weekly = registry.create("weekly")
monthly = registry.create("monthly")
special = registry.create("special")
```

- ✅ Centralized template storage
- ✅ Create by name, not by class
- ✅ Easy to add new types

**Key Insight:** Prototype is worthless if nothing is shared between instances

</details>

---

## Question 4: Builder Pattern - Validation Timing

When should validation happen in the Builder pattern?

**Option A - Validate in setters:**
```python
class QueryBuilder:
    def set_limit(self, limit):
        if limit <= 0:
            raise ValueError("Limit must be positive")
        self._limit = limit
        return self
    
    def build(self):
        return Query(self._limit)
```

**Option B - Validate in build():**
```python
class QueryBuilder:
    def set_limit(self, limit):
        self._limit = limit
        return self
    
    def build(self):
        if self._limit <= 0:
            raise ValueError("Limit must be positive")
        return Query(self._limit)
```
---

**Option C - Validate in Product:**
```python
class QueryBuilder:
    def set_limit(self, limit):
        self._limit = limit
        return self
    
    def build(self):
        return Query(self._limit)

class Query:
    def __init__(self, limit):
        if limit <= 0:
            raise ValueError("Limit must be positive")
        self._limit = limit
```

---

<details>
<summary>Answer</summary>

**B) Validate in build() - best for Builder pattern**

---

**Why B is correct:**

```python
def build(self):
    # Validate complete object state
    if self._limit <= 0:
        raise ValueError("Limit must be positive")
    if not self._table:
        raise ValueError("Table is required")
    return Query(self._limit, self._table)
```

- ✅ **Validates complete state** before creating object
- ✅ **Fails fast** - before Product creation
- ✅ **Single validation point** - easy to maintain
- ✅ **Allows invalid intermediate states** during building

---

**Why this matters:**

```python
# With Option B - can build gradually
builder = QueryBuilder()
builder.set_limit(-5)        # No error yet (invalid intermediate state OK)
builder.set_table("users")
builder.set_limit(10)        # Fix the error
query = builder.build()      # ✅ Valid at build time
```

---

**Why A is too strict:**

```python
def set_limit(self, limit):
    if limit <= 0:
        raise ValueError("Limit must be positive")
    # ...
```

❌ **Prevents valid workflows:**
```python
builder = QueryBuilder()
builder.set_limit(-5)  # ❌ Error immediately!
# Can't even set it to fix it later
```

- ❌ **Invalid intermediate states forbidden**
- ❌ **Can't experiment with values**

**When A is acceptable:**
- Simple builders with independent fields
- When invalid values could cause corruption

---

**Why C is too late:**

```python
class Query:
    def __init__(self, limit):
        if limit <= 0:
            raise ValueError("...")
```

❌ **Product created before validation**
❌ **Harder to debug** - error in Product, not Builder
❌ **Builder can't guarantee validity**

```python
# Error happens deep in Product
builder = QueryBuilder()
builder.set_limit(-5)
builder.set_table("users")
query = builder.build()  # ❌ Error in Query.__init__
# Less clear where the problem originated
```

---

**Complete Example:**

```python
class QueryBuilder:
    def __init__(self):
        self._table = None
        self._limit = None
        self._offset = 0
    
    def set_table(self, table):
        self._table = table
        return self
    
    def set_limit(self, limit):
        self._limit = limit  # No validation yet
        return self
    
    def set_offset(self, offset):
        self._offset = offset
        return self
    
    def build(self):
        # Validate complete state
        if not self._table:
            raise ValueError("Table is required")
        if self._limit is not None and self._limit <= 0:
            raise ValueError("Limit must be positive")
        if self._offset < 0:
            raise ValueError("Offset must be non-negative")
        
        # All valid - create Product
        return Query(self._table, self._limit, self._offset)
```

---

**Validation Strategy Comparison:**

```
┌─────────────┬────────────┬─────────────┬──────────────┐
│ Strategy    │ Strictness │ Flexibility │ Best For     │
├─────────────┼────────────┼─────────────┼──────────────┤
│ In Setters  │ High       │ Low         │ Critical     │
│ (Option A)  │            │             │ constraints  │
├─────────────┼────────────┼─────────────┼──────────────┤
│ In build()  │ Medium     │ High        │ Most cases   │
│ (Option B)  │            │             │ ✅ Recommended│
├─────────────┼────────────┼─────────────┼──────────────┤
│ In Product  │ Low        │ High        │ Simple       │
│ (Option C)  │            │             │ builders     │
└─────────────┴────────────┴─────────────┴──────────────┘
```

---

**UML Diagram:**

```
┌──────────────────────────┐
│    QueryBuilder          │
│  ──────────────────────  │
│  - _table: str           │
│  - _limit: int           │
│  - _offset: int          │
│  ──────────────────────  │
│  + set_table(): Builder  │
│  + set_limit(): Builder  │
│  + build(): Query        │
│    └─ Validates here! ✅ │
└──────────────────────────┘
         │
         │ builds
         ▼
┌──────────────────────────┐
│        Query             │
│  ──────────────────────  │
│  + table: str            │
│  + limit: int            │
│  + execute()             │
└──────────────────────────┘
```

---

**Key Insight:** Builder should validate complete state in `build()`, allowing flexible intermediate states during construction

</details>

---

## Question 5: Adapter - When NOT Needed

When should you NOT use Adapter pattern?

**Option A:**
```python
# Old payment gateway: charge(amount, card)
# New payment gateway: process_payment(amount, card)
# Need: Make old gateway work with new interface
```

**Option B:**
```python
# Library A: save_file(data, path)
# Library B: write_to_disk(path, data)  # Different parameter order
# Need: Unified interface
```

**Option C:**
```python
# Your code: log(level, message)
# Your code: log(level, message)  # Same interface already!
# Need: ???
```

**Option D:**
```python
# JSON API: returns dict
# XML API: returns XML string
# Need: Uniform dict output
```

---

<details>
<summary>Answer</summary>

**C) No adapter needed - same interface!**

---

**Why C doesn't need Adapter:**

```python
# Both have SAME interface
class LoggerA:
    def log(self, level, message): pass

class LoggerB:
    def log(self, level, message): pass

# Just use them directly!
logger = LoggerA()  # or LoggerB()
logger.log("INFO", "message")
```

- ❌ No interface incompatibility
- ❌ No adaptation needed
- ❌ Adapter adds unnecessary complexity

---

**When Adapter is NOT needed:**

1. **Source can be modified**
   ```python
   # Just change the source!
   class OldAPI:
       def old_method(self): pass
   
   # Change to:
   class OldAPI:
       def new_method(self): pass  # Fixed!
   ```

2. **No actual incompatibility**
   ```python
   # Both work the same way
   obj1.method()
   obj2.method()  # Same interface!
   ```

3. **Simple wrapper suffices**
   ```python
   # Don't need full Adapter pattern
   def simple_wrapper(obj):
       return obj.method()
   ```

---
Here are generic UML diagrams for both Adapter pattern variations:

---

## Adapter Pattern - UML Diagrams

### Object Adapter (Composition) - Recommended

```
┌─────────────────┐
│     Client      │
└────────┬────────┘
         │ uses
         ▼
┌─────────────────┐
│  Target (ABC)   │
│  ─────────────  │
│  + request()    │
└────────┬────────┘
         △
         │ implements
         │
┌────────┴────────────────┐
│      Adapter            │
│  ─────────────────────  │
│  - adaptee: Adaptee     │──────┐
│  ─────────────────────  │      │ wraps/delegates
│  + request()            │      │
│    └─ adaptee.method()  │      │
└─────────────────────────┘      │
                                 ▼
                        ┌─────────────────┐
                        │    Adaptee      │
                        │  ─────────────  │
                        │  + method()     │
                        └─────────────────┘
```

---

### Class Adapter (Inheritance) - Less Common

```
┌─────────────────┐
│     Client      │
└────────┬────────┘
         │ uses
         ▼
┌─────────────────┐
│  Target (ABC)   │
│  ─────────────  │
│  + request()    │
└────────┬────────┘
         △
         │ implements
         │
┌────────┴────────────────┐         ┌─────────────────┐
│      Adapter            │─────────│    Adaptee      │
│  ─────────────────────  │inherits │  ─────────────  │
│  + request()            │         │  + method()     │
│    └─ self.method()     │         └─────────────────┘
└─────────────────────────┘
```

---

### Simplified View - Object Adapter

```
Client ──► Target (interface)
              △
              │ implements
              │
           Adapter ────► Adaptee (legacy)
           (bridges)     (incompatible)
```

---

### Flow Diagram

```
Client Request Flow:
─────────────────────

client.request()
    │
    ▼
adapter.request()
    │
    ├─ translates/adapts
    │
    ▼
adaptee.specific_method()
    │
    ▼
returns result
```

---

### Two-Way Adapter (Bidirectional)

```
┌──────────────────────────┐
│   BidirectionalAdapter   │
│  ──────────────────────  │
│  - systemA: SystemA      │──────► SystemA
│  - systemB: SystemB      │──────► SystemB
│  ──────────────────────  │
│  + a_to_b(data)          │
│  + b_to_a(data)          │
└──────────────────────────┘
```

---

### Real Example - Temperature Adapter

```
┌────────────────────────┐
│   WeatherApp (Client)  │
└───────────┬────────────┘
            │ needs Fahrenheit
            ▼
┌────────────────────────┐
│ FahrenheitSensor (ABC) │
│  ────────────────────  │
│  + read_fahrenheit()   │
└───────────┬────────────┘
            △
            │
┌───────────┴─────────────────┐
│   ThermometerAdapter        │
│  ─────────────────────────  │
│  - thermometer: Celsius     │───┐
│  ─────────────────────────  │   │ wraps
│  + read_fahrenheit()        │   │
│    celsius = thermo.get()   │   │
│    return (c * 9/5) + 32    │   │
└─────────────────────────────┘   │
                                  ▼
                    ┌──────────────────────┐
                    │ CelsiusThermometer   │
                    │  ──────────────────  │
                    │  + get_temperature() │
                    └──────────────────────┘
```
---
**Why A needs Adapter:**

```python
class OldGateway:
    def charge(self, amount, card): pass

class NewGateway:
    def process_payment(self, amount, card): pass

# Adapter needed!
class PaymentAdapter:
    def __init__(self, old_gateway):
        self.gateway = old_gateway
    
    def process_payment(self, amount, card):
        return self.gateway.charge(amount, card)
```

- ✅ Different method names
- ✅ Need unified interface
- ✅ Can't modify OldGateway (third-party)

---

**Why B needs Adapter:**

```python
class LibraryA:
    def save_file(self, data, path): pass

class LibraryB:
    def write_to_disk(self, path, data): pass  # Swapped!

# Adapter needed!
class StorageAdapter:
    def __init__(self, library):
        self.lib = library
    
    def save(self, data, path):
        if isinstance(self.lib, LibraryA):
            return self.lib.save_file(data, path)
        else:
            return self.lib.write_to_disk(path, data)
```

- ✅ Different parameter order
- ✅ Different method names
- ✅ Need unified interface

---

**Why D needs Adapter:**

```python
class JSONAdapter:
    def __init__(self, xml_api):
        self.api = xml_api
    
    def get_data(self):
        xml_string = self.api.fetch()
        return self.parse_xml_to_dict(xml_string)
```

- ✅ Different data formats
- ✅ Need consistent output

---

**Decision Tree:**

```
Is there interface incompatibility?
├─ No → ❌ Don't use Adapter
│       └─ Just use objects directly
│
└─ Yes → Can you modify the source?
          ├─ Yes → Modify source (better)
          └─ No → ✅ Use Adapter
```

**Key Insight:** Adapter solves incompatibility - if compatible, don't use it!

</details>

---

## Question 6: Abstract Factory - Real-World Scenario

You're building a document export system that needs to create PDFs, DOCXs with matching fonts and images.

Which factory structure is correct?

**Option A - Simple Factory:**
```python
class DocumentFactory:
    @staticmethod
    def create(type):
        if type == "pdf": return PDFDocument()
        if type == "docx": return DOCXDocument()
```

**Option B - Factory Method:**
```python
class DocumentExporter(ABC):
    @abstractmethod
    def create_document(self): pass

class PDFExporter(DocumentExporter):
    def create_document(self): return PDFDocument()
```

**Option C - Abstract Factory:**
```python
class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self): pass
    @abstractmethod
    def create_font_renderer(self): pass
    @abstractmethod
    def create_image_handler(self): pass

class PDFFactory(DocumentFactory):
    def create_document(self): return PDFDocument()
    def create_font_renderer(self): return PDFFontRenderer()
    def create_image_handler(self): return PDFImageHandler()
```

---

<details>
<summary>Answer</summary>

**C) Abstract Factory - for families of related objects**

---

**Why C is correct:**

```python
class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self): pass
    
    @abstractmethod
    def create_font_renderer(self): pass
    
    @abstractmethod
    def create_image_handler(self): pass

class PDFFactory(DocumentFactory):
    def create_document(self):
        return PDFDocument()
    
    def create_font_renderer(self):
        return PDFFontRenderer()  # PDF-specific
    
    def create_image_handler(self):
        return PDFImageHandler()  # PDF-specific

class DOCXFactory(DocumentFactory):
    def create_document(self):
        return DOCXDocument()
    
    def create_font_renderer(self):
        return DOCXFontRenderer()  # DOCX-specific
    
    def create_image_handler(self):
        return DOCXImageHandler()  # DOCX-specific
```

✅ Creates family of related objects (doc + font + image)
✅ Ensures consistency (all PDF or all DOCX)
✅ Can't mix PDF font with DOCX document

---

**Usage:**

```python
# Client code
class DocumentProcessor:
    def __init__(self, factory: DocumentFactory):
        self.factory = factory
    
    def export(self, content):
        doc = self.factory.create_document()
        font = self.factory.create_font_renderer()
        img_handler = self.factory.create_image_handler()
        
        doc.add_text(content, font)
        doc.add_image("logo.png", img_handler)
        return doc.save()

# Use with PDF
processor = DocumentProcessor(PDFFactory())
processor.export("Content")  # All PDF components

# Switch to DOCX
processor = DocumentProcessor(DOCXFactory())
processor.export("Content")  # All DOCX components
```

---

**Why A is insufficient:**

```python
class DocumentFactory:
    @staticmethod
    def create(type):
        if type == "pdf": return PDFDocument()
```

❌ Only creates document
❌ No fonts/images creation
❌ No consistency guarantee
❌ Must create fonts/images separately
❌ Could mix PDF doc with DOCX fonts (bug!)

---

**Why B is insufficient:**

```python
class PDFExporter(DocumentExporter):
    def create_document(self):
        return PDFDocument()
    # What about fonts? Images?
```

❌ Only creates single object
❌ No related objects handling
❌ Incomplete solution

---

**UML Diagram:**

```
┌──────────────────────────────────────────┐
│      DocumentFactory (ABC)               │
│  ──────────────────────────────────────  │
│  + create_document(): Document           │
│  + create_font_renderer(): FontRenderer  │
│  + create_image_handler(): ImageHandler  │
└──────────────────────────────────────────┘
              △
              │
      ┌───────┴───────┐
      ▼               ▼
┌────────────┐  ┌────────────┐
│PDFFactory  │  │DOCXFactory │
│──────────  │  │──────────  │
│create_doc()│  │create_doc()│──► PDFDocument / DOCXDocument
│create_font│  │create_font()│──► PDFFontRenderer / DOCXFontRenderer
│create_img()│  │create_img()│──► PDFImageHandler / DOCXImageHandler
└────────────┘  └────────────┘
```

**Key Insight:** Abstract Factory creates **families** of related objects that work together

</details>

---

## Question 7: Prototype Registry Pattern

Which implementation correctly uses Prototype Registry?

**Option A:**
```python
class EnemyRegistry:
    def __init__(self):
        self.prototypes = {}
    
    def register(self, name, prototype):
        self.prototypes[name] = prototype
    
    def create(self, name):
        return self.prototypes[name].clone()
```

**Option B:**
```python
class EnemyRegistry:
    prototypes = {}  # Class variable
    
    @classmethod
    def register(cls, name, prototype):
        cls.prototypes[name] = prototype
    
    @classmethod
    def create(cls, name):
        return cls.prototypes.get(name).clone()
```

**Option C:**
```python
ENEMY_REGISTRY = {
    "orc": Orc(),
    "goblin": Goblin(),
    "troll": Troll()
}

def create_enemy(name):
    return ENEMY_REGISTRY[name].clone()
```

---

<details>
<summary>Answer</summary>

**A) Instance-based registry is most flexible**

---

**Why A is correct:**

```python
class EnemyRegistry:
    def __init__(self):
        self.prototypes = {}  # Instance variable
    
    def register(self, name, prototype):
        self.prototypes[name] = prototype
    
    def create(self, name):
        if name not in self.prototypes:
            raise KeyError(f"No prototype for {name}")
        return self.prototypes[name].clone()
    
    def get_registered(self):
        return list(self.prototypes.keys())
```

- ✅ Multiple registries possible (normal, boss, rare)
- ✅ Instance state manageable
- ✅ Easy to test
- ✅ Clear ownership

---

**Complete Example:**

```python
# Base Enemy
class Enemy:
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage
    
    def clone(self):
        import copy
        return copy.deepcopy(self)

# Concrete Enemies
class Orc(Enemy):
    def __init__(self):
        super().__init__(health=100, damage=20)

class Goblin(Enemy):
    def __init__(self):
        super().__init__(health=50, damage=10)

# Registry
registry = EnemyRegistry()
registry.register("orc", Orc())
registry.register("goblin", Goblin())

# Usage
enemy1 = registry.create("orc")
enemy2 = registry.create("orc")
print(enemy1 is enemy2)  # False - clones!

# Multiple registries
normal_enemies = EnemyRegistry()
normal_enemies.register("orc", Orc())

boss_enemies = EnemyRegistry()
boss_enemies.register("orc_chief", OrcChief())
```

---

**Why B has issues:**

```python
class EnemyRegistry:
    prototypes = {}  # Class variable - shared!
```

- ⚠️ All instances share same dict
- ⚠️ Can't have multiple registries
- ⚠️ Less flexible

```python
# Problem:
registry1 = EnemyRegistry()
registry1.register("orc", Orc())

registry2 = EnemyRegistry()
print("orc" in registry2.prototypes)  # True! Shared!
```

---

**Why C is too simple:**

```python
ENEMY_REGISTRY = {  # Global dict
    "orc": Orc(),
    "goblin": Goblin()
}

def create_enemy(name):
    return ENEMY_REGISTRY[name].clone()
```

- ❌ Global state
- ❌ Hard to test
- ❌ No encapsulation
- ❌ Can't have multiple registries

---

**UML Diagram:**

```
┌─────────────────────────────┐
│     EnemyRegistry           │
│  ─────────────────────────  │
│  - prototypes: dict         │
│  ─────────────────────────  │
│  + register(name, proto)    │
│  + create(name): Enemy      │
│  + get_registered(): list   │
└─────────────────────────────┘
         │
         │ contains
         ▼
┌─────────────────────────────┐
│    Enemy (Prototype)        │
│  ─────────────────────────  │
│  + health: int              │
│  + damage: int              │
│  ─────────────────────────  │
│  + clone(): Enemy           │
└─────────────────────────────┘
         △
         │
    ┌────┼────┐
    ▼    ▼    ▼
  Orc Goblin Troll
```
---
**Use Case Diagram:**

```
Game Level Loader
      │
      ├──► Load level config
      │    (enemy types needed)
      │
      ├──► registry.create("orc")  ─────┐
      │                                  │
      ├──► registry.create("goblin") ───┤
      │                                  ├──► Spawn enemies
      └──► registry.create("orc")  ─────┘
           (100s of enemies quickly!)
```

**Key Insight:** Registry centralizes prototype management and enables quick cloning

</details>

---

## Summary - Quiz 1

**Patterns Covered:**
- Factory Method (extensible creation)
- Builder (method chaining pitfall)
- Prototype (when NOT to use)
- Singleton + Builder (hybrid)
- Adapter (when NOT needed)
- Abstract Factory (families)
- Prototype Registry (centralized cloning)

**Key Takeaways:**
1. Factory Method needs abstract creator + template method
2. Builder MUST return `self` for chaining
3. Prototype only useful when objects share configuration
4. Adapter solves incompatibility - don't use if compatible
5. Abstract Factory ensures consistency across object families
6. Prototype Registry centralizes template management