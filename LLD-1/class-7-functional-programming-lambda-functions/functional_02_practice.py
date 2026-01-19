"""
Functional Programming - Practice Exercises
Start with easy, progress to challenging
"""

print("=" * 60)
print("PRACTICE EXERCISES - Try before looking at solutions!")
print("=" * 60)

# ============================================================
# EASY LEVEL - Individual Functions
# ============================================================

print("\n### EASY LEVEL ###\n")

# Exercise 1: map() - Double
print("Exercise 1: Double all numbers")
numbers = [1, 2, 3, 4, 5]
print(f"Input: {numbers}")
print(f"Expected: [2, 4, 6, 8, 10]")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 2: filter() - Positives
print("Exercise 2: Keep only positive numbers")
numbers = [-3, -1, 0, 2, 5, -7, 8]
print(f"Input: {numbers}")
print(f"Expected: [2, 5, 8]")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 3: reduce() - Sum
print("Exercise 3: Calculate sum")
from functools import reduce
numbers = [10, 20, 30, 40]
print(f"Input: {numbers}")
print(f"Expected: 100")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 4: map() - String lengths
print("Exercise 4: Get length of each word")
words = ["hi", "hello", "hey", "python"]
print(f"Input: {words}")
print(f"Expected: [2, 5, 3, 6]")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 5: filter() - Long words
print("Exercise 5: Filter words longer than 3 characters")
words = ["hi", "hello", "cat", "python", "a"]
print(f"Input: {words}")
print(f"Expected: ['hello', 'python']")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# ============================================================
# MEDIUM LEVEL - Combinations
# ============================================================

print("\n### MEDIUM LEVEL ###\n")

# Exercise 6: Square evens
print("Exercise 6: Square all even numbers")
numbers = [1, 2, 3, 4, 5, 6]
print(f"Input: {numbers}")
print(f"Expected: [4, 16, 36]")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 7: Sum of squares
print("Exercise 7: Sum of squares of all numbers")
numbers = [1, 2, 3, 4]
print(f"Input: {numbers}")
print(f"Expected: 30  (1 + 4 + 9 + 16)")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 8: Count starting with 'a'
print("Exercise 8: Count words starting with 'a'")
words = ["apple", "banana", "apricot", "cherry", "avocado"]
print(f"Input: {words}")
print(f"Expected: 3")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 9: Product of positives
print("Exercise 9: Product of positive numbers only")
numbers = [-2, 3, -5, 4, 2, -1]
print(f"Input: {numbers}")
print(f"Expected: 24  (3 * 4 * 2)")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 10: Uppercase first letters
print("Exercise 10: Get first letter of each word in uppercase")
words = ["apple", "banana", "cherry"]
print(f"Input: {words}")
print(f"Expected: ['A', 'B', 'C']")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# ============================================================
# HARD LEVEL - Complex Scenarios
# ============================================================

print("\n### HARD LEVEL ###\n")

# Exercise 11: Average of squares of evens
print("Exercise 11: Average of squares of even numbers")
numbers = [1, 2, 3, 4, 5, 6]
print(f"Input: {numbers}")
print(f"Expected: 18.67  ((4 + 16 + 36) / 3)")
# YOUR CODE HERE:

#print(f"Output: {average:.2f}\n")

# Exercise 12: Flatten and filter
print("Exercise 12: Flatten nested list and keep numbers > 3")
nested = [[1, 2, 3], [4, 5], [6, 7, 8]]
print(f"Input: {nested}")
print(f"Expected: [4, 5, 6, 7, 8]")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 13: Max length word
print("Exercise 13: Find longest word")
words = ["hi", "hello", "hey", "python", "world"]
print(f"Input: {words}")
print(f"Expected: 'python'")
# YOUR CODE HERE:

# print(f"Output: {result}\n")

# Exercise 14: Sum of products
print("Exercise 14: Sum of products of pairs")
pairs = [(1, 2), (3, 4), (5, 6)]
print(f"Input: {pairs}")
print(f"Expected: 44  (1*2 + 3*4 + 5*6 = 2 + 12 + 30)")
# YOUR CODE HERE:

# print(f"Output: {result}\n")

# Exercise 15: Complex pipeline
print("Exercise 15: Get sum of doubled odds")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"Input: {numbers}")
print(f"Expected: 50  (odds: 1,3,5,7,9 → doubled: 2,6,10,14,18 → sum: 50)")
# YOUR CODE HERE:

# print(f"Output: {result}\n")

# ============================================================
# REAL-WORLD SCENARIOS
# ============================================================

print("\n### REAL-WORLD SCENARIOS ###\n")

# Exercise 16: Shopping cart total with discount
print("Exercise 16: Calculate total after 10% discount")
prices = [19.99, 29.99, 9.99, 49.99]
print(f"Input: {prices}")
print(f"Expected: 98.96  (sum after 10% off)")
# YOUR CODE HERE:

# print(f"Output: ${result:.2f}\n")

# Exercise 17: Grade average for passing students
print("Exercise 17: Average grade of students who passed (>= 60)")
grades = [85, 45, 92, 55, 78, 90, 30]
print(f"Input: {grades}")
print(f"Expected: 86.25")
# YOUR CODE HERE:

# print(f"Output: {average:.2f}\n")

# Exercise 18: Extract and transform user data
print("Exercise 18: Get uppercase names of adult users")
users = [
    {"name": "alice", "age": 25},
    {"name": "bob", "age": 17},
    {"name": "charlie", "age": 30}
]
print(f"Input: {users}")
print(f"Expected: ['ALICE', 'CHARLIE']")
# YOUR CODE HERE:

# print(f"Output: {result}\n")

# Exercise 19: Word frequency (hard!)
print("Exercise 19: Most frequent word")
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
print(f"Input: {words}")
print(f"Expected: 'apple' (appears 3 times)")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

# Exercise 20: Nested data processing
print("Exercise 20: Sum all prices from all categories")
data = {
    "electronics": [100, 200, 50],
    "clothing": [30, 45, 20],
    "food": [5, 10, 15]
}
print(f"Input: {data}")
print(f"Expected: 475")
# YOUR CODE HERE:

#print(f"Output: {result}\n")

print("=" * 60)
print("SUMMARY OF TECHNIQUES:")
print("=" * 60)
print("1. map(func, list) - Transform each element")
print("2. filter(pred, list) - Keep matching elements")
print("3. reduce(func, list) - Combine to single value")
print("4. Combine them: filter → map → reduce")
print("5. Always convert map/filter to list when printing")
print("6. reduce needs: from functools import reduce")
print("=" * 60)