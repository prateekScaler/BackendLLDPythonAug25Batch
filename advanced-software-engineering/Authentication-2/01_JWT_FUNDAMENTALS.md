# JWT (JSON Web Tokens) Fundamentals

## What is JWT?

JWT (JSON Web Token) is an open standard (RFC 7519) for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed.

## Why JWT? The Problem with Sessions

```
SESSION-BASED (Stateful)
═══════════════════════

Browser          Server           Session Store (Redis)
   │                │                    │
   │── Login ──────►│                    │
   │                │── Create session ─►│
   │                │◄── session_id ─────│
   │◄── Cookie ─────│                    │
   │                │                    │
   │── Request ────►│                    │
   │  + Cookie      │── Lookup ─────────►│
   │                │◄── User data ──────│
   │◄── Response ───│                    │

Problems:
1. Server must store ALL active sessions
2. Multiple servers need shared session store
3. Session lookup on EVERY request
```

```
TOKEN-BASED (Stateless)
═══════════════════════

Browser          Server
   │                │
   │── Login ──────►│
   │                │  Generate JWT (signed)
   │◄── JWT token ──│
   │                │
   │── Request ────►│
   │  + JWT token   │  Verify signature
   │                │  (No DB lookup!)
   │◄── Response ───│

Benefits:
1. Server stores NOTHING
2. No shared session store needed
3. Token contains all user info
4. Scales horizontally with ease
```

## JWT Structure

A JWT consists of three parts separated by dots (`.`):

```
xxxxx.yyyyy.zzzzz
  │      │      │
  │      │      └── SIGNATURE
  │      └── PAYLOAD
  └── HEADER
```

### 1. Header
```json
{
  "alg": "HS256",    // Algorithm used for signing
  "typ": "JWT"       // Token type
}
```

### 2. Payload (Claims)
```json
{
  "sub": "1234567890",     // Subject (user ID)
  "name": "John Doe",       // Custom claim
  "role": "admin",          // Custom claim
  "iat": 1516239022,        // Issued at (timestamp)
  "exp": 1516242622         // Expiration (timestamp)
}
```

### 3. Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

## Standard Claims (Registered Claims)

| Claim | Name | Description |
|-------|------|-------------|
| `iss` | Issuer | Who created the token |
| `sub` | Subject | Who the token is about (usually user ID) |
| `aud` | Audience | Who the token is for |
| `exp` | Expiration | When the token expires |
| `nbf` | Not Before | Token not valid before this time |
| `iat` | Issued At | When the token was created |
| `jti` | JWT ID | Unique identifier for the token |

## How JWT Verification Works

```
TOKEN VERIFICATION
══════════════════

Received Token: eyJhbGc.eyJzdWI.signature
                   │        │        │
                   ▼        ▼        │
              [Header] [Payload]     │
                   │        │        │
                   └────┬───┘        │
                        │            │
                        ▼            │
              base64(header) + "." + │
              base64(payload)        │
                        │            │
                        ▼            │
              HMAC-SHA256(data, secret)
                        │            │
                        ▼            ▼
                [Computed Sig] == [Received Sig]?
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
           ✅ VALID          ❌ INVALID
         (Trust payload)    (Reject token)
```

## Python Implementation

### Creating a JWT
```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # Keep this secure!

def create_token(user_id, role):
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

### Verifying a JWT
```python
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
```

## Security Considerations

### 1. Never Put Sensitive Data in Payload
```
❌ WRONG:
{
  "password": "secret123",
  "credit_card": "4111-1111-1111-1111"
}

✅ RIGHT:
{
  "sub": "user_123",
  "role": "customer"
}
```

The payload is only Base64 encoded, NOT encrypted!

### 2. Always Verify the Algorithm
```python
# ❌ VULNERABLE - accepts any algorithm including "none"
jwt.decode(token, SECRET_KEY)

# ✅ SAFE - explicitly specify allowed algorithms
jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

### 3. Use Short Expiration Times
- Access tokens: 15-60 minutes
- Refresh tokens: 1-30 days

### 4. Use HTTPS Always
Tokens sent over HTTP can be intercepted!

## Common JWT Attacks

| Attack | Description | Prevention |
|--------|-------------|------------|
| Algorithm None | Setting `alg: none` to bypass signature | Always specify allowed algorithms |
| Secret Brute Force | Guessing weak secrets | Use strong secrets (256+ bits) |
| Token Stealing | XSS stealing tokens from localStorage | Use httpOnly cookies |
| No Expiration | Tokens valid forever | Always set `exp` claim |

## When to Use JWT vs Sessions

| Use Case | Recommended |
|----------|-------------|
| Traditional web app | Sessions |
| Mobile app | JWT |
| Microservices | JWT |
| Single-page app (SPA) | JWT |
| Third-party API | JWT |
| Need instant revocation | Sessions |
