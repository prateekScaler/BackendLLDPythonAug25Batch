"""
Iterators and Generators - Practical Examples
Simple demonstrations of key concepts
"""

print("=" * 60)
print("ITERATORS")
print("=" * 60)

print("\nExample 1: Basic Iterator Usage")
numbers = [1, 2, 3]
iterator = iter(numbers)

print(f"First: {next(iterator)}")  # 1
print(f"Second: {next(iterator)}")  # 2
print(f"Third: {next(iterator)}")  # 3

try:
    print(next(iterator))  # StopIteration
except StopIteration:
    print("Iterator exhausted!")

print("\nExample 2: Custom Iterator")


class Counter:
    def __init__(self, max_count):
        self.max_count = max_count
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.max_count:
            raise StopIteration
        self.current += 1
        return self.current


counter = Counter(5)
for num in counter:
    print(num, end=" ")  # 1 2 3 4 5
print()

print("\nExample 3: Iterator vs Iterable")

# Iterable - can iterate multiple times
numbers = [1, 2, 3]
print("First loop:", list(numbers))
print("Second loop:", list(numbers))  # Works!

# Iterator - one-time use
iterator = iter(numbers)
print("First use:", list(iterator))
print("Second use:", list(iterator))  # Empty!

print()
print("=" * 60)
print("GENERATORS")
print("=" * 60)

print("\nExample 4: Generator Function")


def countdown(n):
    while n > 0:
        yield n
        n -= 1


for num in countdown(5):
    print(num, end=" ")  # 5 4 3 2 1
print()

print("\nExample 5: Generator vs List - Memory")

import sys


# List - all in memory
def squares_list(n):
    return [x ** 2 for x in range(n)]


# Generator - on demand
def squares_gen(n):
    for x in range(n):
        yield x ** 2


lst = squares_list(10)
gen = squares_gen(10)

print(f"List size: {sys.getsizeof(lst)} bytes")
print(f"Generator size: {sys.getsizeof(gen)} bytes")

print("\nExample 6: Generator Expression")

# List comprehension - eager
squares_list = [x ** 2 for x in range(5)]
print(f"List: {squares_list}")

# Generator expression - lazy
squares_gen = (x ** 2 for x in range(5))
print(f"Generator: {squares_gen}")
print(f"Convert to list: {list(squares_gen)}")

print("\nExample 7: Infinite Generator")


def infinite_count():
    num = 0
    while True:
        yield num
        num += 1


counter = infinite_count()
print("First 5 from infinite:")
for _ in range(5):
    print(next(counter), end=" ")
print()

print("\nExample 8: Fibonacci Generator")


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()
print("First 10 Fibonacci:")
for _ in range(10):
    print(next(fib), end=" ")
print()

print("\nExample 9: Data Pipeline with Generators")


def read_data():
    """Simulate reading data"""
    for i in range(10):
        yield i


def filter_even(data):
    """Keep only even numbers"""
    for item in data:
        if item % 2 == 0:
            yield item


def square(data):
    """Square each number"""
    for item in data:
        yield item ** 2


# Chain generators
pipeline = square(filter_even(read_data()))
print("Pipeline result:", list(pipeline))

print("\nExample 10: Batch Processing")


def batch_items(items, batch_size):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


data = range(25)
print("Batches of 10:")
for batch in batch_items(data, 10):
    print(batch)

print("\nExample 11: File Reading (Memory Efficient)")

# Create sample file
with open("/tmp/sample.txt", "w") as f:
    for i in range(100):
        f.write(f"Line {i}\n")


# Generator for reading
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()


# Process only first 5 lines
print("First 5 lines:")
for i, line in enumerate(read_lines("/tmp/sample.txt")):
    print(line)
    if i >= 4:
        break

print()
print("=" * 60)
print("KEY DIFFERENCES")
print("=" * 60)

print("\n1. Memory Usage:")
print("   List: All items in memory")
print("   Generator: One item at a time")

print("\n2. Reusability:")
print("   List: Can iterate multiple times")
print("   Generator: One-time use")

print("\n3. Speed:")
print("   List: Fast if reusing")
print("   Generator: Fast for single pass")

print("\n4. Use Cases:")
print("   List: Small data, need indexing")
print("   Generator: Large data, streaming")