# Authentication - Part 1: Auth vs Auth, Tokens & BCrypt

## Welcome to the World of Identity Verification

> *"In the ancient world, a king's seal was his identity. In the digital world, your password is your seal."*

---

## What You'll Learn

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION JOURNEY                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. HISTORY        Why humans needed to prove identity          │
│      📜             From clay seals to digital signatures        │
│                                                                  │
│   2. AUTH vs AUTH   Authentication ≠ Authorization               │
│      🔐 vs 🎫       "Who are you?" vs "What can you do?"         │
│                                                                  │
│   3. PASSWORDS      The evolution of storing secrets             │
│      🔑             Why plaintext → MD5 → SHA → BCrypt           │
│                                                                  │
│   4. BCRYPT         The gold standard for password hashing       │
│      🛡️             Salts, work factors, and adaptive security   │
│                                                                  │
│   5. TOKENS         Stateless authentication for modern apps     │
│      🎟️             Sessions, JWTs, and bearer tokens            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Learning Path

| Order | File | Description | Time |
|-------|------|-------------|------|
| 1 | `01_HISTORY_OF_AUTHENTICATION.md` | Fascinating history of identity verification | 10 min |
| 2 | `02_AUTH_VS_AUTH.md` | Authentication vs Authorization deep dive | 15 min |
| 3 | `03_PASSWORD_STORAGE_EVOLUTION.md` | Why your password storage matters (with live demos!) | 20 min |
| 4 | `04_BCRYPT_DEEP_DIVE.md` | Understanding BCrypt inside out | 15 min |
| 5 | `05_TOKENS_EXPLAINED.md` | Token-based authentication explained | 15 min |

---

## Interactive Guide

```
┌─────────────────────────────────────────────────────────────────┐
│  📚 VISUAL LEARNING: Open auth_guide/index.html                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  A beautiful light-mode interactive guide with:                  │
│  • Visual timelines and diagrams                                 │
│  • Code examples with syntax highlighting                        │
│  • Interactive quizzes                                           │
│  • Security vulnerability demonstrations                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hands-On Examples

| File | What It Demonstrates |
|------|---------------------|
| `examples/password_hashing_demo.py` | Live demo of password security flaws |
| `examples/token_example.py` | JWT creation and verification |
| `examples/timing_attack_demo.py` | Why string comparison matters |

### Run the Examples

```bash
# Install dependencies
pip install bcrypt pyjwt passlib argon2-cffi

# Run the password demo (see security flaws live!)
python examples/password_hashing_demo.py

# Run the token example
python examples/token_example.py
```

---

## Diagrams

All diagrams are in `diagrams/` folder using Mermaid syntax. View them on:
- GitHub (renders automatically)
- VS Code with Mermaid extension
- https://mermaid.live (paste the code)

---

## Quick Reference

### The Three A's of Security

| Term | Question | Example |
|------|----------|---------|
| **Authentication** | Who are you? | Login with username/password |
| **Authorization** | What can you do? | Admin can delete, User can only view |
| **Accounting** | What did you do? | Audit logs, access history |

### Password Hashing Evolution

| Era | Method | Status | Problem |
|-----|--------|--------|---------|
| 1990s | Plaintext | ❌ Dangerous | Exposed if database leaked |
| 2000s | MD5 | ❌ Broken | Rainbow tables, fast to crack |
| 2000s | SHA-1/256 | ⚠️ Weak | Still too fast, no salt by default |
| 2010s | **BCrypt** | ✅ Good | Slow by design, built-in salt |
| 2015+ | **Argon2** | ✅ Best | Memory-hard, won Password Hashing Competition |

---

## Key Takeaways Preview

```
🔐 AUTHENTICATION answers: "Who are you?"
🎫 AUTHORIZATION answers: "What are you allowed to do?"

🔑 Never store passwords in plaintext
🔑 Never use MD5 or SHA alone for passwords
🔑 BCrypt/Argon2 are slow BY DESIGN (that's the feature!)
🔑 Always use unique salts per password
🔑 Tokens enable stateless authentication
```

---

## Prerequisites

- Basic Python knowledge
- Understanding of HTTP basics
- Curiosity about security!

---

## Real-World Breaches (We'll Analyze These)

| Year | Company | What Happened | Passwords Exposed |
|------|---------|---------------|-------------------|
| 2012 | LinkedIn | SHA-1 unsalted | 117 million |
| 2013 | Adobe | 3DES (not hashing!) | 153 million |
| 2016 | Yahoo | MD5 | 3 billion |
| 2019 | Facebook | Plaintext logs | 600 million |

*We'll understand WHY these happened and how proper hashing would have helped.*

---

Let's begin! Start with [01_HISTORY_OF_AUTHENTICATION.md](./01_HISTORY_OF_AUTHENTICATION.md)
