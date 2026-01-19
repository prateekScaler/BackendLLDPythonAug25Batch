"""
Copy Constructors - Practical Examples
Shows reference vs shallow vs deep copy
"""
import copy

print("=" * 60)
print("Example 1: Reference vs Copy")
print("=" * 60)


class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades

    def __repr__(self):
        return f"Student({self.name}, {self.grades})"


# Original
student1 = Student("Alice", [90, 85, 95])
print(f"Original: {student1}")

# Reference (NOT a copy!)
student2 = student1
student2.grades.append(100)
print(f"\nAfter modifying 'copy':")
print(f"student1: {student1}")  # Changed!
print(f"student2: {student2}")  # Same object
print(f"Same object? {id(student1) == id(student2)}")  # True

print()
print("=" * 60)
print("Example 2: Shallow Copy Problem")
print("=" * 60)


class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members  # List (mutable!)

    def __repr__(self):
        return f"Team({self.name}, {self.members})"


team1 = Team("Alpha", ["Alice", "Bob"])
team2 = copy.copy(team1)  # Shallow copy

print(f"team1: {team1}")
print(f"team2: {team2}")
print(f"Same object? {id(team1) == id(team2)}")  # False
print(f"Same members list? {id(team1.members) == id(team2.members)}")  # True!

team2.members.append("Charlie")
print(f"\nAfter team2.members.append('Charlie'):")
print(f"team1: {team1}")  # Also has Charlie!
print(f"team2: {team2}")

print()
print("=" * 60)
print("Example 3: Deep Copy Solution")
print("=" * 60)

team3 = Team("Beta", ["David", "Eve"])
team4 = copy.deepcopy(team3)  # Deep copy

print(f"team3: {team3}")
print(f"team4: {team4}")
print(f"Same members list? {id(team3.members) == id(team4.members)}")  # False!

team4.members.append("Frank")
print(f"\nAfter team4.members.append('Frank'):")
print(f"team3: {team3}")  # Unchanged ✓
print(f"team4: {team4}")  # Only team4 changed ✓

print()
print("=" * 60)
print("Example 4: Custom Copy Constructor")
print("=" * 60)


class Person:
    def __init__(self, name=None, age=None, friends=None, other=None):
        if other:  # Copy constructor
            self.name = other.name
            self.age = other.age
            self.friends = other.friends.copy()  # Shallow copy list
        else:
            self.name = name
            self.age = age
            self.friends = friends or []

    def __repr__(self):
        return f"Person({self.name}, {self.age}, {self.friends})"


person1 = Person("Alice", 25, ["Bob", "Charlie"])
person2 = Person(other=person1)  # Use copy constructor

print(f"person1: {person1}")
print(f"person2: {person2}")

person2.friends.append("David")
print(f"\nAfter person2.friends.append('David'):")
print(f"person1: {person1}")  # Unchanged ✓
print(f"person2: {person2}")

print()
print("=" * 60)
print("Example 5: Implementing __copy__ and __deepcopy__")
print("=" * 60)


class Box:
    def __init__(self, label, items):
        self.label = label
        self.items = items

    def __copy__(self):
        """Shallow copy"""
        print(f"  __copy__ called for {self.label}")
        return Box(self.label, self.items)

    def __deepcopy__(self, memo):
        """Deep copy"""
        print(f"  __deepcopy__ called for {self.label}")
        return Box(
            copy.deepcopy(self.label, memo),
            copy.deepcopy(self.items, memo)
        )

    def __repr__(self):
        return f"Box({self.label}, {self.items})"


box1 = Box("A", [1, 2, 3])

print("Shallow copy:")
box2 = copy.copy(box1)

print("\nDeep copy:")
box3 = copy.deepcopy(box1)

print()
print("=" * 60)
print("Example 6: Nested Objects Problem")
print("=" * 60)


class Address:
    def __init__(self, city, zip_code):
        self.city = city
        self.zip_code = zip_code

    def __repr__(self):
        return f"Address({self.city}, {self.zip_code})"


class Employee:
    def __init__(self, name, address):
        self.name = name
        self.address = address  # Nested object!

    def __repr__(self):
        return f"Employee({self.name}, {self.address})"


emp1 = Employee("Alice", Address("NYC", "10001"))

# Shallow copy - shares Address object
emp2 = copy.copy(emp1)
emp2.address.city = "LA"

print(f"emp1: {emp1}")  # Changed!
print(f"emp2: {emp2}")

# Deep copy - separate Address object
emp3 = Employee("Bob", Address("NYC", "10001"))
emp4 = copy.deepcopy(emp3)
emp4.address.city = "SF"

print(f"\nemp3: {emp3}")  # Unchanged ✓
print(f"emp4: {emp4}")

print()
print("=" * 60)
print("Example 7: Tricky Interview Question")
print("=" * 60)


class Container:
    def __init__(self, data):
        self.data = data


# Question: What's the final value?
c1 = Container([1, 2, 3])
c2 = c1
c3 = copy.copy(c1)
c4 = copy.deepcopy(c1)

c2.data.append(4)  # Affects c1 (reference)
c3.data.append(5)  # Affects c1 (shallow, shares list)
c4.data.append(6)  # Only affects c4 (deep, independent)

print(f"c1.data: {c1.data}")  # ?
print(f"c2.data: {c2.data}")  # ?
print(f"c3.data: {c3.data}")  # ?
print(f"c4.data: {c4.data}")  # ?

print("\n" + "=" * 60)
print("KEY LESSONS:")
print("=" * 60)
print("✓ Assignment = Reference (same object)")
print("✓ Shallow copy = New object, shared nested objects")
print("✓ Deep copy = Completely independent")
print("✓ Use copy.deepcopy() for safety with nested mutables")
print("✓ Implement __copy__ and __deepcopy__ for custom behavior")