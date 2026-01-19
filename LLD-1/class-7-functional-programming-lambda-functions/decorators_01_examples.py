"""
Python Decorators - Practical Examples
From basic to advanced patterns
"""

print("=" * 60)
print("Example 1: Understanding the Basics")
print("=" * 60)


# Functions are first-class objects
def greet():
    return "Hello!"


# Assign to variable
say_hello = greet
print(say_hello())  # Hello!

# Store in list
functions = [greet, say_hello]
for func in functions:
    print(func())

print()
print("=" * 60)
print("Example 2: Manual Decoration (No @ Syntax)")
print("=" * 60)


def make_uppercase(func):
    def wrapper():
        result = func()
        return result.upper()

    return wrapper


def greet():
    return "hello"


# Manual decoration
greet = make_uppercase(greet)
print(greet())  # HELLO

print()
print("=" * 60)
print("Example 3: Using @ Syntax")
print("=" * 60)


def make_bold(func):
    def wrapper():
        result = func()
        return f"**{result}**"

    return wrapper


@make_bold  # Same as: greet = make_bold(greet)
def greet():
    return "Hello"


print(greet())  # **Hello**

print()
print("=" * 60)
print("Example 4: Decorator with Arguments")
print("=" * 60)


def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result

    return wrapper


@log_decorator
def add(a, b):
    return a + b


@log_decorator
def multiply(x, y, z):
    return x * y * z


print("Final:", add(3, 5))
print()
print("Final:", multiply(2, 3, 4))

print()
print("=" * 60)
print("Example 5: Timing Decorator")
print("=" * 60)

import time


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


@timing_decorator
def slow_function():
    time.sleep(0.5)
    return "Done"


@timing_decorator
def fast_function():
    return sum(range(1000))


slow_function()
fast_function()

print()
print("=" * 60)
print("Example 6: Validation Decorator")
print("=" * 60)


def validate_positive(func):
    def wrapper(x):
        if x <= 0:
            raise ValueError(f"Expected positive number, got {x}")
        return func(x)

    return wrapper


@validate_positive
def square_root(x):
    return x ** 0.5


@validate_positive
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


try:
    print(f"sqrt(16) = {square_root(16)}")
    print(f"sqrt(-4) = {square_root(-4)}")  # Will raise error
except ValueError as e:
    print(f"Error: {e}")

print()
print("=" * 60)
print("Example 7: Memoization (Caching)")
print("=" * 60)


def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            print(f"Cache hit for {args}")
            return cache[args]
        print(f"Computing for {args}")
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(f"fib(5) = {fibonacci(5)}")
print(f"\nCalling fib(5) again:")
print(f"fib(5) = {fibonacci(5)}")

print()
print("=" * 60)
print("Example 8: Decorator with Arguments")
print("=" * 60)


def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results

        return wrapper

    return decorator


@repeat(times=3)
def greet(name):
    return f"Hello, {name}!"


print(greet("Alice"))


@repeat(times=5)
def roll_dice():
    import random
    return random.randint(1, 6)


print(f"Five rolls: {roll_dice()}")

print()
print("=" * 60)
print("Example 9: Authentication Decorator")
print("=" * 60)

# Simulate user session
current_user = None


def login(username):
    global current_user
    current_user = username


def logout():
    global current_user
    current_user = None


def require_auth(func):
    def wrapper(*args, **kwargs):
        if current_user is None:
            raise Exception("Authentication required!")
        print(f"User {current_user} is authenticated")
        return func(*args, **kwargs)

    return wrapper


@require_auth
def view_profile():
    return "Profile: User data here"


@require_auth
def delete_account():
    return "Account deleted"


try:
    print(view_profile())  # Will fail
except Exception as e:
    print(f"Error: {e}")

login("alice")
print(view_profile())  # Works now
logout()

print()
print("=" * 60)
print("Example 10: Stacking Decorators")
print("=" * 60)


def uppercase(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()

    return wrapper


def exclaim(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"{result}!"

    return wrapper


def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result * times

        return wrapper

    return decorator


@repeat(2)  # Applied last (outermost)
@exclaim  # Applied second
@uppercase  # Applied first (closest to function)
def greet():
    return "hello"


print(greet())
# Execution order:
# 1. "hello" → uppercase → "HELLO"
# 2. "HELLO" → exclaim → "HELLO!"
# 3. "HELLO!" → repeat(2) → "HELLO!HELLO!"

print()
print("=" * 60)
print("Example 11: Class-Based Decorator")
print("=" * 60)


class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)


@CountCalls
def say_hello(name):
    return f"Hello, {name}!"


print(say_hello("Alice"))
print(say_hello("Bob"))
print(say_hello("Charlie"))

print()
print("=" * 60)
print("Example 12: Preserving Metadata with functools.wraps")
print("=" * 60)

from functools import wraps


# Without @wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


# With @wraps
def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@bad_decorator
def func1():
    """This is func1's docstring"""
    pass


@good_decorator
def func2():
    """This is func2's docstring"""
    pass


print("Without @wraps:")
print(f"  Name: {func1.__name__}")  # wrapper (wrong!)
print(f"  Doc: {func1.__doc__}")  # None (lost!)

print("\nWith @wraps:")
print(f"  Name: {func2.__name__}")  # func2 (correct!)
print(f"  Doc: {func2.__doc__}")  # Preserved!

print()
print("=" * 60)
print("Example 13: Rate Limiting Decorator")
print("=" * 60)

import time


def rate_limit(max_calls, period):
    """Limit function calls to max_calls per period seconds"""
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside the time window
            calls[:] = [call_time for call_time in calls if call_time > now - period]

            if len(calls) >= max_calls:
                raise Exception(f"Rate limit: Max {max_calls} calls per {period} seconds")

            calls.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@rate_limit(max_calls=3, period=5)
def api_call(endpoint):
    return f"Called {endpoint}"


# First 3 calls work
for i in range(3):
    print(api_call(f"/endpoint{i}"))

# 4th call fails
try:
    print(api_call("/endpoint4"))
except Exception as e:
    print(f"Error: {e}")

print()
print("=" * 60)
print("Example 14: Retry Decorator")
print("=" * 60)


def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


@retry(max_attempts=3, delay=0.5)
def unstable_function():
    import random
    if random.random() < 0.7:
        raise Exception("Random failure")
    return "Success!"


try:
    result = unstable_function()
    print(result)
except Exception as e:
    print(f"All attempts failed: {e}")

print()
print("=" * 60)
print("Example 15: Real-World - Flask-like Routing")
print("=" * 60)

routes = {}


def route(path):
    def decorator(func):
        routes[path] = func
        return func

    return decorator


@route("/")
def home():
    return "Home Page"


@route("/about")
def about():
    return "About Us"


@route("/contact")
def contact():
    return "Contact Form"


# Simulate routing
print("Registered routes:")
for path, handler in routes.items():
    print(f"  {path} -> {handler.__name__}()")


# Simulate request
def handle_request(path):
    if path in routes:
        return routes[path]()
    return "404 Not Found"


print(f"\nGET / -> {handle_request('/')}")
print(f"GET /about -> {handle_request('/about')}")
print(f"GET /missing -> {handle_request('/missing')}")

print()
print("=" * 60)
print("KEY LESSONS:")
print("=" * 60)
print("✓ Decorators wrap functions to extend behavior")
print("✓ @ syntax is shorthand for function application")
print("✓ Use *args, **kwargs for flexibility")
print("✓ Always return the result from wrapper")
print("✓ Use @wraps to preserve function metadata")
print("✓ Decorator with arguments needs extra nesting")
print("✓ Stacking applies bottom-to-top")
print("✓ Great for cross-cutting concerns (logging, auth, etc.)")