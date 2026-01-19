# Encoding vs Encryption vs Hashing

> *"They all transform data, but for completely different purposes."*

These three terms are often confused, but they serve entirely different purposes in computing and security.

---

## The ELI5 (Explain Like I'm 5) Version

### Encoding: Changing the Language

**Analogy: Translating a Letter**

Imagine you write a letter in English, but your friend only reads French. You translate it to French so they can read it.

```
┌─────────────────────────────────────────────────────────────────┐
│                         ENCODING                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Original:   "HELLO"                                            │
│                  │                                               │
│                  │  (Translate to Morse Code)                    │
│                  ▼                                               │
│   Encoded:    ".... . .-.. .-.. ---"                            │
│                  │                                               │
│                  │  (Translate back - anyone can do it!)         │
│                  ▼                                               │
│   Decoded:    "HELLO"                                            │
│                                                                  │
│   🔑 NO KEY NEEDED - anyone who knows Morse can decode it        │
│   📖 The "translation rules" are PUBLIC                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Real example with letters:**
```
Original:    H    E    L    L    O
ASCII:      72   69   76   76   79
Binary:     01001000 01000101 01001100 01001100 01001111
Base64:     SEVMTE8=
```

Anyone can reverse this. It's just a different way of writing the same thing.

---

### Encryption: Locking with a Key

**Analogy: A Locked Diary**

You write in your diary and lock it with a key. Only someone with the key can read it.

```
┌─────────────────────────────────────────────────────────────────┐
│                         ENCRYPTION                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Original:   "HELLO"                                            │
│                  │                                               │
│                  │  + 🔑 Secret Key: "KEY123"                    │
│                  │  (Lock with key)                              │
│                  ▼                                               │
│   Encrypted:  "X#9@kL!mZ"  (looks like gibberish)               │
│                  │                                               │
│                  │  + 🔑 Same Secret Key: "KEY123"               │
│                  │  (Unlock with key)                            │
│                  ▼                                               │
│   Decrypted:  "HELLO"                                            │
│                                                                  │
│   🔑 KEY REQUIRED - only key holder can decrypt                  │
│   🔒 Without the key, it's unreadable                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Simple letter example (Caesar Cipher - shift by 3):**
```
Original:    H   E   L   L   O
             ↓   ↓   ↓   ↓   ↓
            +3  +3  +3  +3  +3  (key = shift 3)
             ↓   ↓   ↓   ↓   ↓
Encrypted:   K   H   O   O   R

To decrypt: shift back by 3 (need to know the key!)
```

Without knowing the key (shift amount), you can't easily reverse it.

---

### Hashing: One-Way Fingerprint

**Analogy: A Meat Grinder**

You put a steak into a meat grinder. You get ground beef. Can you turn ground beef back into a steak? **NO!**

```
┌─────────────────────────────────────────────────────────────────┐
│                          HASHING                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Original:   "HELLO"                                            │
│                  │                                               │
│                  │  (Put through hash function)                  │
│                  ▼                                               │
│   Hash:       "2cf24dba5fb0a30e..."                             │
│                  │                                               │
│                  X  CANNOT go back!                              │
│                  │                                               │
│   Original:   ??? (impossible to recover)                        │
│                                                                  │
│   🚫 NO KEY - not reversible at all                             │
│   👆 Same input ALWAYS gives same hash                          │
│   🔄 Different input gives DIFFERENT hash                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Simple letter example (sum of positions):**
```
H=8, E=5, L=12, L=12, O=15

HELLO → 8 + 5 + 12 + 12 + 15 = 52

Hash of "HELLO" = 52

Can you figure out what word made 52?
Could be "HELLO" or "OLLEH" or "LEHLO" or thousands of others!
That's ONE-WAY!
```

---

## Comparison Table

| Aspect | Encoding | Encryption | Hashing |
|--------|----------|------------|---------|
| **Purpose** | Data format conversion | Confidentiality | Integrity verification |
| **Reversible?** | ✅ Yes, by anyone | ✅ Yes, with key | ❌ No, never |
| **Key needed?** | ❌ No | ✅ Yes | ❌ No |
| **Same input = same output?** | ✅ Yes | ❌ No (if using IV) | ✅ Yes |
| **Use case** | Data transmission | Secrets, messages | Passwords, checksums |

---

## Visual Metaphors

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENCODING = TRANSLATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   📖 English ←→ 📖 French                                       │
│                                                                  │
│   Anyone with a dictionary can translate both ways.              │
│   The "rules" are public knowledge.                              │
│                                                                  │
│   Examples: ASCII, Unicode, Base64, URL encoding                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ENCRYPTION = LOCKED BOX                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   📦🔒 Only opens with the right key                            │
│                                                                  │
│   Without the key, the contents are inaccessible.                │
│   With the key, you get the original back perfectly.             │
│                                                                  │
│   Examples: AES, RSA, ChaCha20                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    HASHING = FINGERPRINT                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   👆 A person → fingerprint (unique identifier)                 │
│                                                                  │
│   You can identify someone by their fingerprint,                 │
│   but you can't reconstruct the person FROM the fingerprint!     │
│                                                                  │
│   Examples: MD5, SHA-256, BCrypt                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## When to Use What?

```
┌─────────────────────────────────────────────────────────────────┐
│              DECISION GUIDE: ENCODING vs ENCRYPTION vs HASHING   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  "I need to send data that a system can read"                    │
│  → Use ENCODING (Base64, URL encoding)                           │
│                                                                  │
│  "I need to send a secret message only the recipient can read"   │
│  → Use ENCRYPTION (AES, RSA)                                     │
│                                                                  │
│  "I need to store a password securely"                           │
│  → Use HASHING (BCrypt, Argon2)                                  │
│                                                                  │
│  "I need to verify a file wasn't tampered with"                  │
│  → Use HASHING (SHA-256 checksum)                                │
│                                                                  │
│  "I need to send binary data in a text format (like JSON)"       │
│  → Use ENCODING (Base64)                                         │
│                                                                  │
│  "I need to protect credit card numbers in transit"              │
│  → Use ENCRYPTION (TLS/HTTPS)                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Real-World Examples

### 1. Encoding in Action

```python
import base64

# Encoding: Transform for compatibility
original = "Hello, World!"
encoded = base64.b64encode(original.encode()).decode()
print(f"Encoded: {encoded}")  # SGVsbG8sIFdvcmxkIQ==

# Decoding: Anyone can do this!
decoded = base64.b64decode(encoded).decode()
print(f"Decoded: {decoded}")  # Hello, World!
```

**Use case:** Sending binary data (like an image) in an email or JSON.

### 2. Encryption in Action

```python
from cryptography.fernet import Fernet

# Generate a key (keep this SECRET!)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
message = "Secret message"
encrypted = cipher.encrypt(message.encode())
print(f"Encrypted: {encrypted}")  # gAAAAABk... (gibberish)

# Decrypt (needs the key!)
decrypted = cipher.decrypt(encrypted).decode()
print(f"Decrypted: {decrypted}")  # Secret message

# Without the key? IMPOSSIBLE to decrypt!
```

**Use case:** Sending confidential data, storing secrets.

### 3. Hashing in Action

```python
import hashlib

# Hash a password
password = "MyPassword123"
hashed = hashlib.sha256(password.encode()).hexdigest()
print(f"Hash: {hashed}")
# a42e89... (always the same for this password)

# Can we reverse it? NO!
# We can only CHECK if a password MATCHES:
def verify_password(input_password, stored_hash):
    input_hash = hashlib.sha256(input_password.encode()).hexdigest()
    return input_hash == stored_hash

print(verify_password("MyPassword123", hashed))  # True
print(verify_password("WrongPassword", hashed))  # False
```

**Use case:** Password storage, file integrity checks.

---

## The Letter-Based ELI5 Examples

### Encoding Example: Pig Latin

```
Original:  HELLO
Rule:      Move first letter to end, add "AY"
Encoded:   ELLOHAY

Anyone who knows Pig Latin can decode:
ELLOHAY → Remove "AY", move last letter to front → HELLO
```

### Encryption Example: Caesar Cipher

```
Original:  HELLO
Key:       Shift by 3 positions
Process:   H→K, E→H, L→O, L→O, O→R
Encrypted: KHOOR

To decrypt, you MUST know the key (shift by 3):
K→H, H→E, O→L, O→L, R→O → HELLO

Without the key, attacker has to try all 25 shifts!
```

### Hashing Example: Word Sum

```
Original:  CAT
Process:   C=3, A=1, T=20 → 3+1+20 = 24
Hash:      24

Now, what word equals 24?
- CAT = 3+1+20 = 24 ✓
- TAC = 20+1+3 = 24 ✓
- ATC = 1+20+3 = 24 ✓
- X = 24 ✓

Many inputs can produce the same hash!
You CANNOT reverse it to find the original word.
```

---

## Common Mistakes

### Mistake 1: Using Encoding for Security

```python
# ❌ WRONG - Base64 is NOT encryption!
password = "secret123"
"secured" = base64.b64encode(password.encode())
# Anyone can decode this! It's not secure!

# ✅ CORRECT - Use hashing for passwords
import bcrypt
secured = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Mistake 2: Using Encryption for Passwords

```python
# ❌ WRONG - Encryption can be reversed if key is stolen
encrypted_password = encrypt(password, key)
# If attacker gets the key, all passwords are exposed!

# ✅ CORRECT - Use hashing (can't be reversed)
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Even if database is stolen, passwords are safe
```

### Mistake 3: Using Hashing for Secrets You Need to Read

```python
# ❌ WRONG - Can't unhash!
api_key = "sk_live_abc123"
stored = sha256(api_key)
# How do you get the API key back? You can't!

# ✅ CORRECT - Use encryption for secrets you need to retrieve
encrypted_key = encrypt(api_key, master_key)
# Can decrypt when needed
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHEAT SHEET                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ENCODING (Format conversion)                                    │
│  • Base64, URL encoding, ASCII, Unicode                          │
│  • Reversible by anyone                                          │
│  • NOT for security!                                             │
│                                                                  │
│  ENCRYPTION (Confidentiality)                                    │
│  • AES, RSA, ChaCha20                                           │
│  • Reversible with key only                                      │
│  • Use for: secrets, messages, data in transit                   │
│                                                                  │
│  HASHING (Integrity/Verification)                                │
│  • SHA-256, BCrypt, Argon2                                       │
│  • NOT reversible                                                │
│  • Use for: passwords, checksums, digital signatures             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Summary

| Transform | Encoding | Encryption | Hashing |
|-----------|----------|------------|---------|
| **Like...** | Translation | Locked box | Meat grinder |
| **Reverse?** | Anyone can | Key holder only | Nobody |
| **Purpose** | Compatibility | Confidentiality | Verification |
| **Key?** | No | Yes | No |

**Remember:**
- **Encoding** = changing format (not security!)
- **Encryption** = hiding with a key (reversible)
- **Hashing** = one-way fingerprint (irreversible)

---

**Next**: Return to [README.md](./README.md) for the complete learning path.

