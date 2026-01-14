"""
OAuth2 Demo Views

This simulates both:
1. An OAuth2 PROVIDER (like Google, GitHub) - handles /authorize, /token, /userinfo
2. An OAuth2 CLIENT (your app) - handles /login, /callback

The demo shows the complete Authorization Code Flow step by step.
"""

import json
from urllib.parse import urlencode, urlparse, parse_qs
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .oauth2_store import (
    REGISTERED_CLIENTS,
    PROVIDER_USERS,
    AUTHORIZATION_CODES,
    ACCESS_TOKENS,
    validate_client,
    authenticate_user,
    create_authorization_code,
    exchange_code_for_tokens,
    validate_access_token,
    refresh_access_token,
    revoke_token,
    reset_store,
)


# ============================================
# DEMO UI PAGES
# ============================================

def home(request):
    """Main demo page with interactive OAuth2 flow visualization."""
    return render(request, 'home.html', {
        'client_id': 'demo-client-id',
        'client_secret': 'demo-client-secret-12345',
        'users': [
            {'email': 'alice@example.com', 'password': 'password123'},
            {'email': 'bob@example.com', 'password': 'secret456'},
        ]
    })


# ============================================
# OAUTH2 PROVIDER ENDPOINTS (Simulating Google/GitHub)
# ============================================

def provider_authorize(request):
    """
    OAuth2 Authorization Endpoint (Provider Side)

    This is like visiting accounts.google.com/oauth/authorize

    STEP 2 of OAuth2 flow:
    - Client redirects user here with client_id, redirect_uri, scope, state
    - Provider shows login/consent page
    - On approval, redirects back to client with authorization code
    """
    # Get OAuth2 parameters from query string
    client_id = request.GET.get('client_id')
    redirect_uri = request.GET.get('redirect_uri')
    response_type = request.GET.get('response_type', 'code')
    scope = request.GET.get('scope', 'profile')
    state = request.GET.get('state', '')

    # Validate client
    valid, result = validate_client(client_id, redirect_uri=redirect_uri)
    if not valid:
        return render(request, 'provider_error.html', {
            'error': result,
            'teaching_point': (
                'The OAuth2 provider validates that the client_id is registered '
                'and the redirect_uri matches what was pre-registered. This prevents '
                'attackers from redirecting authorization codes to malicious sites.'
            )
        })

    # Check response_type
    if response_type != 'code':
        return render(request, 'provider_error.html', {
            'error': f'Unsupported response_type: {response_type}. Only "code" is supported.',
            'teaching_point': 'We implement Authorization Code flow (most secure for server apps).'
        })

    # Store request in session for after login
    request.session['oauth_request'] = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'state': state,
        'client_name': result['name'],
    }

    # Show provider's login page
    return render(request, 'provider_login.html', {
        'client_name': result['name'],
        'scope': scope,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state': state,
    })


@csrf_exempt
def provider_login_submit(request):
    """
    Handle login on the OAuth2 provider.

    TEACHING POINT: User authenticates with the PROVIDER (Google),
    NOT with the client app. The client never sees the user's password!
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    email = request.POST.get('email')
    password = request.POST.get('password')

    # Get OAuth request from session
    oauth_request = request.session.get('oauth_request')
    if not oauth_request:
        return render(request, 'provider_error.html', {
            'error': 'OAuth session expired. Please start over.',
        })

    # Authenticate user
    valid, result = authenticate_user(email, password)
    if not valid:
        return render(request, 'provider_login.html', {
            'error': result,
            'client_name': oauth_request['client_name'],
            'scope': oauth_request['scope'],
            'client_id': oauth_request['client_id'],
            'redirect_uri': oauth_request['redirect_uri'],
            'state': oauth_request['state'],
        })

    # Store authenticated user
    request.session['provider_user'] = email

    # Show consent page
    return render(request, 'provider_consent.html', {
        'user_name': result['name'],
        'user_email': email,
        'client_name': oauth_request['client_name'],
        'scope': oauth_request['scope'],
        'scope_list': oauth_request['scope'].split(),
    })


@csrf_exempt
def provider_consent_submit(request):
    """
    Handle user consent approval/denial.

    TEACHING POINT: User explicitly grants permissions (scopes) to the client app.
    The user can see exactly what data the app is requesting.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    action = request.POST.get('action')
    oauth_request = request.session.get('oauth_request')
    user_email = request.session.get('provider_user')

    if not oauth_request or not user_email:
        return render(request, 'provider_error.html', {
            'error': 'Session expired. Please start over.',
        })

    redirect_uri = oauth_request['redirect_uri']
    state = oauth_request['state']

    if action == 'deny':
        # User denied - redirect with error
        error_params = {
            'error': 'access_denied',
            'error_description': 'User denied the authorization request',
        }
        if state:
            error_params['state'] = state

        return HttpResponseRedirect(f"{redirect_uri}?{urlencode(error_params)}")

    # User approved - create authorization code
    code = create_authorization_code(
        client_id=oauth_request['client_id'],
        user_email=user_email,
        scope=oauth_request['scope'],
        redirect_uri=redirect_uri,
        state=state,
    )

    # Clean up session
    del request.session['oauth_request']
    del request.session['provider_user']

    # Redirect back to client with code
    params = {'code': code}
    if state:
        params['state'] = state

    redirect_url = f"{redirect_uri}?{urlencode(params)}"

    # Show intermediate page for teaching
    return render(request, 'provider_redirect.html', {
        'redirect_url': redirect_url,
        'code': code,
        'state': state,
        'redirect_uri': redirect_uri,
    })


@csrf_exempt
def provider_token(request):
    """
    OAuth2 Token Endpoint (Provider Side)

    This is like https://oauth2.googleapis.com/token

    STEP 4 of OAuth2 flow:
    - Client sends authorization code + client credentials
    - Provider validates and returns access_token + refresh_token
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    # Can receive as form data or JSON
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        data = request.POST

    grant_type = data.get('grant_type')
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')

    if grant_type == 'authorization_code':
        code = data.get('code')
        redirect_uri = data.get('redirect_uri')

        success, result = exchange_code_for_tokens(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )

        if success:
            return JsonResponse(result)
        else:
            return JsonResponse({
                'error': 'invalid_grant',
                'error_description': result,
            }, status=400)

    elif grant_type == 'refresh_token':
        refresh_token = data.get('refresh_token')

        success, result = refresh_access_token(
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
        )

        if success:
            return JsonResponse(result)
        else:
            return JsonResponse({
                'error': 'invalid_grant',
                'error_description': result,
            }, status=400)

    else:
        return JsonResponse({
            'error': 'unsupported_grant_type',
            'error_description': f'Grant type "{grant_type}" is not supported',
        }, status=400)


@csrf_exempt
def provider_userinfo(request):
    """
    OAuth2 UserInfo Endpoint (Protected Resource)

    This is like https://www.googleapis.com/oauth2/v2/userinfo

    STEP 5 of OAuth2 flow:
    - Client sends access_token in Authorization header
    - Provider validates token and returns user data
    """
    # Get access token from Authorization header
    auth_header = request.headers.get('Authorization', '')

    if not auth_header.startswith('Bearer '):
        return JsonResponse({
            'error': 'invalid_request',
            'error_description': 'Missing or invalid Authorization header. Expected: Bearer <token>',
        }, status=401)

    access_token = auth_header[7:]  # Remove 'Bearer ' prefix

    success, result = validate_access_token(access_token)

    if not success:
        return JsonResponse({
            'error': 'invalid_token',
            'error_description': result,
        }, status=401)

    user = result['user']
    scope = result['token_data']['scope']

    # Return user info based on granted scopes
    userinfo = {'sub': user['email']}  # 'sub' is always returned

    if 'profile' in scope:
        userinfo['name'] = user['name']
        userinfo['picture'] = user['picture']

    if 'email' in scope:
        userinfo['email'] = user['email']
        userinfo['email_verified'] = True

    return JsonResponse(userinfo)


@csrf_exempt
def provider_revoke(request):
    """
    OAuth2 Token Revocation Endpoint

    Allows clients to revoke access/refresh tokens (e.g., on logout).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    token = request.POST.get('token')
    client_id = request.POST.get('client_id')
    client_secret = request.POST.get('client_secret')

    if not token:
        return JsonResponse({'error': 'Token required'}, status=400)

    success, message = revoke_token(token, client_id, client_secret)

    if success:
        return JsonResponse({'message': message})
    else:
        return JsonResponse({'error': message}, status=400)


# ============================================
# CLIENT APPLICATION ENDPOINTS (Your App)
# ============================================

def client_callback(request):
    """
    OAuth2 Callback/Redirect URI (Client Side)

    STEP 3 of OAuth2 flow:
    - Provider redirects here with authorization code
    - Client displays the code and prepares to exchange it
    """
    code = request.GET.get('code')
    state = request.GET.get('state')
    error = request.GET.get('error')
    error_description = request.GET.get('error_description')

    if error:
        return render(request, 'client_callback.html', {
            'error': error,
            'error_description': error_description,
            'teaching_point': (
                'The user denied the authorization request, or an error occurred. '
                'Your app should handle this gracefully and not crash.'
            )
        })

    return render(request, 'client_callback.html', {
        'code': code,
        'state': state,
        'client_id': 'demo-client-id',
        'client_secret': 'demo-client-secret-12345',
    })


# ============================================
# API ENDPOINTS FOR DEMO UI
# ============================================

@csrf_exempt
def api_exchange_code(request):
    """API endpoint for the demo UI to exchange code for tokens."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    code = data.get('code')
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    redirect_uri = data.get('redirect_uri')

    success, result = exchange_code_for_tokens(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )

    if success:
        return JsonResponse({
            'success': True,
            'tokens': result,
            'teaching_point': (
                'SUCCESS! The authorization code was exchanged for tokens.\n\n'
                '- access_token: Use this to access protected resources (short-lived)\n'
                '- refresh_token: Use this to get new access tokens (long-lived)\n'
                '- expires_in: Seconds until access_token expires\n\n'
                'SECURITY: This exchange happens server-to-server. The code is '
                'one-time use and expires quickly, so even if intercepted, '
                'it\'s useless without the client_secret.'
            )
        })
    else:
        return JsonResponse({
            'success': False,
            'error': result,
            'teaching_point': (
                'Token exchange FAILED. Common reasons:\n'
                '- Code already used (one-time use)\n'
                '- Code expired (usually 10 min lifetime)\n'
                '- Invalid client credentials\n'
                '- redirect_uri mismatch'
            )
        }, status=400)


@csrf_exempt
def api_get_userinfo(request):
    """API endpoint for the demo UI to fetch user info."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    access_token = data.get('access_token')

    success, result = validate_access_token(access_token)

    if success:
        user = result['user']
        scope = result['token_data']['scope']

        userinfo = {'sub': user['email']}
        if 'profile' in scope:
            userinfo['name'] = user['name']
            userinfo['picture'] = user['picture']
        if 'email' in scope:
            userinfo['email'] = user['email']

        return JsonResponse({
            'success': True,
            'userinfo': userinfo,
            'scope': scope,
            'teaching_point': (
                'SUCCESS! The access token was valid and user info was returned.\n\n'
                'Notice that only data matching the requested SCOPES is returned:\n'
                f'- Requested scopes: {scope}\n'
                '- profile scope: name, picture\n'
                '- email scope: email address\n\n'
                'The user explicitly consented to share this data.'
            )
        })
    else:
        return JsonResponse({
            'success': False,
            'error': result,
            'teaching_point': (
                'Access denied! The token was invalid or expired.\n'
                'Use the refresh token to get a new access token.'
            )
        }, status=401)


@csrf_exempt
def api_refresh_token(request):
    """API endpoint for the demo UI to refresh tokens."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    refresh_token = data.get('refresh_token')
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')

    success, result = refresh_access_token(refresh_token, client_id, client_secret)

    if success:
        return JsonResponse({
            'success': True,
            'tokens': result,
            'teaching_point': (
                'New access token issued using refresh token!\n\n'
                'REFRESH TOKEN FLOW:\n'
                '1. Access token expires (usually 1 hour)\n'
                '2. Client uses refresh token to get new access token\n'
                '3. User doesn\'t need to re-authenticate\n'
                '4. Old access token is invalidated\n\n'
                'This provides security (short-lived access) + UX (no constant re-login).'
            )
        })
    else:
        return JsonResponse({
            'success': False,
            'error': result,
            'teaching_point': (
                'Refresh failed! The refresh token may be:\n'
                '- Expired (usually 30 days)\n'
                '- Revoked by user or admin\n'
                '- Invalid\n\n'
                'User must re-authenticate through the full OAuth2 flow.'
            )
        }, status=400)


@csrf_exempt
def api_revoke_token(request):
    """API endpoint for the demo UI to revoke tokens."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    token = data.get('token')
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')

    success, message = revoke_token(token, client_id, client_secret)

    if success:
        return JsonResponse({
            'success': True,
            'message': message,
            'teaching_point': (
                'Token revoked successfully!\n\n'
                'WHEN TO REVOKE:\n'
                '- User logs out\n'
                '- User disconnects app from their account\n'
                '- Security incident detected\n'
                '- Admin revokes access\n\n'
                'Once revoked, the token cannot be used even if not expired.'
            )
        })
    else:
        return JsonResponse({
            'success': False,
            'error': message,
        }, status=400)


@csrf_exempt
def api_reset(request):
    """Reset OAuth2 demo state."""
    reset_store()
    return JsonResponse({
        'success': True,
        'message': 'OAuth2 demo state reset. All codes and tokens cleared.'
    })


@csrf_exempt
def api_inspect_store(request):
    """Inspect current OAuth2 store state (for demo transparency)."""
    return JsonResponse({
        'authorization_codes': {
            code: {
                'client_id': data['client_id'],
                'user_email': data['user_email'],
                'scope': data['scope'],
                'used': data['used'],
                'expires_at': data['expires_at'].isoformat(),
            }
            for code, data in AUTHORIZATION_CODES.items()
        },
        'access_tokens': {
            token[:20] + '...': {
                'user_email': data['user_email'],
                'scope': data['scope'],
                'expires_at': data['expires_at'].isoformat(),
            }
            for token, data in ACCESS_TOKENS.items()
        },
        'registered_clients': list(REGISTERED_CLIENTS.keys()),
        'teaching_point': (
            'This shows the OAuth2 provider\'s internal state.\n'
            'In production, this would be stored securely in a database.'
        )
    })
