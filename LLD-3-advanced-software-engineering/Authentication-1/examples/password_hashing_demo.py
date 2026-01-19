#!/usr/bin/env python3
"""
Password Hashing Security Demo
==============================

This script demonstrates why proper password hashing matters
by showing live attacks against different hashing methods.

Run: python password_hashing_demo.py

Requirements:
    pip install bcrypt argon2-cffi passlib
"""

import hashlib
import time
import os
from typing import Optional

# Try importing optional libraries
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    print("⚠️  bcrypt not installed. Run: pip install bcrypt")

try:
    from argon2 import PasswordHasher
    ARGON2_AVAILABLE = True
except ImportError:
    ARGON2_AVAILABLE = False
    print("⚠️  argon2 not installed. Run: pip install argon2-cffi")


def print_header(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(method: str, time_taken: float, cracked: bool, password: str = ""):
    """Print a formatted result"""
    status = "✅ CRACKED" if cracked else "❌ Not cracked"
    if cracked:
        print(f"  {method}: {status} in {time_taken:.4f}s → '{password}'")
    else:
        print(f"  {method}: {status} ({time_taken:.4f}s elapsed)")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 1: PLAINTEXT STORAGE (The worst!)
# ═══════════════════════════════════════════════════════════════════════════════

def demo_plaintext():
    print_header("DEMO 1: PLAINTEXT STORAGE")
    print("""
  Scenario: Database stores passwords directly
  Attack: Attacker gets database dump

  Database contents:
  ┌─────────────┬──────────────────┐
  │ user        │ password         │
  ├─────────────┼──────────────────┤
  │ alice       │ ilovecats        │
  │ bob         │ password123      │
  │ admin       │ admin2024!       │
  └─────────────┴──────────────────┘
    """)

    print("  Result: ALL passwords instantly visible! 💀")
    print("  Time to crack: 0.000000 seconds")
    print("\n  ⚠️  NEVER store passwords in plaintext!")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 2: MD5 HASHING (Broken!)
# ═══════════════════════════════════════════════════════════════════════════════

def demo_md5_attack():
    print_header("DEMO 2: MD5 HASHING - Dictionary Attack")

    # Common password list (in real attacks, this would be millions)
    common_passwords = [
        "password", "123456", "password123", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "qwerty",
        "login", "princess", "abc123", "admin123", "root",
        "user", "test", "guest", "master123", "superman",
    ]

    # Simulate a "stolen" hash from a database
    target_password = "dragon"  # The actual password
    target_hash = hashlib.md5(target_password.encode()).hexdigest()

    print(f"""
  Scenario: Database uses MD5 (no salt)
  Stolen hash: {target_hash}

  Attack: Dictionary attack with common passwords
    """)

    start_time = time.time()
    cracked_password = None

    for pwd in common_passwords:
        test_hash = hashlib.md5(pwd.encode()).hexdigest()
        if test_hash == target_hash:
            cracked_password = pwd
            break

    elapsed = time.time() - start_time
    print_result("MD5 Dictionary", elapsed, cracked_password is not None, cracked_password or "")

    # Show hash rate
    hashes_per_sec = len(common_passwords) / elapsed if elapsed > 0 else float('inf')
    print(f"\n  Hash rate: {hashes_per_sec:,.0f} hashes/second (on this CPU)")
    print("  GPU can do: 164,000,000,000 hashes/second!")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 3: SHA-256 WITH SALT (Better, but still fast)
# ═══════════════════════════════════════════════════════════════════════════════

def demo_sha256_salted():
    print_header("DEMO 3: SHA-256 WITH SALT")

    # Create a salted hash
    password = "monkey123"
    salt = os.urandom(16).hex()
    salted_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    print(f"""
  Password: {password}
  Salt: {salt}
  Hash: {salted_hash}

  Attack: Brute force (must try each password with this specific salt)
    """)

    # Demonstrate hash speed
    iterations = 100_000
    start_time = time.time()

    for i in range(iterations):
        hashlib.sha256((salt + f"test{i}").encode()).hexdigest()

    elapsed = time.time() - start_time
    rate = iterations / elapsed

    print(f"  Speed test: {iterations:,} hashes in {elapsed:.3f}s")
    print(f"  Rate: {rate:,.0f} SHA-256 hashes/second")
    print(f"\n  ✅ Salt prevents rainbow tables")
    print(f"  ❌ Still too fast! GPU can crack simple passwords in hours")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 4: BCRYPT (The right way!)
# ═══════════════════════════════════════════════════════════════════════════════

def demo_bcrypt():
    if not BCRYPT_AVAILABLE:
        print_header("DEMO 4: BCRYPT (Skipped - library not installed)")
        return

    print_header("DEMO 4: BCRYPT - Intentionally Slow")

    password = b"password123"

    print("  Testing different cost factors:\n")

    for cost in [4, 8, 10, 12, 14]:
        start_time = time.time()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=cost))
        elapsed = time.time() - start_time

        hashes_per_sec = 1 / elapsed if elapsed > 0 else float('inf')
        print(f"  Cost {cost:2d}: {elapsed:.4f}s per hash ({hashes_per_sec:,.1f}/sec)")

    print(f"""
  At cost=12:
  • Legitimate user: waits ~0.25s (barely noticeable)
  • Attacker: can only try ~4 passwords/second

  To crack a medium password (10^10 guesses):
  • SHA-256: ~7 minutes
  • BCrypt:  ~80 YEARS
    """)

    # Verify password
    print("  Password verification demo:")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
    print(f"  Hash: {hashed.decode()[:40]}...")

    start = time.time()
    is_valid = bcrypt.checkpw(password, hashed)
    print(f"  Correct password: {is_valid} ({time.time()-start:.4f}s)")

    start = time.time()
    is_valid = bcrypt.checkpw(b"wrong_password", hashed)
    print(f"  Wrong password:   {is_valid} ({time.time()-start:.4f}s)")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 5: ARGON2 (State of the art)
# ═══════════════════════════════════════════════════════════════════════════════

def demo_argon2():
    if not ARGON2_AVAILABLE:
        print_header("DEMO 5: ARGON2 (Skipped - library not installed)")
        return

    print_header("DEMO 5: ARGON2 - Memory-Hard Hashing")

    password = "password123"
    ph = PasswordHasher(
        time_cost=2,      # Number of iterations
        memory_cost=65536, # Memory usage in KiB (64 MB)
        parallelism=2     # Number of threads
    )

    print(f"""
  Argon2 parameters:
  • Time cost: 2 iterations
  • Memory cost: 64 MB
  • Parallelism: 2 threads

  Why memory-hard matters:
  • GPUs have fast cores but limited memory per core
  • Requiring 64MB per hash makes GPU attacks impractical
    """)

    start_time = time.time()
    hashed = ph.hash(password)
    elapsed = time.time() - start_time

    print(f"  Hash: {hashed[:50]}...")
    print(f"  Time: {elapsed:.4f}s")

    # Verify
    start = time.time()
    try:
        ph.verify(hashed, password)
        print(f"  Verify correct: True ({time.time()-start:.4f}s)")
    except:
        print(f"  Verify correct: False")

    start = time.time()
    try:
        ph.verify(hashed, "wrong")
        print(f"  Verify wrong: True")
    except:
        print(f"  Verify wrong: False ({time.time()-start:.4f}s)")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 6: TIMING ATTACK VULNERABILITY
# ═══════════════════════════════════════════════════════════════════════════════

def demo_timing_attack():
    print_header("DEMO 6: TIMING ATTACK VULNERABILITY")

    print("""
  A timing attack exploits the time difference in string comparison.

  Vulnerable comparison:
  ┌────────────────────────────────────────────────────────────┐
  │  def check_password(input, stored):                        │
  │      return input == stored  # Stops at first mismatch!   │
  └────────────────────────────────────────────────────────────┘

  If stored = "secret":
  • "aaaaaa" vs "secret" → fails at char 0 (fast)
  • "saaaaa" vs "secret" → fails at char 1 (slightly slower)
  • "seaaaa" vs "secret" → fails at char 2 (even slower)

  By measuring time, attacker can guess password char by char!
    """)

    # Demonstrate (exaggerated for visibility)
    stored_hash = "a1b2c3d4e5f6"

    def vulnerable_compare(a: str, b: str) -> bool:
        """Vulnerable to timing attacks"""
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            time.sleep(0.001)  # Exaggerated delay
            if a[i] != b[i]:
                return False
        return True

    def secure_compare(a: str, b: str) -> bool:
        """Constant-time comparison"""
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        time.sleep(0.001 * len(a))  # Always same time
        return result == 0

    # Test vulnerable
    test_cases = [
        "x1b2c3d4e5f6",  # Wrong at position 0
        "a1x2c3d4e5f6",  # Wrong at position 2
        "a1b2c3d4e5x6",  # Wrong at position 10
    ]

    print("  Vulnerable comparison timing:")
    for test in test_cases:
        start = time.time()
        vulnerable_compare(test, stored_hash)
        elapsed = (time.time() - start) * 1000
        wrong_pos = next((i for i, (a, b) in enumerate(zip(test, stored_hash)) if a != b), -1)
        print(f"    Wrong at pos {wrong_pos:2d}: {elapsed:.2f}ms")

    print("\n  ✅ Use constant-time comparison (bcrypt.checkpw does this)")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 7: COMPARISON SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

def demo_comparison():
    print_header("COMPARISON SUMMARY")

    print("""
  ┌─────────────┬─────────────┬─────────────┬─────────────┬──────────┐
  │ Method      │ Hashes/sec  │ Time to     │ Secure?     │ Use?     │
  │             │ (GPU)       │ crack 10^10 │             │          │
  ├─────────────┼─────────────┼─────────────┼─────────────┼──────────┤
  │ Plaintext   │ N/A         │ Instant     │ ☠️ NO       │ ❌ NEVER │
  │ MD5         │ 164 billion │ ~1 minute   │ ☠️ NO       │ ❌ NEVER │
  │ SHA-256     │ 22 billion  │ ~8 minutes  │ ⚠️ Weak     │ ❌ NO    │
  │ BCrypt (12) │ ~1,400      │ ~226 years  │ ✅ YES      │ ✅ YES   │
  │ Argon2      │ ~1,000      │ ~317 years  │ ✅ BEST     │ ✅ YES   │
  └─────────────┴─────────────┴─────────────┴─────────────┴──────────┘

  Key Takeaways:
  ═════════════

  1. NEVER store plaintext passwords
  2. NEVER use MD5 or SHA for passwords (they're for checksums!)
  3. ALWAYS use BCrypt (cost ≥ 12) or Argon2
  4. ALWAYS use the library's verify function (constant-time)
  5. Increase cost factor as hardware improves
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "🔐" * 30)
    print("     PASSWORD HASHING SECURITY DEMONSTRATION")
    print("🔐" * 30)

    demo_plaintext()
    demo_md5_attack()
    demo_sha256_salted()
    demo_bcrypt()
    demo_argon2()
    demo_timing_attack()
    demo_comparison()

    print("\n" + "=" * 60)
    print("  Demo complete! Now you understand why BCrypt matters.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
