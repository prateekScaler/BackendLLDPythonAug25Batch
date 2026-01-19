"""
Exception Handling - Practical Examples
Simple, focused demonstrations
"""

print("=" * 60)
print("Example 1: Why We Need Exceptions")
print("=" * 60)


# Without exceptions - program crashes
def divide_bad(a, b):
    return a / b


try:
    result = divide_bad(10, 0)  # Crashes!
except ZeroDivisionError:
    print("Program crashed without handling")


# With exceptions - graceful handling
def divide_good(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Can't divide by zero")
        return None


result = divide_good(10, 0)
print(f"Result: {result}")
print("Program continues!")

print()
print("=" * 60)
print("Example 2: try-except-else-finally Flow")
print("=" * 60)


def process_number(value):
    try:
        print("1. Try block")
        number = int(value)
        result = 100 / number
    except ValueError:
        print("2a. Except: Not a number")
        return None
    except ZeroDivisionError:
        print("2b. Except: Zero division")
        return None
    else:
        print("3. Else: Success!")
        return result
    finally:
        print("4. Finally: Always runs")


print("Valid input:")
process_number("10")

print("\nInvalid input:")
process_number("abc")

print("\nZero input:")
process_number("0")

print()
print("=" * 60)
print("Example 3: Multiple Exceptions")
print("=" * 60)


def safe_divide(a, b):
    try:
        result = int(a) / int(b)
        return result
    except ValueError:
        print("Error: Values must be numbers")
    except ZeroDivisionError:
        print("Error: Can't divide by zero")
    except Exception as e:
        print(f"Unexpected error: {e}")


safe_divide("10", "2")  # Works
safe_divide("10", "abc")  # ValueError
safe_divide("10", "0")  # ZeroDivisionError

print()
print("=" * 60)
print("Example 4: Custom Exceptions")
print("=" * 60)


class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Balance ${balance} < Amount ${amount}")


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


try:
    balance = 100
    balance = withdraw(balance, 50)
    print(f"Success! New balance: ${balance}")

    balance = withdraw(balance, 100)
except InsufficientFundsError as e:
    print(f"Error: {e}")
    print(f"Shortfall: ${e.amount - e.balance}")

print()
print("=" * 60)
print("Example 5: Exception Hierarchy")
print("=" * 60)


class ValidationError(Exception):
    pass


class EmailError(ValidationError):
    pass


class PasswordError(ValidationError):
    pass


def validate_user(email, password):
    if "@" not in email:
        raise EmailError("Invalid email format")
    if len(password) < 8:
        raise PasswordError("Password too short")
    return True


# Catch specific exception
try:
    validate_user("test", "pass")
except EmailError:
    print("Fix your email")
except PasswordError:
    print("Fix your password")

# Catch general exception
try:
    validate_user("test@email.com", "short")
except ValidationError as e:  # Catches both Email and Password errors
    print(f"Validation failed: {e}")

print()
print("=" * 60)
print("Example 6: File Handling with finally")
print("=" * 60)


# Without context manager
def read_file_manual(filename):
    file = None
    try:
        file = open(filename)
        content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    finally:
        if file:
            file.close()
            print("File closed")


read_file_manual("nonexistent.txt")


# With context manager (better!)
def read_file_context(filename):
    try:
        with open(filename) as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None


read_file_context("nonexistent.txt")

print()
print("=" * 60)
print("Example 7: Re-raising Exceptions")
print("=" * 60)


def process_data(data):
    try:
        result = risky_operation(data)
        return result
    except ValueError as e:
        print(f"Logging error: {e}")
        raise  # Re-raise for caller to handle


def risky_operation(data):
    if not data:
        raise ValueError("Data is empty")
    return len(data)


try:
    process_data("")
except ValueError:
    print("Caller handled the exception")

print()
print("=" * 60)
print("Example 8: Gotcha - Bare except")
print("=" * 60)


# BAD - Catches EVERYTHING, even Ctrl+C
def bad_function():
    try:
        risky_operation()
    except:  # DON'T DO THIS!
        print("Caught something, but what?")


# GOOD - Be specific
def good_function():
    try:
        risky_operation()
    except ValueError:
        print("Value error")
    except TypeError:
        print("Type error")


print()
print("=" * 60)
print("Example 9: Gotcha - finally return")
print("=" * 60)


def confusing():
    try:
        return "from try"
    finally:
        return "from finally"  # This wins!


print(f"Result: {confusing()}")  # "from finally"


# GOOD - Don't return in finally
def clear():
    try:
        return "from try"
    finally:
        print("Cleanup only")


print(f"Result: {clear()}")  # "from try"

print()
print("=" * 60)
print("Example 10: Real-World - API Call with Retry")
print("=" * 60)

import time


def call_api(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Simulate API call
            if attempt < 2:
                raise ConnectionError("Network error")
            return {"data": "success"}
        except ConnectionError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)


try:
    result = call_api("http://api.example.com")
    print(f"Success: {result}")
except ConnectionError:
    print("All retries failed")

print()
print("=" * 60)
print("Example 11: Real-World - Validation")
print("=" * 60)


class ValidationError(Exception):
    pass


def validate_age(age):
    try:
        age_int = int(age)
    except ValueError:
        raise ValidationError(f"Age must be a number, got: {age}")

    if age_int < 0:
        raise ValidationError("Age cannot be negative")
    if age_int > 150:
        raise ValidationError("Age too high")

    return age_int


# Test cases
for test_age in ["25", "-5", "200", "abc"]:
    try:
        validated = validate_age(test_age)
        print(f"Valid age: {validated}")
    except ValidationError as e:
        print(f"Invalid: {e}")

print()
print("=" * 60)
print("Example 12: When NOT to Use Exceptions")
print("=" * 60)


# BAD - Using exception for control flow
def get_value_bad(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return None


# GOOD - Use built-in method
def get_value_good(dictionary, key):
    return dictionary.get(key)


data = {"name": "Alice"}
print(get_value_good(data, "name"))  # Alice
print(get_value_good(data, "missing"))  # None

print()
print("=" * 60)
print("KEY LESSONS:")
print("=" * 60)
print("✓ Use exceptions for exceptional cases, not control flow")
print("✓ Be specific - catch exact exception types")
print("✓ Use finally for cleanup (or context managers)")
print("✓ Don't swallow exceptions silently")
print("✓ Custom exceptions add clarity")
print("✓ else separates success code")
print("✓ Avoid bare except")
print("✓ Don't return in finally")