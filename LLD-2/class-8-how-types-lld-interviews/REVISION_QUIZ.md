### Question 1:

**Sumit is designing a pricing calculator for a ride-sharing app. The pricing structure involves different algorithms, such as distance-based pricing, time-based pricing, and surge pricing during peak hours. Sumit wants to create a pricing calculation system that can seamlessly switch between different pricing strategies and accommodate future adjustments. What design pattern aligns with Sumit's pricing calculation requirements?**

- A) Decorator
- B) Strategy
- C) Observer
- D) Factory

---

<details>
<summary>Answer</summary>

**B) Strategy**

**Why Strategy:**
- Multiple pricing algorithms (distance, time, surge)
- Need to switch between algorithms at runtime
- Easy to add new pricing strategies without modifying existing code
- Encapsulates each pricing algorithm in separate class

---
**UML Diagram:**
```
┌──────────────────────┐
│  PricingStrategy     │ ← Strategy Interface
├──────────────────────┤
│+ calculate(ride)     │
└──────────────────────┘
           △
           │
    ┌──────┴─────────────┬─────────────┐
    │                    │             │
┌─────────────┐  ┌──────────────┐  ┌─────────────┐
│  Distance   │  │    Time      │  │   Surge     │
│   Based     │  │    Based     │  │   Pricing   │
└─────────────┘  └──────────────┘  └─────────────┘

┌──────────────────────┐
│  PriceCalculator     │ ← Context
├──────────────────────┤
│- strategy: Pricing   │
├──────────────────────┤
│+ calculate()         │
│+ set_strategy()      │
└──────────────────────┘
```

**Key insight:** Strategy pattern allows selecting algorithm at runtime - perfect for switching between different pricing models.
</details>

---

### Question 2:

**Amit is working on a graphical editing software. The application must support rendering text with different fonts, sizes, and colors. The application must also support rendering images with different dimensions and formats. Amit is concerned about the memory overhead of creating multiple text and image objects with the same state. Which design pattern should Amit use to achieve efficient memory usage?**

- A) Prototype
- B) Facade
- C) Flyweight
- D) Adapter

---

<details>
<summary>Answer</summary>

**C) Flyweight**

**Why Flyweight:**
- Shares common state (intrinsic) between objects to reduce memory
- Text with same font/size shares the font object
- Separates intrinsic state (shared) from extrinsic state (unique)
- Minimizes memory footprint when many similar objects exist

---
**UML Diagram:**
```
┌──────────────────────┐
│   TextFlyweight      │ ← Flyweight (shared)
├──────────────────────┤
│- font: str           │ ← Intrinsic state (shared)
│- size: int           │
├──────────────────────┤
│+ render(x, y, color) │ ← Extrinsic (passed in)
└──────────────────────┘

┌──────────────────────┐
│  FlyweightFactory    │ ← Creates/caches flyweights
├──────────────────────┤
│- flyweights: dict    │
├──────────────────────┤
│+ get_flyweight()     │ ← Returns shared instance
└──────────────────────┘

Example:
- 1000 text objects with "Arial, 12pt"
- Without Flyweight: 1000 font objects (wasteful)
- With Flyweight: 1 shared font object (efficient)
```

**Key insight:** Flyweight shares immutable common state to dramatically reduce memory when many similar objects exist.
</details>

---

### Question 3:

**Nitin is developing a RESTful API for an e-commerce platform. He wants to add logging functionality to track incoming requests, their payloads, and response statuses. Nitin aims to implement this logging without cluttering the main API code with repetitive logging statements. Which design pattern can Nitin use to wrap the API endpoints with logging behavior?**

- A) Decorator
- B) Facade
- C) Adapter
- D) Strategy

---

<details>
<summary>Answer</summary>

**A) Decorator**

**Why Decorator:**
- Adds logging behavior dynamically without modifying API code
- Wraps existing API endpoints with additional functionality
- Can stack multiple decorators (logging, authentication, caching)
- Maintains same interface as original API
---
**UML Diagram:**
```
┌──────────────────┐
│   APIEndpoint    │ ← Component Interface
├──────────────────┤
│+ handle_request()│
└──────────────────┘
         △
         │
    ┌────┴─────────────────┐
    │                      │
┌─────────────┐   ┌───────────────────┐
│  UserAPI    │   │ LoggingDecorator  │ ← Wraps API
├─────────────┤   ├───────────────────┤
│+ handle()   │   │- wrapped: API     │
└─────────────┘   │+ handle()         │ ← Adds logging
                  └───────────────────┘
                           │
                           │ wraps
                           ▼
                  ┌───────────────────┐
                  │   UserAPI         │
                  └───────────────────┘

Flow: Request → LoggingDecorator (logs) → UserAPI (processes)
```
---
**Code Implementation:**
```python
from abc import ABC, abstractmethod

# Component Interface
class APIEndpoint(ABC):
    @abstractmethod
    def handle_request(self, request):
        pass

# Concrete Component
class UserAPI(APIEndpoint):
    def handle_request(self, request):
        return {"status": 200, "user": "John Doe"}

# Decorator
class LoggingDecorator(APIEndpoint):
    def __init__(self, wrapped_api: APIEndpoint):
        self._wrapped = wrapped_api
    
    def handle_request(self, request):
        # Log before
        print(f"📝 Request: {request}")
        
        # Call wrapped API
        response = self._wrapped.handle_request(request)
        
        # Log after
        print(f"📝 Response: {response['status']}")
        
        return response

# Usage - Without decorator (cluttered)
api = UserAPI()
print("LOG: Request received")  # Repetitive logging
result = api.handle_request({"user_id": 123})
print(f"LOG: Response {result['status']}")  # Repetitive logging

# Usage - With decorator (clean)
api = UserAPI()
logged_api = LoggingDecorator(api)
result = logged_api.handle_request({"user_id": 123})
# Output:
# 📝 Request: {'user_id': 123}
# 📝 Response: 200
```
---
```python
# Can stack decorators
class AuthDecorator(APIEndpoint):
    def __init__(self, wrapped_api: APIEndpoint):
        self._wrapped = wrapped_api
    
    def handle_request(self, request):
        print("🔐 Checking authentication...")
        return self._wrapped.handle_request(request)

# Stack: Auth → Logging → UserAPI
api = UserAPI()
api = LoggingDecorator(api)
api = AuthDecorator(api)
result = api.handle_request({"user_id": 123})
# Output:
# 🔐 Checking authentication...
# 📝 Request: {'user_id': 123}
# 📝 Response: 200
```

**Key insight:** Decorator wraps objects to add responsibilities dynamically without changing their code - perfect for cross-cutting concerns like logging.
</details>

---

---

### Question 4:

**Prateek is building a game development framework. Different game levels have distinct challenges and environments, requiring unique objects like enemies and power-ups. Prateek needs a way to create these level-specific objects without directly instantiating them in the game code. Which design pattern is suitable for solving this problem and avoiding tight coupling?**

- A) Singleton
- B) Factory
- C) Prototype
- D) Builder

---

<details>
<summary>Answer</summary>

**B) Factory**

**Why Factory:**
- Encapsulates object creation logic for level-specific entities
- Game code doesn't need to know concrete classes
- Easy to add new enemy types or power-ups
- Decouples game logic from object instantiation

---

**UML Diagram:**
```
┌──────────────────────┐
│   GameEntity         │ ← Product Interface
└──────────────────────┘
           △
           │
    ┌──────┴───────┬────────┐
    │              │        │
┌────────┐  ┌──────────┐  ┌────────┐
│ Enemy  │  │ PowerUp  │  │ Obstacle│
└────────┘  └──────────┘  └────────┘

┌──────────────────────┐
│  EntityFactory       │ ← Factory
├──────────────────────┤
│+ create(type, level) │ ← Creates appropriate entity
└──────────────────────┘
           △
           │
    ┌──────┴────────┐
    │               │
┌─────────────┐  ┌─────────────┐
│Level1Factory│  │Level2Factory│ ← Level-specific
└─────────────┘  └─────────────┘
```
---
```python
Game code:
factory = Level1Factory()
enemy = factory.create("boss")  # Don't know concrete class
```

**Key insight:** Factory encapsulates object creation, allowing game to request entities without knowing their concrete classes - reduces coupling.
</details>

---

### Question 5:

**Debina is building a weather app that gathers data from different weather data providers. Each provider offers data in a different format and exposes distinct APIs. Debina aims to normalize the data format and ensure seamless integration with new weather data sources in the future. Which design pattern should Debina use to achieve these goals?**

- A) Adapter
- B) Facade
- C) Decorator
- D) Observer

---

<details>
<summary>Answer</summary>

**A) Adapter**

**Why Adapter:**
- Converts each provider's different format to uniform format
- Each provider has distinct API that needs to be normalized
- Easy to add new providers without changing app code
- Wraps incompatible interfaces to make them compatible

---
**UML Diagram:**
```
┌──────────────────────┐
│  WeatherProvider     │ ← Target Interface (app expects)
├──────────────────────┤
│+ get_temperature()   │
│+ get_humidity()      │
└──────────────────────┘
           △
           │ implements
    ┌──────┴─────────────┐
    │                    │
┌────────────────┐  ┌────────────────┐
│ OpenWeather    │  │  WeatherAPI    │ ← Adapters
│   Adapter      │  │    Adapter     │
├────────────────┤  ├────────────────┤
│- api           │  │- api           │
│+ get_temp()    │  │+ get_temp()    │
└────────────────┘  └────────────────┘
       │                    │
       │ uses               │ uses
       ▼                    ▼
┌────────────────┐  ┌────────────────┐
│ OpenWeatherAPI │  │  WeatherAPI    │ ← 3rd party APIs
│ (format A)     │  │  (format B)    │   (different formats)
└────────────────┘  └────────────────┘

Adapter translates:
- format A → unified format
- format B → unified format
```

**Key insight:** Adapter normalizes different data formats and APIs into uniform interface expected by the app.
</details>

---

### Question 6:

**Jagnesh is developing a software application for data analysis. The application involves data collection, preprocessing, analysis algorithms, and visualization. The interactions between these components can become complex. Jagnesh wants to provide a simplified interface for data analysts to perform end-to-end analysis tasks without dealing with the inner workings of each component. Which design pattern is suitable for this scenario?**

- A) Strategy
- B) Adapter
- C) Facade
- D) Observer

---

<details>
<summary>Answer</summary>

**C) Facade**

**Why Facade:**
- Provides simplified interface to complex subsystems
- Hides complexity of data collection, preprocessing, analysis, visualization
- Data analysts use simple methods, don't need to know internal components
- Single entry point for complex multi-step operations

---

**UML Diagram:**
```
┌──────────────────────┐
│   AnalysisFacade     │ ← Facade (simple interface)
├──────────────────────┤
│+ run_analysis(data)  │ ← One simple method
│+ generate_report()   │
└──────────────────────┘
           │
           │ coordinates
           ▼
    ┌──────┴─────┬────────────┬──────────────┐
    │            │            │              │
┌─────────┐ ┌────────────┐ ┌──────────┐ ┌──────────┐
│DataCol- │ │Preprocess- │ │Analysis  │ │Visualiza-│
│lector   │ │ing         │ │Engine    │ │tion      │
└─────────┘ └────────────┘ └──────────┘ └──────────┘
             ↑ Complex subsystems (hidden from user)

Without Facade:
collector.fetch()
preprocessor.clean()
preprocessor.normalize()
engine.train()
engine.predict()
visualizer.plot()  ← Complex!

With Facade:
facade.run_analysis(data)  ← Simple!
```

**Key insight:** Facade provides simple interface to complex system - users interact with one simple API instead of multiple complex components.
</details>

---

### Question 7:

**Aravinda is building a task management application. Users can create tasks and assign them to different team members. Aravinda wants to implement a feature where team members receive notifications whenever they are assigned a new task or when the due date of a task is approaching. The notifications should be sent through various communication channels, such as in-app alerts, emails, and Slack messages. Which design pattern can Aravinda use to implement this real-time task notification system?**

- A) Observer
- B) Adapter
- C) Facade
- D) Strategy

---

<details>
<summary>Answer</summary>

**A) Observer**

**Why Observer:**
- One task change triggers multiple notifications (one-to-many)
- Team members subscribe to task updates
- Multiple notification channels (email, Slack, in-app) observe same event
- Loose coupling between task and notification systems

---

**UML Diagram:**
```
┌──────────────────┐
│      Task        │ ← Subject (Observable)
├──────────────────┤
│- observers[]     │
├──────────────────┤
│+ attach()        │
│+ notify()        │
│+ assign()        │ ── triggers notify()
└──────────────────┘
         │
         │ notifies
         ▼
┌──────────────────┐
│   TaskObserver   │ ← Observer Interface
├──────────────────┤
│+ update(task)    │
└──────────────────┘
         △
         │
    ┌────┴──────────┬──────────────┐
    │               │              │
┌──────────┐  ┌───────────┐  ┌──────────┐
│  Email   │  │   Slack   │  │  InApp   │ ← Concrete Observers
│ Notifier │  │ Notifier  │  │ Notifier │
└──────────┘  └───────────┘  └──────────┘

Flow:
task.assign(user) → task.notify() → all observers.update()
                                   ├→ Email sent
                                   ├→ Slack message
                                   └→ In-app alert
```
</details>
---

### Question 8:

**Praveen is developing a logging module for a large application. The logging module needs to maintain a single log file throughout the application's execution to avoid file access conflicts and ensure consistency. Which design pattern is suitable for this scenario?**

- A) Singleton
- B) Factory
- C) Prototype
- D) Builder

---

<details>
<summary>Answer</summary>

**A) Singleton**

**Why Singleton:**
- Ensures only ONE logger instance exists
- Single log file handle shared across application
- Prevents multiple file handles causing conflicts
- Consistent logging throughout application lifecycle

---
**UML Diagram:**
```
┌─────────────────────┐
│      Logger         │
├─────────────────────┤
│- _instance: Logger  │ ← Static, single instance
│- log_file: File     │
├─────────────────────┤
│+ get_instance()     │ ← Returns single instance
│+ log(message)       │
└─────────────────────┘

Usage across application:
logger1 = Logger.get_instance()
logger2 = Logger.get_instance()
# logger1 === logger2 (same instance)
# Both write to same file handle
```

**Key insight:** Singleton guarantees single instance with global access point - essential for shared resources like log files.
</details>

---

### Question 9:

**Gokula is working on testing a user API for a social media platform. Each test case requires generating multiple mock users with different attributes to simulate various scenarios. However, calling the API to create each mock user is time-consuming and inefficient. To optimize the user creation process during testing, which design pattern can Gokula use?**

- A) Singleton
- B) Factory
- C) Prototype
- D) Builder

---

<details>
<summary>Answer</summary>

**C) Prototype**

**Why Prototype:**
- Creates new objects by cloning existing ones (faster than API calls)
- Create one prototype user, then clone with variations
- Avoids expensive initialization (API calls, database queries)
- Efficient for creating many similar objects with slight differences

---
**UML Diagram:**
```
┌──────────────────┐
│   UserPrototype  │ ← Prototype Interface
├──────────────────┤
│+ clone()         │
└──────────────────┘
         △
         │
┌────────┴─────────┐
│      User        │ ← Concrete Prototype
├──────────────────┤
│- name            │
│- email           │
│- profile         │
├──────────────────┤
│+ clone()         │ ← Returns copy of self
│+ set_name()      │
└──────────────────┘
Usage:
# Create prototype once (expensive API call)
prototype_user = User("John", "john@example.com")

# Clone for tests (fast, no API calls)
user1 = prototype_user.clone()
user1.set_name("Alice")

user2 = prototype_user.clone()
user2.set_name("Bob")

# Much faster than creating from scratch!
```
</details>
---

### Question 10:

```python
class ConfigManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:  # Lock acquired every time!
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
```

**What is the problem with this thread-safe Singleton implementation?**

- A) It is not thread-safe
- B) It is not performant (acquires lock on every call)
- C) It creates multiple instances
- D) It uses too much memory

---

<details>
<summary>Answer</summary>

**B) It is not performant (acquires lock on every call)**

**Problems:**
- After instance is created, we still check and acquire lock every time
- Lock acquisition is expensive (context switching, waiting)
- Unnecessary overhead for 99.99% of calls after initialization
- Becomes bottleneck in high-concurrency scenarios

**Performance impact:**
```python
# Every call does this, even after instance exists:
config = ConfigManager()  # Checks _instance, acquires lock, checks again
config = ConfigManager()  # Checks _instance, acquires lock, checks again
config = ConfigManager()  # Checks _instance, acquires lock, checks again
# Thousands of unnecessary lock operations!
```

**Better approach (Double-checked locking):**
```python
class ConfigManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:  # First check (no lock!)
            with cls._lock:  # Lock only if needed
                if cls._instance is None:  # Second check (with lock)
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Key insight:** Check existence BEFORE acquiring lock to avoid unnecessary synchronization overhead.
</details>

---
### Question 11:

```python
class DatabaseConnection:
    _instance = DatabaseConnection()  # Created at module load time
    
    def __init__(self):
        if DatabaseConnection._instance is not self:
            raise Exception("Singleton - use get_instance()")
        self.connection_string = "postgresql://localhost:5432/mydb"
        self.pool_size = 10
    
    @staticmethod
    def get_instance():
        return DatabaseConnection._instance
```

**Which Singleton implementation pattern is this?**

- A) Lazy initialization
- B) Eager initialization
- C) Thread-safe initialization
- D) Double-checked locking

---

<details>
<summary>Answer</summary>

**B) Eager initialization**

**Why Eager Initialization:**
- Instance created **immediately at class load time** (not when first accessed)
- `_instance = DatabaseConnection()` executes when module is imported
- No lazy evaluation - created whether needed or not
- Thread-safe by default (created before any threads can access)
---
**UML Diagram:**
```
┌──────────────────────────┐
│   DatabaseConnection     │
├──────────────────────────┤
│- _instance: static       │ ← Created immediately
│- connection_string: str  │
│- pool_size: int          │
├──────────────────────────┤
│+ get_instance(): static  │ ← Returns pre-created instance
└──────────────────────────┘
```
---

**Eager vs Lazy:**
```python
# EAGER - Created at import
class Config:
    _instance = Config()  # Created NOW
    
    @staticmethod
    def get_instance():
        return Config._instance

# Import happens → instance created
# Whether you call get_instance() or not

# LAZY - Created on first access
class Config:
    _instance = None
    
    @staticmethod
    def get_instance():
        if Config._instance is None:
            Config._instance = Config()  # Created only when called
        return Config._instance

# Import happens → nothing created yet
# First get_instance() call → instance created
```
---

**Pros:**
- ✅ Thread-safe (no race condition possible)
- ✅ Simple implementation
- ✅ Instance ready immediately

**Cons:**
- ❌ Wastes memory if never used
- ❌ Cannot pass parameters to constructor
- ❌ Increases application startup time
- ❌ Created even if initialization might fail

**When to use:**
- Resource is always needed (logger, config)
- Initialization is fast and cheap
- Single-threaded or thread-safety critical
- Cannot afford lazy initialization overhead

**Key insight:** Instance created eagerly at load time, not lazily on first access.
</details>

---

### Question 12:

**Jawahar is developing a complex configuration object with over 60 properties. Creating instances using traditional constructor is unwieldy and error-prone. Configuration objects should be immutable to ensure consistency. Which design pattern should Jawahar use?**

- A) Factory
- B) Builder
- C) Singleton
- D) Prototype

---

<details>
<summary>Answer</summary>

**B) Builder**

**Why Builder:**
- Constructs complex objects **step-by-step**
- Handles **many optional parameters** elegantly
- Creates **immutable objects** (set during build, frozen after)
- Provides **fluent, readable API** (method chaining)
- Validates configuration before creating object
- Separates construction from representation

---

**UML Diagram:**
```
┌──────────────────────┐
│   AppConfig          │ ← Product (immutable)
├──────────────────────┤
│- database_host: str  │ (All final/readonly)
│- database_port: int  │
│- api_key: str        │
│- cache_enabled: bool │
│- ... (60 properties) │
└──────────────────────┘
           ▲
           │ builds
           │
┌──────────────────────┐
│  ConfigBuilder       │ ← Builder
├──────────────────────┤
│- _host: str          │ (Mutable during build)
│- _port: int          │
│- _api_key: str       │
│- ... (temp values)   │
├──────────────────────┤
│+ set_database()      │ ─┐
│+ set_api_keys()      │  │ Return self
│+ set_cache()         │  │ (method chaining)
│+ set_logging()       │ ─┘
│+ build(): AppConfig  │ ← Creates immutable object
└──────────────────────┘
```
---

**Solution:**

**Builder vs Constructor:**
```python
# ❌ Constructor - 60 parameters!
config = AppConfig(
    "localhost", 5432, "mydb", "key", "secret",
    True, 3600, "INFO", 100, 30,
    # ... 50 more parameters
    # Which is which? Easy to mix up!
)

# ✅ Builder - Clear and self-documenting
config = (ConfigBuilder()
    .set_database("localhost", 5432, "mydb")
    .set_api_keys("key", "secret")
    .set_cache(True, 3600)
    .build())
```

**Key insight:** Builder separates complex construction from representation, providing a fluent API for creating immutable objects with many properties.
</details>

---

### Question 13:

```python
class QueryBuilder:
    def select(self, fields): return self
    def from_table(self, table): return self
    def where(self, condition): return self
    def join(self, table): return self
    def group_by(self, field): return self
    def order_by(self, field): return self
    def limit(self, n): return self
    def build(self): return "SQL Query"
```
---
```python
class QueryDirector:
    def __init__(self, builder: QueryBuilder):
        self._builder = builder
    
    def build_paginated_query(self, table, page_size):
        """Common recipe: Paginated SELECT"""
        return (self._builder
                .select("*")
                .from_table(table)
                .order_by("id")
                .limit(page_size)
                .build())
    
    def build_analytics_query(self, table, metric):
        """Common recipe: Analytics with grouping"""
        return (self._builder
                .select(f"COUNT({metric})")
                .from_table(table)
                .group_by("date")
                .order_by("date")
                .build())

# Usage
builder = QueryBuilder()
director = QueryDirector(builder)

query1 = director.build_simple_select("users")
query2 = director.build_paginated_query("orders", 50)
query3 = director.build_analytics_query("sales", "revenue")
```
---
**What is the role of QueryDirector in the Builder pattern?**

- A) Creates different types of builders
- B) Validates the built object
- C) Encapsulates common construction recipes/steps
- D) Makes the builder thread-safe

---

<details>
<summary>Answer</summary>

**C) Encapsulates common construction recipes/steps**

**Why Director:**
- **Encapsulates common construction sequences** - reusable recipes
- Knows **how to use the builder** to create common configurations
- Client doesn't need to know construction steps
- Provides **pre-defined construction methods**
- Separates "what to build" (builder) from "how to orchestrate" (director)
---
**Director's Purpose:**
```python
# WITHOUT Director - Client must know all steps
query = (QueryBuilder()
         .select("*")
         .from_table("users")
         .where("age > 18")
         .where("status = 'active'")
         .order_by("created_at")
         .limit(100)
         .build())
# Client repeats this pattern everywhere!

# WITH Director - Encapsulated recipe
query = director.build_active_users_query("users", 100)
# Director knows the recipe, client just calls it!
```
---
**Key Characteristics:**
```
┌──────────────────┐
│     Client       │
└──────────────────┘
         │ calls
         ▼
┌──────────────────┐
│    Director      │ ← Encapsulates recipes
├──────────────────┤
│+ build_simple()  │ ← Recipe 1
│+ build_complex() │ ← Recipe 2
│+ build_custom()  │ ← Recipe 3
└──────────────────┘
         │ uses
         ▼
┌──────────────────┐
│     Builder      │ ← Provides building blocks
├──────────────────┤
│+ step1()         │
│+ step2()         │
│+ build()         │
└────────────────── ┘
```
---
**Real-world analogy:**
- **Builder** = Chef's tools (knife, pan, oven)
- **Director** = Recipe book (tells you how to combine tools)
- **Client** = Home cook (just follows recipe)
---
**Example with multiple recipes:**
```python
class DocumentDirector:
    def __init__(self, builder):
        self._builder = builder
    
    def build_invoice(self, data):
        """Recipe: Standard invoice format"""
        return (self._builder
                .add_header("INVOICE")
                .add_company_logo()
                .add_billing_info(data)
                .add_line_items(data.items)
                .add_total(data.total)
                .add_footer("Thank you")
                .build())
    
    def build_receipt(self, data):
        """Recipe: Simple receipt format"""
        return (self._builder
                .add_header("RECEIPT")
                .add_line_items(data.items)
                .add_total(data.total)
                .build())
    
    def build_quote(self, data):
        """Recipe: Quote format"""
        return (self._builder
                .add_header("QUOTATION")
                .add_company_logo()
                .add_line_items(data.items)
                .add_total(data.total)
                .add_validity_date(30)
                .build())
```
---
**When to use Director:**
- Multiple common construction patterns
- Complex multi-step construction
- Want to reuse construction logic
- Hide complexity from client
- Need different "recipes" for same builder

**Key insight:** Director orchestrates the builder, providing pre-defined recipes so clients don't need to know construction details.
</details>

---

### Question 14:

**Amit needs to integrate Uber with different insurance providers. Each provider has different APIs and data formats. He wants uniform interface in codebase and easy addition of new providers. Which design pattern should he use?**

- A) Factory
- B) Builder
- C) Adapter
- D) Facade

---

<details>
<summary>Answer</summary>

**C) Adapter**

**Why Adapter:**
- Converts **incompatible interfaces** to compatible ones
- Each provider has **different method names and signatures**
- Uber needs **one uniform interface** across all providers
- Easy to **add new providers** without modifying existing code
- Wraps third-party APIs (cannot modify them)

---

**UML Diagram:**
```
┌─────────────────────┐
│ InsuranceProvider   │ ← Target Interface (what Uber wants)
├─────────────────────┤
│+ create_policy()    │
│+ get_status()       │
└─────────────────────┘
           △
           │ implements
    ┌──────┴──────────────────┐
    │              │           │
┌────────────┐ ┌────────────┐ ┌────────────┐
│ICICI Adapter│ │HDFCAdapter │ │BajajAdapter│ ← Adapters
├────────────┤ ├────────────┤ ├────────────┤
│- api       │ │- api       │ │- api       │
├────────────┤ ├────────────┤ ├────────────┤
│+ create()  │ │+ create()  │ │+ create()  │
│+ status()  │ │+ status()  │ │+ status()  │
└────────────┘ └────────────┘ └────────────┘
      │              │              │
      │ uses         │ uses         │ uses
      ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ ICICI API  │ │  HDFC API  │ │ Bajaj API  │ ← Adaptees
└────────────┘ └────────────┘ └────────────┘
  (3rd party)    (3rd party)    (3rd party)
```
---
**Solution:**
```python
from abc import ABC, abstractmethod
from typing import Dict
from dataclasses import dataclass

# Common data format Uber wants
@dataclass
class PolicyResponse:
    policy_id: str
    premium: float
    provider: str

@dataclass
class StatusResponse:
    is_active: bool
    expiry_date: str

# Target interface - what Uber expects
class InsuranceProvider(ABC):
    @abstractmethod
    def create_policy(self, vehicle_id: str, driver_id: str) -> PolicyResponse:
        pass
    
    @abstractmethod
    def get_policy_status(self, policy_id: str) -> StatusResponse:
        pass

# Adapter 1: ICICI Lombard
class ICICIAdapter(InsuranceProvider):
    def __init__(self):
        self._api = ICICILombardAPI()
    
    def create_policy(self, vehicle_id: str, driver_id: str) -> PolicyResponse:
        # Adapt Uber's format to ICICI's format
        vehicle_data = {"id": vehicle_id}
        driver_data = {"id": driver_id}
        
        # Call ICICI API
        result = self._api.create_policy(vehicle_data, driver_data)
        
        # Convert ICICI response to Uber format
        return PolicyResponse(
            policy_id=result["policy_id"],
            premium=result["premium"],
            provider="ICICI Lombard"
        )
    
    def get_policy_status(self, policy_id: str) -> StatusResponse:
        result = self._api.get_policy_status(policy_id)
        return StatusResponse(
            is_active=result["status"] == "active",
            expiry_date=result["expiry"]
        )
```
---
```python
# Adapter 2: HDFC Ergo (different interface!)
class HDFCAdapter(InsuranceProvider):
    def __init__(self):
        self._api = HdfcErgoAPI()
    
    def create_policy(self, vehicle_id: str, driver_id: str) -> PolicyResponse:
        # Adapt to HDFC's different method name and format
        car_info = {"vehicle_id": vehicle_id}
        owner_info = {"driver_id": driver_id}
        
        # Call HDFC API (different method name!)
        result = self._api.initiate_insurance(car_info, owner_info)
        
        # Convert HDFC response to Uber format
        return PolicyResponse(
            policy_id=result["reference"],  # Different key name!
            premium=result["amount"],       # Different key name!
            provider="HDFC Ergo"
        )
    
    def get_policy_status(self, policy_id: str) -> StatusResponse:
        # Different method name!
        result = self._api.check_insurance(policy_id)
        return StatusResponse(
            is_active=result["state"] == "valid",  # Different key!
            expiry_date=result["expires_on"]       # Different key!
        )
    
```
---
```python
# Adapter 3: Bajaj Allianz (yet another different interface!)
class BajajAdapter(InsuranceProvider):
    def __init__(self):
        self._api = BajajAllianzAPI()
    
    def create_policy(self, vehicle_id: str, driver_id: str) -> PolicyResponse:
        vehicle = {"v_id": vehicle_id}
        customer = {"d_id": driver_id}
        
        # Different method name!
        result = self._api.new_policy(vehicle, customer)
        
        return PolicyResponse(
            policy_id=result["policy_no"],  # Different key!
            premium=result["cost"],          # Different key!
            provider="Bajaj Allianz"
        )
    
    def get_policy_status(self, policy_id: str) -> StatusResponse:
        # Different method name!
        result = self._api.policy_details(policy_id)
        return StatusResponse(
            is_active=result["active"],      # Different format!
            expiry_date=result["valid_till"] # Different key!
        )
```
---
```python
# Uber's code - works with ANY provider!
class InsuranceService:
    def __init__(self, provider: InsuranceProvider):
        self._provider = provider
    
    def buy_insurance(self, vehicle_id: str, driver_id: str):
        """Uniform method regardless of provider"""
        policy = self._provider.create_policy(vehicle_id, driver_id)
        print(f"✓ Policy created: {policy.policy_id}")
        print(f"✓ Premium: ₹{policy.premium}")
        print(f"✓ Provider: {policy.provider}")
        return policy
    
    def check_coverage(self, policy_id: str):
        """Uniform method regardless of provider"""
        status = self._provider.get_policy_status(policy_id)
        print(f"✓ Active: {status.is_active}")
        print(f"✓ Expires: {status.expiry_date}")
        return status

# Usage - Easy to switch providers!
icici_service = InsuranceService(ICICIAdapter())
icici_service.buy_insurance("V123", "D456")

hdfc_service = InsuranceService(HDFCAdapter())
hdfc_service.buy_insurance("V123", "D456")

bajaj_service = InsuranceService(BajajAdapter())
bajaj_service.buy_insurance("V123", "D456")

# Adding new provider? Just create new adapter!
class NewProviderAdapter(InsuranceProvider):
    def create_policy(self, vehicle_id, driver_id):
        # Adapt new provider's API
        pass
    
    def get_policy_status(self, policy_id):
        # Adapt new provider's API
        pass

# No changes to InsuranceService! ✅
```
---
**Why not other patterns:**
```python
# ❌ Factory - Creates objects, doesn't adapt interfaces
# ❌ Builder - For complex construction, not interface conversion
# ❌ Facade - Simplifies multiple interfaces, not converts them
# ✅ Adapter - Converts incompatible interface to expected interface
```

---
**Benefits:**
- ✅ Uniform interface across all providers
- ✅ Easy to add new providers (just create adapter)
- ✅ No modification to third-party APIs
- ✅ No modification to Uber's core code
- ✅ Each provider isolated in its adapter
- ✅ Easy to test (mock InsuranceProvider interface)

**When to use Adapter:**
- Integrating third-party libraries with different APIs
- Making incompatible interfaces work together
- Cannot modify existing classes
- Need uniform interface across multiple implementations

**Key insight:** Adapter wraps incompatible interface and translates calls to match what client expects, enabling seamless integration without modifying existing code.
</details>

---

### Question 15:

```python
class Image:
    def __init__(self, pixels):
        self.pixels = pixels
    
    def apply_filter(self):
        return self.pixels

# User wants to apply brightness, then contrast, then blur
# How to combine multiple filters without modifying Image class?
```

**Mahaboob is building an image editor where users can apply multiple transformations (brightness, contrast, blur) in any order. Which pattern is best?**

- A) Strategy
- B) Decorator
- C) Adapter
- D) Chain of Responsibility

---

<details>
<summary>Answer</summary>

**B) Decorator**

**Why Decorator:**
- Adds behavior to objects dynamically
- Can stack multiple decorators
- Maintains interface compatibility
- Open for extension without modifying original class
- Order of decorators matters (brightness → contrast → blur)
---

**UML Diagram:**
```
┌─────────────────┐
│   ImageFilter   │ ← Component Interface
├─────────────────┤
│+ apply_filter() │
└─────────────────┘
         △
         │
    ┌────┴─────────────────────┐
    │                          │
┌───────────┐      ┌──────────────────┐
│   Image   │      │ FilterDecorator  │ ← Base Decorator
├───────────┤      ├──────────────────┤
│- pixels   │      │- wrapped: Image  │ (wraps component)
├───────────┤      ├──────────────────┤
│+ apply()  │      │+ apply()         │
└───────────┘      └──────────────────┘
                            △
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
  ┌─────────────┐   ┌──────────────┐  ┌─────────────┐
  │ Brightness  │   │  Contrast    │  │    Blur     │
  │  Filter     │   │   Filter     │  │   Filter    │
  └─────────────┘   └──────────────┘  └─────────────┘
```
---
**Solution:**
```python
from abc import ABC, abstractmethod

# Component interface
class ImageFilter(ABC):
    @abstractmethod
    def apply_filter(self):
        pass

# Concrete component
class Image(ImageFilter):
    def __init__(self, pixels):
        self.pixels = pixels
    
    def apply_filter(self):
        return self.pixels

# Base decorator
class FilterDecorator(ImageFilter):
    def __init__(self, image: ImageFilter):
        self._image = image
    
    def apply_filter(self):
        return self._image.apply_filter()

# Concrete decorators
class BrightnessFilter(FilterDecorator):
    def apply_filter(self):
        pixels = super().apply_filter()
        return f"Brightness({pixels})"

class ContrastFilter(FilterDecorator):
    def apply_filter(self):
        pixels = super().apply_filter()
        return f"Contrast({pixels})"

class BlurFilter(FilterDecorator):
    def apply_filter(self):
        pixels = super().apply_filter()
        return f"Blur({pixels})"

# Stack decorators dynamically!
image = Image("raw_pixels")
filtered = BrightnessFilter(
              ContrastFilter(
                  BlurFilter(image)))

print(filtered.apply_filter())
# Output: Brightness(Contrast(Blur(raw_pixels)))
```

**Key insight:** Each decorator wraps the previous one, adding its behavior while maintaining the same interface.

**When to use:** Adding responsibilities dynamically, avoiding subclass explosion, reversible modifications
</details>

---

### Question 16:

**A library system tracks the availability of books.
Whenever a borrowed item is returned, the system automatically informs every student who had expressed interest in that item. Each interested student receives an update the moment the book becomes available again**
- A) Factory
- B) Observer
- C) Singleton
- D) Strategy

---

<details>
<summary>Answer</summary>

**B) Observer**

**Why Observer:**
- One-to-many dependency between objects
- When one object changes state, all dependents are notified
- Loose coupling between subject and observers
- Supports broadcast communication
---
**UML Diagram:**
```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│      ┌────────────────────────┐           ┌──────────────────────────┐   │
│      │     <<interface>>      │           │      <<interface>>       │   │
│      │        Subject         │           │        Observer          │   │
│      │────────────────────────│           │──────────────────────────│   │
│      │ + attach(observer)     │◄──────────┤ + update(book)           │   │
│      │ + detach(observer)     │           └──────────────────────────┘   │
│      │ + notify(book)         │                        △                 │
│      └────────────────────────┘                        │                 │
│                  △                                      │                 │
│                  │                                ┌─────┼──────────────┐ │
│                  │                                │     │              │ │
│      ┌────────────────────────┐       ┌────────────────┐ ┌────────────────┐│
│      │       Library          │       │    Student     │ │   Professor     ││
│      │────────────────────────│       │────────────────│ │────────────────││
│      │ - books: list          │       │ + update(book) │ │ + update(book) ││
│      │ - observers: list      │       └────────────────┘ └────────────────┘│
│      │────────────────────────│                                            │
│      │ + return_book(book)    │── triggers ───────────────────────────────►│
│      │ + attach(observer)     │                 notifications               │
│      │ + detach(observer)     │                                            │
│      │ + notify(book)         │                                            │
│      └────────────────────────┘                                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```
---

**Complete solution:**
```python
from abc import ABC, abstractmethod
from typing import List

# Observer interface
class BookObserver(ABC):
    @abstractmethod
    def update(self, book: 'Book') -> None:
        pass

# Subject
class Library:
    def __init__(self):
        self._books: List[Book] = []
        self._observers: List[BookObserver] = []
    
    def attach(self, observer: BookObserver) -> None:
        """Subscribe to book availability notifications"""
        self._observers.append(observer)
    
    def detach(self, observer: BookObserver) -> None:
        """Unsubscribe from notifications"""
        self._observers.remove(observer)
    
    def return_book(self, book: Book) -> None:
        book.is_available = True
        self._notify_all(book)
    
    def _notify_all(self, book: Book) -> None:
        """Notify all observers"""
        for observer in self._observers:
            observer.update(book)
            
```
---
```python
# Concrete observers
class Student(BookObserver):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, book: Book) -> None:
        print(f"📧 {self.name}: {book.title} is available!")

class Professor(BookObserver):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, book: Book) -> None:
        print(f"🔔 Prof. {self.name}: Reserved {book.title}")

# Usage
library = Library()
alice = Student("Alice")
bob = Student("Bob")
prof = Professor("Smith")

# Subscribe
library.attach(alice)
library.attach(bob)
library.attach(prof)

# Book returned - all notified!
book = Book("123", "Design Patterns")
library.return_book(book)

# Output:
# 📧 Alice: Design Patterns is available!
# 📧 Bob: Design Patterns is available!
# 🔔 Prof. Smith: Reserved Design Patterns
```

**When to use:** Event handling, pub-sub systems, notification systems, UI updates
</details>

---

### Question 17:

```python
class ParkingLot:
    def __init__(self):
        self._floors = []
        for i in range(5):
            self._floors.append(Floor(i))  # ParkingLot creates Floors
    
    def __del__(self):
        # When ParkingLot destroyed, Floors are destroyed
        self._floors.clear()

class Floor:
    def __init__(self, number):
        self.number = number
        self.spots = []
```

**What is the relationship between ParkingLot and Floor?**

- A) Association
- B) Aggregation
- C) Composition
- D) Inheritance

---

<details>
<summary>Answer</summary>

**C) Composition**

**Why Composition:**
- ParkingLot **creates and owns** Floors
- Floors **cannot exist independently** of ParkingLot
- When ParkingLot is destroyed, Floors are destroyed
- Strong "part-of" relationship
- Lifetime dependency: Floors die with ParkingLot
---
**UML Diagram:**
```
┌─────────────────┐
│  ParkingLot     │
├─────────────────┤
│- floors: List   │
├─────────────────┤
│+ __init__()     │
│+ __del__()      │
└─────────────────┘
         ◆  ← Filled diamond = Composition
         │     (strong ownership)
         │
         ▼
┌─────────────────┐
│     Floor       │
├─────────────────┤
│- number: int    │
│- spots: List    │
├─────────────────┤
│+ add_spot()     │
└─────────────────┘
```
---
**Characteristics of Composition:**
```python
# 1. Owner creates parts
lot = ParkingLot()  # Creates its own floors

# 2. Parts don't exist independently
# You can't do: floor = Floor(1) then lot.add_floor(floor)
# Floors are created INSIDE ParkingLot

# 3. When owner dies, parts die
del lot  # All floors destroyed too

# 4. Strong coupling - parts are internal implementation
```

**Real-world analogy:** 
- A **house** and its **rooms** (composition)
- If house is demolished, rooms cease to exist
- Rooms are integral parts of the house

**When to use composition:**
- Part cannot exist without whole
- Part is exclusively owned by whole
- Part's lifecycle is managed by whole
- Strong encapsulation needed
</details>

---

### Question 18:

```python
class Library:
    def __init__(self):
        self._members = []  # Members exist independently
    
    def register_member(self, member):
        """Member created outside, library just holds reference"""
        self._members.append(member)
    
    def remove_member(self, member):
        self._members.remove(member)
        # Member object still exists after removal!

class Member:
    def __init__(self, name):
        self.name = name
    
    # Can exist without being part of any library
```

**What is the relationship between Library and Member?**

- A) Association
- B) Aggregation
- C) Composition
- D) Dependency

---

<details>
<summary>Answer</summary>

**B) Aggregation**

**Why Aggregation:**
- Library **holds references** to Members but doesn't create them
- Members **exist independently** of Library
- Members can be part of multiple libraries
- When Library is destroyed, Members still exist
- Weak "has-a" relationship
---
**UML Diagram:**
```
┌─────────────────┐
│    Library      │
├─────────────────┤
│- members: List  │
├─────────────────┤
│+ register()     │
│+ remove()       │
└─────────────────┘
         ◇  ← Empty diamond = Aggregation
         │     (weak ownership)
         │
         ▼
┌─────────────────┐
│     Member      │
├─────────────────┤
│- name: str      │
│- member_id      │
├─────────────────┤
│+ borrow_book()  │
└─────────────────┘
```
---
**Characteristics of Aggregation:**
```python
# 1. Parts created outside owner
alice = Member("Alice")  # Created independently
bob = Member("Bob")

# 2. Owner receives references
city_library = Library()
city_library.register_member(alice)

college_library = Library()
college_library.register_member(alice)  # Same member, multiple libraries!

# 3. Parts outlive owner
del city_library
# Alice still exists!

# 4. Weak coupling - parts are external
```

**Composition vs Aggregation:**
```python
# COMPOSITION - Strong ownership
class Order:
    def __init__(self):
        self.items = []  # Order CREATES items
        self.items.append(OrderItem())  # Can't exist without Order

# AGGREGATION - Weak ownership  
class Playlist:
    def __init__(self):
        self.songs = []  # Playlist holds references
    
    def add_song(self, song):  # Song exists independently
        self.songs.append(song)  # Can exist without Playlist
```

**Real-world analogy:**
- A **department** and its **employees** (aggregation)
- Employees exist before joining department
- Employees can work in multiple departments
- If department closes, employees still exist

**When to use aggregation:**
- Part can exist independently
- Part can be shared by multiple wholes
- Lifecycle not strictly managed by owner
- Flexible, loosely coupled design needed
</details>

---

### Question 19:

```python
class NotificationService:
    def __init__(self):
        self.email_sender = SMTPEmailSender()  # Hardcoded dependency!
    
    def notify_user(self, user, message):
        self.email_sender.send(user.email, message)
```

**What SOLID principle is violated here?**

- A) Single Responsibility Principle
- B) Open/Closed Principle
- C) Liskov Substitution Principle
- D) Dependency Inversion Principle

---

<details>
<summary>Answer</summary>

**D) Dependency Inversion Principle**

**Why DIP is violated:**
- High-level module (NotificationService) depends on low-level module (SMTPEmailSender)
- Depends on concrete class, not abstraction
- Cannot swap email for SMS without modifying NotificationService
- Cannot test without real email infrastructure
- Tightly coupled to implementation details

**Dependency Inversion Principle states:**
> "High-level modules should not depend on low-level modules. Both should depend on abstractions."
---
**Problems with current code:**
```python
# ❌ BAD: Want to add SMS? Must modify NotificationService!
class NotificationService:
    def __init__(self):
        self.sms_sender = TwilioSMSSender()  # Changed here
    
    def notify_user(self, user, message):
        self.sms_sender.send(user.phone, message)  # Changed here

# ❌ BAD: Can't test without real SMTP connection
def test_notify_user():
    service = NotificationService()  # Creates real SMTPEmailSender!
    service.notify_user(user, "Hello")  # Actually sends email!
```
---
**Solution - Depend on abstraction:**
```python
from abc import ABC, abstractmethod

# Abstraction (interface)
class MessageSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass

# Low-level modules implement abstraction
class SMTPEmailSender(MessageSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"📧 Sending email to {recipient}: {message}")

class TwilioSMSSender(MessageSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"📱 Sending SMS to {recipient}: {message}")

class PushNotificationSender(MessageSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"🔔 Sending push to {recipient}: {message}")

# High-level module depends on abstraction
class NotificationService:
    def __init__(self, sender: MessageSender):  # Dependency injection!
        self._sender = sender
    
    def notify_user(self, user, message):
        self._sender.send(user.contact, message)

# Easy to swap implementations!
email_service = NotificationService(SMTPEmailSender())
sms_service = NotificationService(TwilioSMSSender())

# Easy to test with fake!
class FakeSender(MessageSender):
    def send(self, recipient, message):
        self.last_message = message

def test_notify():
    fake = FakeSender()
    service = NotificationService(fake)
    service.notify_user(user, "Hello")
    assert fake.last_message == "Hello"
```
---
**Dependency Flow:**
```
❌ BEFORE (Violates DIP):
┌──────────────────────┐
│ NotificationService  │ (High-level)
└──────────────────────┘
           │
           │ depends on
           ▼
┌──────────────────────┐
│  SMTPEmailSender     │ (Low-level, concrete)
└──────────────────────┘

✅ AFTER (Follows DIP):
┌──────────────────────┐
│ NotificationService  │ (High-level)
└──────────────────────┘
           │
           │ depends on
           ▼
┌──────────────────────┐
│   MessageSender      │ (Abstraction)
└──────────────────────┘
           △
           │ implements
           │
    ┌──────┴────────┐
    │               │
┌─────────────┐ ┌──────────────┐
│ EmailSender │ │  SMSSender   │ (Low-level)
└─────────────┘ └──────────────┘
```

**Key insight:** Both high and low level modules should depend on abstraction, creating an "inversion" of traditional dependency direction.
</details>

---

### Question 20:

```python
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self._items = []  # Order creates and owns items
    
    def add_item(self, product, quantity):
        item = OrderItem(product, quantity, self)  # Order creates item
        self._items.append(item)
    
    def __del__(self):
        # When order deleted, items are deleted too
        self._items.clear()

class OrderItem:
    def __init__(self, product, quantity, order):
        self.product = product
        self.quantity = quantity
        self.order = order  # Back reference to parent
    
    # Cannot exist without an Order
```

**What is the relationship between Order and OrderItem?**

- A) Association
- B) Aggregation  
- C) Composition
- D) Inheritance

---

<details>
<summary>Answer</summary>

**C) Composition**

**Why Composition:**
- Order **creates and exclusively owns** OrderItems
- OrderItems **cannot exist independently** of Order
- When Order is destroyed, OrderItems are destroyed
- Strong lifecycle dependency
- Part-whole relationship with strong ownership
---
**UML Diagram:**
```
┌─────────────────┐
│     Order       │
├─────────────────┤
│- order_id       │
│- items: List    │
├─────────────────┤
│+ add_item()     │
│+ remove_item()  │
│+ calculate()    │
└─────────────────┘
         ◆  ← Filled diamond = Composition
         │     (strong ownership)
         │ 1
         │
         │ *
         ▼
┌─────────────────┐
│   OrderItem     │
├─────────────────┤
│- product        │
│- quantity       │
│- price          │
├─────────────────┤
│+ get_subtotal() │
└─────────────────┘
```
---
**Characteristics demonstrated:**
```python
# 1. Parent creates children
order = Order("ORD123")
order.add_item(product, 2)  # Order creates OrderItem internally

# 2. Children cannot exist without parent
# You CANNOT do this:
# item = OrderItem(product, 2)  # Requires parent Order!
# standalone_items = [item1, item2]  # Makes no sense

# 3. Lifecycle dependency
del order  # All OrderItems destroyed automatically

# 4. Exclusive ownership
# OrderItem belongs to ONE Order only
# Cannot share OrderItem between Orders
```
---
**Real-world examples of Composition:**
```python
# House and Rooms
class House:
    def __init__(self):
        self.rooms = [Room("Living"), Room("Bedroom")]
    # Rooms are part of house structure

# Car and Engine
class Car:
    def __init__(self):
        self.engine = Engine()  # Engine is integral part
    # Engine cannot exist without car context

# Document and Paragraphs
class Document:
    def __init__(self):
        self.paragraphs = []
    
    def add_paragraph(self, text):
        self.paragraphs.append(Paragraph(text))
    # Paragraphs belong to this document
```
---
**Composition vs Aggregation:**
```python
# COMPOSITION - Order and OrderItem
order = Order("123")
order.add_item(product, 2)  # Order CREATES item
# Item belongs exclusively to order
# Item dies with order

# AGGREGATION - Playlist and Song
playlist = Playlist("Favorites")
song = Song("Bohemian Rhapsody")  # Song exists independently
playlist.add_song(song)  # Playlist just holds reference
# Song can be in multiple playlists
# Song continues to exist after playlist deleted
```

**When to use Composition:**
- Part is meaningless without whole
- Part is created by whole
- Part has same lifetime as whole
- Strong encapsulation needed
- Part is implementation detail of whole

**Examples in LLD:**
- ParkingLot ◆→ Floor (floors are part of lot structure)
- Invoice ◆→ LineItem (line items belong to invoice)
- ShoppingCart ◆→ CartItem (cart items exist only in cart)
- Game ◆→ GameState (state belongs to game instance)
</details>

---