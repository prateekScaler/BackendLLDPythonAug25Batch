"""
Python Collections - Practical Examples & Pitfalls
Shows common mistakes and correct usage
"""

print("=" * 60)
print("Example 1: List - Mutable Default Argument")
print("=" * 60)


# ❌ BAD
def add_student_bad(name, students=[]):
    students.append(name)
    return students


class1 = add_student_bad("Alice")
print(f"Class 1: {class1}")

class2 = add_student_bad("Bob")
print(f"Class 2: {class2}")  # Also has Alice!


# ✅ GOOD
def add_student_good(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students


class3 = add_student_good("Charlie")
class4 = add_student_good("David")
print(f"Class 3: {class3}")
print(f"Class 4: {class4}")

print()
print("=" * 60)
print("Example 2: List Multiplication Trap")
print("=" * 60)

# ❌ BAD
matrix_bad = [[0] * 3] * 3
matrix_bad[0][0] = 1
print("Bad matrix:")
for row in matrix_bad:
    print(row)  # All rows changed!

# ✅ GOOD
matrix_good = [[0] * 3 for _ in range(3)]
matrix_good[0][0] = 1
print("\nGood matrix:")
for row in matrix_good:
    print(row)  # Only first row changed

print()
print("=" * 60)
print("Example 3: Tuple - Single Element")
print("=" * 60)

# ❌ WRONG
not_tuple = (42)
print(f"Type: {type(not_tuple)}")  # int!

# ✅ RIGHT
is_tuple = (42,)
print(f"Type: {type(is_tuple)}")  # tuple!

# Also works
also_tuple = 42,
print(f"Type: {type(also_tuple)}")  # tuple!

print()
print("=" * 60)
print("Example 4: Set - Empty Set Creation")
print("=" * 60)

# ❌ WRONG
empty_dict = {}
print(f"Type: {type(empty_dict)}")  # dict!

# ✅ RIGHT
empty_set = set()
print(f"Type: {type(empty_set)}")  # set!

# Set with elements
number_set = {1, 2, 3}
print(f"Set: {number_set}")

print()
print("=" * 60)
print("Example 5: Set - Unhashable Elements")
print("=" * 60)

try:
    # ❌ Lists are not hashable
    bad_set = {[1, 2], [3, 4]}
except TypeError as e:
    print(f"Error: {e}")

# ✅ Tuples are hashable
good_set = {(1, 2), (3, 4)}
print(f"Set with tuples: {good_set}")

# ✅ frozenset for set of sets
set_of_sets = {frozenset([1, 2]), frozenset([3, 4])}
print(f"Set of sets: {set_of_sets}")

print()
print("=" * 60)
print("Example 6: Dict - Unhashable Keys")
print("=" * 60)

try:
    # ❌ Lists can't be keys
    bad_dict = {[1, 2]: "value"}
except TypeError as e:
    print(f"Error: {e}")

# ✅ Tuples can be keys
good_dict = {(1, 2): "value"}
print(f"Dict: {good_dict}")

# ✅ Practical use case
coordinates = {
    (0, 0): "origin",
    (1, 0): "right",
    (0, 1): "up"
}
print(f"Location at (0,0): {coordinates[(0, 0)]}")

print()
print("=" * 60)
print("Example 7: defaultdict vs regular dict")
print("=" * 60)

from collections import defaultdict

# Regular dict
regular = {}
try:
    print(regular["missing"])
except KeyError:
    print("KeyError with regular dict")

# defaultdict
default = defaultdict(int)
print(f"Missing key: {default['missing']}")  # Returns 0
print(f"Dict now: {default}")  # Key added!

# Practical: Grouping
words = ["apple", "banana", "apricot", "berry", "avocado"]
groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)

print("Grouped by first letter:")
for letter, word_list in sorted(groups.items()):
    print(f"  {letter}: {word_list}")

print()
print("=" * 60)
print("Example 8: Counter - Counting Items")
print("=" * 60)

from collections import Counter

votes = ["Alice", "Bob", "Alice", "Charlie", "Alice", "Bob"]
vote_counts = Counter(votes)

print(f"Votes: {vote_counts}")
print(f"Most common: {vote_counts.most_common(1)}")
print(f"Alice's votes: {vote_counts['Alice']}")

# Counter arithmetic
c1 = Counter(["a", "b", "c", "a"])
c2 = Counter(["a", "b", "d"])
print(f"\nc1: {c1}")
print(f"c2: {c2}")
print(f"c1 + c2: {c1 + c2}")
print(f"c1 - c2: {c1 - c2}")

print()
print("=" * 60)
print("Example 9: deque - Fast Both Ends")
print("=" * 60)

from collections import deque

# List is slow at left operations
dq = deque([1, 2, 3])

dq.appendleft(0)  # O(1)
dq.append(4)  # O(1)
print(f"After appends: {dq}")

dq.popleft()  # O(1)
dq.pop()  # O(1)
print(f"After pops: {dq}")

# Maxlen - sliding window
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
    print(f"After adding {i}: {recent}")

print()
print("=" * 60)
print("Example 10: Shallow vs Deep Copy")
print("=" * 60)

import copy

# Original list with nested list
original = [[1, 2], [3, 4]]

# Shallow copy
shallow = original.copy()
shallow[0].append(99)
print(f"Original after shallow: {original}")  # Changed!

# Deep copy
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0].append(99)
print(f"Original after deep: {original}")  # Unchanged!

print()
print("=" * 60)
print("Example 11: Custom UserDict")
print("=" * 60)

from collections import UserDict


class CaseInsensitiveDict(UserDict):
    """Dict with case-insensitive keys"""

    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())


ci_dict = CaseInsensitiveDict()
ci_dict["Name"] = "Alice"
ci_dict["AGE"] = 25

print(ci_dict["name"])  # Works!
print(ci_dict["Name"])  # Also works!
print(ci_dict["NAME"])  # Still works!

print()
print("=" * 60)
print("Example 12: Custom List Subclass")
print("=" * 60)


class UniqueList(list):
    """List that only stores unique items"""

    def append(self, item):
        if item not in self:
            super().append(item)


ul = UniqueList([1, 2, 3])
ul.append(2)  # Ignored
ul.append(4)  # Added
ul.append(2)  # Ignored again
print(f"Unique list: {ul}")

print()
print("=" * 60)
print("KEY LESSONS:")
print("=" * 60)
print("✓ Never use mutable default arguments")
print("✓ List multiplication creates references")
print("✓ Single element tuple needs comma")
print("✓ {} creates dict, not set")
print("✓ Set/dict elements must be hashable")
print("✓ defaultdict auto-creates missing keys")
print("✓ Counter for counting/frequency")
print("✓ deque for fast operations at both ends")
print("✓ Shallow copy shares nested objects")
print("✓ Deep copy for complete independence")