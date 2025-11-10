"""
Exception Chaining - Concise Demo
Why 'from e' matters for debugging
"""

import json

print("=" * 60)
print("EXCEPTION CHAINING: Bad vs Good")
print("=" * 60)

# Example 1: Basic Comparison
print("\n--- Example 1: Context Lost vs Preserved ---")

def read_config_bad(filename):
    raise FileNotFoundError(f"No such file: '{filename}'")

def process_bad(filename):
    try:
        return read_config_bad(filename)
    except FileNotFoundError:
        raise ValueError("Config missing")  # Context lost!

try:
    process_bad("config.txt")
except ValueError as e:
    print("❌ WITHOUT 'from':")
    print(f"   Error: {e}")
    print(f"   Cause: {e.__cause__}")  # None
    print("   Problem: Can't tell if file missing or bad data!")

def read_config_good(filename):
    raise FileNotFoundError(f"No such file: '{filename}'")

def process_good(filename):
    try:
        return read_config_good(filename)
    except FileNotFoundError as e:
        raise ValueError("Config missing") from e  # Context preserved!

try:
    process_good("config.txt")
except ValueError as e:
    print("\n✅ WITH 'from e':")
    print(f"   Error: {e}")
    print(f"   Cause: {type(e.__cause__).__name__}: {e.__cause__}")
    print("   Benefit: Full context! Easy debugging!")

# Example 2: Real-World JSON
print("\n--- Example 2: JSON Processing ---")

def load_json_bad(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Settings missing")
    except json.JSONDecodeError:
        raise ValueError("Settings corrupted")

try:
    load_json_bad("missing.json")
except ValueError as e:
    print("❌ WITHOUT 'from':")
    print(f"   Error: {e}")
    print("   Can't tell: Missing or corrupted?")

def load_json_good(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ValueError("Settings missing") from e
    except json.JSONDecodeError as e:
        raise ValueError("Settings corrupted") from e

try:
    load_json_good("missing.json")
except ValueError as e:
    print("\n✅ WITH 'from e':")
    print(f"   Error: {e}")
    print(f"   Root: {type(e.__cause__).__name__}")
    print("   Clear: File missing (not corrupted)!")

# Example 3: Traceback Visual
print("\n--- Example 3: What Traceback Shows ---")

print("\n❌ Without 'from':")
print("""
ValueError: Config missing
  (FileNotFoundError hidden!)
""")

print("✅ With 'from e':")
print("""
FileNotFoundError: No such file: 'config.txt'

The above exception was the direct cause of:

ValueError: Config missing
  (Full chain visible!)
""")

# Example 4: Database Example
print("\n--- Example 4: Database Error ---")

def db_query_bad():
    raise ConnectionError("DB connection lost")

def get_user_bad(user_id):
    try:
        return db_query_bad()
    except ConnectionError:
        raise RuntimeError("Failed to fetch user")

try:
    get_user_bad(123)
except RuntimeError as e:
    print("❌ WITHOUT 'from':")
    print(f"   Error: {e}")
    print(f"   Cause: {e.__cause__}")
    print("   Why did it fail? Unknown!")

def db_query_good():
    raise ConnectionError("DB connection lost")

def get_user_good(user_id):
    try:
        return db_query_good()
    except ConnectionError as e:
        raise RuntimeError("Failed to fetch user") from e

try:
    get_user_good(123)
except RuntimeError as e:
    print("\n✅ WITH 'from e':")
    print(f"   Error: {e}")
    print(f"   Cause: {e.__cause__}")
    print("   Clear: DB connection issue!")

# Example 5: Attributes
print("\n--- Example 5: Exception Attributes ---")

def demo_attributes():
    try:
        raise ConnectionError("Network timeout")
    except ConnectionError as e:
        raise ValueError("Operation failed") from e

try:
    demo_attributes()
except ValueError as e:
    print(f"Exception: {e}")
    print(f"__cause__: {e.__cause__}")
    print(f"__context__: {e.__context__}")
    print(f"__suppress_context__: {e.__suppress_context__}")

# Example 6: Suppress with 'from None'
print("\n--- Example 6: Suppress Original (Rare) ---")

def suppress_demo():
    try:
        raise ValueError("Original")
    except ValueError:
        raise RuntimeError("New error") from None  # Suppress

try:
    suppress_demo()
except RuntimeError as e:
    print(f"Error: {e}")
    print(f"Cause: {e.__cause__}")  # None
    print("Use 'from None' only when original is irrelevant")

# Summary
print("\n" + "=" * 60)
print("COMPARISON")
print("=" * 60)
print(f"{'Aspect':<25} {'Without':<15} {'With from e':<15}")
print("-" * 60)
print(f"{'Root cause visible':<25} {'❌':<15} {'✅':<15}")
print(f"{'Full context':<25} {'❌':<15} {'✅':<15}")
print(f"{'Easy debugging':<25} {'❌':<15} {'✅':<15}")
print(f"{'Production logs':<25} {'Incomplete':<15} {'Complete':<15}")
print("-" * 60)

print("\n" + "=" * 60)
print("KEY TAKEAWAY")
print("=" * 60)
print("""
🎯 ALWAYS use 'from' when raising in except:

   try:
       risky_operation()
   except SomeError as e:
       raise MyError("message") from e
       #                        ^^^^^^^^

📋 WHEN TO USE:
   • Converting low-level to high-level exceptions
   • Adding context to technical errors
   • Any raise in except block

💡 Saves hours of debugging in production!
""")