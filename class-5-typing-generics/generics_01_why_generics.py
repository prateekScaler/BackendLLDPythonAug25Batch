"""
Generics - Why We Need Them
Shows code duplication problem and generic solution
"""

print("=" * 60)
print("Problem: Code Duplication Without Generics")
print("=" * 60)


# ❌ BAD - Separate class for each type
class IntStack:
    def __init__(self):
        self.items: list[int] = []

    def push(self, item: int) -> None:
        self.items.append(item)

    def pop(self) -> int:
        return self.items.pop()


class StrStack:
    def __init__(self):
        self.items: list[str] = []

    def push(self, item: str) -> None:
        self.items.append(item)

    def pop(self) -> str:
        return self.items.pop()


# Need separate class for EVERY type!
int_stack = IntStack()
int_stack.push(1)
int_stack.push(2)
print(f"IntStack pop: {int_stack.pop()}")

str_stack = StrStack()
str_stack.push("hello")
str_stack.push("world")
print(f"StrStack pop: {str_stack.pop()}")

print("\nProblem: Duplicate code! What if we need FloatStack, BoolStack, etc?")

print()
print("=" * 60)
print("Solution: Generics!")
print("=" * 60)

# ✅ GOOD - One generic class for all types
from typing import TypeVar, Generic

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self):
        self.items: list[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()


# Same class works for ANY type!
int_stack_generic = Stack[int]()
int_stack_generic.push(10)
int_stack_generic.push(20)
print(f"Generic IntStack pop: {int_stack_generic.pop()}")

str_stack_generic = Stack[str]()
str_stack_generic.push("foo")
str_stack_generic.push("bar")
print(f"Generic StrStack pop: {str_stack_generic.pop()}")


# Can even use with custom types!
class User:
    def __init__(self, name: str):
        self.name = name


user_stack = Stack[User]()
user_stack.push(User("Alice"))
user_stack.push(User("Bob"))
user = user_stack.pop()
print(f"User stack pop: {user.name}")

print()
print("=" * 60)
print("Type Safety with Generics")
print("=" * 60)

# mypy catches type errors!
safe_stack = Stack[int]()
safe_stack.push(42)
# safe_stack.push("wrong")  # mypy error: Expected int, got str

num: int = safe_stack.pop()  # mypy knows this is int
print(f"Type-safe pop: {num}")

print()
print("=" * 60)
print("Generic Functions")
print("=" * 60)


# Without generics - need multiple functions
def get_first_int(items: list[int]) -> int:
    return items[0]


def get_first_str(items: list[str]) -> str:
    return items[0]


# With generics - one function!
def get_first(items: list[T]) -> T:
    return items[0]


print(f"First int: {get_first([1, 2, 3])}")
print(f"First str: {get_first(['a', 'b', 'c'])}")
print(f"First float: {get_first([1.5, 2.5, 3.5])}")

print()
print("=" * 60)
print("KEY BENEFITS:")
print("=" * 60)
print("✓ No code duplication")
print("✓ Type safety maintained")
print("✓ Works with ANY type")
print("✓ mypy catches errors")
print("✓ Better IDE autocomplete")