"""
JWT Utility Functions for Educational Demo

This module demonstrates how JWT tokens work:
1. Token Generation (encoding)
2. Token Verification (decoding)
3. Token Structure (header.payload.signature)
4. Why tampering fails
"""

import jwt
import json
import base64
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from django.conf import settings


def create_jwt_token(user_id: int, username: str, role: str = 'user',
                     expiry_minutes: int = None) -> str:
    """
    Create a JWT token for a user.

    JWT Structure:
    - Header: Algorithm and token type
    - Payload: Claims (user data + metadata)
    - Signature: HMAC of header.payload using secret
    """
    if expiry_minutes is None:
        expiry_minutes = settings.JWT_EXPIRY_MINUTES

    now = datetime.now(timezone.utc)

    payload = {
        # Registered Claims (standard)
        'iat': now,                                    # Issued At
        'exp': now + timedelta(minutes=expiry_minutes), # Expiration
        'nbf': now,                                    # Not Before

        # Public/Private Claims (custom)
        'user_id': user_id,
        'username': username,
        'role': role,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_jwt_token(token: str, verify: bool = True) -> dict:
    """
    Decode and verify a JWT token.

    If verify=False, decodes without verification (for inspection only).
    """
    try:
        if verify:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
        else:
            # Decode without verification (dangerous in production!)
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
        return {'success': True, 'payload': payload}
    except jwt.ExpiredSignatureError:
        return {'success': False, 'error': 'Token has expired'}
    except jwt.InvalidTokenError as e:
        return {'success': False, 'error': f'Invalid token: {str(e)}'}


def decode_jwt_parts(token: str) -> dict:
    """
    Manually decode JWT parts to show the structure.
    This is for EDUCATIONAL purposes to show what's inside a JWT.
    """
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {'error': 'Invalid JWT format - must have 3 parts'}

        header_b64, payload_b64, signature_b64 = parts

        # Decode header (add padding if needed)
        header_padded = header_b64 + '=' * (4 - len(header_b64) % 4)
        header = json.loads(base64.urlsafe_b64decode(header_padded))

        # Decode payload
        payload_padded = payload_b64 + '=' * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_padded))

        # Convert timestamps to readable format
        if 'iat' in payload:
            payload['iat_readable'] = datetime.fromtimestamp(
                payload['iat'], timezone.utc
            ).isoformat()
        if 'exp' in payload:
            payload['exp_readable'] = datetime.fromtimestamp(
                payload['exp'], timezone.utc
            ).isoformat()

        return {
            'header': header,
            'header_b64': header_b64,
            'payload': payload,
            'payload_b64': payload_b64,
            'signature_b64': signature_b64,
        }
    except Exception as e:
        return {'error': f'Failed to decode: {str(e)}'}


def tamper_jwt_payload(token: str, new_claims: dict) -> dict:
    """
    Demonstrate token tampering.

    This shows WHY tampering fails:
    1. We modify the payload
    2. We re-encode with base64
    3. We keep the original signature
    4. Verification FAILS because signature doesn't match

    SECURITY LESSON: The signature is a HMAC of (header + payload).
    If you change the payload, the signature becomes invalid.
    """
    try:
        parts = token.split('.')
        header_b64, payload_b64, signature_b64 = parts

        # Decode original payload
        payload_padded = payload_b64 + '=' * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_padded))

        # Store original for comparison
        original_payload = payload.copy()

        # Apply tampering
        payload.update(new_claims)

        # Re-encode tampered payload
        tampered_payload_json = json.dumps(payload, separators=(',', ':'))
        tampered_payload_b64 = base64.urlsafe_b64encode(
            tampered_payload_json.encode()
        ).decode().rstrip('=')

        # Create tampered token (keeping original signature - this is the attack!)
        tampered_token = f"{header_b64}.{tampered_payload_b64}.{signature_b64}"

        # Now verify - this should FAIL!
        verification = decode_jwt_token(tampered_token, verify=True)

        return {
            'original_payload': original_payload,
            'tampered_payload': payload,
            'tampered_token': tampered_token,
            'verification_result': verification,
            'explanation': (
                "The signature was created using the ORIGINAL payload. "
                "When we change the payload but keep the old signature, "
                "the server recalculates the signature and finds a MISMATCH. "
                "This is why JWT is secure against tampering!"
            )
        }
    except Exception as e:
        return {'error': str(e)}


def demonstrate_signature_calculation(token: str) -> dict:
    """
    Show step-by-step how JWT signature is calculated.
    This helps students understand WHY tampering detection works.
    """
    try:
        parts = token.split('.')
        header_b64, payload_b64, signature_b64 = parts

        # The message to sign is: header.payload (base64 encoded)
        message = f"{header_b64}.{payload_b64}"

        # Calculate HMAC-SHA256
        calculated_signature = hmac.new(
            settings.JWT_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()

        calculated_signature_b64 = base64.urlsafe_b64encode(
            calculated_signature
        ).decode().rstrip('=')

        return {
            'message_signed': message,
            'secret_used': settings.JWT_SECRET[:10] + '...',  # Partial for demo
            'algorithm': 'HMAC-SHA256',
            'calculated_signature': calculated_signature_b64,
            'token_signature': signature_b64,
            'signatures_match': calculated_signature_b64 == signature_b64,
            'explanation': (
                f"Signature = HMAC-SHA256('{message}', secret)\n"
                "If anyone modifies header or payload, this calculation "
                "produces a DIFFERENT signature, and verification fails."
            )
        }
    except Exception as e:
        return {'error': str(e)}


def is_token_revoked(token: str) -> bool:
    """Check if token has been revoked."""
    return token in settings.REVOKED_TOKENS


def revoke_token(token: str):
    """Add token to revocation list."""
    settings.REVOKED_TOKENS.add(token)


def clear_revoked_tokens():
    """Clear all revoked tokens (for demo reset)."""
    settings.REVOKED_TOKENS.clear()
