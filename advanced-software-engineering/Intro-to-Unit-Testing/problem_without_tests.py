"""
problem_without_tests.py
========================
This file demonstrates WHY we need automated testing.

THE SCENARIO:
- You write a Calculator class
- You test it manually with print statements
- Weeks later, you modify the code
- Something breaks silently...

Run this file and see the manual testing pain!
"""


# ============================================================
# STEP 1: Your Original Calculator (works fine)
# ============================================================

class Calculator:
    """A simple calculator with basic operations."""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


# ============================================================
# STEP 2: Manual Testing (The Old Way)
# ============================================================

def manual_testing():
    """
    This is how most beginners verify their code works.
    Problems with this approach:
    1. You have to run this manually every time
    2. You have to READ the output and verify with your eyes
    3. You'll skip this when deadlines hit
    4. You'll forget edge cases
    """
    print("=" * 50)
    print("MANUAL TESTING (The Painful Way)")
    print("=" * 50)

    calc = Calculator()

    # Test add
    print(f"add(2, 3) = {calc.add(2, 3)}")           # Should be 5
    print(f"add(-1, 1) = {calc.add(-1, 1)}")         # Should be 0

    # Test subtract
    print(f"subtract(10, 4) = {calc.subtract(10, 4)}")  # Should be 6

    # Test multiply
    print(f"multiply(3, 4) = {calc.multiply(3, 4)}")    # Should be 12

    # Test divide
    print(f"divide(10, 2) = {calc.divide(10, 2)}")      # Should be 5.0

    print("\n>> Now YOU have to read all output and verify each one!")
    print(">> Did you check? Are you sure? What if there are 100 functions?")
    print()


# ============================================================
# STEP 3: The Real Problem - Code Changes Over Time
# ============================================================

class CalculatorV2:
    """
    Two weeks later, you "optimize" the multiply function.
    You introduce a bug accidentally.
    """

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        # "Optimization" - but there's a bug!
        # Someone thought they'd handle negative numbers specially
        if a < 0 or b < 0:
            return -(abs(a) * abs(b))  # BUG: -2 * -3 should be +6, not -6!
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def demonstrate_silent_bug():
    """
    The bug in CalculatorV2 might go unnoticed with casual testing.
    """
    print("=" * 50)
    print("SILENT BUG DEMONSTRATION")
    print("=" * 50)

    calc = CalculatorV2()

    # These pass - so you think everything works
    print(f"multiply(3, 4) = {calc.multiply(3, 4)}")      # 12 - Correct!
    print(f"multiply(5, 5) = {calc.multiply(5, 5)}")      # 25 - Correct!
    print(f"multiply(-2, 3) = {calc.multiply(-2, 3)}")    # -6 - Correct!

    # This has a bug - but did you think to test it?
    result = calc.multiply(-2, -3)
    print(f"multiply(-2, -3) = {result}")                  # -6 - WRONG! Should be +6

    print("\n>> The bug: negative × negative should be positive!")
    print(">> Without automated tests, this bug ships to production.")
    print(">> Users find the bug. You get a 2 AM call.")
    print()


# ============================================================
# STEP 4: The Scale Problem
# ============================================================

def demonstrate_scale_problem():
    """
    Imagine testing this manually every time you change code.
    """
    print("=" * 50)
    print("THE SCALE PROBLEM")
    print("=" * 50)

    test_cases = [
        ("add", 2, 3, 5),
        ("add", 0, 0, 0),
        ("add", -1, 1, 0),
        ("add", -5, -3, -8),
        ("add", 1000000, 1, 1000001),
        ("subtract", 10, 4, 6),
        ("subtract", 0, 5, -5),
        ("subtract", -3, -3, 0),
        ("multiply", 3, 4, 12),
        ("multiply", 0, 100, 0),
        ("multiply", -2, 3, -6),
        ("multiply", -2, -3, 6),  # This will fail with CalculatorV2!
        ("divide", 10, 2, 5),
        ("divide", 7, 2, 3.5),
        ("divide", 0, 5, 0),
    ]

    print(f"You have {len(test_cases)} test cases.")
    print("Every time you change code, you need to verify ALL of them.")
    print("Manually.")
    print("With your eyes.")
    print("Every. Single. Time.")
    print()
    print("In real projects, you might have 500+ test cases.")
    print("Manual testing doesn't scale!")
    print()
    print(">> SOLUTION: Automated Unit Tests (see first_unit_test.py)")
    print()


# ============================================================
# RUN THE DEMONSTRATIONS
# ============================================================

if __name__ == "__main__":
    manual_testing()
    demonstrate_silent_bug()
    demonstrate_scale_problem()
