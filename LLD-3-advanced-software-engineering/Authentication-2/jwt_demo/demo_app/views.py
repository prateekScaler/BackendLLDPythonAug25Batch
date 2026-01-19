"""
JWT Demo Views

Educational views demonstrating:
1. How clients obtain JWT tokens
2. How to use tokens for authentication
3. Token structure and inspection
4. Tampering attacks and why they fail
5. Token expiry and revocation
"""

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from .jwt_utils import (
    create_jwt_token,
    decode_jwt_token,
    decode_jwt_parts,
    tamper_jwt_payload,
    demonstrate_signature_calculation,
    is_token_revoked,
    revoke_token,
    clear_revoked_tokens,
)

# Simple in-memory user store for demo (use Django's User model in production)
DEMO_USERS = {
    'alice': {'password': make_password('password123'), 'role': 'admin', 'id': 1},
    'bob': {'password': make_password('secret456'), 'role': 'user', 'id': 2},
    'charlie': {'password': make_password('test789'), 'role': 'user', 'id': 3},
}


def home(request):
    """Main demo page with interactive UI."""
    return render(request, 'home.html', {
        'users': [
            {'username': 'alice', 'password': 'password123', 'role': 'admin'},
            {'username': 'bob', 'password': 'secret456', 'role': 'user'},
            {'username': 'charlie', 'password': 'test789', 'role': 'user'},
        ]
    })


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """
    Login endpoint - returns JWT token on successful authentication.

    TEACHING POINT: This is how a client obtains a JWT token.
    The server verifies credentials and issues a signed token.
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')

        if username not in DEMO_USERS:
            return JsonResponse({
                'success': False,
                'error': 'User not found',
                'teaching_point': 'Authentication failed at step 1: user lookup'
            }, status=401)

        user = DEMO_USERS[username]
        if not check_password(password, user['password']):
            return JsonResponse({
                'success': False,
                'error': 'Invalid password',
                'teaching_point': 'Authentication failed at step 2: password verification'
            }, status=401)

        # Generate JWT token
        token = create_jwt_token(
            user_id=user['id'],
            username=username,
            role=user['role']
        )

        return JsonResponse({
            'success': True,
            'token': token,
            'teaching_point': (
                'Server verified credentials and issued a signed JWT. '
                'This token contains user claims and is cryptographically signed. '
                'Client should store this (localStorage, cookie, etc.) and send '
                'it with future requests in the Authorization header.'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def verify_token(request):
    """
    Verify a JWT token and return protected data.

    TEACHING POINT: This demonstrates how servers validate tokens
    and extract user information without database lookup.
    """
    try:
        data = json.loads(request.body)
        token = data.get('token', '')

        if not token:
            return JsonResponse({
                'success': False,
                'error': 'No token provided',
                'teaching_point': 'Requests to protected endpoints must include a token'
            }, status=401)

        # Check if token is revoked
        if is_token_revoked(token):
            return JsonResponse({
                'success': False,
                'error': 'Token has been revoked',
                'teaching_point': (
                    'Even though this token has a valid signature and is not expired, '
                    'it was explicitly revoked (e.g., on logout). The server maintains '
                    'a revocation list to invalidate tokens before their natural expiry.'
                )
            }, status=401)

        # Verify token
        result = decode_jwt_token(token, verify=True)

        if result['success']:
            payload = result['payload']
            return JsonResponse({
                'success': True,
                'user': {
                    'id': payload.get('user_id'),
                    'username': payload.get('username'),
                    'role': payload.get('role'),
                },
                'protected_data': f"Secret message for {payload.get('username')}!",
                'teaching_point': (
                    'Token verified successfully! The server: '
                    '1) Decoded the token, '
                    '2) Verified the signature matches, '
                    '3) Checked expiration time, '
                    '4) Extracted user claims WITHOUT database lookup. '
                    'This is why JWT is stateless and scalable!'
                )
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result['error'],
                'teaching_point': (
                    'Token verification failed. Possible reasons: '
                    '1) Token expired (check exp claim), '
                    '2) Invalid signature (token was tampered), '
                    '3) Malformed token structure'
                )
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def decode_token(request):
    """
    Decode a JWT token to show its structure (without verification).

    TEACHING POINT: JWT payload is NOT encrypted, just encoded!
    Anyone can read the payload. Security comes from the signature.
    """
    try:
        data = json.loads(request.body)
        token = data.get('token', '')

        if not token:
            return JsonResponse({'success': False, 'error': 'No token provided'}, status=400)

        parts = decode_jwt_parts(token)

        if 'error' in parts:
            return JsonResponse({'success': False, 'error': parts['error']}, status=400)

        return JsonResponse({
            'success': True,
            'parts': parts,
            'teaching_point': (
                'JWT has 3 parts separated by dots: HEADER.PAYLOAD.SIGNATURE\n\n'
                '1. HEADER: Algorithm and token type (base64 encoded)\n'
                '2. PAYLOAD: Claims/data (base64 encoded) - NOT ENCRYPTED!\n'
                '3. SIGNATURE: HMAC of header.payload using secret key\n\n'
                'IMPORTANT: Anyone can decode and read the payload! '
                'Never put sensitive data (passwords, secrets) in JWT. '
                'The signature only prevents MODIFICATION, not READING.'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def tamper_token(request):
    """
    Demonstrate what happens when someone tries to tamper with a JWT.

    TEACHING POINT: Shows why JWT signature makes tampering detectable.
    """
    try:
        data = json.loads(request.body)
        token = data.get('token', '')
        new_claims = data.get('new_claims', {})

        if not token:
            return JsonResponse({'success': False, 'error': 'No token provided'}, status=400)

        result = tamper_jwt_payload(token, new_claims)

        if 'error' in result:
            return JsonResponse({'success': False, 'error': result['error']}, status=400)

        return JsonResponse({
            'success': True,
            'result': result,
            'attack_scenarios': [
                {
                    'name': 'Privilege Escalation',
                    'description': 'Attacker tries to change role from "user" to "admin"',
                    'why_attempted': 'Gain unauthorized access to admin features'
                },
                {
                    'name': 'Identity Theft',
                    'description': 'Attacker tries to change user_id to another user',
                    'why_attempted': 'Access another user\'s data or impersonate them'
                },
                {
                    'name': 'Extend Session',
                    'description': 'Attacker tries to modify exp (expiration) claim',
                    'why_attempted': 'Keep using a token beyond its intended lifetime'
                }
            ],
            'teaching_point': (
                'TAMPERING FAILS because:\n\n'
                '1. Attacker intercepts token\n'
                '2. Attacker decodes payload (easy - just base64)\n'
                '3. Attacker modifies claims (e.g., role: "admin")\n'
                '4. Attacker re-encodes payload with base64\n'
                '5. Attacker sends modified token with OLD signature\n'
                '6. Server calculates: HMAC(new_header.new_payload, secret)\n'
                '7. Server compares with provided signature: MISMATCH!\n'
                '8. Server rejects the token\n\n'
                'The attacker cannot create a valid signature without the SECRET KEY!'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def explain_signature(request):
    """
    Show step-by-step how the JWT signature is calculated.

    TEACHING POINT: Demystify the cryptography behind JWT.
    """
    try:
        data = json.loads(request.body)
        token = data.get('token', '')

        if not token:
            return JsonResponse({'success': False, 'error': 'No token provided'}, status=400)

        result = demonstrate_signature_calculation(token)

        if 'error' in result:
            return JsonResponse({'success': False, 'error': result['error']}, status=400)

        return JsonResponse({
            'success': True,
            'signature_demo': result,
            'teaching_point': (
                'The signature is calculated as:\n'
                'signature = HMAC-SHA256(base64(header) + "." + base64(payload), secret)\n\n'
                'This means:\n'
                '1. Only someone with the SECRET can create valid signatures\n'
                '2. Changing ANY byte in header or payload changes the signature\n'
                '3. Server can verify by recalculating and comparing\n'
                '4. No database lookup needed - just cryptographic verification!'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def revoke_user_token(request):
    """
    Revoke a JWT token (add to blacklist).

    TEACHING POINT: JWT revocation requires server-side state.
    """
    try:
        data = json.loads(request.body)
        token = data.get('token', '')

        if not token:
            return JsonResponse({'success': False, 'error': 'No token provided'}, status=400)

        revoke_token(token)

        return JsonResponse({
            'success': True,
            'message': 'Token has been revoked',
            'teaching_point': (
                'JWT REVOCATION CHALLENGE:\n\n'
                'JWTs are stateless by design - the server doesn\'t track them. '
                'But what if a user logs out or their account is compromised?\n\n'
                'Solutions:\n'
                '1. SHORT EXPIRY: Use short-lived tokens (5-15 min) with refresh tokens\n'
                '2. BLACKLIST: Maintain a list of revoked tokens (defeats statelessness)\n'
                '3. TOKEN VERSIONING: Store version in user record, increment on logout\n'
                '4. JTI CLAIM: Use unique token IDs and track revoked IDs\n\n'
                'Trade-off: Revocation adds state, which reduces scalability benefits of JWT.'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def create_expired_token(request):
    """
    Create a token that's already expired (for demo purposes).

    TEACHING POINT: Show how expiration works.
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', 'demo_user')
        user_id = data.get('user_id', 999)

        # Create token with negative expiry (already expired)
        token = create_jwt_token(
            user_id=user_id,
            username=username,
            role='user',
            expiry_minutes=-1  # Expired 1 minute ago
        )

        return JsonResponse({
            'success': True,
            'token': token,
            'teaching_point': (
                'This token has exp (expiration) set in the PAST.\n'
                'When you try to verify it, you\'ll get "Token has expired".\n\n'
                'WHY EXPIRY MATTERS:\n'
                '1. Limits damage if token is stolen\n'
                '2. Forces re-authentication periodically\n'
                '3. Allows credential changes to take effect\n\n'
                'Best practice: Short-lived access tokens (5-15 min) + '
                'longer-lived refresh tokens for seamless UX.'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def impersonation_demo(request):
    """
    Demonstrate how token theft enables impersonation.

    TEACHING POINT: Why protecting JWT tokens is critical.
    """
    try:
        data = json.loads(request.body)
        token = data.get('token', '')

        if not token:
            return JsonResponse({'success': False, 'error': 'No token provided'}, status=400)

        # Verify the token
        result = decode_jwt_token(token, verify=True)

        if not result['success']:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=401)

        payload = result['payload']

        return JsonResponse({
            'success': True,
            'impersonation_demo': {
                'attacker_action': 'Stole token from Alice\'s browser/network',
                'server_sees': {
                    'user_id': payload.get('user_id'),
                    'username': payload.get('username'),
                    'role': payload.get('role'),
                },
                'result': f"Server trusts attacker as {payload.get('username')}!",
            },
            'teaching_point': (
                'JWT IMPERSONATION RISK:\n\n'
                'If an attacker obtains a valid JWT token, they CAN impersonate '
                'the user until the token expires. The server has NO WAY to know '
                'the request isn\'t from the legitimate user.\n\n'
                'ATTACK VECTORS:\n'
                '1. XSS: Steal from localStorage/cookies\n'
                '2. MITM: Intercept over unencrypted connection\n'
                '3. Malware: Access browser storage\n'
                '4. Shoulder surfing: Copy from dev tools\n\n'
                'DEFENSES:\n'
                '1. HTTPS only (prevents MITM)\n'
                '2. HttpOnly cookies (prevents XSS)\n'
                '3. Short expiry times\n'
                '4. Bind token to IP/User-Agent (reduces portability)\n'
                '5. Refresh token rotation'
            )
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def reset_demo(request):
    """Reset demo state (clear revoked tokens)."""
    clear_revoked_tokens()
    return JsonResponse({
        'success': True,
        'message': 'Demo state reset. All revoked tokens cleared.'
    })
