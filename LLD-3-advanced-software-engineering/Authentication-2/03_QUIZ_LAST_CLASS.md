# Quiz: Authentication-1 Review

## Topics Covered
- Encoding vs Encryption vs Hashing
- Password Security & BCrypt
- Session-Based Authentication
- Rainbow Tables & Salting

---

## Question 1: The Fundamental Difference

What is the key difference between encoding and encryption?

**Options:**
- A) Encoding is faster than encryption
- B) Encoding is reversible by anyone; encryption requires a key to reverse
- C) Encoding is more secure than encryption
- D) There is no difference

**Answer:** B

**Explanation:**
- Encoding (like Base64) is just format conversion - anyone can decode it
- Encryption requires a secret key to decrypt
- Base64 is NOT security - it's just translation!

---

## Question 2: Password Storage

A developer stores passwords like this:
```python
stored_password = base64.b64encode(password.encode())
```

What's wrong with this approach?

**Options:**
- A) Base64 is too slow
- B) Base64 is encoding, not hashing - anyone can decode it
- C) Base64 uses too much storage
- D) Nothing wrong, this is secure

**Answer:** B

**Explanation:**
```python
# This is NOT secure!
encoded = base64.b64encode(b"password123")  # cGFzc3dvcmQxMjM=
decoded = base64.b64decode(encoded)          # password123

# Anyone can reverse it!
```

---

## Question 3: Hashing Properties

Which statement about hashing is FALSE?

**Options:**
- A) Same input always produces same output (deterministic)
- B) You can recover the original input from the hash (reversible)
- C) Small input change produces completely different hash (avalanche effect)
- D) It's a one-way function

**Answer:** B

**Explanation:**
Hashing is ONE-WAY. You cannot reverse a hash to get the original input. That's why it's used for password storage - even if the database is stolen, attackers can't recover passwords directly.

---

## Question 4: Rainbow Table Attack

What is a rainbow table attack?

**Options:**
- A) An attack that uses colorful UI to trick users
- B) A pre-computed table mapping common passwords to their hashes
- C) An attack that intercepts network traffic
- D) A brute force attack that tries random passwords

**Answer:** B

**Explanation:**
```
RAINBOW TABLE
═════════════
password     → 5f4dcc3b5aa765d61d8327deb882cf99
123456       → e10adc3949ba59abbe56e057f20f883e
qwerty       → d8578edf8458ce06fbc5bb76a58c5ca4
...millions more...

Attacker just looks up the hash in the table!
```

---

## Question 5: Salt Purpose

What does "salting" a password prevent?

**Options:**
- A) SQL injection attacks
- B) Cross-site scripting (XSS)
- C) Rainbow table attacks and identifying users with same password
- D) Brute force attacks

**Answer:** C

**Explanation:**
```
WITHOUT SALT:
  Alice: "password" → 5f4dcc3b...
  Bob:   "password" → 5f4dcc3b...  (SAME!)

WITH SALT:
  Alice: "RANDOM1" + "password" → a7b9c2d1...
  Bob:   "RANDOM2" + "password" → e3f4g5h6... (DIFFERENT!)
```

Salt makes pre-computed tables useless because each password has a unique salt.

---

## Question 6: BCrypt Advantage

Why is BCrypt preferred over SHA-256 for password hashing?

**Options:**
- A) BCrypt produces shorter hashes
- B) BCrypt is intentionally slow and has adaptive cost factor
- C) BCrypt is newer than SHA-256
- D) BCrypt doesn't require a salt

**Answer:** B

**Explanation:**
- SHA-256 is designed to be FAST (good for checksums, bad for passwords)
- BCrypt is designed to be SLOW (intentionally!)
- BCrypt's "cost factor" can be increased as computers get faster
- A cost of 12 means 2^12 = 4096 iterations

```python
# BCrypt with cost factor 12
bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
```

---

## Question 7: BCrypt Output

What information is contained in a BCrypt hash like `$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.fqfWS8YX.qoZGK`?

**Options:**
- A) Just the hash
- B) Algorithm version, cost factor, salt, and hash
- C) Only the salt and hash
- D) The original password (encrypted)

**Answer:** B

**Explanation:**
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.fqfWS8YX.qoZGK
 │   │  └──────────┬──────────┘└──────────────┬──────────────┘
 │   │             │                          │
 │   │            SALT (22 chars)            HASH (31 chars)
 │   │
 │   └── Cost factor (12 = 2^12 iterations)
 │
 └── Algorithm version (2b)
```

---

## Question 8: Session-Based Auth

In session-based authentication, what does the server store?

**Options:**
- A) The user's password
- B) Session data (user ID, login time, etc.) mapped to a session ID
- C) Nothing - it's stateless
- D) The user's JWT token

**Answer:** B

**Explanation:**
```
Server stores:
┌─────────────────────────────────────────┐
│ Session Store (Redis/Database)          │
├─────────────────────────────────────────┤
│ session_abc123 → {user_id: 42, ...}     │
│ session_xyz789 → {user_id: 15, ...}     │
└─────────────────────────────────────────┘

Client stores: Only the session ID (in a cookie)
```

---

## Question 9: Session Scaling Problem

Why might sessions be challenging when scaling to multiple servers?

**Options:**
- A) Sessions use too much bandwidth
- B) Each server has its own session store; a user's session might not exist on another server
- C) Sessions expire too quickly
- D) Sessions don't support HTTPS

**Answer:** B

**Explanation:**
```
MULTIPLE SERVERS PROBLEM
════════════════════════

           ┌── Server 1 (has session abc123)
User ────► │
 (Load     │
 Balancer) └── Server 2 (doesn't know abc123!) ❌

Solution: Shared session store (like Redis)

           ┌── Server 1 ──┐
User ────► │              ├──► Redis (all sessions)
           └── Server 2 ──┘
```

---

## Question 10: Cookie Security Flags

Which cookie flag prevents JavaScript from accessing the session cookie?

**Options:**
- A) Secure
- B) SameSite
- C) HttpOnly
- D) Path

**Answer:** C

**Explanation:**
```
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict

HttpOnly  → JavaScript cannot read (prevents XSS stealing cookies)
Secure    → Only sent over HTTPS
SameSite  → Prevents CSRF attacks
```

---

## Bonus Question: Encoding vs Encryption vs Hashing

Match each scenario to the correct technique:

| Scenario | Technique |
|----------|-----------|
| 1. Sending binary data in JSON | ? |
| 2. Storing user passwords | ? |
| 3. Protecting API keys you need to retrieve | ? |
| 4. Verifying file hasn't been tampered | ? |

**Answer:**
1. **Encoding** (Base64) - Convert binary to text
2. **Hashing** (BCrypt) - One-way, can't be reversed
3. **Encryption** (AES) - Can be decrypted with key
4. **Hashing** (SHA-256) - Verify integrity with checksum

---

## Key Takeaways

1. **Encoding ≠ Security** - Base64 is not encryption!
2. **Hashing is one-way** - You can't unhash
3. **Always salt passwords** - Defeats rainbow tables
4. **BCrypt > SHA for passwords** - Intentionally slow
5. **Sessions need shared storage** - For multiple servers
6. **Use HttpOnly cookies** - Prevent XSS attacks
