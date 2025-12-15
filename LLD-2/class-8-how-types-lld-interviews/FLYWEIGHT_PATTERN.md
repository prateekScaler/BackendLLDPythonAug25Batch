# Flyweight Pattern 

## Intent
**Share common state among many objects to minimize memory usage when dealing with large numbers of similar objects.**

---

## Problem Statement
Creating thousands of similar objects consumes excessive memory. Most objects share common data (intrinsic state) with only small variations (extrinsic state).

**Example:** Text editor with 100,000 characters - storing font/size for each character individually wastes memory.

---

## Generic UML

```
┌──────────────────────┐
│   FlyweightFactory   │ ← Manages flyweight pool
├──────────────────────┤
│- flyweights: dict    │   (cache/pool)
├──────────────────────┤
│+ get_flyweight(key)  │ ← Returns cached or creates new
└──────────────────────┘
           │
           │ creates/manages
           ▼
┌──────────────────────┐
│     Flyweight        │ ← Shared object
├──────────────────────┤
│- intrinsic_state     │ ← Shared, immutable
├──────────────────────┤
│+ operation(extrinsic)│ ← Receives unique state as param
└──────────────────────┘

┌──────────────────────┐
│       Client         │
├──────────────────────┤
│- extrinsic_state     │ ← Unique per object
├──────────────────────┤
│+ uses flyweights     │
└──────────────────────┘
```

**Key Concepts:**
- **Intrinsic State**: Shared, stored in flyweight (font, color palette, texture)
- **Extrinsic State**: Unique, passed by client (position, character, size)
- **Factory**: Ensures flyweights are shared (caching)

---

## Example 1: Text Editor

**Problem:** 100,000 characters, each storing font data = wasteful

```python
# Without Flyweight - Memory waste
class Character:
    def __init__(self, char, font, size, color):
        self.char = char          # Unique (extrinsic)
        self.font = font          # Shared (wasteful duplication!)
        self.size = size          # Shared (wasteful duplication!)
        self.color = color        # Shared (wasteful duplication!)

# 100,000 characters = 100,000 font objects!
```

```python
# With Flyweight - Memory efficient
class CharacterStyle:  # Flyweight
    def __init__(self, font, size, color):
        self.font = font      # Intrinsic (shared)
        self.size = size      # Intrinsic (shared)
        self.color = color    # Intrinsic (shared)
    
    def render(self, char, position):  # Extrinsic passed in
        print(f"Render '{char}' at {position} with {self.font}")

class StyleFactory:
    _styles = {}
    
    @classmethod
    def get_style(cls, font, size, color):
        key = (font, size, color)
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font, size, color)
        return cls._styles[key]  # Returns cached

# Usage
style1 = StyleFactory.get_style("Arial", 12, "black")
style2 = StyleFactory.get_style("Arial", 12, "black")
# style1 is style2 = True (same object!)

style1.render('H', (0, 0))
style1.render('e', (10, 0))
# Only 1 style object for all 'Arial 12 black' characters
```

**UML:**
```
┌──────────────────┐
│  StyleFactory    │
├──────────────────┤
│- _styles: dict   │
├──────────────────┤
│+ get_style()     │
└──────────────────┘
         │
         ▼
┌──────────────────┐
│ CharacterStyle   │ ← Flyweight (shared)
├──────────────────┤
│- font: str       │ ← Intrinsic
│- size: int       │
│- color: str      │
├──────────────────┤
│+ render(char, pos)│ ← Extrinsic passed
└──────────────────┘

Memory: 10 unique styles instead of 100,000 duplicates!
```

---

## Example 2: Game Trees/Forest

**Problem:** 10,000 trees in forest - storing texture/mesh for each wastes memory

```python
class TreeType:  # Flyweight
    def __init__(self, name, texture, mesh):
        self.name = name          # Intrinsic
        self.texture = texture    # Intrinsic (large data)
        self.mesh = mesh          # Intrinsic (large data)
    
    def render(self, x, y, scale):  # Extrinsic
        print(f"Render {self.name} at ({x}, {y}) scale {scale}")

class TreeFactory:
    _tree_types = {}
    
    @classmethod
    def get_tree_type(cls, name, texture, mesh):
        if name not in cls._tree_types:
            cls._tree_types[name] = TreeType(name, texture, mesh)
        return cls._tree_types[name]

class Tree:
    def __init__(self, x, y, tree_type):
        self.x = x              # Extrinsic (unique position)
        self.y = y              # Extrinsic
        self.tree_type = tree_type  # Reference to flyweight
    
    def render(self):
        self.tree_type.render(self.x, self.y, 1.0)

# Usage
oak_type = TreeFactory.get_tree_type("Oak", "oak.png", "oak.obj")
pine_type = TreeFactory.get_tree_type("Pine", "pine.png", "pine.obj")

# 10,000 trees but only 2 TreeType objects!
forest = [
    Tree(100, 200, oak_type),
    Tree(150, 220, oak_type),
    Tree(200, 250, pine_type),
    # ... 9,997 more trees
]

# Memory: 2 large textures/meshes instead of 10,000!
```

**UML:**
```
┌──────────────────┐
│  TreeFactory     │
└──────────────────┘
         │
         ▼
┌──────────────────┐
│    TreeType      │ ← Flyweight (2 instances)
├──────────────────┤
│- texture: Image  │ ← Heavy intrinsic
│- mesh: 3DModel   │ ← Heavy intrinsic
└──────────────────┘
         ▲
         │ references
┌──────────────────┐
│      Tree        │ ← 10,000 instances
├──────────────────┤
│- x, y: int       │ ← Light extrinsic
│- tree_type       │
└──────────────────┘
```

---

## Example 3: Icon Cache (UI System)

```python
class Icon:  # Flyweight
    def __init__(self, image_path):
        self.image = self._load_image(image_path)  # Intrinsic (heavy)
    
    def draw(self, x, y, size):  # Extrinsic
        # Draw image at position with size
        pass

class IconFactory:
    _icons = {}
    
    @classmethod
    def get_icon(cls, image_path):
        if image_path not in cls._icons:
            cls._icons[image_path] = Icon(image_path)
        return cls._icons[image_path]

# 1000 file icons in file explorer
# But only 1 Icon("file.png") object shared by all!
icons = [IconFactory.get_icon("file.png") for _ in range(1000)]
```

---

## Where Flyweight is Used

### Real-World Applications:

1. **Text Editors**
   - Font rendering (Word, VS Code)
   - Character formatting

2. **Game Development**
   - Particle systems (1000s of particles, few types)
   - Terrain rendering (repeated textures)
   - Trees/vegetation in open world

3. **GUI Systems**
   - Icon caching (file explorers)
   - Widget themes (button styles)

4. **Web Browsers**
   - CSS style caching
   - Font rendering

5. **Database Systems**
   - String interning
   - Connection pooling

### Libraries/Frameworks:
- **Java**: String pool (automatic flyweight)
- **Python**: Integer caching (-5 to 256)
- **Game Engines**: Unity, Unreal (texture/mesh sharing)
- **Browsers**: Chrome, Firefox (style computation)

---

## Flyweight vs Prototype Pattern

| Aspect | Flyweight | Prototype |
|--------|-----------|-----------|
| **Purpose** | Minimize memory by sharing | Fast object creation by cloning |
| **Focus** | Memory optimization | Creation speed optimization |
| **Sharing** | Objects are shared (same instance) | Objects are cloned (separate instances) |
| **State** | Intrinsic (shared) + Extrinsic (passed) | Entire state copied |
| **Mutability** | Flyweight is immutable | Clone can be modified independently |
| **Use Case** | Many similar objects | Expensive initialization |

### Code Comparison:

```python
# FLYWEIGHT - Shared instances
factory = StyleFactory()
style1 = factory.get_style("Arial", 12, "black")
style2 = factory.get_style("Arial", 12, "black")
# style1 is style2 → True (SAME object)
# Modify style1 affects all users!

# PROTOTYPE - Cloned instances
prototype = User("Surya", "Surya@example.com")
user1 = prototype.clone()
user2 = prototype.clone()
# user1 is user2 → False (DIFFERENT objects)
# Modify user1 doesn't affect user2
```

### Visual Difference:

```
FLYWEIGHT - Sharing
┌─────────┐    ┌─────────┐    ┌─────────┐
│Client 1 │───→│         │←───│Client 2 │
└─────────┘    │Flyweight│    └─────────┘
               │(shared) │
┌─────────┐    │         │    ┌─────────┐
│Client 3 │───→│         │←───│Client 4 │
└─────────┘    └─────────┘    └─────────┘
           All point to SAME object

PROTOTYPE - Cloning
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Proto   │───→│ Clone 1 │    │ Clone 2 │
└─────────┘    └─────────┘    └─────────┘
                     ↑             ↑
                 Different     Different
                  objects       objects
```

### When to Use Which:

**Use Flyweight when:**
- ✅ Many objects with shared state
- ✅ Memory is constrained
- ✅ Objects are mostly immutable
- ✅ Identity doesn't matter (can share instances)

**Use Prototype when:**
- ✅ Object creation is expensive (DB calls, API)
- ✅ Need independent copies
- ✅ Objects will be modified
- ✅ Cloning faster than creation

---

## Key Takeaways

### Flyweight Pattern:
1. **Split state**: Intrinsic (shared) + Extrinsic (unique)
2. **Factory manages pool**: Ensures sharing
3. **Immutability**: Flyweights should not change
4. **Trade-off**: Less memory ↔ More computation (passing extrinsic state)

### Memory Impact:
```
Without Flyweight:
10,000 objects × 1 MB each = 10 GB memory

With Flyweight:
10 flyweights × 1 MB + 10,000 × 100 bytes = 10 MB + 1 MB = 11 MB
Savings: 99% reduction!
```

### Implementation Checklist:
- [ ] Identify intrinsic (shareable) state
- [ ] Identify extrinsic (unique) state
- [ ] Create flyweight class (immutable)
- [ ] Create factory with caching
- [ ] Pass extrinsic state as method parameters

---

## Quick Reference

**Pattern Type:** Structural  
**Problem:** Too many similar objects consuming memory  
**Solution:** Share common parts, externalize unique parts  
**When to use:** Large number of objects with shared state  
**Related patterns:** Prototype (creates copies), Singleton (one instance)