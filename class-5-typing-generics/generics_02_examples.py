"""
Generics - Practical Examples
Common patterns and use cases
"""
from __future__ import annotations

from typing import TypeVar, Generic, Callable

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

print("=" * 60)
print("Example 1: Generic Box/Container")
print("=" * 60)


class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    def set(self, value: T) -> None:
        self.value = value


# Works with any type
int_box = Box[int](42)
print(f"Int box: {int_box.get()}")

str_box = Box[str]("hello")
print(f"Str box: {str_box.get()}")

list_box = Box[list[int]]([1, 2, 3])
print(f"List box: {list_box.get()}")

print()
print("=" * 60)
print("Example 2: Generic Pair/Tuple")
print("=" * 60)


class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def get_key(self) -> K:
        return self.key

    def get_value(self) -> V:
        return self.value

    def swap(self) -> 'Pair[V, K]':
        return Pair(self.value, self.key)


# Different type combinations
pair1 = Pair[str, int]("age", 25)
print(f"Pair: {pair1.get_key()} = {pair1.get_value()}")

pair2 = Pair[int, str](1, "one")
print(f"Pair: {pair2.get_key()} = {pair2.get_value()}")

swapped = pair1.swap()
print(f"Swapped: {swapped.get_key()} = {swapped.get_value()}")

print()
print("=" * 60)
print("Example 3: Generic Result Type")
print("=" * 60)


class Result(Generic[T]):
    def __init__(self, value: T | None = None, error: str | None = None):
        self.value = value
        self.error = error

    def is_ok(self) -> bool:
        return self.error is None

    def unwrap(self) -> T:
        if self.is_ok():
            return self.value  # type: ignore
        raise ValueError(self.error)


# Success case
success = Result[int](value=42)
if success.is_ok():
    print(f"Success: {success.unwrap()}")

# Error case
failure = Result[int](error="Something went wrong")
if not failure.is_ok():
    print(f"Failure: {failure.error}")

print()
print("=" * 60)
print("Example 4: Generic Functions")
print("=" * 60)


def first_element(items: list[T]) -> T | None:
    """Get first element or None"""
    return items[0] if items else None


def last_element(items: list[T]) -> T | None:
    """Get last element or None"""
    return items[-1] if items else None


def reverse(items: list[T]) -> list[T]:
    """Reverse a list"""
    return items[::-1]


numbers = [1, 2, 3, 4, 5]
print(f"First: {first_element(numbers)}")
print(f"Last: {last_element(numbers)}")
print(f"Reversed: {reverse(numbers)}")

words = ["hello", "world"]
print(f"First word: {first_element(words)}")
print(f"Reversed words: {reverse(words)}")

print()
print("=" * 60)
print("Example 5: Generic Map Function")
print("=" * 60)

U = TypeVar('U')


def map_list(items: list[T], func: Callable[[T], U]) -> list[U]:
    """Map function over list"""
    return [func(item) for item in items]


nums = [1, 2, 3, 4]
strings = map_list(nums, str)  # int -> str
print(f"Map to strings: {strings}")

doubled = map_list(nums, lambda x: x * 2)  # int -> int
print(f"Map to doubled: {doubled}")

lengths = map_list(["hi", "hello", "hey"], len)  # str -> int
print(f"Map to lengths: {lengths}")

print()
print("=" * 60)
print("Example 6: Constrained Generics")
print("=" * 60)

# Only numeric types allowed
NumT = TypeVar('NumT', int, float)


def add(a: NumT, b: NumT) -> NumT:
    """Add two numbers"""
    return a + b  # type: ignore


print(f"Add ints: {add(5, 10)}")
print(f"Add floats: {add(5.5, 10.5)}")
# add("hello", "world")  # mypy error!

print()
print("=" * 60)
print("Example 7: Generic Queue")
print("=" * 60)


class Queue(Generic[T]):
    def __init__(self):
        self.items: list[T] = []

    def enqueue(self, item: T) -> None:
        self.items.append(item)

    def dequeue(self) -> T | None:
        return self.items.pop(0) if self.items else None

    def size(self) -> int:
        return len(self.items)

    def is_empty(self) -> bool:
        return len(self.items) == 0


# Task queue
queue = Queue[str]()
queue.enqueue("task1")
queue.enqueue("task2")
queue.enqueue("task3")

print(f"Queue size: {queue.size()}")
while not queue.is_empty():
    task = queue.dequeue()
    print(f"Processing: {task}")

print()
print("=" * 60)
print("PATTERNS SUMMARY:")
print("=" * 60)
print("✓ Box/Container - holds single value")
print("✓ Pair/Tuple - holds two values")
print("✓ Result - success or error")
print("✓ Collections - Stack, Queue, etc.")
print("✓ Functions - map, filter, reduce")
print("✓ Constrained - only certain types")