# JWT (JSON Web Tokens) - Complete Guide

## Before JWT: A History of Tokens

### Common Misconceptions About "Tokens"

The word "token" causes confusion! Let's clarify:

| Misconception | Reality |
|---------------|---------|
| "Token = JWT" | NO! JWT is just ONE TYPE of token. The word "token" is generic - like saying "vehicle" instead of "car" |
| "Tokens are encrypted" | NO! Most tokens (including JWT) are NOT encrypted. They're **signed**, not encrypted. Anyone can read the contents! |
| "Tokens = Secure by default" | NO! Tokens can be stolen, just like session IDs. They need proper handling (HTTPS, secure storage, expiry) |

### Types of Tokens Used Before JWT

| Token Type | Era | How It Works | Problems |
|------------|-----|--------------|----------|
| **Opaque Tokens** | 1990s+ | Random string (like session ID). Server looks up in DB to validate | Requires DB lookup every time. Same as sessions basically! |
| **SAML Tokens** | 2002 | XML-based tokens for enterprise SSO. Self-contained with signatures | HUGE (XML is verbose), complex to implement, not web-friendly |
| **Simple Web Tokens (SWT)** | 2009 | URL-encoded key-value pairs with HMAC signature | No standard structure, limited to symmetric signing |
| **JWT** | 2010-2015 | JSON-based, Base64 encoded, supports symmetric & asymmetric signing | Became the standard! Compact, web-friendly, well-supported |

### SAML vs JWT: Why JWT Won

```
SAML TOKEN (Actual Example - Simplified)
════════════════════════════════════════

<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    Version="2.0" IssueInstant="2024-01-15T10:00:00Z">
  <saml:Issuer>https://idp.company.com</saml:Issuer>
  <saml:Subject>
    <saml:NameID>sumit@company.com</saml:NameID>
  </saml:Subject>
  <saml:Conditions NotBefore="2024-01-15T10:00:00Z"
                   NotOnOrAfter="2024-01-15T11:00:00Z">
  </saml:Conditions>
  <ds:Signature>...hundreds of bytes...</ds:Signature>
</saml:Assertion>

Size: ~2000+ bytes


JWT TOKEN (Same Information)
════════════════════════════

eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2lkcC5jb21wY
W55LmNvbSIsInN1YiI6ImpvaG5AY29tcGFueS5jb20iLCJleHAiOj
E3MDUzMTI0MDB9.signature...

Size: ~300 bytes

JWT is 6-7x smaller and JSON is easier to parse!
```

---

## What is JWT?

JWT (JSON Web Token) is a compact, URL-safe way to represent claims between two parties. It's a **self-contained** token that includes user information and a signature to verify authenticity.

**Pronunciation:** "jot" (rhymes with "dot")

**RFC:** 7519 (official internet standard since 2015)

### JWT Timeline

```
JWT HISTORY
═══════════

2010: JWT concept introduced by Microsoft & others
2011: Initial draft specification
2015: JWT becomes RFC 7519 (official internet standard!)
2024: Most widely used token format for web authentication

Key Contributors:
• Microsoft (original concept)
• Google (adoption & promotion)
• Auth0 (major advocate & tooling)
```

---

## Why JWT? Sessions vs Tokens

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

---

## Why is JWT Encoded (Base64)?

**Common Question:** "Why encode JWT if it's not for security?"

### Reason 1: URL Safety

```
THE PROBLEM: JSON has characters that break URLs
═══════════════════════════════════════════════

JSON payload:
{"user": "sumit", "role": "admin"}

If you put this directly in a URL:
https://api.com/verify?token={"user": "sumit", "role": "admin"}
                              ↑     ↑      ↑     ↑
                              Curly braces, quotes, colons, spaces
                              ALL break URLs!

Base64 encoding produces URL-safe characters:
https://api.com/verify?token=eyJ1c2VyIjoiam9obiIsInJvbGUiOiJhZG1pbiJ9
                              ↑
                              Only letters, numbers, +, /, =
                              (Base64URL uses - and _ instead of + and /)
```

### Reason 2: Header Compatibility

```
HTTP HEADERS DON'T LIKE SPECIAL CHARACTERS
══════════════════════════════════════════

Raw JSON in header:
Authorization: Bearer {"user":"sumit","exp":1234567890}
               ↑ Fails! Headers have character restrictions

Base64 encoded:
Authorization: Bearer eyJ1c2VyIjoiam9obiIsImV4cCI6MTIzNDU2Nzg5MH0
               ✓ Works! All safe characters
```

### Reason 3: Binary Safety

```python
# The signature is BINARY data (hash output)
# Binary can't be displayed as text directly

signature_bytes = b'\x8f\x12\xab\x03\xff...'  # Raw binary

# Base64 converts binary to printable characters
import base64
signature_b64 = base64.urlsafe_b64encode(signature_bytes)
# Result: "jxKrA_8..." - now it's text!
```

> **Remember:** Base64 encoding is NOT encryption! It's like writing your message in a different alphabet - anyone who knows Base64 can decode it instantly. The signature provides integrity, not secrecy.

---

## JWT Structure

A JWT consists of three parts separated by dots (`.`):

```
xxxxx.yyyyy.zzzzz
  │      │      │
  │      │      └── SIGNATURE (verification)
  │      │
  │      └── PAYLOAD (data/claims)
  │
  └── HEADER (algorithm info)
```

### The Three Parts Explained

#### 1. Header
```json
{
  "alg": "HS256",    // Algorithm used for signing
  "typ": "JWT"       // Token type
}
```

#### 2. Payload (Claims)
```json
{
  "sub": "1234567890",     // Subject (user ID)
  "name": "Sumit",         // Custom claim
  "role": "admin",         // Custom claim
  "iat": 1516239022,       // Issued at (timestamp)
  "exp": 1516242622        // Expiration (timestamp)
}
```

#### 3. Signature
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

---

## Standard Claims (Registered Claims)

| Claim | Name | Description |
|-------|------|-------------|
| `iss` | Issuer | Who created the token |
| `sub` | Subject | Who the token is about (usually user ID) |
| `aud` | Audience | Who the token is for |
| `exp` | **Expiration** | **When the token expires (IMPORTANT!)** |
| `nbf` | Not Before | Token not valid before this time |
| `iat` | Issued At | When the token was created |
| `jti` | JWT ID | Unique identifier for the token |

> **Always set `exp`!** A token without expiration is valid forever - a huge security risk.

---

## How JWT Verification Works

```
JWT VERIFICATION
════════════════

1. Receive token: eyJhbGc.eyJzdWI.signature
                     │        │        │
                     ▼        ▼        │
                [Header] [Payload]     │
                     │        │        │
                     └────┬───┘        │
                          │            │
                          ▼            │
2. Recalculate:   HMAC-SHA256(        │
                    base64(header) +   │
                    "." +              │
                    base64(payload),   │
                    SECRET_KEY         │
                  )                    │
                          │            │
                          ▼            ▼
3. Compare:     [Computed Sig] == [Received Sig]?
                          │
               ┌──────────┴──────────┐
               │                     │
               ▼                     ▼
          ✅ VALID              ❌ INVALID
        Trust the payload      Reject token
```

**Key Insight:** The server doesn't need to look up anything in a database! It just:
1. Recalculates the signature using its secret key
2. Compares with the received signature
3. If they match, the payload is trustworthy

---

## Critical Security Point: Payload is NOT Encrypted!

The payload is only Base64 encoded. **Anyone can decode and read it!**

| Never Put in Payload | Safe for Payload |
|---------------------|------------------|
| Passwords | User ID |
| Credit card numbers | Email (if not sensitive) |
| Social security numbers | Role/permissions |
| Any sensitive PII | Expiration time |

```python
# Anyone can decode the payload!
import base64
import json

token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.signature"
payload_b64 = token.split('.')[1]
payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '=='))
print(payload)  # {'sub': '123'} - visible to anyone!
```

---

## What If Someone Steals a JWT Token?

**This is JWT's biggest weakness!** Unlike sessions, you can't easily invalidate a stolen JWT.

### How JWT Tokens Get Stolen

| Attack Vector | How It Happens | Prevention |
|---------------|----------------|------------|
| **XSS Attack** | Malicious JavaScript reads token from localStorage | Store in httpOnly cookie, use Content Security Policy |
| **Man-in-the-Middle** | Token intercepted on unencrypted connection | Always use HTTPS, HSTS headers |
| **Browser Extension** | Malicious extension reads localStorage/headers | Store tokens securely, short expiration |
| **Shared Computer** | Token left in browser on public computer | Short expiration, logout clears tokens |

### The Problem: You Can't "Delete" a JWT

```
JWT THEFT SCENARIO
══════════════════

1. Attacker steals your JWT token (valid for 24 hours)

2. You realize it's stolen at hour 2

3. With Sessions:
   DELETE FROM sessions WHERE user_id = 123
   ✓ Attacker is IMMEDIATELY locked out!

4. With JWT:
   You can't "unvalidate" the token!
   The signature is still valid
   Attacker has 22 more hours of access!

The JWT contains everything needed to verify it.
Server doesn't "remember" which tokens it issued.
```

### Solutions for JWT Revocation

| Solution | How It Works | Tradeoff |
|----------|--------------|----------|
| **Short Expiration** | Access token: 15-30 min, Refresh token: 7-30 days | More frequent refresh needed |
| **Token Blacklist** | Maintain list of revoked tokens in Redis | Loses stateless benefit! |
| **Token Versioning** | Store token_version in user table, bump on logout | Needs DB lookup for version |
| **Refresh Token Rotation** | Each refresh invalidates old refresh token | More complex implementation |

---

## Access & Refresh Tokens: The Two-Token System

### The Dilemma

```
THE DILEMMA
═══════════

Option A: Short-lived token (15 minutes)
├── ✅ If stolen, attacker has limited time
├── ❌ User must re-login every 15 minutes
└── Terrible user experience!

Option B: Long-lived token (30 days)
├── ✅ User stays logged in for a month
├── ❌ If stolen, attacker has 30 days of access!
└── Huge security risk!

THE SOLUTION: Use BOTH!
├── Access Token: Short-lived (15 min) - used frequently
└── Refresh Token: Long-lived (30 days) - used rarely, kept safe
```

### The Two Tokens

| Aspect | Access Token | Refresh Token |
|--------|--------------|---------------|
| **Lifetime** | 15-30 minutes | 7-30 days |
| **Purpose** | Used for every API request | Get new access tokens |
| **Exposure** | High (sent frequently) | Low (sent rarely) |
| **If stolen** | Limited damage window | More serious, but kept safe |
| **Storage** | Memory (safest) | HttpOnly cookie / Secure storage |

**Real-World Analogy:**
- **Refresh Token** = Hotel booking confirmation (show once at check-in, kept safe)
- **Access Token** = Room key card (use for every door, expires daily, replaced easily)

### The Complete Flow

```
THE COMPLETE FLOW VISUALIZED
════════════════════════════

┌─────────┐                                    ┌─────────┐
│  User   │                                    │  Server │
└────┬────┘                                    └────┬────┘
     │                                              │
     │  1. POST /login {username, password}        │
     │ ────────────────────────────────────────────>│
     │                                              │
     │  {access_token, refresh_token}              │
     │ <────────────────────────────────────────────│
     │                                              │
     │  2. GET /api/data (access_token)            │
     │ ────────────────────────────────────────────>│  ✓ Valid
     │ <────────────────────────────────────────────│
     │                                              │
     │  ... 15 minutes later ...                   │
     │                                              │
     │  3. GET /api/data (access_token)            │
     │ ────────────────────────────────────────────>│  ✗ Expired!
     │  401 Unauthorized                           │
     │ <────────────────────────────────────────────│
     │                                              │
     │  4. POST /refresh (refresh_token)           │
     │ ────────────────────────────────────────────>│  ✓ Valid
     │  {new_access_token}                         │
     │ <────────────────────────────────────────────│
     │                                              │
     │  5. GET /api/data (new_access_token)        │
     │ ────────────────────────────────────────────>│  ✓ Valid
     │ <────────────────────────────────────────────│
```

---

## Where to Store Tokens (Production)

### Pattern 1: Memory + HttpOnly Cookie (Recommended)

Access token in JavaScript memory, refresh token in HttpOnly cookie.

| Pros | Cons |
|------|------|
| XSS can't steal access token | More complex to implement |
| XSS can't read refresh token | |
| Survives page refresh via refresh endpoint | |

```javascript
// Access token in memory (variable)
let accessToken = response.access_token;

// Refresh token set by server as HttpOnly cookie
// Set-Cookie: refresh_token=xyz; HttpOnly; Secure; SameSite=Strict

// On page load, call refresh endpoint to get new access token
async function onPageLoad() {
    const response = await fetch('/api/auth/refresh', {
        credentials: 'include'  // Send HttpOnly cookie
    });
    accessToken = response.access_token;
}
```

**Used by:** Auth0, Okta, many enterprise apps

### Pattern 2: localStorage (Common but Less Secure)

Both tokens in localStorage. Simple but vulnerable to XSS.

| Pros | Cons |
|------|------|
| Simple to implement | XSS can steal tokens! |
| Survives page refresh | |
| Works with any API | |

**Acceptable for:** Internal tools, low-risk apps, when combined with strong CSP

### Pattern 3: Mobile Secure Storage (Best for Mobile)

iOS Keychain or Android Keystore. Hardware-backed encryption.

| Pros |
|------|
| Hardware encryption |
| Protected by device PIN/biometrics |
| Other apps can't access |
| No XSS risk |

**Why JWT shines:** Mobile apps don't have browsers/cookies, making JWT perfect!

---

## Advanced: Refresh Token Rotation

**Problem:** If a refresh token is stolen, attacker can keep generating access tokens forever.

**Solution:** Every time a refresh token is used, issue a NEW refresh token and invalidate the old one.

```
REFRESH TOKEN ROTATION
══════════════════════

Normal Flow:
1. User calls /refresh with refresh_token_v1
2. Server returns:
   - New access_token
   - New refresh_token_v2 (old one invalidated!)
3. User must use refresh_token_v2 next time

Attack Detection:
1. Attacker steals refresh_token_v1
2. Real user refreshes first → gets refresh_token_v2
3. Attacker tries refresh_token_v1 → REJECTED!
4. Server detects reuse → Revokes ALL tokens for user
5. Both attacker AND user must re-login
   (User is notified of suspicious activity)
```

```python
# Server-side refresh with rotation
def refresh_token_endpoint(request):
    old_refresh_token = request.data['refresh_token']

    # Verify and decode
    payload = verify_refresh_token(old_refresh_token)

    # Check if token was already used (rotation detection)
    if is_token_blacklisted(old_refresh_token):
        # ALERT: Token reuse detected! Possible theft!
        revoke_all_tokens_for_user(payload['user_id'])
        raise SecurityException("Refresh token reuse detected")

    # Blacklist the old refresh token
    blacklist_token(old_refresh_token)

    # Issue new tokens
    new_access_token = create_access_token(payload['user_id'])
    new_refresh_token = create_refresh_token(payload['user_id'])

    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token  # NEW token!
    }
```

---

## Python Implementation

### Setup

```bash
pip install PyJWT
```

### Creating a JWT

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-super-secret-key-keep-it-safe"  # In production: use env variable!

def create_access_token(user_id: int, role: str) -> str:
    """Create a JWT access token."""
    payload = {
        "sub": str(user_id),      # Subject (user ID)
        "role": role,              # Custom claim
        "iat": datetime.utcnow(),  # Issued at
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expires in 1 hour
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# Usage
token = create_access_token(user_id=42, role="admin")
print(token)
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIs...
```

### Verifying a JWT

```python
def verify_token(token: str) -> dict:
    """Verify and decode a JWT token."""
    try:
        # Decode and verify the token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]  # IMPORTANT: Always specify allowed algorithms!
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")

    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


# Usage
try:
    payload = verify_token(token)
    print(f"User ID: {payload['sub']}")
    print(f"Role: {payload['role']}")
except Exception as e:
    print(f"Error: {e}")
```

### Create Both Tokens

```python
def create_tokens(user_id: int) -> dict:
    """Create access and refresh tokens."""
    access_token = jwt.encode({
        'sub': str(user_id),
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }, SECRET_KEY, algorithm='HS256')

    refresh_token = jwt.encode({
        'sub': str(user_id),
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
```

---

## Complete Django Example

```python
# views.py
import jwt
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from functools import wraps
import json

SECRET_KEY = settings.SECRET_KEY  # Use Django's secret key

# Decorator to protect views
def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Get token from header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return JsonResponse({'error': 'Token is missing'}, status=401)

        # Format: "Bearer <token>"
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return JsonResponse({'error': 'Invalid token format'}, status=401)

        # Verify token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_data = payload  # Attach user info to request
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    # TODO: Verify credentials against database
    if username and password:
        token = jwt.encode({
            'sub': username,
            'role': 'user',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return JsonResponse({'token': token})

    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@token_required
def protected(request):
    return JsonResponse({
        'message': 'This is protected!',
        'user': request.user_data['sub'],
        'role': request.user_data['role']
    })


# Refresh endpoint
@csrf_exempt
def refresh(request):
    """Get new access token using refresh token."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    refresh_token = data.get('refresh_token')

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])

        if payload.get('type') != 'refresh':
            return JsonResponse({'error': 'Invalid token type'}, status=401)

        # Create new access token
        new_access = jwt.encode({
            'sub': payload['sub'],
            'type': 'access',
            'exp': datetime.utcnow() + timedelta(minutes=15)
        }, SECRET_KEY, algorithm='HS256')

        return JsonResponse({'access_token': new_access})

    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid refresh token'}, status=401)
```

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('protected/', views.protected, name='protected'),
    path('refresh/', views.refresh, name='refresh'),
]
```

### Testing with cURL

```bash
# 1. Login to get token
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "sumit", "password": "secret"}'

# Response: {"token": "eyJhbGciOiJIUzI1NiIs..."}

# 2. Access protected route with token
curl http://localhost:8000/api/protected/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

# Response: {"message": "This is protected!", "user": "sumit", "role": "user"}
```

---

## Common JWT Attacks & Prevention

| Attack | Description | Prevention |
|--------|-------------|------------|
| **Algorithm None** | Setting `alg: none` to bypass signature | Always specify `algorithms=['HS256']` |
| **Weak Secret** | Brute-forcing short secrets | Use 256+ bit random secret |
| **Token Stealing** | XSS stealing from localStorage | Use httpOnly cookies or memory |
| **No Expiration** | Tokens valid forever | Always set `exp` claim |

---

## Security Best Practices

### Common Mistakes vs Best Practices

| Mistake | Best Practice |
|---------|---------------|
| `SECRET = "secret"` | `SECRET = os.environ['JWT_SECRET']` (256+ bits) |
| `jwt.decode(token, SECRET)` | `jwt.decode(token, SECRET, algorithms=['HS256'])` |
| `{'sub': '1'}` (no expiry) | `{'sub': '1', 'exp': ...}` |
| `{'password': 'secret123'}` | `{'sub': '1', 'role': 'user'}` (non-sensitive only) |

### Full Checklist

1. **Never hardcode secrets** - Use environment variables or secrets manager
2. **Always specify algorithms** - Prevent "algorithm none" attacks
3. **Always set expiration** - Tokens should not live forever
4. **Use short expiration for access tokens** - 15-30 minutes
5. **Use HTTPS always** - Tokens sent over HTTP can be intercepted
6. **Store tokens securely** - Memory + HttpOnly cookie is best
7. **Implement refresh token rotation** - Detect stolen tokens
8. **Never put sensitive data in payload** - It's not encrypted!

---

## JWT vs Sessions: When to Use What?

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| E-commerce site (Amazon-like) | **Sessions** | Need instant logout, cart state, fraud detection |
| Mobile app | **JWT** | No browser cookies, easier header-based auth |
| Banking application | **Sessions** | Critical need for instant session termination |
| Microservices API | **JWT** | Stateless verification, no shared DB needed |
| Public API (Stripe, Razorpay) | **JWT/API Keys** | External clients can't share session store |
| Admin dashboard | **Sessions** | Need to track active admins, revoke instantly |
| SPA + Separate API | **JWT** | Simpler than CORS + cookies configuration |
| Hybrid (best of both) | **JWT + Redis blacklist** | Stateless scaling + ability to revoke |

> **Real World:** Many companies use BOTH! Sessions for web app, JWT for mobile app and APIs. Choose based on your specific requirements.

---

## Try It Yourself!

### JWT Debugger Tools

| Tool | URL | Description |
|------|-----|-------------|
| jwt.io | https://jwt.io | Decode, verify, and generate JWTs |
| jwt.ms | https://jwt.ms | Microsoft's JWT decoder |
| token.dev | https://token.dev | Generate and test tokens |

### Class Demo: Tampering with JWT

```
LIVE DEMO STEPS
═══════════════

1. Go to jwt.io

2. In the "Encoded" box, you'll see a sample JWT
   Header.Payload.Signature (color-coded!)

3. In "Decoded" section, try changing:
   • Change "name": "Sumit Mishra" to your name
   • Change "admin": false to "admin": true

4. Watch the signature turn RED!
   This shows tampering is DETECTED.

5. Now enter the correct secret key
   Watch the signature turn BLUE (valid again)

KEY INSIGHT: Without the secret key, you can change
the payload but the signature will be INVALID!
```

### Quick Python Script for Demo

```python
import jwt
import datetime

SECRET_KEY = "demo-secret-key-12345"

# Create a token
payload = {
    "user_id": 123,
    "name": "Prateek",
    "role": "instructor",
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("Generated Token:")
print(token)
print("\n" + "="*50 + "\n")

# Decode and show payload
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
print("Decoded Payload:")
print(decoded)

# Now copy this token to jwt.io!
```

> **Real World Tokens:** Open your browser DevTools (F12) → Application → Storage → Cookies or Local Storage. Many sites store JWTs there. Copy one to jwt.io to inspect!
