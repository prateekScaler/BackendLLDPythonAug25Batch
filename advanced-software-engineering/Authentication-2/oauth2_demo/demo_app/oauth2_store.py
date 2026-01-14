"""
OAuth2 In-Memory Store for Demo

This simulates what a real OAuth2 provider would have in a database.
In production, use a proper database with proper security!
"""

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from django.contrib.auth.hashers import make_password, check_password

# ============================================
# OAUTH2 PROVIDER DATA (Simulating Google/GitHub)
# ============================================

# Registered OAuth2 Clients (like registering your app with Google)
REGISTERED_CLIENTS = {
    'demo-client-id': {
        'client_secret': 'demo-client-secret-12345',
        'name': 'My Demo App',
        'redirect_uris': [
            'http://localhost:8000/callback/',
            'http://127.0.0.1:8000/callback/',
        ],
        'allowed_scopes': ['profile', 'email', 'read', 'write'],
    }
}

# Users on the OAuth Provider (like Google accounts)
PROVIDER_USERS = {
    'alice@example.com': {
        'password': make_password('password123'),
        'name': 'Alice Smith',
        'email': 'alice@example.com',
        'picture': 'https://i.pravatar.cc/150?u=alice',
    },
    'bob@example.com': {
        'password': make_password('secret456'),
        'name': 'Bob Jones',
        'email': 'bob@example.com',
        'picture': 'https://i.pravatar.cc/150?u=bob',
    },
}

# Temporary storage for authorization codes (short-lived, one-time use)
AUTHORIZATION_CODES = {}

# Issued access tokens
ACCESS_TOKENS = {}

# Issued refresh tokens
REFRESH_TOKENS = {}

# User consent records (which apps users have authorized)
USER_CONSENTS = {}


# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_code():
    """Generate a random authorization code."""
    return secrets.token_urlsafe(32)


def generate_token():
    """Generate a random access/refresh token."""
    return secrets.token_urlsafe(48)


def validate_client(client_id, client_secret=None, redirect_uri=None):
    """Validate OAuth2 client credentials."""
    if client_id not in REGISTERED_CLIENTS:
        return False, "Invalid client_id"

    client = REGISTERED_CLIENTS[client_id]

    if client_secret and client['client_secret'] != client_secret:
        return False, "Invalid client_secret"

    if redirect_uri and redirect_uri not in client['redirect_uris']:
        return False, f"Invalid redirect_uri. Registered URIs: {client['redirect_uris']}"

    return True, client


def authenticate_user(email, password):
    """Authenticate a user on the OAuth provider."""
    if email not in PROVIDER_USERS:
        return False, "User not found"

    user = PROVIDER_USERS[email]
    if not check_password(password, user['password']):
        return False, "Invalid password"

    return True, user


def create_authorization_code(client_id, user_email, scope, redirect_uri, state):
    """Create an authorization code after user consent."""
    code = generate_code()

    AUTHORIZATION_CODES[code] = {
        'client_id': client_id,
        'user_email': user_email,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state,
        'created_at': datetime.now(timezone.utc),
        'expires_at': datetime.now(timezone.utc) + timedelta(minutes=10),
        'used': False,
    }

    return code


def exchange_code_for_tokens(code, client_id, client_secret, redirect_uri):
    """Exchange authorization code for access and refresh tokens."""
    if code not in AUTHORIZATION_CODES:
        return False, "Invalid authorization code"

    code_data = AUTHORIZATION_CODES[code]

    # Check if code was already used (one-time use)
    if code_data['used']:
        return False, "Authorization code already used (security: codes are one-time use)"

    # Check expiration
    if datetime.now(timezone.utc) > code_data['expires_at']:
        return False, "Authorization code expired"

    # Validate client
    if code_data['client_id'] != client_id:
        return False, "Client ID mismatch"

    # Validate redirect_uri
    if code_data['redirect_uri'] != redirect_uri:
        return False, "Redirect URI mismatch"

    # Validate client_secret
    valid, result = validate_client(client_id, client_secret)
    if not valid:
        return False, result

    # Mark code as used
    code_data['used'] = True

    # Generate tokens
    access_token = generate_token()
    refresh_token = generate_token()

    ACCESS_TOKENS[access_token] = {
        'user_email': code_data['user_email'],
        'client_id': client_id,
        'scope': code_data['scope'],
        'created_at': datetime.now(timezone.utc),
        'expires_at': datetime.now(timezone.utc) + timedelta(hours=1),
    }

    REFRESH_TOKENS[refresh_token] = {
        'user_email': code_data['user_email'],
        'client_id': client_id,
        'scope': code_data['scope'],
        'access_token': access_token,
        'created_at': datetime.now(timezone.utc),
        'expires_at': datetime.now(timezone.utc) + timedelta(days=30),
    }

    return True, {
        'access_token': access_token,
        'token_type': 'Bearer',
        'expires_in': 3600,  # 1 hour in seconds
        'refresh_token': refresh_token,
        'scope': code_data['scope'],
    }


def validate_access_token(token):
    """Validate an access token and return user info."""
    if token not in ACCESS_TOKENS:
        return False, "Invalid access token"

    token_data = ACCESS_TOKENS[token]

    if datetime.now(timezone.utc) > token_data['expires_at']:
        return False, "Access token expired"

    user = PROVIDER_USERS.get(token_data['user_email'])
    if not user:
        return False, "User not found"

    return True, {
        'token_data': token_data,
        'user': user,
    }


def refresh_access_token(refresh_token, client_id, client_secret):
    """Use refresh token to get a new access token."""
    if refresh_token not in REFRESH_TOKENS:
        return False, "Invalid refresh token"

    refresh_data = REFRESH_TOKENS[refresh_token]

    if datetime.now(timezone.utc) > refresh_data['expires_at']:
        return False, "Refresh token expired"

    if refresh_data['client_id'] != client_id:
        return False, "Client ID mismatch"

    # Validate client_secret
    valid, result = validate_client(client_id, client_secret)
    if not valid:
        return False, result

    # Invalidate old access token
    old_access_token = refresh_data['access_token']
    if old_access_token in ACCESS_TOKENS:
        del ACCESS_TOKENS[old_access_token]

    # Generate new access token
    new_access_token = generate_token()

    ACCESS_TOKENS[new_access_token] = {
        'user_email': refresh_data['user_email'],
        'client_id': client_id,
        'scope': refresh_data['scope'],
        'created_at': datetime.now(timezone.utc),
        'expires_at': datetime.now(timezone.utc) + timedelta(hours=1),
    }

    # Update refresh token reference
    refresh_data['access_token'] = new_access_token

    return True, {
        'access_token': new_access_token,
        'token_type': 'Bearer',
        'expires_in': 3600,
        'scope': refresh_data['scope'],
    }


def revoke_token(token, client_id, client_secret):
    """Revoke an access or refresh token."""
    # Validate client
    valid, result = validate_client(client_id, client_secret)
    if not valid:
        return False, result

    if token in ACCESS_TOKENS:
        del ACCESS_TOKENS[token]
        return True, "Access token revoked"

    if token in REFRESH_TOKENS:
        # Also revoke associated access token
        access_token = REFRESH_TOKENS[token].get('access_token')
        if access_token in ACCESS_TOKENS:
            del ACCESS_TOKENS[access_token]
        del REFRESH_TOKENS[token]
        return True, "Refresh token and associated access token revoked"

    return False, "Token not found"


def reset_store():
    """Reset all OAuth2 data (for demo purposes)."""
    AUTHORIZATION_CODES.clear()
    ACCESS_TOKENS.clear()
    REFRESH_TOKENS.clear()
    USER_CONSENTS.clear()
