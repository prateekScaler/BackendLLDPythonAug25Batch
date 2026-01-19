# Password Storage Evolution: A Security Journey

> *"Those who don't learn from history are doomed to have their password database leaked on the dark web."*

---

## The Problem: Why Password Storage Matters

When attackers breach a database, they get your password storage. What they can do with it depends entirely on HOW you stored passwords.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE BREACH SCENARIO                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Attacker gets database dump:                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ users table                                              │    │
│  │ ═════════════════════════════════════════════════════   │    │
│  │ id │ email              │ password_field                │    │
│  │ 1  │ alice@example.com  │ ???                           │    │
│  │ 2  │ bob@example.com    │ ???                           │    │
│  │ 3  │ ceo@company.com    │ ???                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  What's in password_field determines the damage:                 │
│                                                                  │
│  • Plaintext?     → Instant access to all accounts              │
│  • MD5?           → Cracked in minutes                          │
│  • SHA-256?       → Cracked in hours/days                       │
│  • BCrypt?        → Cracking one password takes weeks           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Evolution Timeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    PASSWORD STORAGE EVOLUTION                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Era 1: PLAINTEXT (1960s-1980s)                                 │
│  ════════════════════════════════                               │
│  password_field = "secret123"                                   │
│  Status: ☠️ CATASTROPHICALLY INSECURE                           │
│                                                                  │
│  Era 2: SIMPLE HASH (1990s)                                     │
│  ════════════════════════════════                               │
│  password_field = MD5("secret123")                              │
│  Status: ☠️ BROKEN (rainbow tables)                             │
│                                                                  │
│  Era 3: SALTED HASH (2000s)                                     │
│  ════════════════════════════════                               │
│  password_field = SHA256(salt + "secret123")                    │
│  Status: ⚠️ WEAK (GPUs crack billions/sec)                      │
│                                                                  │
│  Era 4: ADAPTIVE HASHING (2010s+)                               │
│  ════════════════════════════════                               │
│  password_field = BCrypt("secret123", cost=12)                  │
│  Status: ✅ SECURE (slow by design)                             │
│                                                                  │
│  Era 5: MEMORY-HARD (2015+)                                     │
│  ════════════════════════════════                               │
│  password_field = Argon2("secret123", memory=64MB)              │
│  Status: ✅ MOST SECURE (resists GPU/ASIC attacks)              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Era 1: Plaintext Storage (The Dark Ages)

### How It Worked

```python
# 1960s-1980s: Just store the password directly!
def register(username, password):
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)  # Stored as-is!
    )

def login(username, password):
    stored = db.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    return stored['password'] == password  # Direct comparison
```

### The Database Looked Like

```
┌────────────────────────────────────────┐
│ users table                            │
├────────────────────────────────────────┤
│ username    │ password                 │
├─────────────┼──────────────────────────┤
│ alice       │ ilovecats                │
│ bob         │ password123              │
│ ceo         │ company2024!             │
│ admin       │ admin                    │
└────────────────────────────────────────┘

☠️ Anyone with database access sees ALL passwords!
☠️ Backup tapes contain passwords!
☠️ Database admins can impersonate anyone!
```

### Real-World Disaster: Facebook (2019)

```
┌─────────────────────────────────────────────────────────────────┐
│  FACEBOOK BREACH - 2019                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  What happened: Passwords were logged in PLAINTEXT               │
│                                                                  │
│  Affected: 600 MILLION users                                     │
│                                                                  │
│  How long: Passwords exposed since 2012 (7 years!)               │
│                                                                  │
│  Who could see: 20,000+ Facebook employees                       │
│                                                                  │
│  Source: Internal logging system stored passwords                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Era 2: Simple Hashing (MD5/SHA-1)

### The Idea

"Don't store the password - store a one-way hash!"

```python
import hashlib

def register(username, password):
    # Hash the password - can't be reversed!
    hashed = hashlib.md5(password.encode()).hexdigest()
    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, hashed)
    )

def login(username, password):
    stored_hash = db.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    input_hash = hashlib.md5(password.encode()).hexdigest()
    return stored_hash['password_hash'] == input_hash
```

### The Database Now Looks Like

```
┌────────────────────────────────────────────────────────────┐
│ users table                                                │
├────────────────────────────────────────────────────────────┤
│ username    │ password_hash                                │
├─────────────┼──────────────────────────────────────────────┤
│ alice       │ 5f4dcc3b5aa765d61d8327deb882cf99            │  (password)
│ bob         │ 482c811da5d5b4bc6d497ffa98491e38            │  (password123)
│ charlie     │ 5f4dcc3b5aa765d61d8327deb882cf99            │  (password)
└────────────────────────────────────────────────────────────┘

⚠️ Notice: alice and charlie have the SAME hash!
   This reveals they use the same password.
```

### The Attack: Rainbow Tables

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAINBOW TABLE ATTACK                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Attacker pre-computes hashes for common passwords:              │
│                                                                  │
│  Rainbow Table (pre-computed):                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  password          │ MD5 hash                            │   │
│  │  password          │ 5f4dcc3b5aa765d61d8327deb882cf99    │   │
│  │  123456            │ e10adc3949ba59abbe56e057f20f883e    │   │
│  │  qwerty            │ d8578edf8458ce06fbc5bb76a58c5ca4    │   │
│  │  letmein           │ 0d107d09f5bbe40cade3de5c71e9e9b7    │   │
│  │  ... millions more ...                                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Attack:                                                         │
│  1. Get hash: 5f4dcc3b5aa765d61d8327deb882cf99                  │
│  2. Look up in rainbow table                                     │
│  3. Found! Password is "password"                                │
│                                                                  │
│  Time: INSTANT (just a lookup!)                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Live Demo: How Fast MD5 Cracks

```python
# examples/password_hashing_demo.py shows this live!

import hashlib
import time

# Common passwords to try
common_passwords = [
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "abc123", "monkey", "master", "dragon",
    "111111", "baseball", "iloveyou", "trustno1", "sunshine"
]

# Suppose we found this hash in a breached database
target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"  # MD5 of "password"

start = time.time()
for pwd in common_passwords:
    if hashlib.md5(pwd.encode()).hexdigest() == target_hash:
        print(f"CRACKED! Password is: {pwd}")
        break
elapsed = time.time() - start

print(f"Time to crack: {elapsed:.6f} seconds")
# Output: Time to crack: 0.000023 seconds
```

### Real-World Disaster: LinkedIn (2012)

```
┌─────────────────────────────────────────────────────────────────┐
│  LINKEDIN BREACH - 2012                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Storage method: SHA-1 (no salt!)                                │
│                                                                  │
│  Affected: 117 MILLION passwords                                 │
│                                                                  │
│  Cracking results:                                               │
│  • 90% cracked within days using rainbow tables                  │
│  • Remaining 10% cracked within weeks                            │
│                                                                  │
│  Most common passwords found:                                    │
│  1. 123456 (753,305 users)                                      │
│  2. linkedin (172,523 users)                                     │
│  3. password (144,458 users)                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Era 3: Salted Hashing

### The Solution to Rainbow Tables

```python
import hashlib
import os

def register(username, password):
    # Generate unique random salt for THIS user
    salt = os.urandom(16).hex()  # 32 character hex string

    # Hash password WITH salt
    salted = salt + password
    hashed = hashlib.sha256(salted.encode()).hexdigest()

    db.execute(
        "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
        (username, salt, hashed)
    )

def login(username, password):
    row = db.execute(
        "SELECT salt, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    # Hash input with stored salt
    salted = row['salt'] + password
    input_hash = hashlib.sha256(salted.encode()).hexdigest()

    return row['password_hash'] == input_hash
```

### The Database Now Looks Like

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ users table                                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ username │ salt                             │ password_hash                 │
├──────────┼──────────────────────────────────┼───────────────────────────────┤
│ alice    │ a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 │ 8d7e...completely different   │
│ bob      │ x9y8z7w6v5u4t3s2r1q0p9o8n7m6l5k4 │ 3f2a...also different         │
│ charlie  │ q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6 │ 9c4b...unique!                │
└─────────────────────────────────────────────────────────────────────────────┘

✅ Even if alice and charlie have the same password,
   their hashes are DIFFERENT because of unique salts!

✅ Rainbow tables are USELESS - attacker would need a
   separate rainbow table for each salt (impossible!)
```

### Why Salt Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOW SALT DEFEATS RAINBOW TABLES               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WITHOUT SALT:                                                   │
│  password → SHA256 → abc123def456...                             │
│  password → SHA256 → abc123def456... (same hash!)               │
│                                                                  │
│  Attacker can pre-compute: "password" → abc123def456...          │
│  Then look up any hash instantly.                                │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  WITH SALT:                                                      │
│  salt1 + password → SHA256 → xyz789ghi012...                     │
│  salt2 + password → SHA256 → mno345pqr678... (different!)       │
│                                                                  │
│  Attacker would need to pre-compute:                             │
│  • "salt1password", "salt1password1", "salt1password2"...        │
│  • "salt2password", "salt2password1", "salt2password2"...        │
│  • For EVERY possible salt × EVERY possible password             │
│                                                                  │
│  With 16-byte salt = 2^128 possible salts                        │
│  Rainbow table size would be: IMPOSSIBLE                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The Remaining Problem: SPEED

```python
# SHA-256 is TOO FAST for password hashing!

import hashlib
import time

password = "password123"
iterations = 1_000_000

start = time.time()
for _ in range(iterations):
    hashlib.sha256(password.encode()).hexdigest()
elapsed = time.time() - start

print(f"SHA-256: {iterations:,} hashes in {elapsed:.2f} seconds")
print(f"Rate: {iterations/elapsed:,.0f} hashes/second")

# Output:
# SHA-256: 1,000,000 hashes in 0.42 seconds
# Rate: 2,380,952 hashes/second

# With GPU: 10+ BILLION hashes/second!
```

### The Attack: Brute Force with GPUs

```
┌─────────────────────────────────────────────────────────────────┐
│                    GPU CRACKING POWER (2024)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Algorithm      │ Hashes per Second (RTX 4090)                   │
│  ══════════════════════════════════════════════════════════════ │
│  MD5            │ 164 BILLION/sec                                │
│  SHA-1          │ 27 BILLION/sec                                 │
│  SHA-256        │ 22 BILLION/sec                                 │
│  BCrypt (cost 5)│ 184,000/sec                                    │  ← 120,000x slower!
│  BCrypt (cost 12)│ 1,400/sec                                     │  ← 15 MILLION x slower!
│  Argon2         │ ~1,000/sec                                     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Time to crack 8-character password (lowercase + digits):        │
│                                                                  │
│  SHA-256:  2.8 trillion combinations ÷ 22B/sec = 2 minutes       │
│  BCrypt:   2.8 trillion combinations ÷ 1.4K/sec = 63 YEARS       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Era 4: Adaptive Hashing (BCrypt)

### The Key Insight

**"Make hashing intentionally SLOW"**

```python
import bcrypt
import time

password = "password123"

# BCrypt - intentionally slow
start = time.time()
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
elapsed = time.time() - start

print(f"BCrypt (cost 12): {elapsed:.3f} seconds per hash")
# Output: BCrypt (cost 12): 0.284 seconds per hash

# Compare: SHA-256 does 2+ million hashes in that same time!
```

### Why Slow Is Good

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHY SLOW = SECURE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  For LEGITIMATE users:                                           │
│  • Login takes 0.3 seconds extra                                 │
│  • Barely noticeable                                             │
│  • Happens once per session                                      │
│                                                                  │
│  For ATTACKERS:                                                  │
│  • Must hash EVERY guess                                         │
│  • 0.3 seconds × millions of guesses = YEARS                    │
│  • GPU speedup is limited by algorithm design                    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Cracking "password123" (a weak password):                       │
│                                                                  │
│  SHA-256:  Found in top 1000 list → cracked in 0.0001 seconds   │
│  BCrypt:   Found in top 1000 list → cracked in 5 minutes        │
│                                                                  │
│  Cracking "Tr0ub4dor&3" (a medium password):                     │
│                                                                  │
│  SHA-256:  ~10 billion guesses → cracked in 1 hour              │
│  BCrypt:   ~10 billion guesses → cracked in 226 YEARS           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Comparison: All Methods

| Method | Speed | Salt | Adaptive | Security | Use Today? |
|--------|-------|------|----------|----------|------------|
| Plaintext | N/A | No | No | ☠️ None | ❌ NEVER |
| MD5 | 164B/sec | No | No | ☠️ Broken | ❌ NEVER |
| SHA-1 | 27B/sec | No | No | ☠️ Broken | ❌ NEVER |
| SHA-256 | 22B/sec | Manual | No | ⚠️ Weak | ❌ Not for passwords |
| SHA-256 + salt | 22B/sec | Yes | No | ⚠️ Weak | ❌ Not for passwords |
| **BCrypt** | ~1K/sec | Built-in | Yes | ✅ Good | ✅ YES |
| **Argon2** | ~1K/sec | Built-in | Yes | ✅ Best | ✅ YES (preferred) |

---

## The Security Flaw Demo

Run `examples/password_hashing_demo.py` to see these attacks live:

```bash
cd examples
python password_hashing_demo.py
```

You'll see:
1. How fast MD5 gets cracked
2. How salting helps (but not enough)
3. Why BCrypt is orders of magnitude harder to crack
4. Live timing comparisons

---

## Key Takeaways

```
┌─────────────────────────────────────────────────────────────────┐
│                    REMEMBER THESE RULES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ NEVER store plaintext passwords                              │
│                                                                  │
│  ❌ NEVER use MD5 or SHA for passwords                           │
│     (They're for checksums, not security!)                       │
│                                                                  │
│  ❌ NEVER use unsalted hashes                                    │
│                                                                  │
│  ❌ NEVER roll your own password hashing                         │
│                                                                  │
│  ✅ ALWAYS use BCrypt or Argon2                                  │
│                                                                  │
│  ✅ ALWAYS use a high work factor (BCrypt ≥ 12)                  │
│                                                                  │
│  ✅ ALWAYS use a library (don't implement yourself!)             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Next**: [04_BCRYPT_DEEP_DIVE.md](./04_BCRYPT_DEEP_DIVE.md) — Understanding BCrypt inside out

