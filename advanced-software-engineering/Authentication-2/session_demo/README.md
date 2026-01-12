# Session-Based Authentication Demo

A Django project designed for **live teaching** session-based authentication concepts.

## Quick Start

```bash
# Navigate to project directory
cd session_demo

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django django-cors-headers

# Run migrations (creates database and session tables)
python manage.py migrate

# Start the server
python manage.py runserver
```

Open http://localhost:8000 in your browser!

---

## What This Demo Covers

| Concept | What Students Will Learn |
|---------|-------------------------|
| **Sessions** | How server-side session storage works |
| **Cookies** | Session ID cookies, HttpOnly, Secure, SameSite flags |
| **Login/Logout** | Complete authentication flow |
| **CORS** | Cross-origin requests with cookies |
| **Headers** | Request/response headers in authentication |

---

## Demo Walkthrough

### Demo 1: Understanding Sessions

**Objective:** Show that sessions store data on the SERVER, not in the cookie.

1. Open http://localhost:8000
2. Open DevTools → Application → Cookies
3. Click **"Create Test User"** (only needed once)
4. Click **"Login"**
5. **Observe:**
   - New `sessionid` cookie appears
   - The cookie value is just a random ID (e.g., `abc123xyz`)
   - Click **"Get Session Info"** to see what's stored on the server

**Key Teaching Point:**
```
Browser cookie: sessionid=abc123xyz  (just an ID!)
Server stores:  {user_id: 1, is_authenticated: true, ...}

The client CANNOT see or modify the server data!
```

### Demo 2: Cookie Attributes

**Objective:** Show how HttpOnly prevents JavaScript access.

1. Go to **"Cookie Attributes Demo"** section
2. Create a cookie WITH HttpOnly checked
3. Open browser console, type: `document.cookie`
4. Notice the cookie does NOT appear!
5. Now create a cookie WITHOUT HttpOnly
6. Type `document.cookie` again - now it appears!

**Key Teaching Point:**
```javascript
// With HttpOnly = true
document.cookie  // Returns: ""  (can't see session cookie!)

// With HttpOnly = false
document.cookie  // Returns: "demo_cookie=value123"
```

### Demo 3: Protected Resources

**Objective:** Show how sessions enable authentication.

1. Click **"Logout"** first
2. Click **"Access Protected Resource"**
3. **Result:** 401 Unauthorized
4. Click **"Login"**
5. Click **"Access Protected Resource"** again
6. **Result:** Success! Secret data returned

**What's happening:**
```
Without login:
Browser → GET /api/protected/ (no sessionid cookie)
Server  → "I don't know who you are!" → 401

With login:
Browser → GET /api/protected/ + Cookie: sessionid=abc123
Server  → Looks up abc123 → "Ah, you're John!" → 200 + data
```

### Demo 4: CORS with Cookies

**Objective:** Show CORS complexity with cookies.

1. Go to http://localhost:8000/cors-test/
2. Read the explanation of same-origin vs cross-origin
3. Make a cross-origin request WITH credentials
4. Check Network tab for:
   - `Access-Control-Allow-Origin` header
   - `Access-Control-Allow-Credentials` header

**Key Teaching Point:**
```
When credentials: 'include' is used:
- Access-Control-Allow-Origin CANNOT be "*"
- Must specify exact origin
- Access-Control-Allow-Credentials: true required
```

---

## Settings to Toggle (Live Demo)

Open `session_demo/settings.py` and toggle these settings:

### Session Cookie Age
```python
# Short expiry - watch it expire!
SESSION_COOKIE_AGE = 60 * 5  # 5 minutes

# Long expiry
SESSION_COOKIE_AGE = 60 * 60 * 24  # 24 hours
```

### HttpOnly Flag
```python
# SECURE - JavaScript can't read
SESSION_COOKIE_HTTPONLY = True

# INSECURE - JavaScript can read (demo only!)
SESSION_COOKIE_HTTPONLY = False
```

### SameSite Flag
```python
# Strict - maximum CSRF protection
SESSION_COOKIE_SAMESITE = 'Strict'

# Lax - balanced (default)
SESSION_COOKIE_SAMESITE = 'Lax'

# None - allows cross-site (requires Secure=True)
SESSION_COOKIE_SAMESITE = 'None'
```

### Session Storage
```python
# Database (default)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Cookie-based (visible in browser!)
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
```

**Remember:** Restart the server after changing settings!

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Demo dashboard |
| `/api/create-user/` | POST | Create test user |
| `/api/login/` | POST | Login (create session) |
| `/api/logout/` | POST | Logout (destroy session) |
| `/api/session/` | GET | View session info |
| `/api/session/set/` | POST | Store data in session |
| `/api/session/data/` | GET | Get all session data |
| `/api/protected/` | GET | Protected resource |
| `/api/cookie/set/` | GET | Set custom cookie |
| `/api/cookie/delete/` | GET | Delete custom cookie |
| `/api/headers/` | GET | View request headers |
| `/api/cors/` | GET | CORS test endpoint |
| `/cors-test/` | GET | CORS test page |

---

## Browser DevTools Guide

### Where to Find Cookies
```
Chrome/Edge:
DevTools (F12) → Application → Storage → Cookies → localhost:8000

Firefox:
DevTools (F12) → Storage → Cookies → http://localhost:8000
```

### Cookie Attributes to Show Students
| Column | Meaning |
|--------|---------|
| Name | Cookie name (sessionid, csrftoken) |
| Value | The session ID (random string) |
| Domain | Which domain owns this cookie |
| Path | URL path the cookie applies to |
| Expires | When the cookie expires |
| HttpOnly | ✓ = JavaScript can't read it |
| Secure | ✓ = Only sent over HTTPS |
| SameSite | CSRF protection level |

### Network Tab - What to Show
1. Login request → Response headers show `Set-Cookie`
2. Subsequent requests → Request headers show `Cookie`
3. CORS requests → Look for `Access-Control-*` headers

---

## Common Demo Scenarios

### Scenario 1: "Why can't I stay logged in?"
Toggle `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`, close and reopen browser.

### Scenario 2: "What if someone steals my cookie?"
1. Login and copy the sessionid value
2. Open incognito window
3. Manually set the cookie (via DevTools)
4. Access protected resource - you're "logged in"!

**Lesson:** This is why we use HttpOnly, Secure, short expiry!

### Scenario 3: "Why does my session data disappear?"
1. Store data in session
2. Change `SESSION_ENGINE` to `'signed_cookies'`
3. Restart server
4. Old session is gone (different storage!)

---

## Troubleshooting

### "No module named 'corsheaders'"
```bash
pip install django-cors-headers
```

### "OperationalError: no such table: django_session"
```bash
python manage.py migrate
```

### "Invalid credentials" on login
```bash
# Create test user first
curl -X POST http://localhost:8000/api/create-user/
```

### CORS errors in console
Check that `CORS_ALLOW_ALL_ORIGINS = True` in settings.py

---

## File Structure

```
session_demo/
├── manage.py
├── README.md
├── session_demo/
│   ├── __init__.py
│   ├── settings.py      ← Main settings (toggle options here!)
│   ├── urls.py
│   └── wsgi.py
├── auth_app/
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   └── views.py         ← All demo endpoints
├── templates/
│   ├── home.html        ← Main demo dashboard
│   └── cors_test.html   ← CORS demo page
└── static/
```

---

### Key Concepts to Emphasize
1. **Session ID ≠ Session Data** - The cookie only has the ID!
2. **HttpOnly is critical** - Prevents XSS from stealing sessions
3. **Server controls everything** - Can invalidate sessions instantly
4. **CORS + Cookies is tricky** - Need explicit configuration

---

Happy Teaching! 🎓
