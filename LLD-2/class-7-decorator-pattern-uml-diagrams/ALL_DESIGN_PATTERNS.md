# Design Patterns - Complete Overview

> All 23 Gang of Four (GoF) patterns + common variations

---

## Pattern Categories

### 🏗️ Creational Patterns (5)
*How objects are created*

| Pattern | Frequency | One-liner |
|---------|-----------|-----------|
| **Singleton** | ⭐⭐⭐⭐⭐ Very Common | One instance globally |
| **Factory Method** | ⭐⭐⭐⭐⭐ Very Common | Create via inheritance |
| **Abstract Factory** | ⭐⭐⭐ Common | Create families of objects |
| **Builder** | ⭐⭐⭐⭐ Very Common | Step-by-step construction |
| **Prototype** | ⭐⭐ Occasionally | Clone objects |

---

### 🔧 Structural Patterns (7)
*How objects are composed*

| Pattern | Frequency | One-liner |
|---------|-----------|-----------|
| **Adapter** | ⭐⭐⭐⭐⭐ Very Common | Convert interface |
| **Decorator** | ⭐⭐⭐⭐ Very Common | Add responsibilities dynamically |
| **Proxy** | ⭐⭐⭐⭐ Very Common | Control access to object |
| **Facade** | ⭐⭐⭐⭐⭐ Very Common | Simplified interface |
| **Bridge** | ⭐⭐ Occasionally | Separate abstraction from implementation |
| **Composite** | ⭐⭐⭐ Common | Tree structure (part-whole) |
| **Flyweight** | ⭐ Rarely | Share fine-grained objects |

---

### 🎭 Behavioral Patterns (11)
*How objects interact and communicate*

| Pattern | Frequency | One-liner |
|---------|-----------|-----------|
| **Strategy** | ⭐⭐⭐⭐⭐ Very Common | Swap algorithms |
| **Observer** | ⭐⭐⭐⭐⭐ Very Common | One-to-many notification |
| **Command** | ⭐⭐⭐⭐ Very Common | Encapsulate request as object |
| **Template Method** | ⭐⭐⭐⭐ Very Common | Algorithm skeleton |
| **State** | ⭐⭐⭐ Common | Object changes behavior with state |
| **Iterator** | ⭐⭐⭐⭐⭐ Very Common | Traverse collection |
| **Chain of Responsibility** | ⭐⭐⭐ Common | Pass request along chain |
| **Mediator** | ⭐⭐ Occasionally | Centralize complex communication |
| **Memento** | ⭐⭐ Occasionally | Capture/restore object state |
| **Visitor** | ⭐ Rarely | Add operations without modifying classes |
| **Interpreter** | ⭐ Rarely | Grammar/language interpreter |

---

## Most Used Patterns (Top 10)

**Interview Gold - Master These:**

1. **Singleton** ⭐⭐⭐⭐⭐
2. **Factory Method** ⭐⭐⭐⭐⭐
3. **Strategy** ⭐⭐⭐⭐⭐
4. **Observer** ⭐⭐⭐⭐⭐
5. **Decorator** ⭐⭐⭐⭐
6. **Adapter** ⭐⭐⭐⭐⭐
7. **Facade** ⭐⭐⭐⭐⭐
8. **Proxy** ⭐⭐⭐⭐
9. **Builder** ⭐⭐⭐⭐
10. **Command** ⭐⭐⭐⭐

**Know these 10 cold for interviews!**

---

## Patterns Covered in Detail

✅ **Singleton** - Database connections, loggers  
✅ **Factory Method** - Payment gateways, notifications  
✅ **Abstract Factory** - UI themes, database connectors  
✅ **Builder** - Query builders, complex objects  
✅ **Prototype** - Game characters, templates  
✅ **Adapter** - Legacy system integration  
✅ **Decorator** - I/O streams, middleware  
✅ **Strategy** - Routing algorithms, pricing  
✅ **Observer** - Event systems, MVC  

---

## Patterns Not Yet Covered

### 🏗️ Creational: None (All covered!)

---

### 🔧 Structural Patterns

---

#### Proxy Pattern

**Purpose:** Control access to an object

**UML:**
```
┌─────────┐       ┌─────────────┐
│ Client  │──────►│   Subject   │
└─────────┘       └──────△──────┘
                         │ implements
                  ┌──────┴──────┐
                  ▼             ▼
            RealSubject      Proxy
                             │
                             └──► wraps RealSubject
```

**Code:**
```python
class RealService:
    def request(self):
        return "Real service"

class Proxy:
    def __init__(self):
        self._real_service = None
    
    def request(self):
        if self._real_service is None:
            self._real_service = RealService()  # Lazy loading
        return self._real_service.request()
```

**Types:**
- **Virtual Proxy:** Lazy loading (load on demand)
- **Protection Proxy:** Access control
- **Remote Proxy:** Network calls (RPC)
- **Cache Proxy:** Cache results

**Use Cases:**
- Lazy loading images/videos
- Database connection pooling
- API rate limiting
- Authentication/authorization checks

**Real Examples:**
- Django ORM QuerySets (lazy evaluation)
- Hibernate proxies
- ES6 Proxy object

---

#### Facade Pattern

**Purpose:** Simplified interface to complex subsystem

**UML:**
```
┌─────────┐       ┌─────────────┐
│ Client  │──────►│   Facade    │
└─────────┘       └──────┬──────┘
                         │ simplifies
                  ┌──────┼──────┐
                  ▼      ▼      ▼
             SubsystemA  B   C
```

**Code:**
```python
# Complex subsystems
class CPU:
    def freeze(self): pass
    def jump(self, position): pass
    def execute(self): pass

class Memory:
    def load(self, position, data): pass

class HardDrive:
    def read(self, lba, size): pass

# Facade - simple interface
class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hd = HardDrive()
    
    def start(self):
        self.cpu.freeze()
        self.memory.load(0, self.hd.read(0, 1024))
        self.cpu.jump(0)
        self.cpu.execute()

# Usage
computer = ComputerFacade()
computer.start()  # Simple! Hides complexity
```

**Use Cases:**
- Library wrappers (hide complex APIs)
- Payment gateway facade (Stripe, PayPal, etc.)
- Database access layer
- Operating system API

**Real Examples:**
- jQuery (facade over DOM API)
- Pandas (facade over NumPy)
- requests library (facade over urllib)

---

#### Composite Pattern

**Purpose:** Treat individual objects and compositions uniformly (tree structure)

**UML:**
```
        ┌───────────┐
        │ Component │
        └─────△─────┘
              │
      ┌───────┴───────┐
      ▼               ▼
   Leaf          Composite
                    │
                    └──► children: Component[]
```

**Code:**
```python
class FileSystemComponent(ABC):
    @abstractmethod
    def get_size(self):
        pass

class File(FileSystemComponent):
    def __init__(self, size):
        self._size = size
    
    def get_size(self):
        return self._size

class Folder(FileSystemComponent):
    def __init__(self):
        self._children = []
    
    def add(self, component):
        self._children.append(component)
    
    def get_size(self):
        return sum(child.get_size() for child in self._children)

# Usage
file1 = File(100)
file2 = File(200)
folder1 = Folder()
folder1.add(file1)
folder1.add(file2)

root = Folder()
root.add(folder1)
root.add(File(50))

print(root.get_size())  # 350 (treats tree uniformly)
```

**Use Cases:**
- File systems (files and folders)
- UI component trees (React, HTML DOM)
- Organization hierarchies
- Graphics (shapes containing shapes)

**Real Examples:**
- React component tree
- XML/HTML DOM
- GUI frameworks (Swing, JavaFX)

---

#### Bridge Pattern

**Purpose:** Separate abstraction from implementation

**UML:**
```
┌──────────────┐       ┌──────────────────┐
│ Abstraction  │──────►│ Implementation   │
└──────△───────┘       └────────△─────────┘
       │                        │
   ┌───┴───┐            ┌──────┴──────┐
   ▼       ▼            ▼             ▼
Refined  Refined   ConcreteImpl  ConcreteImpl
   A        B            A             B
```

**Code:**
```python
# Implementation interface
class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius):
        pass

class VectorRenderer(Renderer):
    def render_circle(self, radius):
        print(f"Drawing circle (vector) with radius {radius}")

class RasterRenderer(Renderer):
    def render_circle(self, radius):
        print(f"Drawing circle (raster) with radius {radius}")

# Abstraction
class Shape:
    def __init__(self, renderer):
        self.renderer = renderer

class Circle(Shape):
    def __init__(self, renderer, radius):
        super().__init__(renderer)
        self.radius = radius
    
    def draw(self):
        self.renderer.render_circle(self.radius)

# Usage - can mix and match!
circle1 = Circle(VectorRenderer(), 5)
circle1.draw()  # Vector rendering

circle2 = Circle(RasterRenderer(), 5)
circle2.draw()  # Raster rendering
```

**Use Cases:**
- Graphics systems (shape + rendering)
- Database drivers (abstraction + implementation)
- Device drivers (abstraction + OS-specific impl)
- UI themes (component + theme implementation)

**Key Insight:** Prevents "Cartesian product" explosion
```
Without Bridge: 2 shapes × 2 renderers = 4 classes
With Bridge: 2 shapes + 2 renderers = 4 classes (but scales better!)
```

---

#### Flyweight Pattern

**Purpose:** Share common state to reduce memory usage

**UML:**
```
┌─────────┐       ┌─────────────┐
│ Client  │──────►│  Flyweight  │
└─────────┘       │  Factory    │
                  └──────┬──────┘
                         │ manages
                         ▼
                  ┌─────────────┐
                  │  Flyweight  │
                  │ (shared)    │
                  └─────────────┘
```

**Code:**
```python
class TreeType:
    """Flyweight - shared state"""
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture

class TreeFactory:
    _tree_types = {}
    
    @classmethod
    def get_tree_type(cls, name, color, texture):
        key = (name, color, texture)
        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(name, color, texture)
        return cls._tree_types[key]

class Tree:
    """Unique state per tree"""
    def __init__(self, x, y, tree_type):
        self.x = x
        self.y = y
        self.tree_type = tree_type  # Shared!
    
    def draw(self):
        print(f"Draw {self.tree_type.name} at ({self.x}, {self.y})")

# Usage - 1000 trees, but only 3 TreeType objects!
factory = TreeFactory()
oak_type = factory.get_tree_type("Oak", "green", "oak.png")

trees = []
for i in range(1000):
    trees.append(Tree(i, i, oak_type))  # Reuses oak_type
```

**Use Cases:**
- Game development (thousands of similar objects)
- Text editors (character rendering)
- Web browsers (font rendering)
- Caching systems

**Real Examples:**
- Java String pool
- Font rendering in browsers
- Particle systems in games

---

### 🎭 Behavioral Patterns

---

#### Command Pattern

**Purpose:** Encapsulate request as an object

**UML:**
```
┌─────────┐       ┌─────────────┐
│ Invoker │──────►│  Command    │
└─────────┘       └──────△──────┘
                         │ implements
                  ┌──────┴──────┐
                  ▼             ▼
            ConcreteCmd1   ConcreteCmd2
                  │             │
                  └─────┬───────┘
                        ▼
                   Receiver
```

**Code:**
```python
# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

# Receiver
class Light:
    def turn_on(self):
        print("Light ON")
    
    def turn_off(self):
        print("Light OFF")

# Concrete commands
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

# Invoker
class RemoteControl:
    def __init__(self):
        self.command = None
    
    def set_command(self, command):
        self.command = command
    
    def press_button(self):
        self.command.execute()
    
    def press_undo(self):
        self.command.undo()

# Usage
light = Light()
light_on = LightOnCommand(light)

remote = RemoteControl()
remote.set_command(light_on)
remote.press_button()  # Light ON
remote.press_undo()    # Light OFF
```

**Use Cases:**
- Undo/redo functionality
- Transaction management
- Job queues
- GUI buttons/menu items
- Macro recording

**Real Examples:**
- Git commands
- Database transactions
- Text editor undo/redo
- Task schedulers (Celery)

---

#### Template Method Pattern

**Purpose:** Define algorithm skeleton, subclasses implement steps

**UML:**
```
┌─────────────────────┐
│  AbstractClass      │
├─────────────────────┤
│ + templateMethod()  │ ← algorithm skeleton
│ # primitiveOp1()    │ ← abstract steps
│ # primitiveOp2()    │
└──────────△──────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
ConcreteA     ConcreteB
```

**Code:**
```python
class DataProcessor(ABC):
    def process(self):  # Template method
        self.read_data()
        self.process_data()  # Varies
        self.save_data()
    
    def read_data(self):
        print("Reading data...")
    
    @abstractmethod
    def process_data(self):
        pass
    
    def save_data(self):
        print("Saving data...")

class CSVProcessor(DataProcessor):
    def process_data(self):
        print("Processing CSV...")

class JSONProcessor(DataProcessor):
    def process_data(self):
        print("Processing JSON...")

# Usage
csv = CSVProcessor()
csv.process()  # read → process CSV → save
```

**Use Cases:**
- Testing frameworks (setUp, test, tearDown)
- Data processing pipelines
- Game AI (assess, decide, act)
- HTTP request handling

**Real Examples:**
- JUnit/pytest (setUp/tearDown)
- Django class-based views
- Spring Framework templates

---

#### State Pattern

**Purpose:** Object changes behavior when state changes

**UML:**
```
┌─────────────┐       ┌─────────────┐
│   Context   │──────►│    State    │
│             │       └──────△──────┘
│ - state     │              │
└─────────────┘       ┌──────┴──────┐
                      ▼             ▼
                 ConcreteA     ConcreteB
```

**Code:**
```python
class State(ABC):
    @abstractmethod
    def handle(self, context):
        pass

class DraftState(State):
    def handle(self, context):
        print("Draft → Publishing")
        context.state = PublishedState()

class PublishedState(State):
    def handle(self, context):
        print("Published → Archived")
        context.state = ArchivedState()

class ArchivedState(State):
    def handle(self, context):
        print("Cannot change archived post")

class Post:
    def __init__(self):
        self.state = DraftState()
    
    def change_state(self):
        self.state.handle(self)

# Usage
post = Post()
post.change_state()  # Draft → Published
post.change_state()  # Published → Archived
post.change_state()  # Cannot change
```

**Use Cases:**
- Order status (pending → shipped → delivered)
- TCP connection states
- Game character states (idle, running, jumping)
- Document workflow (draft → review → published)

**Real Examples:**
- E-commerce order tracking
- Game state machines
- Network protocols

---

#### Iterator Pattern

**Purpose:** Traverse collection without exposing structure

**UML:**
```
┌──────────────┐       ┌────────────┐
│  Aggregate   │──────►│  Iterator  │
└──────△───────┘       └─────△──────┘
       │                     │
   ┌───┴───┐            ┌────┴────┐
   ▼       ▼            ▼         ▼
Concrete  Concrete  Concrete  Concrete
Aggregate         Iterator
```

**Code:**
```python
class Iterator(ABC):
    @abstractmethod
    def has_next(self):
        pass
    
    @abstractmethod
    def next(self):
        pass

class BookCollection:
    def __init__(self):
        self._books = []
    
    def add_book(self, book):
        self._books.append(book)
    
    def __iter__(self):
        return BookIterator(self._books)

class BookIterator(Iterator):
    def __init__(self, books):
        self._books = books
        self._index = 0
    
    def has_next(self):
        return self._index < len(self._books)
    
    def next(self):
        if self.has_next():
            book = self._books[self._index]
            self._index += 1
            return book

# Usage (Python's built-in protocol)
collection = BookCollection()
collection.add_book("Book 1")
collection.add_book("Book 2")

for book in collection:
    print(book)
```

**Use Cases:**
- Iterate over custom collections
- Database result sets
- Tree/graph traversal
- Streaming data

**Real Examples:**
- Python's `__iter__` protocol
- Java's Iterator interface
- C++ STL iterators
- Database cursors

---

#### Chain of Responsibility Pattern

**Purpose:** Pass request along chain until handled

**UML:**
```
┌─────────┐       ┌─────────────┐
│ Client  │──────►│   Handler   │
└─────────┘       └──────△──────┘
                         │
                  ┌──────┴──────┐
                  ▼             ▼
            ConcreteA     ConcreteB
                │             │
                └─────┬───────┘
                      ▼
                    next handler
```

**Code:**
```python
class Handler(ABC):
    def __init__(self):
        self._next = None
    
    def set_next(self, handler):
        self._next = handler
        return handler
    
    @abstractmethod
    def handle(self, request):
        pass

class AuthHandler(Handler):
    def handle(self, request):
        if not request.get("authenticated"):
            print("Auth failed")
            return False
        if self._next:
            return self._next.handle(request)
        return True

class ValidationHandler(Handler):
    def handle(self, request):
        if not request.get("valid"):
            print("Validation failed")
            return False
        if self._next:
            return self._next.handle(request)
        return True

class ProcessHandler(Handler):
    def handle(self, request):
        print("Processing request")
        return True

# Usage
auth = AuthHandler()
validate = ValidationHandler()
process = ProcessHandler()

auth.set_next(validate).set_next(process)

request = {"authenticated": True, "valid": True}
auth.handle(request)  # Passes through chain
```

**Use Cases:**
- Middleware (Express, Django)
- Event handling (UI events)
- Logging levels (DEBUG → INFO → WARNING → ERROR)
- Support ticket escalation

**Real Examples:**
- Express.js middleware
- Java Servlet filters
- Exception handling

---

#### Mediator Pattern

**Purpose:** Centralize complex communication

**UML:**
```
┌────────────┐       ┌────────────┐
│ Colleague  │◄─────►│  Mediator  │
└────────────┘       └─────┬──────┘
                           │ manages
                     ┌─────┼─────┐
                     ▼     ▼     ▼
                   ColA  ColB  ColC
```

**Code:**
```python
class ChatMediator:
    def __init__(self):
        self._users = []
    
    def add_user(self, user):
        self._users.append(user)
    
    def send_message(self, message, sender):
        for user in self._users:
            if user != sender:
                user.receive(message)

class User:
    def __init__(self, name, mediator):
        self.name = name
        self.mediator = mediator
    
    def send(self, message):
        print(f"{self.name} sends: {message}")
        self.mediator.send_message(message, self)
    
    def receive(self, message):
        print(f"{self.name} receives: {message}")

# Usage
mediator = ChatMediator()
alice = User("Alice", mediator)
bob = User("Bob", mediator)

mediator.add_user(alice)
mediator.add_user(bob)

alice.send("Hello!")  # Bob receives
```

**Use Cases:**
- Chat rooms
- Air traffic control
- GUI dialog boxes
- Event bus systems

---

#### Memento Pattern

**Purpose:** Capture and restore object state

**UML:**
```
┌──────────────┐       ┌────────────┐
│ Originator   │──────►│  Memento   │
└──────────────┘       └────────────┘
       │
       ▼
┌──────────────┐
│ Caretaker    │ stores mementos
└──────────────┘
```

**Code:**
```python
class EditorMemento:
    def __init__(self, state):
        self._state = state
    
    def get_state(self):
        return self._state

class TextEditor:
    def __init__(self):
        self._content = ""
    
    def write(self, text):
        self._content += text
    
    def save(self):
        return EditorMemento(self._content)
    
    def restore(self, memento):
        self._content = memento.get_state()
    
    def __str__(self):
        return self._content

# Usage (undo/redo)
editor = TextEditor()
history = []

editor.write("Hello ")
history.append(editor.save())

editor.write("World")
history.append(editor.save())

print(editor)  # Hello World

editor.restore(history[0])
print(editor)  # Hello
```

**Use Cases:**
- Undo/redo functionality
- Database transactions
- Game save states
- Version control systems

---

#### Visitor Pattern

**Purpose:** Add operations without modifying classes

**UML:**
```
┌────────────┐       ┌────────────┐
│  Element   │◄──────│  Visitor   │
└─────△──────┘       └─────△──────┘
      │                    │
ConcreteElements    ConcreteVisitors
```

**Code:**
```python
class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle):
        pass
    
    @abstractmethod
    def visit_square(self, square):
        pass

class AreaCalculator(ShapeVisitor):
    def visit_circle(self, circle):
        return 3.14 * circle.radius ** 2
    
    def visit_square(self, square):
        return square.side ** 2

class Shape(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def accept(self, visitor):
        return visitor.visit_circle(self)

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def accept(self, visitor):
        return visitor.visit_square(self)

# Usage
shapes = [Circle(5), Square(4)]
calculator = AreaCalculator()

for shape in shapes:
    area = shape.accept(calculator)
    print(f"Area: {area}")
```

**Use Cases:**
- Compiler design (AST traversal)
- XML/JSON parsing
- Reporting on object structures
- Code analysis tools

---

#### Interpreter Pattern

**Purpose:** Implement grammar/language interpreter

**UML:**
```
┌──────────────────┐
│ AbstractExpression│
└────────△─────────┘
         │
    ┌────┴────┐
    ▼         ▼
Terminal  NonTerminal
Expression Expression
```

**Code:**
```python
class Expression(ABC):
    @abstractmethod
    def interpret(self):
        pass

class Number(Expression):
    def __init__(self, value):
        self.value = value
    
    def interpret(self):
        return self.value

class Add(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self):
        return self.left.interpret() + self.right.interpret()

class Subtract(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def interpret(self):
        return self.left.interpret() - self.right.interpret()

# Usage: (5 + 3) - 2
expr = Subtract(
    Add(Number(5), Number(3)),
    Number(2)
)
print(expr.interpret())  # 6
```

**Use Cases:**
- SQL parsers
- Regular expressions
- Configuration file parsers
- DSL (Domain Specific Language) interpreters

---

## Quick Comparison

### Creational

| Pattern | Use When |
|---------|----------|
| Singleton | Need exactly one instance |
| Factory Method | Create objects via inheritance |
| Abstract Factory | Create families of related objects |
| Builder | Complex object construction |
| Prototype | Clone expensive objects |

### Structural

| Pattern | Use When |
|---------|----------|
| Adapter | Incompatible interfaces |
| Decorator | Add responsibilities dynamically |
| Proxy | Control access (lazy, protection, cache) |
| Facade | Simplify complex subsystem |
| Bridge | Separate abstraction from implementation |
| Composite | Tree structure (part-whole) |
| Flyweight | Share to reduce memory |

### Behavioral

| Pattern | Use When |
|---------|----------|
| Strategy | Swap algorithms at runtime |
| Observer | One-to-many notification |
| Command | Encapsulate request (undo/redo) |
| Template Method | Algorithm skeleton |
| State | Behavior changes with state |
| Iterator | Traverse collection |
| Chain of Responsibility | Pass request along chain |
| Mediator | Centralize complex communication |
| Memento | Save/restore state |
| Visitor | Add operations without modifying |
| Interpreter | Implement grammar/language |

---

## Interview Priority

**Must Know (Top 10):**
1. Singleton
2. Factory Method
3. Strategy
4. Observer
5. Decorator
6. Adapter
7. Facade
8. Proxy
9. Builder
10. Command

**Should Know:**
- Template Method
- State
- Composite
- Iterator
- Chain of Responsibility

**Nice to Know:**
- Abstract Factory
- Prototype
- Bridge
- Mediator
- Memento

**Rarely Asked:**
- Flyweight
- Visitor
- Interpreter

---

## Pattern Relationships

**Commonly Combined:**
- Factory Method + Singleton
- Decorator + Strategy
- Observer + Mediator
- Command + Memento (undo/redo)
- Template Method + Factory Method
- Facade + Abstract Factory

**Confused Often:**
- Strategy vs State (swap algorithm vs state transition)
- Adapter vs Decorator vs Proxy (all wrap, different purposes)
- Factory Method vs Abstract Factory (one vs family)
- Composite vs Decorator (tree vs wrap)

---

## Summary

**23 GoF Patterns:**
- 5 Creational
- 7 Structural
- 11 Behavioral

**Focus for Interviews:**
Top 10 patterns cover 90% of interview questions!

**Remember:**
Patterns are tools, not rules. Use them when they make sense, not because they exist.