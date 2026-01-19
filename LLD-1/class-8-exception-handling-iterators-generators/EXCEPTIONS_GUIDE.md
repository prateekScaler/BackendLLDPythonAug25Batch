# Exception Handling in Python

## 🎯 What are Exceptions?

**Exceptions are events that disrupt normal program flow**

```python
# Without exception handling - program crashes
result = 10 / 0  # ZeroDivisionError: division by zero
print("This never runs")

# With exception handling - program continues
try:
    result = 10 / 0
except ZeroDivisionError:
    result = None
    print("Can't divide by zero")
print("Program continues")  # This runs!
```

**Key:** Exceptions allow graceful error handling instead of crashes

All exceptions in Python inherit from the base class Exception, which in turn inherits from BaseException.
````
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 └── Exception
      ├── ArithmeticError
      │    ├── ZeroDivisionError
      │    └── OverflowError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── ValueError
      ├── TypeError
      ├── NameError
      ├── AttributeError
      ├── FileNotFoundError
      ├── IOError
      ├── ImportError
      ├── RuntimeError
      ├── StopIteration
      └── ...
````
---

## ❓ Why Do We Need Exception Handling?

### Without Exception Handling

```python
def withdraw(balance, amount):
    return balance - amount

balance = 100
balance = withdraw(balance, 150)  # -50 (overdraft!)
print(f"Balance: ${balance}")
```

**Problems:**
- No validation
- Invalid states allowed
- Silent failures
- Hard to debug

### With Exception Handling

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    return balance - amount

try:
    balance = 100
    balance = withdraw(balance, 150)
except ValueError as e:
    print(f"Error: {e}")
    # Balance unchanged
```

**Benefits:**
- Clear error conditions
- Prevents invalid states
- Explicit error handling
- Better debugging

---

## 🔍 When Do We Need Exception Handling?

```
# Exception Handling Decision Flow

**Operation** → **Can it fail?**

- **Yes → Use Exception Handling**
  - File I/O  
  - Network calls  
  - User input  
  - External resources  
  - Division / Math  
  - Type conversions  

- **No → No exception needed**
```

### Use Exception Handling For:

✅ **File operations** - file might not exist
```python
try:
    with open("data.txt") as f:
        content = f.read()
except FileNotFoundError:
    content = ""
```

✅ **Network calls** - connection can fail
```python
try:
    response = requests.get(url)
except requests.ConnectionError:
    print("Network error")
```

✅ **User input** - can be invalid
```python
try:
    age = int(input("Age: "))
except ValueError:
    age = None
```

✅ **Type conversions** - might not convert
```python
try:
    value = int("abc")
except ValueError:
    value = 0
```

❌ **Don't Use For:**
- Normal control flow (use if/else)
- Expected behavior (use return values)
- Validation (check before operating)

---

## 🛠️ Basic Syntax

### try-except
```python
try:
    result = risky_operation()
except SomeError:
    result = default_value
```

### try-except-else
```python
try:
    result = risky_operation()
except SomeError:
    print("Error occurred")
else:
    print("Success!")  # Only runs if no exception
```

### try-except-finally
```python
try:
    file = open("data.txt")
    data = file.read()
except FileNotFoundError:
    data = None
finally:
    file.close()  # Always runs, even if exception
```

### try-except-else-finally
```python
try:
    result = risky_operation()
except SomeError:
    print("Error")
else:
    print("Success")  # No exception
finally:
    cleanup()  # Always runs
```

---

## 📊 Common Built-in Exceptions

```python
# ValueError - Invalid value
int("abc")  # ValueError

# TypeError - Wrong type
"text" + 5  # TypeError

# KeyError - Missing dict key
d = {"a": 1}
d["b"]  # KeyError

# IndexError - Invalid index
lst = [1, 2, 3]
lst[10]  # IndexError

# AttributeError - Missing attribute
"text".nonexistent  # AttributeError

# FileNotFoundError - File doesn't exist
open("missing.txt")  # FileNotFoundError

# ZeroDivisionError - Division by zero
10 / 0  # ZeroDivisionError
```

---

## 🎨 Creating Custom Exceptions

### Basic Custom Exception
```python
class InvalidAgeError(Exception):
    pass

def set_age(age):
    if age < 0:
        raise InvalidAgeError("Age cannot be negative")
    return age

try:
    set_age(-5)
except InvalidAgeError as e:
    print(f"Error: {e}")
```

### Custom Exception with Data
```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Balance ${balance} insufficient for ${amount}")

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    withdraw(100, 150)
except InsufficientFundsError as e:
    print(f"Error: {e}")
    print(f"Shortfall: ${e.amount - e.balance}")
```

### Exception Hierarchy
```python
class BankError(Exception):
    """Base exception for banking operations"""
    pass

class InsufficientFundsError(BankError):
    """Raised when account has insufficient funds"""
    pass

class InvalidAccountError(BankError):
    """Raised when account doesn't exist"""
    pass

# Catch specific or general
try:
    withdraw(account, amount)
except InsufficientFundsError:
    print("Not enough money")
except BankError:  # Catches all bank errors
    print("Banking error")
```

---

## ⚠️ Common Gotchas

### Gotcha 1: Bare except catches everything
```python
# ❌ BAD - Catches EVERYTHING, even Ctrl+C
try:
    risky_operation()
except:
    print("Error")

# ✅ GOOD - Be specific
try:
    risky_operation()
except ValueError:
    print("Value error")
except TypeError:
    print("Type error")
```

### Gotcha 2: Exception swallowing
```python
# ❌ BAD - Hides errors
try:
    important_operation()
except Exception:
    pass  # Silent failure!

# ✅ GOOD - Log or re-raise
try:
    important_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise  # Re-raise for caller to handle
```

### Gotcha 3: Too broad exception
```python
# ❌ BAD - Catches unrelated errors
try:
    value = int(user_input)
    result = calculate(value)
except Exception:  # Catches both conversion and calculation errors
    print("Error")

# ✅ GOOD - Separate handling
try:
    value = int(user_input)
except ValueError:
    print("Invalid input")
else:
    try:
        result = calculate(value)
    except CalculationError:
        print("Calculation failed")
```

### Gotcha 4: finally modifies return
```python
# ❌ CONFUSING
def func():
    try:
        return "try"
    finally:
        return "finally"  # This wins!

print(func())  # "finally"

# ✅ GOOD - Don't return in finally
def func():
    try:
        return "try"
    finally:
        cleanup()  # Side effects only
```

### Gotcha 5: Exception in finally
```python
# ❌ BAD - finally exception masks original
try:
    risky_operation()  # Raises ValueError
except ValueError:
    pass
finally:
    cleanup()  # Raises RuntimeError - hides ValueError!

# ✅ GOOD - Handle finally exceptions
try:
    risky_operation()
except ValueError:
    pass
finally:
    try:
        cleanup()
    except RuntimeError:
        logger.error("Cleanup failed")
```

---

## 🎯 Best Practices

### 1. Be Specific
```python
# ❌ BAD
try:
    process()
except Exception:  # Too broad
    pass

# ✅ GOOD
try:
    process()
except FileNotFoundError:  # Specific
    handle_missing_file()
except PermissionError:
    handle_permission_denied()
```

### 2. Use else for Success Code
```python
# ❌ BAD
try:
    file = open("data.txt")
    data = file.read()
    process(data)  # Might raise, confused with file error
except FileNotFoundError:
    pass

# ✅ GOOD
try:
    file = open("data.txt")
except FileNotFoundError:
    pass
else:
    data = file.read()
    process(data)  # Clear separation
```

### 3. Use finally for Cleanup
```python
# ✅ GOOD - Always closes
file = None
try:
    file = open("data.txt")
    process(file)
except Exception as e:
    logger.error(e)
finally:
    if file:
        file.close()  # Always runs

# ✅ BETTER - Use context manager
with open("data.txt") as file:
    process(file)  # Automatic cleanup
```

### 4. Don't Swallow Exceptions
```python
# ❌ BAD
try:
    critical_operation()
except Exception:
    pass  # Silent failure

# ✅ GOOD - Log and/or re-raise
try:
    critical_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise  # Let caller handle
```

### 5. Fail Fast
```python
# ❌ BAD - Continues with bad data
def process_user(user_id):
    try:
        user = get_user(user_id)
    except UserNotFoundError:
        user = None  # Continues with None!
    
    update_user(user)  # Fails later

# ✅ GOOD - Fail immediately
def process_user(user_id):
    user = get_user(user_id)  # Let exception propagate
    update_user(user)
```

---

## 📝 Scenario-Based Examples

### Scenario 1: API Call with Retry
```python
import time

def call_api(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
        except requests.HTTPError as e:
            if e.response.status_code >= 500:
                # Server error, retry
                continue
            else:
                # Client error, don't retry
                raise
```

### Scenario 2: File Processing Pipeline
```python
def process_file(filename):
    file = None
    try:
        # Open file
        file = open(filename)
        
        # Parse content
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in {filename}")
        
        # Validate data
        if "required_field" not in data:
            raise ValueError("Missing required field")
        
        return data
        
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    finally:
        if file:
            file.close()
```

### Scenario 3: Transaction with Rollback
```python
def transfer_money(from_account, to_account, amount):
    try:
        # Start transaction
        db.begin_transaction()
        
        # Debit
        if from_account.balance < amount:
            raise InsufficientFundsError()
        from_account.balance -= amount
        
        # Credit
        to_account.balance += amount
        
        # Commit
        db.commit()
        
    except InsufficientFundsError:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Transfer failed: {e}")
        raise
```

### Scenario 4: Resource Management
```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        return False  # Don't suppress exception

# Usage
try:
    with DatabaseConnection() as conn:
        conn.execute("INSERT ...")
        conn.execute("UPDATE ...")
except DatabaseError as e:
    print(f"Database error: {e}")
```

### Scenario 5: Validation Chain
```python
class ValidationError(Exception):
    pass

def validate_user_data(data):
    try:
        # Email validation
        if "@" not in data["email"]:
            raise ValidationError("Invalid email")
        
        # Age validation
        age = int(data["age"])
        if age < 0 or age > 150:
            raise ValidationError("Invalid age")
        
        # Password validation
        if len(data["password"]) < 8:
            raise ValidationError("Password too short")
        
        return True
        
    except KeyError as e:
        raise ValidationError(f"Missing field: {e}")
    except ValueError:
        raise ValidationError("Age must be a number")
```

---

## 🔑 Quick Reference

| Keyword | Purpose | When Runs |
|---------|---------|-----------|
| **try** | Code that might fail | Always |
| **except** | Handle exception | If exception occurs |
| **else** | Success code | If no exception |
| **finally** | Cleanup code | Always (even with exception) |
| **raise** | Throw exception | When called |

### Exception Flow

```
try:
    code              # Run first
except Error:
    handle            # Run if exception
else:
    success           # Run if NO exception
finally:
    cleanup           # ALWAYS run
```

---

## 💡 When NOT to Use Exceptions

```python
# ❌ BAD - Using exception for control flow
try:
    value = dictionary[key]
except KeyError:
    value = default

# ✅ GOOD - Use get()
value = dictionary.get(key, default)

# ❌ BAD - Expected behavior
try:
    if user.is_admin():
        do_admin_stuff()
except AttributeError:
    pass

# ✅ GOOD - Check first
if hasattr(user, 'is_admin') and user.is_admin():
    do_admin_stuff()
```

---

## 🎓 Interview Quick Answers

**Q: try-except vs if-else?**
A: Use if-else for expected conditions, try-except for exceptional cases

**Q: When to use custom exceptions?**
A: When you need domain-specific error handling with additional context

**Q: What does finally do?**
A: Runs cleanup code always, even if exception occurs

**Q: Should you catch Exception?**
A: No, be specific. Catching Exception is too broad

**Q: How to re-raise exception?**
A: Use bare `raise` statement in except block

---

## ✅ Key Takeaways

1. **Use exceptions for exceptional cases**, not control flow
2. **Be specific** - catch exact exception types
3. **Don't swallow** - log or re-raise
4. **Use finally** for cleanup (or context managers)
5. **Fail fast** - don't continue with invalid state
6. **Custom exceptions** add clarity and context
7. **else clause** separates success code
8. **Exceptions are expensive** - don't use in hot paths