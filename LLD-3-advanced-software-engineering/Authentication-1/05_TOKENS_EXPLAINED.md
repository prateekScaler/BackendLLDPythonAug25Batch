# Tokens Explained: From Sessions to JWTs

> *"A token is like a movie ticket - it proves you paid, without the theater needing to check with the box office every time."*

---

## The Problem: Stateful vs Stateless

### Traditional Sessions (Stateful)

```
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION-BASED AUTH                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Client                          Server                          │
│  ══════                          ══════                          │
│                                                                  │
│  1. Login ─────────────────────► Validate credentials            │
│     (username, password)         Create session in DB            │
│                                  ┌──────────────────────┐        │
│                                  │ sessions table       │        │
│                                  │ sid: abc123          │        │
│                                  │ user_id: 42          │        │
│                                  │ expires: 2024-01-15  │        │
│                                  └──────────────────────┘        │
│                                          │                       │
│  ◄───────────────────────────────────────┘                       │
│  Set-Cookie: session_id=abc123                                   │
│                                                                  │
│  2. Every Request ─────────────► Look up session in DB           │
│     Cookie: session_id=abc123    Is abc123 valid?                │
│                                  Get user_id from session        │
│     ◄────────────────────────────                               │
│     Response                                                     │
│                                                                  │
│  Problem: Database lookup on EVERY request!                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Token-Based Auth (Stateless)

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN-BASED AUTH                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Client                          Server                          │
│  ══════                          ══════                          │
│                                                                  │
│  1. Login ─────────────────────► Validate credentials            │
│     (username, password)         Create signed token             │
│                                  (NO database write!)            │
│                                          │                       │
│  ◄───────────────────────────────────────┘                       │
│  { "token": "eyJhbGc..." }                                       │
│                                                                  │
│  2. Every Request ─────────────► Verify token signature          │
│     Authorization: Bearer eyJ...  Decode user info from token    │
│                                  (NO database lookup!)           │
│     ◄────────────────────────────                               │
│     Response                                                     │
│                                                                  │
│  Benefit: Server doesn't need to store anything!                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Comparison: Sessions vs Tokens

| Aspect | Sessions | Tokens (JWT) |
|--------|----------|--------------|
| **Storage** | Server-side (DB/Redis) | Client-side |
| **Scalability** | Requires shared session store | No shared state needed |
| **Performance** | DB lookup per request | CPU-only verification |
| **Revocation** | Easy (delete from DB) | Harder (need blacklist) |
| **Size** | Small cookie (~20 bytes) | Larger (~500+ bytes) |
| **Cross-domain** | Difficult (cookie rules) | Easy (just send header) |
| **Mobile apps** | Cookie handling is tricky | Native support |

---

## What Is a JWT?

**JWT = JSON Web Token**

A JWT is a self-contained token that carries information (claims) and a cryptographic signature.

```
┌─────────────────────────────────────────────────────────────────┐
│                    JWT STRUCTURE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                           │
│  eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4i    │
│  OnRydWUsImlhdCI6MTUxNjIzOTAyMn0.                                │
│  POstGetfAytaZS82wHcjoTyoqhMyxXiWdR7Nn7A28cM                     │
│                                                                  │
│  └───────────┬───────────┘└──────────────┬──────────────┘└──┬──┘ │
│           HEADER                      PAYLOAD            SIGNATURE│
│                                                                  │
│  Each part is Base64URL encoded and separated by dots (.)        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The Three Parts

#### 1. Header
```json
{
  "alg": "HS256",    // Algorithm used for signature
  "typ": "JWT"       // Type of token
}
```

#### 2. Payload (Claims)
```json
{
  "sub": "1234567890",       // Subject (user ID)
  "name": "John Doe",        // Custom claim
  "admin": true,             // Custom claim
  "iat": 1516239022,         // Issued at (timestamp)
  "exp": 1516242622          // Expiration (timestamp)
}
```

#### 3. Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

---

## Standard JWT Claims

| Claim | Name | Description |
|-------|------|-------------|
| `iss` | Issuer | Who created the token |
| `sub` | Subject | Who the token is about (usually user ID) |
| `aud` | Audience | Who the token is intended for |
| `exp` | Expiration | When the token expires (Unix timestamp) |
| `nbf` | Not Before | Token not valid before this time |
| `iat` | Issued At | When the token was created |
| `jti` | JWT ID | Unique identifier for the token |

---

## JWT in Python

### Installation

```bash
pip install pyjwt
```

### Creating and Verifying JWTs

```python
import jwt
import datetime
from typing import Optional

SECRET_KEY = "your-256-bit-secret"  # In production: use env variable!
ALGORITHM = "HS256"


# ═══════════════════════════════════════════════════════════════
# CREATING A TOKEN (after successful login)
# ═══════════════════════════════════════════════════════════════

def create_access_token(user_id: int, role: str, expires_minutes: int = 30) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: The user's ID
        role: The user's role (for authorization)
        expires_minutes: Token validity period

    Returns:
        Encoded JWT string
    """
    now = datetime.datetime.utcnow()
    payload = {
        # Standard claims
        "sub": str(user_id),              # Subject
        "iat": now,                        # Issued at
        "exp": now + datetime.timedelta(minutes=expires_minutes),  # Expiration

        # Custom claims
        "role": role,
        "type": "access"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ═══════════════════════════════════════════════════════════════
# VERIFYING A TOKEN (on every protected request)
# ═══════════════════════════════════════════════════════════════

def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT.

    Returns:
        Decoded payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None

    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# USAGE EXAMPLE
# ═══════════════════════════════════════════════════════════════

# After successful login
token = create_access_token(user_id=42, role="admin")
print(f"Token: {token}")

# On subsequent requests
payload = verify_access_token(token)
if payload:
    print(f"User ID: {payload['sub']}")
    print(f"Role: {payload['role']}")
    print(f"Expires: {datetime.datetime.fromtimestamp(payload['exp'])}")
else:
    print("Invalid or expired token")
```

---

## JWT Security: What Can Go Wrong

### Vulnerability 1: Algorithm Confusion Attack

```python
# ❌ VULNERABLE - Accepts any algorithm
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256", "none"])

# Attacker can create token with alg="none" (no signature!)

# ✅ SECURE - Explicitly specify allowed algorithms
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

### Vulnerability 2: Weak Secret Key

```python
# ❌ VULNERABLE - Guessable secret
SECRET_KEY = "secret"

# ❌ VULNERABLE - Too short
SECRET_KEY = "abc123"

# ✅ SECURE - Long, random secret
import secrets
SECRET_KEY = secrets.token_hex(32)  # 256 bits
# Example: "8f4b3c2a1d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3"
```

### Vulnerability 3: Storing Sensitive Data in Payload

```python
# ❌ WRONG - JWT payload is NOT encrypted, just encoded!
payload = {
    "sub": "123",
    "credit_card": "4111-1111-1111-1111",  # Anyone can decode this!
    "ssn": "123-45-6789"
}

# Proof that anyone can read it:
import base64
token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMiLCJjcmVkaXRfY2FyZCI6IjQxMTEtMTExMS0xMTExLTExMTEifQ.signature"
payload_part = token.split('.')[1]
decoded = base64.urlsafe_b64decode(payload_part + '==')
print(decoded)  # Shows ALL the data!

# ✅ CORRECT - Only store non-sensitive identifiers
payload = {
    "sub": "123",
    "role": "user"
}
```

---

## Access Tokens vs Refresh Tokens

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN TYPES                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ACCESS TOKEN                    REFRESH TOKEN                   │
│  ════════════                    ═════════════                   │
│                                                                  │
│  Purpose: Access protected       Purpose: Get new access         │
│           resources                       tokens                 │
│                                                                  │
│  Lifetime: Short (15-60 min)     Lifetime: Long (days/weeks)     │
│                                                                  │
│  Stored: Memory/sessionStorage   Stored: httpOnly cookie         │
│                                          or secure storage       │
│                                                                  │
│  Sent: Authorization header      Sent: Only to /refresh endpoint │
│                                                                  │
│  If stolen: Limited damage       If stolen: Can get new tokens   │
│             (expires quickly)               (more serious)       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The Refresh Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    REFRESH TOKEN FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Login ──────────────────────► Returns:                       │
│                                   - access_token (15 min)        │
│                                   - refresh_token (7 days)       │
│                                                                  │
│  2. API Calls ──────────────────► Use access_token               │
│     (for 15 minutes)              Authorization: Bearer <access> │
│                                                                  │
│  3. Access token expires!                                        │
│     API returns 401                                              │
│                                                                  │
│  4. Client calls /refresh ──────► Send refresh_token             │
│                                   Server validates               │
│                                   Returns NEW access_token       │
│                                                                  │
│  5. Continue API calls with new access token                     │
│                                                                  │
│  User stays logged in for 7 days without re-entering password!   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
import jwt
import datetime
import secrets
from typing import Tuple

SECRET_KEY = "your-secret-key"
REFRESH_SECRET = "different-secret-for-refresh"

def create_token_pair(user_id: int) -> Tuple[str, str]:
    """Create both access and refresh tokens"""
    now = datetime.datetime.utcnow()

    # Access token - short lived
    access_payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": now + datetime.timedelta(minutes=15)
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")

    # Refresh token - long lived
    refresh_payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": now + datetime.timedelta(days=7),
        "jti": secrets.token_hex(16)  # Unique ID for revocation
    }
    refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET, algorithm="HS256")

    return access_token, refresh_token


def refresh_access_token(refresh_token: str) -> str:
    """Get new access token using refresh token"""
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])

        if payload.get("type") != "refresh":
            raise ValueError("Not a refresh token")

        # Optional: Check if refresh token is blacklisted
        # if is_token_revoked(payload['jti']):
        #     raise ValueError("Token has been revoked")

        # Create new access token
        user_id = int(payload["sub"])
        access_payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        return jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")

    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid refresh token: {e}")
```

---

## Token Revocation Strategies

Since JWTs are stateless, revoking them is tricky:

```
┌─────────────────────────────────────────────────────────────────┐
│                    REVOCATION STRATEGIES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. SHORT EXPIRATION (Recommended for access tokens)             │
│     • Set exp to 15-30 minutes                                   │
│     • Stolen token is only valid briefly                         │
│     • Use refresh tokens for longer sessions                     │
│                                                                  │
│  2. TOKEN BLACKLIST                                              │
│     • Store revoked token IDs in Redis/DB                        │
│     • Check blacklist on each request                            │
│     • Defeats "stateless" benefit, but necessary sometimes       │
│                                                                  │
│  3. TOKEN VERSIONING                                             │
│     • Store "token_version" in user record                       │
│     • Include version in token                                   │
│     • Increment version to invalidate all tokens                 │
│                                                                  │
│  4. REFRESH TOKEN ROTATION                                       │
│     • Issue new refresh token with each refresh                  │
│     • Old refresh token becomes invalid                          │
│     • Detect token reuse (indicates theft)                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## JWT vs Opaque Tokens

| Aspect | JWT | Opaque Token |
|--------|-----|--------------|
| Content | Contains data (claims) | Random string |
| Validation | Self-contained (check signature) | Requires lookup |
| Size | Large (~500+ bytes) | Small (~32 bytes) |
| Revocation | Difficult | Easy (delete from DB) |
| Debugging | Easy (decode and inspect) | Requires DB query |
| Use case | Microservices, APIs | Simple apps, sensitive data |

```python
# JWT - self-contained
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature"

# Opaque token - just a reference
opaque_token = "a3f4b2c1d8e9f0a1b2c3d4e5f6a7b8c9"
# Server looks this up: SELECT user_id FROM tokens WHERE token = 'a3f4b2c1...'
```

---

## Best Practices

```
┌─────────────────────────────────────────────────────────────────┐
│                    JWT BEST PRACTICES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ Use strong secrets (256+ bits)                               │
│  ✅ Set reasonable expiration times                              │
│  ✅ Use HTTPS always                                             │
│  ✅ Validate all claims on every request                         │
│  ✅ Store tokens securely (httpOnly cookies or secure storage)   │
│  ✅ Use different secrets for access vs refresh tokens           │
│  ✅ Implement token refresh flow                                 │
│                                                                  │
│  ❌ Don't store sensitive data in JWT payload                    │
│  ❌ Don't use weak/guessable secrets                             │
│  ❌ Don't accept "none" algorithm                                │
│  ❌ Don't store tokens in localStorage (XSS vulnerable)          │
│  ❌ Don't use JWTs for session management if you need revocation │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOKEN CHEAT SHEET                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  JWT Structure:                                                  │
│  header.payload.signature                                        │
│                                                                  │
│  Create token:                                                   │
│  jwt.encode(payload, secret, algorithm="HS256")                 │
│                                                                  │
│  Verify token:                                                   │
│  jwt.decode(token, secret, algorithms=["HS256"])                │
│                                                                  │
│  Standard claims:                                                │
│  • sub (subject)     • iat (issued at)                          │
│  • exp (expiration)  • iss (issuer)                             │
│                                                                  │
│  Token lifetimes:                                                │
│  • Access: 15-60 minutes                                         │
│  • Refresh: 1-30 days                                            │
│                                                                  │
│  Send in header:                                                 │
│  Authorization: Bearer <token>                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Summary

Tokens provide a stateless way to handle authentication, perfect for:
- Distributed systems / microservices
- Mobile applications
- Single Page Applications (SPAs)
- Cross-domain authentication

But remember: JWTs are not encrypted (only signed), so never put sensitive data in them!

---

**End of Authentication Part 1**

For Part 2, we'll cover:
- OAuth 2.0 and OpenID Connect
- Multi-factor Authentication
- Passwordless Authentication
- Security Headers and CSRF Protection

