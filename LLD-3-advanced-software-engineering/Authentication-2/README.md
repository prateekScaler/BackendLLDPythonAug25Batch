# Authentication Demos

Three Django demo applications demonstrating different authentication methods with clean, tabbed interfaces.

## Demos

| Demo | Port | Description |
|------|------|-------------|
| session_demo | 8001 | Session-based authentication with cookies |
| jwt_demo | 8002 | JWT (JSON Web Token) authentication |
| oauth2_demo | 8003 | OAuth2 Authorization Code Flow |

## Quick Start

```bash
./run_all.sh
```

This script automatically:
- Detects Python installation
- Installs all dependencies (Django, PyJWT, etc.)
- Runs database migrations for each demo
- Starts all three servers simultaneously
- Labels output from each server for easy debugging

Press `Ctrl+C` to stop all servers.

## Access the Demos

After running `./run_all.sh`:

- **Session Demo:** http://localhost:8001
- **JWT Demo:** http://localhost:8002
- **OAuth2 Demo:** http://localhost:8003

## Features

Each demo includes:
- Clean tabbed interface for easy navigation
- Step-by-step walkthrough of the authentication flow
- Teaching points explaining security concepts
- Interactive experiments to understand how each method works

## Access Tokens vs Refresh Tokens

Modern JWT authentication uses a **two-token system** for security:

| Token Type | Lifespan | Purpose | Storage |
|------------|----------|---------|---------|
| **Access Token** | 15-30 minutes | Short-lived, used for API requests | Memory or HttpOnly cookie |
| **Refresh Token** | 7-30 days | Long-lived, used only to get new access tokens | HttpOnly cookie (secure) |

### Why Two Tokens?

```
Problem with Single Long-Lived Token:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Token valid for 30 days → If stolen, attacker has 30 days of access!

Solution: Two-Token System
━━━━━━━━━━━━━━━━━━━━━━━━━━
Access token (15 min) → If stolen, attacker only has 15 min
Refresh token (30 days) → Stored securely, rarely transmitted
```

### Token Flow

```
1. Login → Get both tokens
2. API Request → Use access token (Authorization: Bearer <token>)
3. Access token expires → Use refresh token to get new access token
4. Refresh token expires → User must login again
```

### Security Best Practices

- **Access tokens**: Can be stored in memory (JavaScript variable)
- **Refresh tokens**: Must be stored in HttpOnly cookies (XSS-safe)
- **Refresh token rotation**: Each use invalidates the old refresh token
- **Never store sensitive data** in JWT payload (it's only base64 encoded, not encrypted)

For detailed explanation with diagrams, see: `auth2_guide/04b_access_refresh_tokens.html`

## Running Individually

```bash
# Session demo
cd session_demo && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver

# JWT demo
cd jwt_demo && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver

# OAuth2 demo
cd oauth2_demo && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
```
