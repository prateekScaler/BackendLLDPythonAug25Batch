"""
Prototype Design Pattern - Demo
Practical examples showing when and how to use the Prototype pattern.
"""

import copy
import time
from typing import Dict, List

# ============================================================================
# Example 1: Game Enemy System (Performance Optimization)
# ============================================================================

print("=" * 60)
print("Example 1: Game Enemy System - Performance Optimization")
print("=" * 60)

class Enemy:
    """Game enemy with expensive initialization"""
    
    def __init__(self, enemy_type: str):
        self.type = enemy_type
        self.texture = self._load_texture(enemy_type)
        self.animations = self._load_animations(enemy_type)
        self.stats = self._load_stats(enemy_type)
        self.position = [0, 0]
        self.health = self.stats["health"]
    
    def _load_texture(self, enemy_type: str) -> str:
        """Simulate expensive texture loading"""
        time.sleep(0.05)  # Simulating I/O
        return f"Texture_{enemy_type}.png"
    
    def _load_animations(self, enemy_type: str) -> List[str]:
        """Simulate expensive animation loading"""
        time.sleep(0.03)  # Simulating I/O
        return ["idle", "walk", "attack", "die"]
    
    def _load_stats(self, enemy_type: str) -> Dict:
        """Load enemy statistics"""
        stats_map = {
            "zombie": {"health": 50, "damage": 10, "speed": 2},
            "skeleton": {"health": 30, "damage": 15, "speed": 4},
            "dragon": {"health": 500, "damage": 100, "speed": 10}
        }
        return stats_map.get(enemy_type, {})
    
    def clone(self):
        """Create a deep copy of this enemy"""
        return copy.deepcopy(self)
    
    def spawn_at(self, x: int, y: int):
        """Clone and position at specific location"""
        clone = self.clone()
        clone.position = [x, y]
        clone.health = clone.stats["health"]  # Reset health
        return clone
    
    def __repr__(self):
        return f"Enemy({self.type}, pos={self.position}, hp={self.health})"


# WITHOUT Prototype Pattern - slow!
print("\n❌ WITHOUT Prototype (creating from scratch each time):")
start = time.time()
zombies_slow = []
for i in range(20):
    zombie = Enemy("zombie")  # Expensive creation each time!
    zombie.position = [i * 10, 0]
    zombies_slow.append(zombie)
time_without = time.time() - start
print(f"Created 20 zombies in {time_without:.2f} seconds")
print(f"Sample: {zombies_slow[0]}")

# WITH Prototype Pattern - fast!
print("\n✅ WITH Prototype (cloning from template):")
start = time.time()
zombie_prototype = Enemy("zombie")  # Create once
zombies_fast = []
for i in range(20):
    zombie = zombie_prototype.spawn_at(i * 10, 0)  # Clone!
    zombies_fast.append(zombie)
time_with = time.time() - start
print(f"Created 20 zombies in {time_with:.2f} seconds")
print(f"Sample: {zombies_fast[0]}")
print(f"⚡ Speedup: {time_without/time_with:.1f}x faster!")

# ============================================================================
# Example 2: Prototype Registry Pattern
# ============================================================================

print("\n" + "=" * 60)
print("Example 2: Prototype Registry - Managing Multiple Prototypes")
print("=" * 60)

class PrototypeRegistry:
    """Central registry for managing prototypes"""
    
    def __init__(self):
        self._prototypes: Dict[str, Enemy] = {}
    
    def register(self, name: str, prototype: Enemy):
        """Register a prototype"""
        self._prototypes[name] = prototype
        print(f"✓ Registered prototype: {name}")
    
    def unregister(self, name: str):
        """Remove a prototype"""
        if name in self._prototypes:
            del self._prototypes[name]
            print(f"✓ Unregistered prototype: {name}")
    
    def get(self, name: str, **kwargs) -> Enemy:
        """Get a clone of registered prototype"""
        if name not in self._prototypes:
            raise ValueError(f"Prototype '{name}' not found!")
        
        clone = self._prototypes[name].clone()
        
        # Apply customizations
        for key, value in kwargs.items():
            setattr(clone, key, value)
        
        return clone
    
    def list_prototypes(self):
        """List all registered prototypes"""
        print("\nRegistered prototypes:")
        for name, proto in self._prototypes.items():
            print(f"  - {name}: {proto.type} (hp={proto.stats['health']})")


# Setup registry
print("\nSetting up prototype registry...")
registry = PrototypeRegistry()

# Register enemy prototypes
registry.register("zombie", Enemy("zombie"))
registry.register("skeleton", Enemy("skeleton"))
registry.register("dragon", Enemy("dragon"))

registry.list_prototypes()

# Create enemies from registry
print("\nCreating enemies from registry:")
enemies = [
    registry.get("zombie", position=[10, 0]),
    registry.get("zombie", position=[20, 0]),
    registry.get("skeleton", position=[30, 0]),
    registry.get("skeleton", position=[40, 0]),
    registry.get("dragon", position=[50, 100]),
]

for enemy in enemies:
    print(f"  {enemy}")

# ============================================================================
# Example 3: Document Templates (Complex Configuration)
# ============================================================================

print("\n" + "=" * 60)
print("Example 3: Document Templates - Complex Configuration")
print("=" * 60)

class Document:
    """Document with complex configuration"""
    
    def __init__(self, title: str = ""):
        self.title = title
        self.font_family = "Arial"
        self.font_size = 12
        self.margins = {"top": 1, "bottom": 1, "left": 1, "right": 1}
        self.header = ""
        self.footer = ""
        self.page_numbers = True
        self.line_spacing = 1.5
        self.content = []
    
    def clone(self):
        """Clone this document with all settings"""
        return copy.deepcopy(self)
    
    def __repr__(self):
        return (f"Document('{self.title}', font={self.font_family}/{self.font_size}, "
                f"pages={len(self.content)})")


# Create template documents
print("\nCreating template documents...")

# Template 1: Report template
report_template = Document("Report Template")
report_template.font_family = "Times New Roman"
report_template.font_size = 11
report_template.margins = {"top": 1.5, "bottom": 1.5, "left": 1.25, "right": 1.25}
report_template.header = "Company Name | Report"
report_template.footer = "Page {page} | Confidential"
report_template.line_spacing = 2.0
print(f"✓ Created: {report_template}")

# Template 2: Letter template
letter_template = Document("Letter Template")
letter_template.font_family = "Calibri"
letter_template.font_size = 11
letter_template.header = "Company Letterhead"
letter_template.footer = "Company Address | Contact"
letter_template.page_numbers = False
print(f"✓ Created: {letter_template}")

# Use templates to create documents
print("\nCreating documents from templates:")

q1_report = report_template.clone()
q1_report.title = "Q1 Sales Report"
q1_report.content = ["Q1 sales data...", "Analysis..."]
print(f"  {q1_report}")

q2_report = report_template.clone()
q2_report.title = "Q2 Sales Report"
q2_report.content = ["Q2 sales data..."]
print(f"  {q2_report}")

welcome_letter = letter_template.clone()
welcome_letter.title = "Welcome Letter"
welcome_letter.content = ["Dear Customer...", "Welcome..."]
print(f"  {welcome_letter}")

# ============================================================================
# Example 4: Shallow vs Deep Copy Demonstration
# ============================================================================

print("\n" + "=" * 60)
print("Example 4: Shallow vs Deep Copy - Understanding the Difference")
print("=" * 60)

class Player:
    """Player with inventory (mutable list)"""
    
    def __init__(self, name: str):
        self.name = name
        self.inventory = []
        self.level = 1
    
    def add_item(self, item: str):
        self.inventory.append(item)
    
    def shallow_clone(self):
        """Shallow copy - shares inventory!"""
        return copy.copy(self)
    
    def deep_clone(self):
        """Deep copy - independent inventory"""
        return copy.deepcopy(self)
    
    def __repr__(self):
        return f"Player('{self.name}', level={self.level}, items={self.inventory})"


print("\nDemonstrating shallow copy problem:")
player1 = Player("Hero")
player1.add_item("sword")
print(f"Original: {player1}")

player2 = player1.shallow_clone()
player2.name = "Hero Clone"
player2.level = 2
player2.add_item("shield")

print(f"After shallow clone and modifications:")
print(f"  Original: {player1}")
print(f"  Clone:    {player2}")
print(f"⚠️  Both share inventory list! Original affected by clone's changes!")

print("\nDemonstrating deep copy solution:")
player3 = Player("Warrior")
player3.add_item("axe")
print(f"Original: {player3}")

player4 = player3.deep_clone()
player4.name = "Warrior Clone"
player4.level = 3
player4.add_item("helmet")

print(f"After deep clone and modifications:")
print(f"  Original: {player3}")
print(f"  Clone:    {player4}")
print(f"✅ Independent inventories! Original not affected!")

# ============================================================================
# Example 5: Best Practices - Resetting State After Clone
# ============================================================================

print("\n" + "=" * 60)
print("Example 5: Best Practice - Resetting Runtime State")
print("=" * 60)

class BossEnemy(Enemy):
    """Boss enemy that needs state reset after cloning"""
    
    def __init__(self, boss_type: str):
        super().__init__(boss_type)
        self.is_enraged = False
        self.target_player = None
        self.phase = 1
    
    def clone_fresh(self):
        """Clone with runtime state reset"""
        clone = copy.deepcopy(self)
        
        # Reset runtime state
        clone.health = clone.stats["health"]  # Full health
        clone.position = [0, 0]               # Reset position
        clone.is_enraged = False              # Reset enrage
        clone.target_player = None            # Clear target
        clone.phase = 1                       # Reset phase
        
        return clone
    
    def __repr__(self):
        return (f"BossEnemy({self.type}, hp={self.health}/{self.stats['health']}, "
                f"phase={self.phase}, enraged={self.is_enraged})")


print("\nCloning boss enemy:")
boss_prototype = BossEnemy("dragon")
boss_prototype.health = 250  # Damaged
boss_prototype.is_enraged = True
boss_prototype.phase = 2
boss_prototype.position = [100, 100]
print(f"Prototype (mid-battle): {boss_prototype}")

# Clone with state reset
boss1 = boss_prototype.clone_fresh()
boss1.position = [50, 50]
boss2 = boss_prototype.clone_fresh()
boss2.position = [150, 50]

print(f"\n✅ Fresh clones (state reset):")
print(f"  Boss 1: {boss1}")
print(f"  Boss 2: {boss2}")
print(f"  Both start fresh, ready for battle!")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 60)
print("Summary: When to Use Prototype Pattern")
print("=" * 60)
print("""
✅ Use Prototype Pattern When:
  1. Object creation is expensive (I/O, network, complex initialization)
  2. Need many similar objects (game enemies, UI components)
  3. Object has complex configuration (documents, connections)
  4. Want to avoid subclass explosion

⚡ Benefits:
  - Huge performance improvement for expensive objects
  - Simplified object creation (clone vs configure)
  - Reduced coupling (don't need to know concrete classes)
  - Runtime flexibility (choose prototype dynamically)

⚠️ Remember:
  - Use deep copy for mutable nested objects
  - Reset runtime state after cloning
  - Consider using a registry for managing prototypes
  - Test cloning behavior thoroughly
""")
