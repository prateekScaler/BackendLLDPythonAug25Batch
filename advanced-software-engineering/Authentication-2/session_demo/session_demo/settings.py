"""
Django Settings for Session-Based Authentication Demo
======================================================

This settings file is designed for LIVE TEACHING.
Each section has toggleable options with explanations.

HOW TO USE:
1. Toggle settings ON/OFF to demonstrate different behaviors
2. Restart server after changes: python manage.py runserver
3. Check browser DevTools > Application > Cookies to see effects

"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# SECURITY WARNING: Keep the secret key used in production secret!
# For demo purposes only - never use this in production!
# =============================================================================
SECRET_KEY = 'demo-secret-key-for-teaching-purposes-only-12345'

# =============================================================================
# DEBUG MODE
# ----------
# True  = Show detailed error pages (for development)
# False = Show generic error pages (for production)
# =============================================================================
DEBUG = True

ALLOWED_HOSTS = ['*']  # Allow all hosts for demo purposes


# =============================================================================
# INSTALLED APPS
# =============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',        # <-- Required for session-based auth!
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'corsheaders',                     # <-- For CORS demo (pip install django-cors-headers)

    # Our demo app
    'auth_app',
]


# =============================================================================
# MIDDLEWARE
# ----------
# Order matters! CorsMiddleware should be at the top.
# SessionMiddleware is required for session-based authentication.
# =============================================================================
MIDDLEWARE = [
    # CORS middleware - must be BEFORE CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    # Session middleware - THIS IS WHAT ENABLES SESSIONS!
    # Try commenting this out and see what happens to sessions
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    # CSRF middleware - protects against Cross-Site Request Forgery
    # Try toggling this to see CSRF protection in action
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'session_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'session_demo.wsgi.application'


# =============================================================================
# DATABASE
# --------
# Using SQLite for simplicity. Sessions will be stored in database by default.
# =============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =============================================================================
# PASSWORD VALIDATION (simplified for demo)
# =============================================================================
AUTH_PASSWORD_VALIDATORS = []


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# =============================================================================
# STATIC FILES
# =============================================================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
#                    SESSION CONFIGURATION
# =============================================================================
# This is the MAIN section for teaching sessions!
# =============================================================================

# -----------------------------------------------------------------------------
# SESSION ENGINE - Where sessions are stored
# -----------------------------------------------------------------------------
# TOGGLE BETWEEN THESE OPTIONS TO DEMONSTRATE DIFFERENT STORAGE:

# Option 1: Database-backed sessions (DEFAULT)
# Sessions stored in django_session table
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Option 2: Cache-backed sessions (faster, needs Redis/Memcached)
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Option 3: File-based sessions
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_FILE_PATH = BASE_DIR / 'sessions'  # Create this folder

# Option 4: Cookie-based sessions (stored in browser, signed but visible!)
# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


# -----------------------------------------------------------------------------
# SESSION COOKIE NAME
# -----------------------------------------------------------------------------
# The name of the cookie. Check DevTools > Application > Cookies
# Try changing this and see the cookie name change!
SESSION_COOKIE_NAME = 'sessionid'  # Default Django name
# SESSION_COOKIE_NAME = 'my_app_session'  # Custom name


# -----------------------------------------------------------------------------
# SESSION COOKIE AGE (in seconds)
# -----------------------------------------------------------------------------
# How long until the session expires
# Try different values and watch the cookie expiry in DevTools!

SESSION_COOKIE_AGE = 60 * 60  # 1 hour (for demo - see it expire quickly)
# SESSION_COOKIE_AGE = 60 * 5  # 5 minutes (even quicker for demo!)
# SESSION_COOKIE_AGE = 60 * 60 * 24  # 24 hours
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2 weeks (Django default)


# -----------------------------------------------------------------------------
# SESSION EXPIRE AT BROWSER CLOSE
# -----------------------------------------------------------------------------
# If True, session expires when browser closes (session cookie)
# If False, session persists based on SESSION_COOKIE_AGE

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Cookie deleted on browser close


# -----------------------------------------------------------------------------
# HTTPONLY FLAG - JavaScript Access Prevention
# -----------------------------------------------------------------------------
# True  = JavaScript CANNOT read this cookie (document.cookie won't show it)
# False = JavaScript CAN read this cookie
#
# DEMO: Toggle this and run in browser console:
#       console.log(document.cookie)
#       With HttpOnly=True, session cookie won't appear!

SESSION_COOKIE_HTTPONLY = True  # SECURE - Recommended!
# SESSION_COOKIE_HTTPONLY = False  # INSECURE - For demo only!


# -----------------------------------------------------------------------------
# SECURE FLAG - HTTPS Only
# -----------------------------------------------------------------------------
# True  = Cookie only sent over HTTPS
# False = Cookie sent over HTTP and HTTPS
#
# For localhost demo, keep this False. In production, use True!

SESSION_COOKIE_SECURE = False  # For localhost demo
# SESSION_COOKIE_SECURE = True  # For production (HTTPS only)


# -----------------------------------------------------------------------------
# SAMESITE FLAG - CSRF Protection
# -----------------------------------------------------------------------------
# 'Strict' = Cookie only sent for same-site requests (maximum security)
# 'Lax'    = Cookie sent for same-site + top-level navigations (balanced)
# 'None'   = Cookie always sent (requires Secure=True)
# False    = Don't set SameSite attribute
#
# DEMO: Try 'Strict' and then access from a different origin!

SESSION_COOKIE_SAMESITE = 'Lax'  # Good default
# SESSION_COOKIE_SAMESITE = 'Strict'  # Maximum security
# SESSION_COOKIE_SAMESITE = 'None'  # Allows cross-site (needs Secure=True)


# -----------------------------------------------------------------------------
# SESSION COOKIE DOMAIN
# -----------------------------------------------------------------------------
# None = Cookie only valid for exact domain
# '.example.com' = Cookie valid for all subdomains

SESSION_COOKIE_DOMAIN = None  # Default - current domain only
# SESSION_COOKIE_DOMAIN = '.localhost'  # All localhost subdomains


# -----------------------------------------------------------------------------
# SESSION COOKIE PATH
# -----------------------------------------------------------------------------
# '/' = Cookie sent for all paths on the domain

SESSION_COOKIE_PATH = '/'


# =============================================================================
#                    CSRF COOKIE CONFIGURATION
# =============================================================================
# Similar settings for CSRF token cookie

CSRF_COOKIE_HTTPONLY = False  # False so JavaScript can read it for AJAX
CSRF_COOKIE_SECURE = False    # For localhost demo
CSRF_COOKIE_SAMESITE = 'Lax'


# =============================================================================
#                    CORS CONFIGURATION
# =============================================================================
# Cross-Origin Resource Sharing - for when frontend and backend are on
# different domains/ports.
#
# Install: pip install django-cors-headers
# =============================================================================

# -----------------------------------------------------------------------------
# ALLOW ALL ORIGINS (for demo only - NEVER use in production!)
# -----------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True  # Allow any origin (demo only!)
# CORS_ALLOW_ALL_ORIGINS = False  # Restrict to specific origins


# -----------------------------------------------------------------------------
# ALLOWED ORIGINS (when CORS_ALLOW_ALL_ORIGINS = False)
# -----------------------------------------------------------------------------
# Specify exactly which origins can make requests
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # React dev server
    "http://127.0.0.1:3000",
    "http://localhost:5173",      # Vite dev server
    "http://localhost:8080",      # Vue dev server
]


# -----------------------------------------------------------------------------
# ALLOW CREDENTIALS (cookies, auth headers)
# -----------------------------------------------------------------------------
# True  = Browser will send cookies with cross-origin requests
# False = Browser won't send cookies (stateless API)
#
# DEMO: Toggle this and see if session cookie is sent from different origin!

CORS_ALLOW_CREDENTIALS = True  # Allow cookies in CORS requests
# CORS_ALLOW_CREDENTIALS = False  # Don't allow cookies


# -----------------------------------------------------------------------------
# ALLOWED HEADERS
# -----------------------------------------------------------------------------
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# -----------------------------------------------------------------------------
# ALLOWED METHODS
# -----------------------------------------------------------------------------
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]


# =============================================================================
#                    LOGGING (for debugging)
# =============================================================================
# Uncomment to see detailed request/response logs

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }


# =============================================================================
# QUICK REFERENCE: Cookie Attributes in Browser DevTools
# =============================================================================
#
# When you open DevTools > Application > Cookies, you'll see:
#
# | Attribute | What It Means                                    |
# |-----------|--------------------------------------------------|
# | Name      | Cookie name (sessionid, csrftoken, etc.)         |
# | Value     | The actual session ID (random string)            |
# | Domain    | Which domain this cookie belongs to              |
# | Path      | URL path the cookie applies to                   |
# | Expires   | When the cookie expires (or "Session")           |
# | Size      | Size of the cookie in bytes                      |
# | HttpOnly  | Check = JavaScript can't read it                 |
# | Secure    | Check = Only sent over HTTPS                     |
# | SameSite  | Strict/Lax/None - CSRF protection level          |
#
# =============================================================================
