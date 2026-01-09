# BCrypt Deep Dive

> *"BCrypt: The password hashing algorithm that refuses to hurry."*

---

## What Is BCrypt?

BCrypt is a password hashing function designed in 1999 by Niels Provos and David Mazières. It's based on the Blowfish cipher and was specifically designed to be **slow** and **adaptable**.

```
┌─────────────────────────────────────────────────────────────────┐
│                    BCRYPT AT A GLANCE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Created:     1999                                               │
│  Based on:    Blowfish cipher                                    │
│  Key feature: Adaptive cost factor                               │
│  Salt:        Built-in (22 characters)                           │
│  Output:      60 characters (fixed)                              │
│  Status:      Industry standard for password hashing             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Anatomy of a BCrypt Hash

```
$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW
└─┬┘└┬┘└──────────────────┬─────────────────┘└──────────┬───────┘
  │  │                    │                             │
  │  │                    │                             │
  │  │                    Salt (22 chars)               Hash (31 chars)
  │  │
  │  Cost factor (12 = 2^12 = 4096 iterations)
  │
  Algorithm version ($2b$ = current standard)
```

### Breaking It Down

| Part | Value | Meaning |
|------|-------|---------|
| `$2b$` | Algorithm | BCrypt variant (2b is current standard) |
| `12` | Cost factor | 2^12 = 4,096 iterations |
| `R9h/cIPz0gi.URNNX3kh2O` | Salt | 22-char random salt (128 bits) |
| `PST9/PgBkqquzi.Ss7KIUgO2t0jWMUW` | Hash | 31-char hash output |

---

## The Cost Factor Explained

The cost factor (also called "work factor" or "rounds") determines how many iterations BCrypt performs. Each increment **doubles** the time.

```
┌─────────────────────────────────────────────────────────────────┐
│                    COST FACTOR IMPACT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Cost │ Iterations │ Time (approx)  │ Recommendation             │
│  ─────┼────────────┼────────────────┼────────────────────────── │
│   4   │     16     │   ~1 ms        │ ❌ Too fast                │
│   8   │    256     │  ~10 ms        │ ❌ Too fast                │
│  10   │  1,024     │  ~50 ms        │ ⚠️ Minimum acceptable      │
│  11   │  2,048     │ ~100 ms        │ ✅ Reasonable              │
│  12   │  4,096     │ ~200 ms        │ ✅ Recommended             │
│  13   │  8,192     │ ~400 ms        │ ✅ Good for high security  │
│  14   │ 16,384     │ ~800 ms        │ ⚠️ May impact UX           │
│  15   │ 32,768     │ ~1.6 sec       │ ⚠️ Slow login              │
│                                                                  │
│  Rule of thumb: Target 250-500ms for interactive logins          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Choosing the Right Cost Factor

```python
import bcrypt
import time

def find_optimal_cost(target_time_ms=250):
    """Find the cost factor that takes approximately target_time_ms"""
    password = b"test_password"

    for cost in range(4, 20):
        start = time.time()
        bcrypt.hashpw(password, bcrypt.gensalt(rounds=cost))
        elapsed_ms = (time.time() - start) * 1000

        print(f"Cost {cost:2d}: {elapsed_ms:7.1f} ms")

        if elapsed_ms >= target_time_ms:
            print(f"\n✅ Recommended cost factor: {cost}")
            return cost

    return 12  # Default

# Run this on YOUR production hardware!
find_optimal_cost(250)
```

---

## How BCrypt Works Internally

```
┌─────────────────────────────────────────────────────────────────┐
│                    BCRYPT ALGORITHM                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: password, cost                                           │
│                                                                  │
│  1. Generate 128-bit random salt (or use provided)               │
│     salt = random_bytes(16)                                      │
│                                                                  │
│  2. Initialize Blowfish state with expensive key setup           │
│     state = EksBlowfishSetup(cost, salt, password)               │
│                                                                  │
│  3. Repeatedly encrypt magic string 2^cost times                 │
│     ctext = "OrpheanBeholderScryDoubt"  (24 bytes)              │
│     for i in range(2^cost):                                      │
│         ctext = Blowfish_Encrypt(state, ctext)                   │
│                                                                  │
│  4. Combine and encode                                           │
│     output = "$2b$" + cost + "$" + base64(salt) + base64(ctext) │
│                                                                  │
│  Output: 60-character string                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why "OrpheanBeholderScryDoubt"?

The magic string "OrpheanBeholderScryDoubt" is encrypted repeatedly. This is a reference to a villain in Dungeons & Dragons - the Beholder creature that has an eye attack called "Scry". It's a fun Easter egg from the cryptographers!

---

## Using BCrypt in Python

### Installation

```bash
pip install bcrypt
```

### Basic Usage

```python
import bcrypt

# ═══════════════════════════════════════════════════════════════
# HASHING A PASSWORD (during registration)
# ═══════════════════════════════════════════════════════════════

password = "my_secure_password"

# Generate salt and hash in one step
# rounds=12 is the cost factor (2^12 iterations)
hashed = bcrypt.hashpw(
    password.encode('utf-8'),  # Must be bytes
    bcrypt.gensalt(rounds=12)
)

print(f"Hash: {hashed.decode()}")
# $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.GeNaGWDl1mKPpC

# Store 'hashed' in your database


# ═══════════════════════════════════════════════════════════════
# VERIFYING A PASSWORD (during login)
# ═══════════════════════════════════════════════════════════════

# User enters password during login
entered_password = "my_secure_password"

# Retrieve hash from database
stored_hash = hashed  # (from database)

# Check if password matches
if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash):
    print("✅ Login successful!")
else:
    print("❌ Invalid password")


# ═══════════════════════════════════════════════════════════════
# WRONG PASSWORD EXAMPLE
# ═══════════════════════════════════════════════════════════════

wrong_password = "wrong_password"

if bcrypt.checkpw(wrong_password.encode('utf-8'), stored_hash):
    print("✅ Login successful!")
else:
    print("❌ Invalid password")  # This will print
```

### Production-Ready Example

```python
import bcrypt
from typing import Optional

class PasswordService:
    """Production-ready password hashing service"""

    DEFAULT_COST = 12
    MIN_COST = 10
    MAX_COST = 15

    def __init__(self, cost: int = DEFAULT_COST):
        if not self.MIN_COST <= cost <= self.MAX_COST:
            raise ValueError(f"Cost must be between {self.MIN_COST} and {self.MAX_COST}")
        self.cost = cost

    def hash_password(self, password: str) -> str:
        """
        Hash a password for storage.

        Args:
            password: Plain text password

        Returns:
            BCrypt hash string (60 characters)
        """
        if not password:
            raise ValueError("Password cannot be empty")

        if len(password) > 72:
            # BCrypt only uses first 72 bytes
            raise ValueError("Password too long (max 72 characters)")

        salt = bcrypt.gensalt(rounds=self.cost)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            password: Plain text password to verify
            hashed: BCrypt hash from database

        Returns:
            True if password matches, False otherwise
        """
        if not password or not hashed:
            return False

        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed.encode('utf-8')
            )
        except (ValueError, TypeError):
            # Invalid hash format
            return False

    def needs_rehash(self, hashed: str) -> bool:
        """
        Check if a hash was created with an older cost factor.

        Use this to upgrade hashes over time as hardware improves.
        """
        try:
            # Extract cost from hash: $2b$XX$...
            current_cost = int(hashed.split('$')[2])
            return current_cost < self.cost
        except (IndexError, ValueError):
            return True  # Invalid hash, needs rehashing


# Usage
password_service = PasswordService(cost=12)

# Registration
hashed = password_service.hash_password("user_password")
# Store in database

# Login
if password_service.verify_password("user_password", hashed):
    # Check if we should upgrade the hash
    if password_service.needs_rehash(hashed):
        new_hash = password_service.hash_password("user_password")
        # Update hash in database
    # Login successful
```

---

## BCrypt Limitations

### 1. Maximum Password Length: 72 Bytes

```python
import bcrypt

# BCrypt silently truncates passwords longer than 72 bytes!
password_72 = "a" * 72
password_73 = "a" * 72 + "b"  # The 'b' is IGNORED!

hash_72 = bcrypt.hashpw(password_72.encode(), bcrypt.gensalt())

# These will BOTH match!
print(bcrypt.checkpw(password_72.encode(), hash_72))  # True
print(bcrypt.checkpw(password_73.encode(), hash_72))  # True! (truncated)

# Solution: Pre-hash long passwords
import hashlib

def hash_long_password(password: str, salt: bytes) -> bytes:
    """Handle passwords longer than 72 bytes"""
    if len(password.encode('utf-8')) > 72:
        # Pre-hash with SHA-256, then bcrypt the result
        pre_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return bcrypt.hashpw(pre_hash.encode(), salt)
    return bcrypt.hashpw(password.encode('utf-8'), salt)
```

### 2. Not Memory-Hard (Vulnerable to GPU/ASIC Attacks)

```
┌─────────────────────────────────────────────────────────────────┐
│                    BCRYPT vs ARGON2                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BCrypt:                                                         │
│  • CPU-intensive (many iterations)                               │
│  • Low memory usage (~4 KB)                                      │
│  • Can be accelerated with specialized hardware                  │
│                                                                  │
│  Argon2 (newer alternative):                                     │
│  • CPU-intensive AND memory-intensive                            │
│  • Configurable memory usage (64+ MB typical)                    │
│  • Resistant to GPU/ASIC attacks (memory is expensive)           │
│                                                                  │
│  Recommendation:                                                 │
│  • BCrypt is still GOOD and widely supported                     │
│  • Argon2 is BETTER for new projects if available                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## BCrypt vs Other Algorithms

| Feature | BCrypt | PBKDF2 | scrypt | Argon2 |
|---------|--------|--------|--------|--------|
| Year | 1999 | 2000 | 2009 | 2015 |
| CPU-hard | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Memory-hard | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| Built-in salt | ✅ Yes | ❌ Manual | ✅ Yes | ✅ Yes |
| Max password | 72 bytes | Unlimited | Unlimited | Unlimited |
| GPU resistant | ⚠️ Partial | ❌ No | ✅ Yes | ✅ Yes |
| Recommended | ✅ Yes | ⚠️ Legacy | ✅ Yes | ✅ Best |

---

## Upgrading Hash Cost Over Time

As hardware gets faster, you should increase the cost factor. Here's how to do it transparently:

```python
import bcrypt

class PasswordManager:
    CURRENT_COST = 13  # Increase this over time

    def verify_and_upgrade(self, password: str, stored_hash: str) -> tuple[bool, Optional[str]]:
        """
        Verify password and return new hash if upgrade needed.

        Returns:
            (is_valid, new_hash_if_needed)
        """
        # Verify password
        if not bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return False, None

        # Check if hash needs upgrade
        stored_cost = int(stored_hash.split('$')[2])

        if stored_cost < self.CURRENT_COST:
            # Rehash with higher cost
            new_hash = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt(rounds=self.CURRENT_COST)
            ).decode()
            return True, new_hash

        return True, None


# Usage in login flow
pm = PasswordManager()

def login(username: str, password: str):
    user = get_user(username)
    if not user:
        return False

    is_valid, new_hash = pm.verify_and_upgrade(password, user.password_hash)

    if not is_valid:
        return False

    if new_hash:
        # Transparently upgrade hash
        update_user_hash(user.id, new_hash)
        print(f"Upgraded password hash for {username}")

    return True
```

---

## Common Mistakes

### Mistake 1: Using Low Cost Factor

```python
# ❌ WRONG - Too fast!
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=4))

# ✅ CORRECT - Use 12 or higher
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
```

### Mistake 2: Storing Salt Separately

```python
# ❌ WRONG - Salt is already in the hash!
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode(), salt)
db.save(user_id, salt, hashed)  # Don't save salt separately!

# ✅ CORRECT - Hash contains everything
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
db.save(user_id, hashed)  # Just save the hash
```

### Mistake 3: Not Handling Encoding

```python
# ❌ WRONG - Will crash
hashed = bcrypt.hashpw(password, bcrypt.gensalt())  # password must be bytes!

# ✅ CORRECT
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```

### Mistake 4: Timing Attacks in Verification

```python
# ❌ WRONG - Vulnerable to timing attacks
def verify(password, hashed):
    return bcrypt.hashpw(password.encode(), hashed) == hashed

# ✅ CORRECT - Use the built-in function (constant-time comparison)
def verify(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    BCRYPT CHEAT SHEET                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Installation:                                                   │
│  pip install bcrypt                                              │
│                                                                  │
│  Hash a password:                                                │
│  hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))  │
│                                                                  │
│  Verify a password:                                              │
│  bcrypt.checkpw(password.encode(), stored_hash)                 │
│                                                                  │
│  Cost factor:                                                    │
│  • Minimum: 10                                                   │
│  • Recommended: 12                                               │
│  • High security: 13-14                                          │
│                                                                  │
│  Output format:                                                  │
│  $2b$12$[22-char salt][31-char hash] = 60 chars total           │
│                                                                  │
│  Limitations:                                                    │
│  • Max 72-byte password                                          │
│  • Not memory-hard (consider Argon2 for new projects)            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Next**: [05_TOKENS_EXPLAINED.md](./05_TOKENS_EXPLAINED.md) — Token-based authentication

