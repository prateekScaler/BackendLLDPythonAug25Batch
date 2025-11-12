# Code Quality Principles - Quiz

## Question 1: The Scaling Challenge

Your startup just raised Series A funding. You're scaling from 5 to 50 engineers and from 1,000 to 1,000,000 users.

Your CTO says: **"Our biggest problem isn't features or infrastructure - it's our codebase. Every change takes 10x longer than it should, and we keep breaking things."**

**What's likely the ROOT CAUSE of this problem?**

- A) The team needs more experienced developers
- B) The codebase lacks good code quality principles (readability, testability, reusability, etc.)
- C) The servers are too slow
- D) The programming language choice was wrong

---

<details>
<summary>Answer</summary>

**B) The codebase lacks good code quality principles**

**Explanation:**

When startups scale, the **codebase quality** becomes the bottleneck:

**Why this happens:**
- **Unreadable code** → New devs take weeks to onboard
- **Untestable code** → Bugs reach production constantly
- **Copy-pasted code** → Same bug exists in 10 places
- **Monolithic files** → 50 developers editing same files
- **Duplicated logic** → Changes require updating 20+ places

**The Fix:**
Good code quality principles aren't "nice to have" - they're **essential for scaling**.

**Real World Example:**
- **Startup with poor quality:** 50 engineers, shipping 1 feature/week
- **Startup with good quality:** 50 engineers, shipping 10 features/week

The difference? The second codebase is **readable, testable, reusable, modular, and maintainable**.

**Why not A?** Even experienced developers struggle with bad codebases. Good developers in a bad codebase < junior developers in a good codebase.

**Why not C/D?** Infrastructure and language matter, but code quality impacts developer productivity 100x more when scaling.

</details>

---

## Question 2: Readability

Look at these two functions:

**Function A:**
```python
def p(a, b):
    return a * b * 0.5
```

**Function B:**
```python
def calculate_triangle_area(base, height):
    return base * height * 0.5
```

**Which function is better in terms of readability?**

- A) Function A is better because it's shorter
- B) Function B is better because it's self-explanatory
- C) Both are equally readable
- D) Function A is more professional

---

<details>
<summary>Answer</summary>

**B) Function B is better because it's self-explanatory**

**Explanation:**
- Function B uses descriptive names that explain what the function does
- No need to guess what `p`, `a`, or `b` represent
- Anyone reading the code instantly understands it calculates triangle area

**Key Principle:** **READABILITY** - Clear names make code self-documenting.

</details>

---

## Question 3: Testability

Compare these two functions:

**Function A:**
```python
def process_user_bad():
    name = input("Enter name: ")
    age = input("Enter age: ")
    print(f"{name} is {age} years old")
```

**Function B:**
```python
def format_user_info(name, age):
    return f"{name} is {age} years old"

# Test example:
assert format_user_info("Alice", 25) == "Alice is 25 years old"
```

**Which function is better in terms of testability?**

- A) Function A because it's more complete
- B) Function B because it separates logic from input/output operations
- C) Function A because it handles user interaction
- D) Both are equally testable

---

<details>
<summary>Answer</summary>

**B) It separates logic from input/output operations**

**Explanation:**
- Function A mixes logic with I/O (`input()` and `print()`)
- Function B is a pure function - takes inputs, returns output, no side effects
- You can test Function B with a simple assertion - no user interaction needed
- Function A requires manual testing - you'd have to type values every time

**Key Principle:** **TESTABILITY** - Separate pure logic from I/O to enable automated testing.

</details>

---

## Question 4: Reusability

Which approach is more reusable?

**Approach A:**
```python
def send_welcome_email_bad():
    subject = "Welcome to Our App"
    message = "Hello, welcome to our application!"
    print(f"Sending: {subject} - {message}")
```

**Approach B:**
```python
def send_email(subject, message, recipient):
    print(f"To: {recipient} | Subject: {subject} | Message: {message}")

# Can reuse for any email:
send_email("Welcome", "Hello!", "user@example.com")
send_email("Reset Password", "Click here", "user@example.com")
```

**Which approach is better in terms of reusability?**

- A) Approach A because it's simpler
- B) Approach B because it's parameterized instead of having hardcoded values
- C) Approach A because it's more specific
- D) Both are equally reusable

---

<details>
<summary>Answer</summary>

**B) It's parameterized instead of having hardcoded values**

**Explanation:**
- Approach A has hardcoded subject and message - only works for welcome emails
- Approach B accepts parameters - can send ANY type of email
- With Approach A, you'd need to write `send_password_reset_email()`, `send_confirmation_email()`, etc.
- With Approach B, one function handles all cases

**Key Principle:** **REUSABILITY** - Parameterize instead of hardcoding = write once, use everywhere.

</details>

---

## Question 5: Parallel Development

Your team has 6 developers. Which structure will cause fewer merge conflicts?

**Structure A:**
```python
class AppBad:
    def login(self): pass
    def logout(self): pass
    def create_post(self): pass
    def delete_post(self): pass
    def send_message(self): pass
    def receive_message(self): pass
    # Multiple devs editing same file = conflicts!
```

**Structure B:**
```python
# auth.py
class AuthService:
    def login(self): pass
    def logout(self): pass

# posts.py
class PostService:
    def create_post(self): pass
    def delete_post(self): pass

# messaging.py
class MessageService:
    def send_message(self): pass
    def receive_message(self): pass
```

**Which structure is better in terms of parallel development?**

- A) Structure A because everything is in one place
- B) Structure B because each developer can work on different files simultaneously
- C) Structure A because it's simpler
- D) Both are equally good for team collaboration

---

<details>
<summary>Answer</summary>

**B) Each developer can work on different files simultaneously**

**Explanation:**
- Structure A: All 6 developers editing the same file → constant merge conflicts
- Structure B: Auth developer works on `auth.py`, posts developer works on `posts.py` → no conflicts
- Separating by responsibility/domain lets teams work independently

**Key Principle:** **PARALLEL DEVELOPMENT** - Separate code by domain so multiple developers don't collide.

</details>

---
## Question 6: Maintainability 

Continuing from Question 5, your company changes the tax rate from 10% to 15%.

**With Implementation A (duplicated code):**
How many places do you need to change `0.1` to `0.15`?

**With Implementation B (DRY code):**
How many places do you need to change the tax calculation?

**Choose the correct answer:**

- A) Implementation A: 1 place, Implementation B: 1 place
- B) Implementation A: 2 places, Implementation B: 1 place
- C) Implementation A: 3 places, Implementation B: 2 places
- D) Implementation A: 2 places, Implementation B: 3 places

---

<details>
<summary>Answer</summary>

**B) Implementation A: 2 places, Implementation B: 1 place**

**Explanation:**

**Implementation A:**
- Change `total * 0.1` in `calculate_order_total_bad()` → 0.15
- Change `total * 0.1` in `calculate_invoice_total_bad()` → 0.15
- **Total: 2 places** (and if you forget one, you have a bug!)

**Implementation B:**
- Change `subtotal * 0.1` in `calculate_tax()` → 0.15
- **Total: 1 place** (automatically affects all functions that call it)

**Key Principle:** **MAINTAINABILITY** - Single source of truth means one place to change, reducing bugs.

</details>

---

## Quick Principle Reference

| Principle | Ask Yourself | Bad Sign | Good Sign |
|-----------|-------------|----------|-----------|
| **Readability** | Can I understand this at 2 AM? | `def p(a, b)` | `def calculate_triangle_area(base, height)` |
| **Testability** | Can I test without database/input? | Logic + I/O mixed | Pure functions |
| **Reusability** | Will I copy-paste this? | Hardcoded values | Parameters |
| **Parallel Dev** | Will my team have conflicts? | One giant file | Separated modules |
| **Maintainability** | How many places to change? | Duplicated everywhere | DRY - one place |