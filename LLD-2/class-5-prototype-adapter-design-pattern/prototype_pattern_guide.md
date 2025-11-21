# Prototype Design Pattern

## 📖 Definition

**"Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype."**

**In simpler terms:** Create new objects by cloning existing ones instead of creating from scratch.

---

## 🎯 The Problem

### Scenario 1: Expensive Object Creation

```python
class GameCharacter:
    def __init__(self, character_class):
        self.character_class = character_class
        self.texture = self._load_texture()      # 0.5 seconds!
        self.animations = self._load_animations()  # 1.0 second!
        self.sounds = self._load_sounds()         # 0.3 seconds!
        self.ai = self._initialize_ai()           # 0.2 seconds!
        # Total: 2 seconds per character!
    
    def _load_texture(self):
        time.sleep(0.5)  # Simulating disk I/O
        return f"Texture for {self.character_class}"
    
    def _load_animations(self):
        time.sleep(1.0)
        return ["walk", "run", "attack"]
    
    def _load_sounds(self):
        time.sleep(0.3)
        return ["footstep", "attack_sound"]
    
    def _initialize_ai(self):
        time.sleep(0.2)
        return "AI_System"

# Need 100 warrior characters for battle scene
warriors = []
for i in range(100):
    warrior = GameCharacter("warrior")  # 2 seconds each!
    warriors.append(warrior)
# Total: 200 seconds! 💥
```

**Problems:**
- ❌ Repeated expensive operations (loading textures, animations, etc.)
- ❌ Slow performance (200 seconds for 100 characters!)
- ❌ Wasteful (loading same assets 100 times)

### Scenario 2: Complex Object Configuration

```python
# Complex database connection configuration
connection = DatabaseConnection()
connection.set_host("prod-db.example.com")
connection.set_port(5432)
connection.set_username("app_user")
connection.set_password("secure_password")
connection.set_pool_size(20)
connection.set_timeout(30)
connection.set_ssl_enabled(True)
connection.set_retry_count(3)
connection.configure_logging("INFO")
connection.set_connection_params({
    "sslmode": "require",
    "application_name": "MyApp",
    "connect_timeout": 10
})
# 10+ lines of configuration!

# Need 50 connections with same configuration
connections = []
for i in range(50):
    conn = DatabaseConnection()
    conn.set_host("prod-db.example.com")  # Repeat all configuration!
    conn.set_port(5432)
    # ... 8 more lines ...
    connections.append(conn)
# Configuration duplicated 50 times! 💥
```

**Problems:**
- ❌ Configuration code duplication
- ❌ Error-prone (easy to miss a setting)
- ❌ Hard to maintain (change configuration in 50 places?)

---

## ✅ The Solution: Prototype Pattern

**Instead of creating from scratch, clone a pre-configured prototype!**

```python
import copy

# Create ONE prototype (2 seconds)
warrior_prototype = GameCharacter("warrior")

# Clone prototype 100 times (near-instant!)
warriors = []
for i in range(100):
    warrior = copy.deepcopy(warrior_prototype)  # <0.001 seconds!
    warriors.append(warrior)
# Total: ~2 seconds! ✅
# 100x faster!
```

---

## 🏗️ Implementation

### Basic Implementation

```python
import copy
from abc import ABC, abstractmethod

# Step 1: Define prototype interface
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        """Return a copy of self"""
        pass

# Step 2: Concrete prototype
class GameCharacter(Prototype):
    def __init__(self, name, health, weapon):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.position = [0, 0]
    
    def clone(self):
        """Shallow clone"""
        return copy.copy(self)
    
    def deep_clone(self):
        """Deep clone"""
        return copy.deepcopy(self)

# Usage
original = GameCharacter("Warrior", 100, "Sword")

# Shallow clone
clone1 = original.clone()
clone1.name = "Warrior Clone 1"

# Deep clone
clone2 = original.deep_clone()
clone2.name = "Warrior Clone 2"
```

### With Prototype Registry (Recommended)

```python
import copy

class PrototypeRegistry:
    """Central registry for prototype objects"""
    
    def __init__(self):
        self._prototypes = {}
    
    def register(self, name: str, prototype):
        """Register a prototype"""
        self._prototypes[name] = prototype
    
    def unregister(self, name: str):
        """Remove a prototype"""
        del self._prototypes[name]
    
    def clone(self, name: str, **kwargs):
        """Clone a registered prototype"""
        prototype = self._prototypes.get(name)
        if not prototype:
            raise ValueError(f"Prototype '{name}' not found")
        
        clone = copy.deepcopy(prototype)
        
        # Apply any customizations
        for key, value in kwargs.items():
            setattr(clone, key, value)
        
        return clone

# Usage
registry = PrototypeRegistry()

# Register prototypes
warrior_proto = GameCharacter("Warrior", 100, "Sword")
mage_proto = GameCharacter("Mage", 50, "Staff")

registry.register("warrior", warrior_proto)
registry.register("mage", mage_proto)

# Clone with customization
warrior1 = registry.clone("warrior", name="Warrior #1")
warrior2 = registry.clone("warrior", name="Warrior #2")
mage1 = registry.clone("mage", name="Mage #1", health=60)
```

---

## 🎮 Real-World Example: Game Enemy System

### The Problem

```python
# Game with different enemy types
class Enemy:
    def __init__(self, enemy_type):
        self.type = enemy_type
        self.texture = self._load_texture(enemy_type)      # Expensive!
        self.animations = self._load_animations(enemy_type)  # Expensive!
        self.stats = self._load_stats(enemy_type)
        self.ai = self._initialize_ai(enemy_type)
    
    def _load_texture(self, enemy_type):
        time.sleep(0.1)  # I/O operation
        return f"Texture_{enemy_type}"
    
    def _load_animations(self, enemy_type):
        time.sleep(0.2)  # I/O operation
        return ["idle", "walk", "attack"]
    
    def _load_stats(self, enemy_type):
        stats_map = {
            "zombie": {"health": 50, "damage": 10, "speed": 2},
            "skeleton": {"health": 30, "damage": 15, "speed": 4},
            "dragon": {"health": 500, "damage": 100, "speed": 10}
        }
        return stats_map.get(enemy_type, {})
    
    def _initialize_ai(self, enemy_type):
        time.sleep(0.1)  # Complex initialization
        return f"AI_{enemy_type}"

# Spawn 100 zombies - takes 40 seconds!
zombies = [Enemy("zombie") for _ in range(100)]
```

### The Solution: Prototype Pattern

```python
import copy

class Enemy:
    def __init__(self, enemy_type):
        self.type = enemy_type
        self.texture = self._load_texture(enemy_type)
        self.animations = self._load_animations(enemy_type)
        self.stats = self._load_stats(enemy_type)
        self.ai = self._initialize_ai(enemy_type)
        self.position = [0, 0]
        self.is_alive = True
    
    # ... same loading methods ...
    
    def clone(self):
        """Clone this enemy"""
        return copy.deepcopy(self)
    
    def spawn_at(self, x, y):
        """Spawn a clone at specific position"""
        clone = self.clone()
        clone.position = [x, y]
        return clone

# Create prototypes ONCE (0.4 seconds each)
class EnemyFactory:
    def __init__(self):
        self._prototypes = {}
        self._initialize_prototypes()
    
    def _initialize_prototypes(self):
        """Create prototype for each enemy type"""
        self._prototypes["zombie"] = Enemy("zombie")
        self._prototypes["skeleton"] = Enemy("skeleton")
        self._prototypes["dragon"] = Enemy("dragon")
        # Total: 1.2 seconds for all prototypes
    
    def create_enemy(self, enemy_type, x=0, y=0):
        """Create enemy by cloning prototype"""
        prototype = self._prototypes.get(enemy_type)
        if not prototype:
            raise ValueError(f"Unknown enemy type: {enemy_type}")
        
        return prototype.spawn_at(x, y)

# Usage
factory = EnemyFactory()  # 1.2 seconds to initialize

# Spawn 100 zombies - takes ~0.1 seconds!
zombies = [factory.create_enemy("zombie", i*10, 0) for i in range(100)]

# Spawn mixed enemies - still fast!
enemies = []
enemies.extend([factory.create_enemy("zombie", i*10, 0) for i in range(50)])
enemies.extend([factory.create_enemy("skeleton", i*10, 100) for i in range(30)])
enemies.extend([factory.create_enemy("dragon", i*50, 200) for i in range(5)])
# Total: ~0.2 seconds instead of 34 seconds!
```

---

## 📊 Shallow vs Deep Copy

### When to Use Each

```python
class Character:
    def __init__(self, name):
        self.name = name
        self.inventory = []  # Mutable list
        self.health = 100

# Shallow copy
char1 = Character("Hero")
char1.inventory.append("sword")

char2 = copy.copy(char1)
char2.name = "Hero Clone"
char2.inventory.append("shield")

print(char1.inventory)  # ['sword', 'shield'] - SHARED!
print(char2.inventory)  # ['sword', 'shield']

# Deep copy
char3 = copy.deepcopy(char1)
char3.inventory.append("potion")

print(char1.inventory)  # ['sword', 'shield']
print(char3.inventory)  # ['sword', 'shield', 'potion'] - INDEPENDENT!
```

**Decision guide:**

```python
# Use shallow copy when:
# - No mutable nested objects
# - Want to share nested objects
# - Performance is critical

class Point:
    def __init__(self, x, y):
        self.x = x  # Immutable
        self.y = y  # Immutable
    
    def clone(self):
        return copy.copy(self)  # Shallow is fine

# Use deep copy when:
# - Has mutable nested objects
# - Need complete independence
# - Object graph is complex

class Character:
    def __init__(self, name, inventory, skills):
        self.name = name
        self.inventory = inventory  # List - mutable!
        self.skills = skills        # List - mutable!
    
    def clone(self):
        return copy.deepcopy(self)  # Deep copy needed
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: Forgetting to Clone Mutable Attributes

```python
# ❌ Wrong
class Player:
    def __init__(self, name):
        self.name = name
        self.items = []
    
    def clone(self):
        # Shallow copy - items list is shared!
        return copy.copy(self)

player1 = Player("Alice")
player1.items.append("sword")

player2 = player1.clone()
player2.items.append("shield")

print(player1.items)  # ['sword', 'shield'] - Oops!

# ✅ Correct
class Player:
    def clone(self):
        return copy.deepcopy(self)  # Deep copy
```

### Pitfall 2: Cloning Singletons

```python
# ❌ Wrong
class GameManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    # DON'T clone singletons!

# ✅ Correct
class GameManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __deepcopy__(self, memo):
        # Return the same instance
        return self
    
    def __copy__(self):
        # Return the same instance
        return self
```

### Pitfall 3: Not Resetting State

```python
# ❌ Wrong
class Enemy:
    def __init__(self):
        self.health = 100
        self.position = [0, 0]
        self.target = None
    
    def clone(self):
        return copy.deepcopy(self)

enemy1 = Enemy()
enemy1.health = 50  # Damaged
enemy1.position = [100, 200]
enemy1.target = some_player

enemy2 = enemy1.clone()
# enemy2 starts damaged and with wrong position/target!

# ✅ Correct
class Enemy:
    def clone(self):
        clone = copy.deepcopy(self)
        # Reset runtime state
        clone.health = self.max_health  # Reset to full health
        clone.position = [0, 0]
        clone.target = None
        return clone
```

---

## 💡 Best Practices

### 1. Use Prototype Registry

```python
# Centralized prototype management
class GamePrototypes:
    def __init__(self):
        self.registry = PrototypeRegistry()
        self._initialize()
    
    def _initialize(self):
        # Register all prototypes at startup
        self.registry.register("warrior", Warrior())
        self.registry.register("mage", Mage())
        self.registry.register("archer", Archer())
    
    def create(self, name, **kwargs):
        return self.registry.clone(name, **kwargs)

# Single initialization, multiple clones
prototypes = GamePrototypes()
warrior1 = prototypes.create("warrior", name="Fighter #1")
warrior2 = prototypes.create("warrior", name="Fighter #2")
```

### 2. Implement Clone Methods

```python
class Prototype:
    def clone(self):
        """Shallow clone"""
        return copy.copy(self)
    
    def deep_clone(self):
        """Deep clone"""
        return copy.deepcopy(self)
    
    def __copy__(self):
        """Called by copy.copy()"""
        return self.clone()
    
    def __deepcopy__(self, memo):
        """Called by copy.deepcopy()"""
        return self.deep_clone()
```

### 3. Document Cloning Behavior

```python
class Character:
    """
    Game character class.
    
    Cloning behavior:
    - Shallow clone: Shares inventory and skills lists
    - Deep clone: Creates independent copies of all attributes
    
    Use deep_clone() for independent characters.
    """
    
    def clone(self):
        """Returns shallow copy (shared inventory)"""
        return copy.copy(self)
    
    def deep_clone(self):
        """Returns deep copy (independent inventory)"""
        return copy.deepcopy(self)
```

---

## 🎯 When to Use Prototype Pattern

### ✅ Use Prototype When:

1. **Object creation is expensive**
   - Loading resources from disk
   - Complex initialization
   - Network calls

2. **Need many similar objects**
   - Game enemies (100 zombies)
   - UI components (many buttons)
   - Database connections

3. **Object has complex configuration**
   - Many parameters to set
   - Avoid repeating configuration code

4. **Runtime type determination**
   - Don't know exact type until runtime
   - Clone based on user selection

### ❌ Don't Use When:

1. **Objects are simple to create**
   - Few parameters
   - No expensive initialization

2. **Each object is unique**
   - No benefit from cloning
   - Different configuration each time

3. **Deep object graphs with circular references**
   - Complex to clone correctly
   - Performance overhead

---

## 🔑 Key Takeaways

- **What:** Create objects by cloning existing prototypes
- **Why:** Avoid expensive initialization, simplify complex object creation
- **When:** Creating many similar objects with expensive setup
- **How:** Use `copy.copy()` (shallow) or `copy.deepcopy()` (deep)

**Remember:**
- Prototype = Template for cloning
- Use Registry to manage prototypes
- Deep copy for mutable nested objects
- Reset runtime state after cloning
- Document cloning behavior

The Prototype Pattern is about **efficiency through reuse**! 🚀
