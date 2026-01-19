# Exception Handling Quiz 🧠

## Question 1: finally Return Trap

```python
def mystery():
    try:
        return "A"
    except:
        return "B"
    finally:
        return "C"

print(mystery())
```

**What's the output?**
- A) `"A"`
- B) `"B"`
- C) `"C"`
- D) `SyntaxError`

---
<details>
<summary>Answer</summary>

**C) `"C"`**

**Explanation:** `finally` block ALWAYS executes, and if it has a return statement, it overrides the return from try/except blocks. This is a common gotcha!

**Rule:** Never use `return` in finally block.
</details>

---

## Question 2: Exception Hierarchy

```python
try:
    raise ValueError("Error")
except Exception:
    print("A")
except ValueError:
    print("B")
```

**What prints?**
- A) `"A"`
- B) `"B"`
- C) `"A"` then `"B"`
- D) `"B"` then `"A"`

---

<details>
<summary>Answer</summary>

**A) `"A"`**

**Explanation:** Exception handlers are checked top-to-bottom. Since `ValueError` is a subclass of `Exception`, the first handler catches it. The second handler is unreachable.

**Rule:** Order matters! Put specific exceptions before general ones.

**Real-World Pitfall:**
```python
try:
    process_data()
except Exception as e:
    log_error(e)  # Catches everything first!
except ValueError:
    handle_bad_input()  # Never reached!
```
</details>

---

## Question 3: Bare except Danger

```python
try:
    result = 10 / 0
except:
    print("Caught")
```

**What's the problem?**
- A) Won't catch ZeroDivisionError
- B) Catches too much (even KeyboardInterrupt)
- C) Syntax error
- D) No problem

---
<details>
<summary>Answer</summary>

**B) Catches too much**

**Explanation:** Bare `except:` catches EVERYTHING including:
- `KeyboardInterrupt` (Ctrl+C)
- `SystemExit` (exit() calls)
- Memory errors
- System exceptions

This makes debugging impossible and prevents graceful shutdown.

**Rule:** Always specify exception types: `except ZeroDivisionError:`
</details>

---

## Question 4: Re-raising Exceptions

```python
def process():
    try:
        risky_operation()
    except ValueError:
        print("Logged")
        raise

try:
    process()
except ValueError:
    print("Handled")
```

**What happens if risky_operation() raises ValueError?**
- A) Only `"Logged"` prints
- B) Only `"Handled"` prints
- C) Both print
- D) Exception is lost

---

<details>
<summary>Answer</summary>

**C) Both print**

**Explanation:** Bare `raise` in except block re-raises the same exception, allowing both functions to handle it.

Flow:
1. `risky_operation()` raises ValueError
2. `process()` catches it, prints "Logged", re-raises
3. Outer try catches it, prints "Handled"

**Pattern:** Log-and-rethrow pattern for observability.
</details>

---

## Question 5: else Clause Timing

```python
def test(value):
    try:
        result = 10 / value
    except ZeroDivisionError:
        print("A")
    else:
        print("B")
    finally:
        print("C")

test(2)
```

**What's the output?**
- A) `B C`
- B) `A C`
- C) `A B C`
- D) `C B`

---

<details>
<summary>Answer</summary>

**A) `B C`**

**Execution order:**
1. `try` executes successfully (no exception)
2. `else` runs because no exception → prints "B"
3. `finally` always runs → prints "C"

**Note:** `else` only runs if NO exception occurs in try block.

If test(0):
- Output would be `A C` (except runs, else skipped, finally always)
</details>

---

## Question 6: Custom Exception Benefits

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError(f"Insufficient funds")
    return balance - amount

def transfer(from_acc, to_acc, amount):
    try:
        from_acc = withdraw(from_acc, amount)
        to_acc += amount
    except ValueError:
        print("Transfer failed")
```

**What's the problem with using ValueError?**
- A) ValueError is too specific
- B) Can't distinguish from other validation errors
- C) Should use Exception instead
- D) No problem

---
<details>
<summary>Answer</summary>

**B) Can't distinguish from other validation errors**

**Explanation:** Generic exceptions make it hard to handle specific business logic errors differently.

**Better approach with custom exception:**
```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Need ${amount - balance} more")

def transfer(from_acc, to_acc, amount):
    try:
        from_acc = withdraw(from_acc, amount)
    except InsufficientFundsError as e:
        # Specific handling for insufficient funds
        notify_user(f"Short ${e.amount - e.balance}")
    except ValueError:
        # Different handling for other validation errors
        log_error("Invalid input")
```

**Benefits:**
- Clear intent and semantics
- Carry additional context (balance, amount)
- Different handling for different business errors
- Better API for callers

</details>

---

## Question 7: When NOT to Catch Exceptions

```python
# Option A
def get_user(user_id):
    try:
        return database.find(user_id)
    except UserNotFoundError:
        return None

# Option B  
def get_user(user_id):
    return database.find(user_id)  # Let it raise

# Which is better?
```

**Which approach is better?**
- A) Option A - always handle exceptions
- B) Option B - let caller handle it
- C) Both are equally good
- D) Depends on the context

---
<details>
<summary>Answer</summary>

**D) Depends on the context**

**Option B is often better because:**

```python
# Caller knows what to do
try:
    user = get_user(user_id)
    send_email(user)
except UserNotFoundError:
    show_error("User not found")

# vs returning None (silent failure)
user = get_user(user_id)
send_email(user)  # Crashes with AttributeError!
```

**Don't catch exceptions when:**
- You can't meaningfully handle them
- Caller needs to know it failed
- Returning None hides the error
- Exception has useful context

**Do catch exceptions when:**
- You can recover (retry, fallback)
- You're at API boundary
- You need to add context
- You can provide default value safely

**Rule:** Don't swallow exceptions unless you have a good reason.

</details>

---

## Question 8: Exception for Control Flow?

```python
# Option A
def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return None

# Option B
def parse_int(value):
    if value.isdigit():
        return int(value)
    return None
```

**Which is better practice?**
- A) Option A (exception-based)
- B) Option B (check first)
- C) Both are fine
- D) Neither

---
<details>
<summary>Answer</summary>

**B) Option B (check first)**

**Explanation:** Don't use exceptions for expected conditions (control flow).

**Why check first is better:**
```python
# Exceptions are slow
for i in range(1000000):
    try:
        x = int(some_value)  # Slower if often fails
    except ValueError:
        x = 0

# Checking is fast
for i in range(1000000):
    x = int(some_value) if some_value.isdigit() else 0
```

**Use exceptions for:**
- Truly exceptional cases (file missing, network down)
- Cases you can't check beforehand

**Don't use exceptions for:**
- Normal program flow
- Expected invalid input
- Validation that can be checked
- Performance-critical loops

**Python principles:**
- **EAFP** (Easier to Ask Forgiveness than Permission): Good for rare errors
- **LBYL** (Look Before You Leap): Good for common validation

</details>

---

## Question 9: Exception Chaining

```python
def process_file(filename):
    try:
        data = read_file(filename)
    except FileNotFoundError:
        raise ValueError("Config missing")

try:
    process_file("config.txt")
except ValueError as e:
    print(e)
```

**What information is lost?**
- A) Nothing, it works fine
- B) Original filename
- C) That FileNotFoundError happened
- D) The function name

---
<details>
<summary>Answer</summary>

**C) Original FileNotFoundError context is lost**

**Problem:** Can't tell if ValueError came from missing file or bad data!

**Better - use exception chaining:**
```python
def process_file(filename):
    try:
        data = read_file(filename)
    except FileNotFoundError as e:
        raise ValueError("Config missing") from e
        #                                  ^^^^^^^^
        # Preserves original exception

# Now you can see both:
# ValueError: Config missing
# The above exception was the direct cause of...
# FileNotFoundError: [Errno 2] No such file: 'config.txt'
```

**Benefits:**
- Full error context preserved
- Easier debugging
- Shows cause chain
- Don't lose original exception type

**Rule:** When converting exceptions, use `from` to preserve context.

</details>

---

## Question 10: Exception in finally

```python
def tricky():
    try:
        return "A"
    finally:
        1 / 0

try:
    result = tricky()
    print(result)
except ZeroDivisionError:
    print("Caught")
```

**What's the output?**
- A) `"A"`
- B) `"Caught"`
- C) `"A"` then `"Caught"`
- D) Unhandled ZeroDivisionError

---
<details>
<summary>Answer</summary>

**B) `"Caught"`**

**Explanation:** Exception in `finally` block OVERRIDES the return value from try block!

Flow:
1. `try` prepares to return "A"
2. `finally` executes and raises ZeroDivisionError
3. The return "A" is **discarded**
4. Exception propagates to outer try-except
5. Prints "Caught"

**Gotcha:** Exceptions in finally mask the try block's return value or exception!

**Rule:** Keep finally clean - only cleanup code, never raise exceptions.
</details>

---

## 🔑 Key Concepts Tested

1. **finally override** - Can override return values and mask exceptions
2. **Exception order** - Specific before general
3. **Bare except** - Dangerous, catches everything
4. **Re-raising** - `raise` without exception re-raises current
5. **else timing** - Runs only if no exception
6. **Custom exceptions** - Better semantics and context
7. **When NOT to catch** - Let exceptions propagate when appropriate
8. **Control flow** - Don't use exceptions for normal flow
9. **Exception chaining** - Preserve context with `from`
10. **finally exceptions** - Can mask original behavior

---