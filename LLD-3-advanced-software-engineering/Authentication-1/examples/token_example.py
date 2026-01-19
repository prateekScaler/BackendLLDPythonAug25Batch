#!/usr/bin/env python3
"""
JWT Token Authentication Demo
=============================

This script demonstrates creating and verifying JWT tokens.

Run: python token_example.py

Requirements:
    pip install pyjwt
"""

import datetime
import base64
import json
import hmac
import hashlib
from typing import Optional, Dict, Any

# Try importing PyJWT
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("⚠️  PyJWT not installed. Run: pip install pyjwt")
    print("    Falling back to manual implementation for demo.\n")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

SECRET_KEY = "your-256-bit-secret-key-here-make-it-long"
ALGORITHM = "HS256"


def print_header(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 1: JWT STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

def demo_jwt_structure():
    print_header("DEMO 1: JWT STRUCTURE")

    # Create a sample JWT manually to show structure
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "admin": True,
        "iat": 1516239022
    }

    # Base64URL encode (not regular base64!)
    def b64url_encode(data: dict) -> str:
        json_bytes = json.dumps(data, separators=(',', ':')).encode()
        return base64.urlsafe_b64encode(json_bytes).rstrip(b'=').decode()

    header_b64 = b64url_encode(header)
    payload_b64 = b64url_encode(payload)

    # Create signature
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=').decode()

    token = f"{header_b64}.{payload_b64}.{signature_b64}"

    print(f"""
  JWT consists of three parts separated by dots (.)

  ┌─────────────────────────────────────────────────────────────┐
  │  HEADER (Algorithm & Type)                                  │
  │  {json.dumps(header)}
  │  Base64: {header_b64}
  └─────────────────────────────────────────────────────────────┘
                            ↓
  ┌─────────────────────────────────────────────────────────────┐
  │  PAYLOAD (Claims/Data)                                      │
  │  {json.dumps(payload, indent=2)}
  │  Base64: {payload_b64}
  └─────────────────────────────────────────────────────────────┘
                            ↓
  ┌─────────────────────────────────────────────────────────────┐
  │  SIGNATURE                                                  │
  │  HMAC-SHA256(header.payload, secret)                        │
  │  Base64: {signature_b64}
  └─────────────────────────────────────────────────────────────┘

  Complete Token:
  {token[:40]}...
    """)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 2: CREATING TOKENS WITH PyJWT
# ═══════════════════════════════════════════════════════════════════════════════

def demo_create_token():
    print_header("DEMO 2: CREATING JWT TOKENS")

    if not JWT_AVAILABLE:
        print("  (Skipped - PyJWT not installed)")
        return None

    # Create an access token
    now = datetime.datetime.utcnow()
    payload = {
        # Standard claims
        "sub": "user_42",                    # Subject (user ID)
        "iat": now,                          # Issued at
        "exp": now + datetime.timedelta(minutes=30),  # Expires

        # Custom claims
        "name": "Alice Smith",
        "email": "alice@example.com",
        "role": "admin",
        "permissions": ["read", "write", "delete"]
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    print(f"""
  Creating token for user:
  • User ID: {payload['sub']}
  • Name: {payload['name']}
  • Role: {payload['role']}
  • Expires: {payload['exp']}

  Generated Token:
  {token}

  Token length: {len(token)} characters
    """)

    return token


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 3: VERIFYING TOKENS
# ═══════════════════════════════════════════════════════════════════════════════

def demo_verify_token(token: str):
    print_header("DEMO 3: VERIFYING JWT TOKENS")

    if not JWT_AVAILABLE:
        print("  (Skipped - PyJWT not installed)")
        return

    print("  Valid token verification:")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"  ✅ Token is valid!")
        print(f"  Decoded payload:")
        for key, value in decoded.items():
            if key in ['iat', 'exp']:
                # Convert timestamp to readable date
                value = datetime.datetime.fromtimestamp(value)
            print(f"    • {key}: {value}")
    except jwt.ExpiredSignatureError:
        print("  ❌ Token has expired")
    except jwt.InvalidTokenError as e:
        print(f"  ❌ Invalid token: {e}")

    # Test with wrong secret
    print("\n  Verification with wrong secret:")
    try:
        jwt.decode(token, "wrong-secret", algorithms=[ALGORITHM])
        print("  ✅ Token valid (this shouldn't happen!)")
    except jwt.InvalidSignatureError:
        print("  ❌ Invalid signature - token was tampered with or wrong secret")

    # Test with tampered token
    print("\n  Verification with tampered payload:")
    parts = token.split('.')
    # Decode payload, modify it, re-encode
    payload_json = base64.urlsafe_b64decode(parts[1] + '==')
    payload_dict = json.loads(payload_json)
    payload_dict['role'] = 'superadmin'  # Try to escalate privileges!
    tampered_payload = base64.urlsafe_b64encode(
        json.dumps(payload_dict).encode()
    ).rstrip(b'=').decode()
    tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"

    try:
        jwt.decode(tampered_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("  ✅ Tampered token accepted (SECURITY BREACH!)")
    except jwt.InvalidSignatureError:
        print("  ❌ Tampered token rejected - signature doesn't match")
        print("     (This is the expected secure behavior)")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 4: TOKEN EXPIRATION
# ═══════════════════════════════════════════════════════════════════════════════

def demo_token_expiration():
    print_header("DEMO 4: TOKEN EXPIRATION")

    if not JWT_AVAILABLE:
        print("  (Skipped - PyJWT not installed)")
        return

    # Create an already-expired token
    now = datetime.datetime.utcnow()
    expired_payload = {
        "sub": "user_42",
        "exp": now - datetime.timedelta(hours=1)  # Expired 1 hour ago
    }
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)

    print("  Testing expired token:")
    try:
        jwt.decode(expired_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("  ✅ Token accepted (SECURITY ISSUE!)")
    except jwt.ExpiredSignatureError:
        print("  ❌ Token rejected: ExpiredSignatureError")
        print("     (This is correct behavior)")

    # Create a not-yet-valid token (nbf claim)
    future_payload = {
        "sub": "user_42",
        "nbf": now + datetime.timedelta(hours=1),  # Valid 1 hour from now
        "exp": now + datetime.timedelta(hours=2)
    }
    future_token = jwt.encode(future_payload, SECRET_KEY, algorithm=ALGORITHM)

    print("\n  Testing not-yet-valid token (nbf claim):")
    try:
        jwt.decode(future_token, SECRET_KEY, algorithms=[ALGORITHM])
        print("  ✅ Token accepted")
    except jwt.ImmatureSignatureError:
        print("  ❌ Token rejected: ImmatureSignatureError")
        print("     (Token is not valid yet)")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 5: ACCESS + REFRESH TOKEN FLOW
# ═══════════════════════════════════════════════════════════════════════════════

def demo_refresh_token():
    print_header("DEMO 5: ACCESS + REFRESH TOKEN FLOW")

    if not JWT_AVAILABLE:
        print("  (Skipped - PyJWT not installed)")
        return

    REFRESH_SECRET = "different-secret-for-refresh-tokens"
    now = datetime.datetime.utcnow()

    # Create token pair
    access_token = jwt.encode({
        "sub": "user_42",
        "type": "access",
        "exp": now + datetime.timedelta(minutes=15)
    }, SECRET_KEY, algorithm=ALGORITHM)

    refresh_token = jwt.encode({
        "sub": "user_42",
        "type": "refresh",
        "exp": now + datetime.timedelta(days=7)
    }, REFRESH_SECRET, algorithm=ALGORITHM)

    print(f"""
  Token Pair Created:

  ACCESS TOKEN (short-lived: 15 minutes)
  ──────────────────────────────────────
  {access_token[:50]}...

  REFRESH TOKEN (long-lived: 7 days)
  ──────────────────────────────────────
  {refresh_token[:50]}...

  Flow:
  1. Client stores both tokens
  2. Uses access token for API calls
  3. When access token expires (401 response):
     - Send refresh token to /refresh endpoint
     - Get new access token
     - Continue making API calls
  4. When refresh token expires:
     - User must log in again
    """)

    # Simulate refresh
    print("  Simulating token refresh:")
    try:
        refresh_payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=[ALGORITHM])
        if refresh_payload.get('type') == 'refresh':
            # Issue new access token
            new_access = jwt.encode({
                "sub": refresh_payload['sub'],
                "type": "access",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            }, SECRET_KEY, algorithm=ALGORITHM)
            print(f"  ✅ New access token issued!")
            print(f"     {new_access[:40]}...")
    except jwt.InvalidTokenError as e:
        print(f"  ❌ Refresh failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 6: SECURITY VULNERABILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def demo_security_vulnerabilities():
    print_header("DEMO 6: JWT SECURITY VULNERABILITIES")

    print("""
  Common JWT Vulnerabilities:

  1. ALGORITHM CONFUSION ATTACK
  ════════════════════════════
  Some libraries accept "alg": "none" which means NO signature!

  Attacker creates:
  {
    "alg": "none",     ← No signature required!
    "typ": "JWT"
  }

  Prevention:
  • ALWAYS specify allowed algorithms explicitly
  • jwt.decode(token, secret, algorithms=["HS256"])  ✅
  • jwt.decode(token, secret)  ❌ (might accept "none")

  2. WEAK SECRET KEY
  ══════════════════
  ❌ "secret"           → Can be brute-forced
  ❌ "company123"       → Can be dictionary attacked
  ✅ 256-bit random key → Computationally infeasible

  3. SENSITIVE DATA IN PAYLOAD
  ════════════════════════════
  JWT payload is NOT encrypted, only encoded!

  ❌ Storing: credit_card, ssn, password
  ✅ Storing: user_id, role, permissions

  Anyone can decode the payload:
    """)

    # Demonstrate decoding
    sample_token = "eyJhbGciOiJIUzI1NiJ9.eyJjcmVkaXRfY2FyZCI6IjQxMTEtMTExMS0xMTExLTExMTEifQ.sig"
    payload_b64 = sample_token.split('.')[1]
    # Add padding if needed
    padding = 4 - len(payload_b64) % 4
    if padding != 4:
        payload_b64 += '=' * padding
    decoded = base64.urlsafe_b64decode(payload_b64)
    print(f"  Encoded: {sample_token.split('.')[1]}")
    print(f"  Decoded: {decoded.decode()}")
    print("\n  Anyone can see this data without the secret key!")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO 7: PRACTICAL USAGE PATTERN
# ═══════════════════════════════════════════════════════════════════════════════

def demo_practical_usage():
    print_header("DEMO 7: PRACTICAL USAGE PATTERN")

    if not JWT_AVAILABLE:
        print("  (Skipped - PyJWT not installed)")
        return

    print("""
  Complete Authentication Flow:
    """)

    # Simulated user database
    users_db = {
        "alice": {"id": 1, "password_hash": "...", "role": "admin"},
        "bob": {"id": 2, "password_hash": "...", "role": "user"}
    }

    def login(username: str, password: str) -> Optional[Dict[str, str]]:
        """Simulate login and return tokens"""
        user = users_db.get(username)
        if not user:
            return None
        # In real app: verify password with bcrypt

        now = datetime.datetime.utcnow()
        access_token = jwt.encode({
            "sub": str(user['id']),
            "username": username,
            "role": user['role'],
            "type": "access",
            "exp": now + datetime.timedelta(minutes=15)
        }, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": access_token, "token_type": "bearer"}

    def protected_endpoint(token: str) -> Dict[str, Any]:
        """Simulate a protected API endpoint"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {
                "success": True,
                "user_id": payload['sub'],
                "role": payload['role'],
                "message": f"Hello, {payload['username']}!"
            }
        except jwt.ExpiredSignatureError:
            return {"success": False, "error": "Token expired"}
        except jwt.InvalidTokenError:
            return {"success": False, "error": "Invalid token"}

    # Demo the flow
    print("  Step 1: User logs in")
    tokens = login("alice", "password123")
    if tokens:
        print(f"  ✅ Login successful!")
        print(f"     Token: {tokens['access_token'][:40]}...")

        print("\n  Step 2: User accesses protected resource")
        result = protected_endpoint(tokens['access_token'])
        print(f"  ✅ Response: {result}")

        print("\n  Step 3: Attempt with invalid token")
        result = protected_endpoint("invalid.token.here")
        print(f"  ❌ Response: {result}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "🎟️" * 30)
    print("     JWT TOKEN AUTHENTICATION DEMONSTRATION")
    print("🎟️" * 30)

    demo_jwt_structure()
    token = demo_create_token()
    if token:
        demo_verify_token(token)
    demo_token_expiration()
    demo_refresh_token()
    demo_security_vulnerabilities()
    demo_practical_usage()

    print("\n" + "=" * 60)
    print("  Demo complete! You now understand JWT tokens.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
