# OAuth2 Authorization Code Flow Demo

An interactive educational Django project demonstrating how OAuth2 "Login with Google/GitHub" works.

## Setup

```bash
cd oauth2_demo

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

## Demo Provider Users

| Email              | Password    |
|--------------------|-------------|
| alice@example.com  | password123 |
| bob@example.com    | secret456   |

## The Three Actors

1. **User** - The person who wants to use your app
2. **Client App** - Your application (has client_id + client_secret)
3. **OAuth Provider** - Google, GitHub, etc. (holds user data)

## The Authorization Code Flow (6 Steps)

### Step 1: User Clicks "Login with Provider"
- Client constructs authorization URL
- Includes: client_id, redirect_uri, scope, state

### Step 2: Redirect to Provider
- User is sent to provider's domain (accounts.google.com)
- Provider validates client_id and redirect_uri

### Step 3: User Authenticates & Consents
- User logs in to PROVIDER (not your app!)
- User sees consent screen showing requested permissions
- User approves or denies

### Step 4: Provider Redirects with Code
- Provider generates one-time authorization code
- Redirects back to your app's callback URL
- Code in URL: `?code=xyz123&state=abc`

### Step 5: Exchange Code for Tokens (Server-to-Server)
- Your server sends: code + client_id + client_secret
- Provider validates and returns: access_token + refresh_token
- This happens server-side, never exposed to browser

### Step 6: Access Protected Resources
- Send access_token in Authorization header
- Provider returns user data based on granted scopes

## Security Features Demonstrated

### Why Authorization Code Flow?
- Code is short-lived (10 min) and one-time use
- client_secret never exposed to browser
- Even if code is intercepted, attacker needs secret

### State Parameter (CSRF Protection)
- Random string sent with auth request
- Must match when callback is received
- Prevents cross-site request forgery attacks

### Scopes (Principle of Least Privilege)
- Request only what you need
- User sees exactly what data you're requesting
- More scopes = users less likely to approve

### Refresh Tokens
- Access tokens are short-lived (1 hour)
- Refresh tokens are long-lived (30+ days)
- Get new access tokens without re-authentication

## Key Teaching Points

1. **User credentials stay with provider** - Your app never sees passwords
2. **Authorization code != Access token** - Code is exchanged server-side
3. **client_secret is SECRET** - Never expose to frontend
4. **Scopes limit access** - Users control what data is shared
5. **Short-lived access tokens** - Limit damage if stolen
6. **State prevents CSRF** - Always validate on callback
