"""
best_practices_demo.py
======================
Demonstrates GOOD vs BAD testing practices.

Each section shows:
1. The BAD way (and why it's problematic)
2. The GOOD way (and why it's better)

Run this file:
    python best_practices_demo.py
    python -m unittest best_practices_demo -v
    pytest best_practices_demo.py -v
"""

import unittest
import time


# ============================================================
# CODE TO TEST
# ============================================================

class Calculator:
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


class UserValidator:
    def is_valid_email(self, email):
        """Simple email validation."""
        return "@" in email and "." in email.split("@")[-1]

    def is_valid_age(self, age):
        """Age must be between 0 and 150."""
        return isinstance(age, int) and 0 <= age <= 150

    def is_valid_username(self, username):
        """Username: 3-20 chars, alphanumeric only."""
        if not username or not isinstance(username, str):
            return False
        return 3 <= len(username) <= 20 and username.isalnum()


# ============================================================
# PRACTICE 1: ONE ASSERTION PER BEHAVIOR
# ============================================================

class BadTestMultipleAssertions(unittest.TestCase):
    """
    BAD: Multiple unrelated assertions in one test.

    Problems:
    - If the second assertion fails, you don't know about the third
    - Test name doesn't describe which scenario
    - Hard to understand what exactly broke
    """

    def test_calculator(self):
        calc = Calculator()
        # Testing multiple unrelated things
        self.assertEqual(calc.add(2, 3), 5)
        self.assertEqual(calc.subtract(10, 4), 6)
        self.assertEqual(calc.multiply(3, 4), 12)
        self.assertEqual(calc.divide(10, 2), 5)
        # If multiply fails, divide is never tested!


class GoodTestOneAssertionPerBehavior(unittest.TestCase):
    """
    GOOD: Each test focuses on ONE behavior.

    Benefits:
    - Clear test names tell you exactly what broke
    - All behaviors are tested even if one fails
    - Easy to locate and fix issues
    """

    def setUp(self):
        self.calc = Calculator()

    def test_add_returns_sum_of_two_numbers(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract_returns_difference(self):
        self.assertEqual(self.calc.subtract(10, 4), 6)

    def test_multiply_returns_product(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)

    def test_divide_returns_quotient(self):
        self.assertEqual(self.calc.divide(10, 2), 5)


# ============================================================
# PRACTICE 2: DESCRIPTIVE TEST NAMES
# ============================================================

class BadTestNames(unittest.TestCase):
    """
    BAD: Vague, unclear test names.

    When this fails, what broke? No idea!
    """

    def test_email(self):
        validator = UserValidator()
        self.assertTrue(validator.is_valid_email("test@example.com"))

    def test_1(self):
        validator = UserValidator()
        self.assertFalse(validator.is_valid_email("invalid"))

    def test_it_works(self):
        validator = UserValidator()
        self.assertTrue(validator.is_valid_age(25))


class GoodTestNames(unittest.TestCase):
    """
    GOOD: Descriptive names following: test_<what>_<scenario>_<expected>

    When this fails, the name tells you exactly what's broken!
    """

    def test_is_valid_email_with_valid_email_returns_true(self):
        validator = UserValidator()
        self.assertTrue(validator.is_valid_email("test@example.com"))

    def test_is_valid_email_without_at_symbol_returns_false(self):
        validator = UserValidator()
        self.assertFalse(validator.is_valid_email("invalid"))

    def test_is_valid_email_without_domain_returns_false(self):
        validator = UserValidator()
        self.assertFalse(validator.is_valid_email("test@"))

    def test_is_valid_age_with_valid_age_returns_true(self):
        validator = UserValidator()
        self.assertTrue(validator.is_valid_age(25))


# ============================================================
# PRACTICE 3: TEST EDGE CASES
# ============================================================

class BadTestNoEdgeCases(unittest.TestCase):
    """
    BAD: Only testing the "happy path".

    Bugs hide at boundaries! This misses them.
    """

    def test_age_validation(self):
        validator = UserValidator()
        self.assertTrue(validator.is_valid_age(25))
        # What about 0? 150? -1? 151? "twenty"?


class GoodTestWithEdgeCases(unittest.TestCase):
    """
    GOOD: Test boundaries and edge cases.

    This catches bugs that hide at extremes.
    """

    def setUp(self):
        self.validator = UserValidator()

    # Happy path
    def test_is_valid_age_normal_age_returns_true(self):
        self.assertTrue(self.validator.is_valid_age(25))

    # Boundary: minimum valid
    def test_is_valid_age_zero_returns_true(self):
        self.assertTrue(self.validator.is_valid_age(0))

    # Boundary: maximum valid
    def test_is_valid_age_150_returns_true(self):
        self.assertTrue(self.validator.is_valid_age(150))

    # Just below boundary
    def test_is_valid_age_negative_returns_false(self):
        self.assertFalse(self.validator.is_valid_age(-1))

    # Just above boundary
    def test_is_valid_age_over_150_returns_false(self):
        self.assertFalse(self.validator.is_valid_age(151))

    # Wrong type
    def test_is_valid_age_string_returns_false(self):
        self.assertFalse(self.validator.is_valid_age("twenty"))

    def test_is_valid_age_float_returns_false(self):
        self.assertFalse(self.validator.is_valid_age(25.5))


# ============================================================
# PRACTICE 4: AAA PATTERN (ARRANGE-ACT-ASSERT)
# ============================================================

class BadTestNoStructure(unittest.TestCase):
    """
    BAD: Code is jumbled, hard to follow.
    """

    def test_something(self):
        v = UserValidator()
        self.assertTrue(v.is_valid_username("john123"))
        self.assertFalse(v.is_valid_username("ab"))
        self.assertFalse(v.is_valid_username(""))
        u = "valid_user"  # Wait, what is this for?
        self.assertTrue(v.is_valid_username("validuser"))


class GoodTestAAAPattern(unittest.TestCase):
    """
    GOOD: Clear Arrange-Act-Assert structure.

    Each section is visually separated and clear.
    """

    def test_is_valid_username_with_valid_username_returns_true(self):
        # Arrange
        validator = UserValidator()
        username = "john123"

        # Act
        result = validator.is_valid_username(username)

        # Assert
        self.assertTrue(result)

    def test_is_valid_username_too_short_returns_false(self):
        # Arrange
        validator = UserValidator()
        username = "ab"  # Only 2 chars, minimum is 3

        # Act
        result = validator.is_valid_username(username)

        # Assert
        self.assertFalse(result)

    def test_is_valid_username_empty_returns_false(self):
        # Arrange
        validator = UserValidator()
        username = ""

        # Act
        result = validator.is_valid_username(username)

        # Assert
        self.assertFalse(result)


# ============================================================
# PRACTICE 5: TESTS MUST BE FAST
# ============================================================

class BadSlowTest(unittest.TestCase):
    """
    BAD: Slow tests with unnecessary delays.

    If you have 100 tests with 1 second sleep each = 100 seconds!
    Developers will skip running tests.

    NOTE: This test is commented out to not slow down the suite.
    """

    # def test_slow_operation(self):
    #     time.sleep(2)  # DON'T DO THIS!
    #     calc = Calculator()
    #     self.assertEqual(calc.add(1, 1), 2)
    pass


class GoodFastTest(unittest.TestCase):
    """
    GOOD: Fast tests with no delays.

    Unit tests should complete in milliseconds.
    """

    def test_fast_operation(self):
        # No sleep, no network, no database
        calc = Calculator()
        self.assertEqual(calc.add(1, 1), 2)
        # This runs in < 1 millisecond


# ============================================================
# PRACTICE 6: TEST ISOLATION (NO SHARED STATE)
# ============================================================

# Global state - DON'T DO THIS
_bad_counter = 0


class BadSharedStateTest(unittest.TestCase):
    """
    BAD: Tests depend on global/shared state.

    These tests might pass or fail depending on run order!
    """

    def test_counter_increment_first(self):
        global _bad_counter
        _bad_counter += 1
        self.assertEqual(_bad_counter, 1)

    def test_counter_increment_second(self):
        # This assumes test_first ran before!
        global _bad_counter
        _bad_counter += 1
        self.assertEqual(_bad_counter, 2)  # Fragile!


class GoodIsolatedTest(unittest.TestCase):
    """
    GOOD: Each test has fresh state via setUp.

    Tests are independent - order doesn't matter.
    """

    def setUp(self):
        # Fresh counter for EACH test
        self.counter = 0

    def test_counter_increment(self):
        self.counter += 1
        self.assertEqual(self.counter, 1)  # Always passes

    def test_counter_increment_again(self):
        # This doesn't depend on other tests
        self.counter += 1
        self.assertEqual(self.counter, 1)  # Always passes


# ============================================================
# PRACTICE 7: TEST BEHAVIOR, NOT IMPLEMENTATION
# ============================================================

class CalculatorWithCache:
    """Calculator that caches results (internal implementation detail)."""

    def __init__(self):
        self._cache = {}  # Internal detail!

    def add(self, a, b):
        key = (a, b)
        if key not in self._cache:
            self._cache[key] = a + b
        return self._cache[key]


class BadTestImplementation(unittest.TestCase):
    """
    BAD: Testing internal implementation details.

    If we change how caching works, test breaks even though
    the behavior (input -> output) is still correct!
    """

    def test_add_uses_cache(self):
        calc = CalculatorWithCache()
        calc.add(2, 3)
        # Testing internal state - BAD!
        self.assertIn((2, 3), calc._cache)


class GoodTestBehavior(unittest.TestCase):
    """
    GOOD: Test input -> output (black box testing).

    We don't care HOW it computes - just that the result is correct.
    Implementation can change freely.
    """

    def test_add_returns_correct_sum(self):
        calc = CalculatorWithCache()
        result = calc.add(2, 3)
        # Only testing the PUBLIC behavior
        self.assertEqual(result, 5)

    def test_add_same_inputs_returns_same_result(self):
        calc = CalculatorWithCache()
        result1 = calc.add(2, 3)
        result2 = calc.add(2, 3)
        # Testing behavior: calling twice gives same answer
        self.assertEqual(result1, result2)


# ============================================================
# SUMMARY: RUN ALL TESTS
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Running Best Practices Demo Tests")
    print("=" * 60)
    print()
    print("Notice how GOOD tests have clear names in the output!")
    print("When tests fail, good names tell you exactly what broke.")
    print()
    print("-" * 60)

    unittest.main(verbosity=2)
