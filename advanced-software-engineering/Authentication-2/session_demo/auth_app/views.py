"""
Views for Session-Based Authentication Demo
============================================

This file contains all the views for demonstrating:
1. Session creation and management
2. Cookie attributes (HttpOnly, Secure, SameSite)
3. Login/Logout flow
4. Session data storage
5. Custom cookie creation
6. CORS behavior

Each view is documented with what to observe in the browser.
"""

import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings


# =============================================================================
# HOME PAGE - Dashboard for all demos
# =============================================================================

def home(request):
    """
    Main demo dashboard page.

    WHAT TO OBSERVE:
    - Open DevTools > Application > Cookies
    - You'll see 'csrftoken' cookie (for CSRF protection)
    - After login, you'll see 'sessionid' cookie too
    """
    context = {
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None,
        'session_key': request.session.session_key,
        'session_data': dict(request.session) if request.session.session_key else {},
    }
    return render(request, 'home.html', context)


# =============================================================================
# SESSION INFO API - See what's in the session
# =============================================================================

def session_info(request):
    """
    API endpoint that returns current session information.

    WHAT TO OBSERVE:
    - Session key (the value in your sessionid cookie)
    - Session data (what the server stores)
    - Whether user is authenticated

    DEMO: Call this before and after login to see the difference!
    """
    return JsonResponse({
        'session_key': request.session.session_key,
        'session_data': dict(request.session),
        'is_authenticated': request.user.is_authenticated,
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        } if request.user.is_authenticated else None,
        'session_cookie_name': settings.SESSION_COOKIE_NAME,
        'session_cookie_age': settings.SESSION_COOKIE_AGE,
        'session_cookie_httponly': settings.SESSION_COOKIE_HTTPONLY,
        'session_cookie_secure': settings.SESSION_COOKIE_SECURE,
        'session_cookie_samesite': settings.SESSION_COOKIE_SAMESITE,
    })


# =============================================================================
# LOGIN API
# =============================================================================

@csrf_exempt  # Disable CSRF for demo simplicity (don't do this in production!)
@require_http_methods(["POST"])
def login_view(request):
    """
    Login endpoint that creates a session.

    WHAT TO OBSERVE (in DevTools > Network):
    1. Request: POST with username/password
    2. Response Headers: Set-Cookie: sessionid=xxx; HttpOnly; Path=/; ...
    3. After this, check Application > Cookies for new sessionid

    WHAT TO OBSERVE (in DevTools > Application > Cookies):
    - New 'sessionid' cookie appears
    - Check the HttpOnly, Secure, SameSite columns
    - Note the Expires date (based on SESSION_COOKIE_AGE)

    REQUEST BODY:
    {
        "username": "testuser",
        "password": "testpass123"
    }
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Authenticate using Django's built-in authentication
    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({
            'error': 'Invalid credentials',
            'hint': 'Use username: testuser, password: testpass123'
        }, status=401)

    # This is the KEY LINE - it creates the session!
    # Django will:
    # 1. Generate a random session_id
    # 2. Store session data in the database (or cache/file based on settings)
    # 3. Set the sessionid cookie in the response
    login(request, user)

    return JsonResponse({
        'message': 'Login successful!',
        'user': {
            'id': user.id,
            'username': user.username,
        },
        'session_key': request.session.session_key,
        'explanation': (
            'Check DevTools > Application > Cookies. '
            'You should see a new "sessionid" cookie. '
            'This cookie will be sent with every subsequent request automatically!'
        )
    })


# =============================================================================
# LOGOUT API
# =============================================================================

@csrf_exempt
def logout_view(request):
    """
    Logout endpoint that destroys the session.

    WHAT TO OBSERVE:
    1. Before: sessionid cookie exists
    2. After: sessionid cookie is deleted (or set to expire immediately)
    3. Response Headers: Set-Cookie with expires in the past

    DEMO: Check the session_info before and after logout
    """
    # Store session key for demo output
    old_session_key = request.session.session_key

    # This destroys the session!
    # Django will:
    # 1. Delete session data from the database
    # 2. Send a Set-Cookie header to delete the cookie
    logout(request)

    return JsonResponse({
        'message': 'Logged out successfully!',
        'old_session_key': old_session_key,
        'explanation': (
            'The session has been destroyed. '
            'Check DevTools > Application > Cookies - '
            'the sessionid cookie should be gone!'
        )
    })


# =============================================================================
# PROTECTED RESOURCE - Requires authentication
# =============================================================================

def protected_resource(request):
    """
    A protected endpoint that requires authentication.

    WHAT TO OBSERVE:
    - Without login: Returns 401 Unauthorized
    - With login: Returns the secret data

    DEMO:
    1. Try accessing this without logging in
    2. Login and try again
    3. The difference is the sessionid cookie being sent!
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Unauthorized',
            'message': 'You must be logged in to access this resource',
            'hint': 'Login first, then the browser will automatically send the session cookie'
        }, status=401)

    return JsonResponse({
        'message': 'Welcome to the protected resource!',
        'secret_data': 'This is secret data only for authenticated users',
        'user': {
            'id': request.user.id,
            'username': request.user.username,
        },
        'how_it_works': (
            'The browser automatically sent the sessionid cookie. '
            'Django looked up the session in the database and found your user!'
        )
    })


# =============================================================================
# SET CUSTOM COOKIE - Demonstrate cookie attributes
# =============================================================================

@csrf_exempt
def set_custom_cookie(request):
    """
    Demonstrates setting a custom cookie with various attributes.

    WHAT TO OBSERVE:
    1. The new cookie in DevTools > Application > Cookies
    2. Compare attributes with the sessionid cookie
    3. Try accessing document.cookie in console - which cookies appear?

    QUERY PARAMS (to customize the cookie):
    - httponly: true/false
    - secure: true/false
    - samesite: Strict/Lax/None
    - max_age: seconds (e.g., 60 for 1 minute)
    """
    # Get parameters from query string
    httponly = request.GET.get('httponly', 'true').lower() == 'true'
    secure = request.GET.get('secure', 'false').lower() == 'true'
    samesite = request.GET.get('samesite', 'Lax')
    max_age = int(request.GET.get('max_age', 3600))
    cookie_name = request.GET.get('name', 'demo_cookie')
    cookie_value = f'demo_value_{datetime.now().strftime("%H%M%S")}'

    response = JsonResponse({
        'message': f'Cookie "{cookie_name}" has been set!',
        'cookie_settings': {
            'name': cookie_name,
            'value': cookie_value,
            'httponly': httponly,
            'secure': secure,
            'samesite': samesite,
            'max_age': max_age,
        },
        'try_this': (
            f'Open browser console and type: document.cookie '
            f'If HttpOnly is {httponly}, the cookie will {"NOT " if httponly else ""}appear!'
        )
    })

    # Set the cookie with specified attributes
    response.set_cookie(
        cookie_name,
        cookie_value,
        max_age=max_age,
        httponly=httponly,
        secure=secure,
        samesite=samesite,
    )

    return response


# =============================================================================
# DELETE CUSTOM COOKIE
# =============================================================================

@csrf_exempt
def delete_custom_cookie(request):
    """
    Deletes a custom cookie.

    QUERY PARAMS:
    - name: cookie name to delete (default: demo_cookie)
    """
    cookie_name = request.GET.get('name', 'demo_cookie')

    response = JsonResponse({
        'message': f'Cookie "{cookie_name}" has been deleted!',
        'explanation': 'Check DevTools > Application > Cookies'
    })

    response.delete_cookie(cookie_name)

    return response


# =============================================================================
# SESSION DATA MANIPULATION
# =============================================================================

@csrf_exempt
def set_session_data(request):
    """
    Store arbitrary data in the session.

    WHAT TO OBSERVE:
    - Session data is stored on the SERVER, not in the cookie
    - The cookie only contains the session_id
    - All the actual data is in Django's database

    REQUEST BODY:
    {
        "key": "favorite_color",
        "value": "blue"
    }
    """
    try:
        data = json.loads(request.body)
        key = data.get('key')
        value = data.get('value')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not key:
        return JsonResponse({'error': 'Key is required'}, status=400)

    # Store in session - this is saved to the database!
    request.session[key] = value

    return JsonResponse({
        'message': f'Stored "{key}" = "{value}" in session',
        'session_key': request.session.session_key,
        'all_session_data': dict(request.session),
        'explanation': (
            'This data is stored on the SERVER in the database. '
            'The browser only has the session_id cookie - '
            'it cannot see or modify this data!'
        )
    })


def get_session_data(request):
    """
    Get all data stored in the current session.

    WHAT TO OBSERVE:
    - The session_id in your cookie maps to this data on the server
    - Users cannot tamper with this data (unlike JWT payloads!)
    """
    return JsonResponse({
        'session_key': request.session.session_key,
        'session_data': dict(request.session),
        'explanation': (
            'This data is stored securely on the server. '
            'The client only has the session_id - no way to read or modify!'
        )
    })


# =============================================================================
# CORS DEMO ENDPOINT
# =============================================================================

def cors_demo(request):
    """
    Endpoint to test CORS behavior.

    WHAT TO OBSERVE:
    1. Response headers (Access-Control-Allow-*)
    2. Whether cookies are sent from different origins
    3. Preflight OPTIONS requests

    DEMO:
    1. Open this page: http://localhost:8000/cors-test/
    2. Click the button to make a request from a different origin
    3. Check Network tab for CORS headers
    """
    return JsonResponse({
        'message': 'CORS demo endpoint',
        'origin': request.headers.get('Origin', 'Same origin (no Origin header)'),
        'cookies_received': dict(request.COOKIES),
        'is_authenticated': request.user.is_authenticated,
        'cors_settings': {
            'CORS_ALLOW_ALL_ORIGINS': settings.CORS_ALLOW_ALL_ORIGINS,
            'CORS_ALLOW_CREDENTIALS': settings.CORS_ALLOW_CREDENTIALS,
            'CORS_ALLOWED_ORIGINS': getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
        }
    })


# =============================================================================
# HEADERS INFO - Show all request headers
# =============================================================================

def headers_info(request):
    """
    Shows all HTTP headers received by the server.

    WHAT TO OBSERVE:
    - Cookie header (contains all cookies)
    - Origin header (for CORS)
    - User-Agent, Accept, etc.

    DEMO: Compare headers from browser vs curl/Postman
    """
    headers = {}
    for key, value in request.headers.items():
        headers[key] = value

    return JsonResponse({
        'headers': headers,
        'cookies': dict(request.COOKIES),
        'method': request.method,
        'path': request.path,
    })


# =============================================================================
# CREATE TEST USER - For demo purposes
# =============================================================================

@csrf_exempt
def create_test_user(request):
    """
    Creates a test user for demo purposes.

    This will create:
    - Username: testuser
    - Password: testpass123
    """
    try:
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        return JsonResponse({
            'message': 'Test user created!',
            'credentials': {
                'username': 'testuser',
                'password': 'testpass123'
            }
        })
    except Exception as e:
        # User might already exist
        return JsonResponse({
            'message': 'User already exists or error occurred',
            'credentials': {
                'username': 'testuser',
                'password': 'testpass123'
            },
            'error': str(e)
        })


# =============================================================================
# CORS TEST PAGE - HTML page to test cross-origin requests
# =============================================================================

def cors_test_page(request):
    """
    HTML page that simulates a different origin making requests.
    """
    return render(request, 'cors_test.html')
