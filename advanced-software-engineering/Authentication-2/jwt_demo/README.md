# JWT (JSON Web Token) Demo

An interactive educational Django project to demonstrate how JWT authentication works.

## Setup

```bash
cd jwt_demo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Then open http://localhost:8000 in your browser.

## Demo Users

| Username | Password    | Role  |
|----------|-------------|-------|
| alice    | password123 | admin |
| bob      | secret456   | user  |
| charlie  | test789     | user  |

## What You'll Learn

### 1. How Clients Get JWT Tokens
- Login with username/password
- Server verifies credentials
- Server creates and signs JWT
- Client stores token (localStorage, cookies, etc.)

### 2. JWT Structure (Header.Payload.Signature)
- **Header**: Algorithm and token type (base64)
- **Payload**: User claims and metadata (base64) - NOT ENCRYPTED!
- **Signature**: HMAC-SHA256 of header.payload using secret

### 3. Token Impersonation Risk
- If someone steals your token, they ARE you
- Server cannot distinguish legitimate user from attacker
- Why HTTPS, HttpOnly cookies, and short expiry matter

### 4. Tampering Attacks (Why They Fail)
- Attackers can read and modify the payload (it's just base64)
- BUT they cannot create a valid signature without the secret
- Server recalculates signature and detects mismatch

### 5. Attack Scenarios Demonstrated
- **Privilege Escalation**: Change role from "user" to "admin"
- **Identity Theft**: Change user_id to another user
- **Session Extension**: Modify expiration time

### 6. Expiration and Revocation
- `exp` claim sets token lifetime
- Short-lived tokens limit damage window
- Revocation challenges JWT's stateless design
- Solutions: blacklists, refresh tokens, token versioning

## Key Teaching Points

1. **JWT payload is NOT encrypted** - never put secrets in it
2. **Security comes from the signature** - prevents tampering
3. **Stateless = scalable but revocation is hard**
4. **Always use HTTPS** - tokens in transit are vulnerable
5. **Short expiry + refresh tokens** = security + good UX
