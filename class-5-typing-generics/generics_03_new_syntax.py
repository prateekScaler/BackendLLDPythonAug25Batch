"""
Generics - New Syntax (Python 3.12+)
Cleaner, more concise syntax
"""

print("=" * 60)
print("Old Syntax vs New Syntax")
print("=" * 60)

# ============================================================
# OLD SYNTAX (Python < 3.12)
# ============================================================
from typing import TypeVar, Generic

T = TypeVar('T')


class OldBox(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value


old_box = OldBox[int](42)
print(f"Old syntax: {old_box.get()}")


# ============================================================
# NEW SYNTAX (Python 3.12+)
# ============================================================

class NewBox[T]:  # No Generic[T] needed!
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value


new_box = NewBox[int](42)
print(f"New syntax: {new_box.get()}")

print()
print("=" * 60)
print("Example 1: Generic Stack (New Syntax)")
print("=" * 60)


class Stack[T]:
    def __init__(self):
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def peek(self) -> T | None:
        return self.items[-1] if self.items else None


stack = Stack[int]()
stack.push(1)
stack.push(2)
stack.push(3)
print(f"Peek: {stack.peek()}")
print(f"Pop: {stack.pop()}")

print()
print("=" * 60)
print("Example 2: Multiple Type Parameters")
print("=" * 60)


class Pair[K, V]:
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def display(self) -> str:
        return f"{self.key}: {self.value}"


pair = Pair[str, int]("age", 25)
print(f"Pair: {pair.display()}")

print()
print("=" * 60)
print("Example 3: Generic Functions (New Syntax)")
print("=" * 60)


def first[T](items: list[T]) -> T | None:
    return items[0] if items else None


def reverse[T](items: list[T]) -> list[T]:
    return items[::-1]


print(f"First: {first([1, 2, 3])}")
print(f"Reverse: {reverse(['a', 'b', 'c'])}")

print()
print("=" * 60)
print("Example 4: Bounded Generics (New Syntax)")
print("=" * 60)


class Animal:
    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


def make_speak[T: Animal](animal: T) -> T:
    """T must be Animal or subclass"""
    print(animal.speak())
    return animal


dog = make_speak(Dog())
cat = make_speak(Cat())
# make_speak("hello")  # mypy error: str is not Animal

print()
print("=" * 60)
print("Example 5: Real-World Generic Repository")
print("=" * 60)


class Repository[T]:
    def __init__(self):
        self.items: dict[int, T] = {}
        self.next_id = 1

    def add(self, item: T) -> int:
        """Add item and return ID"""
        id = self.next_id
        self.items[id] = item
        self.next_id += 1
        return id

    def get(self, id: int) -> T | None:
        """Get item by ID"""
        return self.items.get(id)

    def get_all(self) -> list[T]:
        """Get all items"""
        return list(self.items.values())

    def delete(self, id: int) -> bool:
        """Delete item by ID"""
        if id in self.items:
            del self.items[id]
            return True
        return False


# User repository
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"


user_repo = Repository[User]()
id1 = user_repo.add(User("Alice", "alice@example.com"))
id2 = user_repo.add(User("Bob", "bob@example.com"))

print(f"All users: {user_repo.get_all()}")
print(f"Get user {id1}: {user_repo.get(id1)}")


# Product repository (same code, different type!)
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price})"


product_repo = Repository[Product]()
product_repo.add(Product("Laptop", 999.99))
product_repo.add(Product("Mouse", 29.99))

print(f"All products: {product_repo.get_all()}")

print()
print("=" * 60)
print("COMPARISON:")
print("=" * 60)
print("Old Syntax:")
print("  from typing import TypeVar, Generic")
print("  T = TypeVar('T')")
print("  class Box(Generic[T]): ...")
print()
print("New Syntax (Python 3.12+):")
print("  class Box[T]: ...")
print()
print("✓ Cleaner and more concise")
print("✓ No import needed")
print("✓ More intuitive")
print("✓ Same functionality")