"""
first_unit_test.py
==================
Your first unit tests with Python's unittest module.

This file demonstrates:
1. Basic test structure
2. Common assertions
3. Testing success AND failure paths
4. The AAA pattern (Arrange-Act-Assert)

Run this file:
    python first_unit_test.py

Or with verbose output:
    python -m unittest first_unit_test -v

Or with pytest:
    pytest first_unit_test.py -v
"""

import unittest


# ============================================================
# CODE TO TEST (Same Calculator from problem_without_tests.py)
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
# UNIT TESTS
# ============================================================

class TestCalculatorAdd(unittest.TestCase):
    """Tests for the add method."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        # Arrange
        calc = Calculator()
        a, b = 2, 3

        # Act
        result = calc.add(a, b)

        # Assert
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        calc = Calculator()
        result = calc.add(-2, -3)
        self.assertEqual(result, -5)

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        calc = Calculator()
        result = calc.add(-1, 1)
        self.assertEqual(result, 0)

    def test_add_with_zero(self):
        """Test adding with zero."""
        calc = Calculator()
        self.assertEqual(calc.add(5, 0), 5)
        self.assertEqual(calc.add(0, 5), 5)
        self.assertEqual(calc.add(0, 0), 0)


class TestCalculatorSubtract(unittest.TestCase):
    """Tests for the subtract method."""

    def test_subtract_positive_numbers(self):
        calc = Calculator()
        result = calc.subtract(10, 4)
        self.assertEqual(result, 6)

    def test_subtract_results_in_negative(self):
        calc = Calculator()
        result = calc.subtract(5, 10)
        self.assertEqual(result, -5)


class TestCalculatorMultiply(unittest.TestCase):
    """Tests for the multiply method."""

    def test_multiply_positive_numbers(self):
        calc = Calculator()
        result = calc.multiply(3, 4)
        self.assertEqual(result, 12)

    def test_multiply_with_zero(self):
        """Anything times zero is zero."""
        calc = Calculator()
        self.assertEqual(calc.multiply(100, 0), 0)
        self.assertEqual(calc.multiply(0, 100), 0)

    def test_multiply_negative_numbers(self):
        """Negative times negative is positive."""
        calc = Calculator()
        result = calc.multiply(-2, -3)
        self.assertEqual(result, 6)  # This catches the bug from CalculatorV2!

    def test_multiply_mixed_signs(self):
        """Positive times negative is negative."""
        calc = Calculator()
        self.assertEqual(calc.multiply(-2, 3), -6)
        self.assertEqual(calc.multiply(2, -3), -6)


class TestCalculatorDivide(unittest.TestCase):
    """Tests for the divide method."""

    def test_divide_evenly(self):
        calc = Calculator()
        result = calc.divide(10, 2)
        self.assertEqual(result, 5)

    def test_divide_with_remainder(self):
        calc = Calculator()
        result = calc.divide(7, 2)
        self.assertEqual(result, 3.5)

    def test_divide_zero_by_number(self):
        """Zero divided by anything is zero."""
        calc = Calculator()
        result = calc.divide(0, 5)
        self.assertEqual(result, 0)

    def test_divide_by_zero_raises_error(self):
        """
        IMPORTANT: Test error conditions too!
        Use assertRaises to verify exceptions are raised.
        """
        calc = Calculator()

        # Method 1: Using context manager (preferred)
        with self.assertRaises(ValueError):
            calc.divide(10, 0)

    def test_divide_by_zero_error_message(self):
        """Test that the error message is correct."""
        calc = Calculator()

        with self.assertRaises(ValueError) as context:
            calc.divide(10, 0)

        self.assertEqual(str(context.exception), "Cannot divide by zero")


# ============================================================
# DEMONSTRATING DIFFERENT ASSERTIONS
# ============================================================

class TestAssertionExamples(unittest.TestCase):
    """Examples of different assertion methods."""

    def test_assertEqual(self):
        """Check two values are equal."""
        self.assertEqual(1 + 1, 2)
        self.assertEqual("hello", "hello")
        self.assertEqual([1, 2], [1, 2])

    def test_assertNotEqual(self):
        """Check two values are NOT equal."""
        self.assertNotEqual(1, 2)

    def test_assertTrue_assertFalse(self):
        """Check boolean conditions."""
        self.assertTrue(5 > 3)
        self.assertFalse(5 < 3)

    def test_assertIsNone_assertIsNotNone(self):
        """Check for None values."""
        result = None
        self.assertIsNone(result)

        result = "something"
        self.assertIsNotNone(result)

    def test_assertIn_assertNotIn(self):
        """Check membership."""
        my_list = [1, 2, 3]
        self.assertIn(2, my_list)
        self.assertNotIn(5, my_list)

    def test_assertIsInstance(self):
        """Check type."""
        calc = Calculator()
        self.assertIsInstance(calc, Calculator)
        self.assertIsInstance(5, int)
        self.assertIsInstance("hello", str)


# ============================================================
# SETUP AND TEARDOWN (for shared initialization)
# ============================================================

class TestWithSetUp(unittest.TestCase):
    """
    setUp() runs BEFORE each test method.
    tearDown() runs AFTER each test method.
    Useful when many tests need the same object.
    """

    def setUp(self):
        """Create a fresh Calculator before each test."""
        self.calc = Calculator()

    def tearDown(self):
        """Cleanup after each test (if needed)."""
        # In this case, nothing to clean up
        pass

    def test_add(self):
        # No need to create Calculator - setUp did it
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)

    def test_subtract(self):
        result = self.calc.subtract(10, 4)
        self.assertEqual(result, 6)


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    # This runs all test classes when you execute the file directly
    # Run with: python first_unit_test.py
    unittest.main()
