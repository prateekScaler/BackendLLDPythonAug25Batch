"""
Functional Programming in Python - Practical Examples
Demonstrates FP concepts with real-world scenarios
"""

print("=" * 60)
print("Example 1: OOP vs Functional - Bank Account")
print("=" * 60)


# OOP Style - Mutable state
class BankAccountOOP:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        self.balance -= amount
        return self.balance


account_oop = BankAccountOOP(100)
print(f"Initial: ${account_oop.balance}")
account_oop.deposit(50)
print(f"After deposit: ${account_oop.balance}")
account_oop.withdraw(30)
print(f"After withdraw: ${account_oop.balance}")

print("\nFunctional Style - Immutable")


# Functional Style - Immutable
def deposit(balance, amount):
    return balance + amount


def withdraw(balance, amount):
    return balance - amount


balance = 100
print(f"Initial: ${balance}")
balance = deposit(balance, 50)
print(f"After deposit: ${balance}")
balance = withdraw(balance, 30)
print(f"After withdraw: ${balance}")

print()
print("=" * 60)
print("Example 2: First-Class Functions")
print("=" * 60)


# Functions as values
def add(x, y):
    return x + y


def multiply(x, y):
    return x * y


# Store in dictionary
operations = {
    '+': add,
    '*': multiply,
    '/': lambda x, y: x / y
}

print(f"5 + 3 = {operations['+'](5, 3)}")
print(f"5 * 3 = {operations['*'](5, 3)}")
print(f"6 / 2 = {operations['/'](6, 2)}")

print()
print("=" * 60)
print("Example 3: Higher-Order Functions")
print("=" * 60)


# Function that takes function as parameter
def apply_operation(func, x, y):
    return func(x, y)


result = apply_operation(lambda a, b: a + b, 10, 20)
print(f"Sum: {result}")

result = apply_operation(lambda a, b: a * b, 10, 20)
print(f"Product: {result}")


# Function that returns function
def make_multiplier(n):
    return lambda x: x * n


times_three = make_multiplier(3)
times_five = make_multiplier(5)

print(f"10 * 3 = {times_three(10)}")
print(f"10 * 5 = {times_five(10)}")

print()
print("=" * 60)
print("Example 4: Pure vs Impure Functions")
print("=" * 60)

# Impure - depends on external state
counter = 0


def impure_increment():
    global counter
    counter += 1
    return counter


print(f"Call 1: {impure_increment()}")  # 1
print(f"Call 2: {impure_increment()}")  # 2 (different!)


# Pure - same input, same output
def pure_increment(value):
    return value + 1


print(f"Call 1: {pure_increment(5)}")  # 6
print(f"Call 2: {pure_increment(5)}")  # 6 (same!)

print()
print("=" * 60)
print("Example 5: Lambda Functions")
print("=" * 60)


# Regular function
def square_regular(x):
    return x ** 2


# Lambda function
square_lambda = lambda x: x ** 2

numbers = [1, 2, 3, 4, 5]
map_val = map(square_regular, numbers)
print(f"Using regular: {list(map(square_regular, numbers))}")
print(f"Using lambda:  {list(map(square_lambda, numbers))}")
print(f"Inline lambda: {list(map(lambda x: x ** 2, numbers))}")

# Multiple arguments
add = lambda x, y: x + y
print(f"\n5 + 3 = {add(5, 3)}")

# No arguments
get_pi = lambda: 3.14159
print(f"Pi = {get_pi()}")

print()
print("=" * 60)
print("Example 6: map() - Transform Elements")
print("=" * 60)

numbers = [1, 2, 3, 4, 5]

# Square all numbers
squared = list(map(lambda x: x ** 2, numbers))
print(f"Squared: {squared}")

# Convert to strings
strings = list(map(str, numbers))
print(f"As strings: {strings}")

# Multiple iterables
list1 = [1, 2, 3]
list2 = [10, 20, 30]
sums = list(map(lambda x, y: x + y, list1, list2))
print(f"Sums: {sums}")


# Real-world: Extract names
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


people = [Person("Alice", 25), Person("Bob", 30), Person("Charlie", 35)]
names = list(map(lambda p: p.name, people))
print(f"Names: {names}")

print()
print("=" * 60)
print("Example 7: filter() - Select Elements")
print("=" * 60)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")

# Keep numbers > 5
greater_five = list(filter(lambda x: x > 5, numbers))
print(f"Greater than 5: {greater_five}")

# Filter by range
in_range = list(filter(lambda x: 3 <= x <= 7, numbers))
print(f"Between 3-7: {in_range}")

# Real-world: Filter adults
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30}
]
adults = list(filter(lambda p: p["age"] >= 18, people))
print(f"Adults: {[p['name'] for p in adults]}")

print()
print("=" * 60)
print("Example 8: reduce() - Combine to One")
print("=" * 60)

from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum
total = reduce(lambda x, y: x + y, numbers)
print(f"Sum: {total}")

# Product
product = reduce(lambda x, y: x * y, numbers)
print(f"Product: {product}")

# Maximum
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(f"Maximum: {maximum}")

# Flatten nested lists
nested = [[1, 2], [3, 4], [5, 6]]
flat = reduce(lambda x, y: x + y, nested)
print(f"Flattened: {flat}")

# Count occurrences
words = ["apple", "banana", "apple", "cherry", "apple"]
apple_count = reduce(
    lambda count, word: count + (1 if word == "apple" else 0),
    words,
    0  # Initial value
)
print(f"'apple' count: {apple_count}")

print()
print("=" * 60)
print("Example 9: Combining map, filter, reduce")
print("=" * 60)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Get sum of squares of even numbers
result = reduce(
    lambda x, y: x + y,
    map(lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers)
        )
)
print(f"Sum of squares of evens: {result}")
# Even: [2,4,6,8,10] → Squared: [4,16,36,64,100] → Sum: 220

# Step by step (more readable)
evens = filter(lambda x: x % 2 == 0, numbers)
squared = map(lambda x: x ** 2, evens)
total = reduce(lambda x, y: x + y, squared)
print(f"Step by step result: {total}")

print()
print("=" * 60)
print("Example 10: List Comprehension vs Functional")
print("=" * 60)

numbers = [1, 2, 3, 4, 5, 6]

# Get doubled even numbers

# List comprehension (Pythonic)
result_lc = [x * 2 for x in numbers if x % 2 == 0]
print(f"List comp: {result_lc}")

# Functional style
result_fp = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, numbers)))
print(f"Functional: {result_fp}")

# Both give: [4, 8, 12]

print()
print("=" * 60)
print("Example 11: Real-World Use Cases")
print("=" * 60)

# Use case 1: Data transformation pipeline
users = [
    {"name": "Alice", "age": 25, "active": True},
    {"name": "Bob", "age": 17, "active": True},
    {"name": "Charlie", "age": 30, "active": False},
    {"name": "David", "age": 22, "active": True}
]

# Get names of active adult users
active_adults = list(map(
    lambda u: u["name"],
    filter(lambda u: u["age"] >= 18 and u["active"], users)
))
print(f"Active adults: {active_adults}")

# Use case 2: Price calculations
prices = [10.00, 25.50, 5.75, 100.00]

# Apply 20% discount and add 10% tax
final_prices = list(map(
    lambda p: p * 0.8 * 1.1,  # 20% off, then 10% tax
    prices
))
print(f"Final prices: {[f'${p:.2f}' for p in final_prices]}")

# Use case 3: Word processing
text = "the quick brown fox jumps over the lazy dog"
words = text.split()

# Count words longer than 3 characters
long_words_count = len(list(filter(lambda w: len(w) > 3, words)))
print(f"Words longer than 3 chars: {long_words_count}")

print()
print("=" * 60)
print("KEY LESSONS:")
print("=" * 60)
print("✓ Functions are first-class citizens")
print("✓ Pure functions = predictable, testable")
print("✓ Lambdas for short, simple operations")
print("✓ map() transforms each element")
print("✓ filter() selects matching elements")
print("✓ reduce() combines to single value")
print("✓ List comprehensions often more Pythonic")
print("✓ Functional style enables composition")