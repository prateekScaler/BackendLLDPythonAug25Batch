# OAuth 2.0 Concepts

## Think About This First...

We already have sessions and JWTs. Before diving into OAuth, think through these real-world scenarios:

**Q1:** You're building a website and want users to log in. Sessions or JWT can do this. Why would you need anything else?

> Sessions and JWT work great when users create accounts on **your** site. But OAuth solves a different problem: letting users log in with an **existing identity** (Google, GitHub) without creating yet another password.

**Q2:** **CRED** wants to fetch your credit card statements from HDFC Bank to show your spending patterns. How does CRED get access to your bank data?

> Without OAuth, you'd have to share your HDFC netbanking password with CRED! OAuth lets HDFC issue a **limited-scope token** to CRED — read credit card statements only, but NOT transfer money or change your PIN.

**Q3:** **INDmoney** wants to show all your mutual fund holdings from Groww, Zerodha, and Coin in one dashboard. How do they fetch your portfolio data safely?

> OAuth. Groww/Zerodha asks YOU for explicit consent ("Allow INDmoney to view your holdings?") and gives INDmoney a token that **only allows reading portfolio data** — they can't place trades or withdraw money.

**Q4:** You use **Buffer** (social media scheduler) to auto-post content to your Twitter/X account. How does Buffer post tweets without knowing your Twitter password?

> OAuth with **granular scopes**! Twitter shows you: "Buffer wants to: Post tweets, Read your profile. But NOT: Read your DMs, Change your password." You approve only what's needed.

---

## The Pre-OAuth Dark Ages (2005-2007)

This actually happened! Apps would literally ask for your password:

```
App: "Enter your Gmail password to import contacts"
User: "password123"
App: *stores password in their database*
App: *logs into Gmail AS the user*
App: *could read all emails, not just contacts*

Security nightmare!
```

### But wait... Why do Google/Facebook ALLOW other apps to use them for login?

It's not charity — it's **strategic business**:

| Reason | Explanation |
|--------|-------------|
| **Data & Insights** | Google knows which apps you use, when, how often. "User logged into Zomato 47 times this month" = valuable data for ads! |
| **User Lock-in** | If 50 apps use your Google login, you'll NEVER leave Google. Switching email = losing access to everything! |
| **Platform Dominance** | More apps using "Login with Google" = Google becomes the internet's ID card. They become essential infrastructure. |
| **API Monetization** | Free for small apps, but companies like Uber/Airbnb pay for high-volume API access. |
| **Trust Transfer** | Users trust "Login with Google" more than "Create account on RandomApp.com". Google's trust = more signups for apps! |

> **Think about it:** Would you rather be the app that needs Google, or BE Google that everyone needs? That's why Apple, Microsoft, GitHub all offer OAuth too — it's a platform power play!

---

## OAuth History & Timeline

**Is OAuth a Protocol?** Yes! OAuth 2.0 is an open standard/protocol defined by RFC 6749 (2012). It specifies exactly how different parties should communicate to grant access safely.

```
OAUTH TIMELINE
══════════════

2006: Blaine Cook (Twitter) needs a way to let third-party apps
      access Twitter accounts without storing passwords

2007: OAuth 1.0 draft created by Twitter, Google, and others
      - Complex signature requirements
      - Hard to implement correctly

2010: OAuth 1.0a (security fix for session fixation attack)

2012: OAuth 2.0 (RFC 6749) - Complete rewrite!
      - Simpler implementation
      - Bearer tokens (no signatures needed)
      - Multiple grant types for different scenarios
      - This is what everyone uses today!

2014: OpenID Connect 1.0 - Identity layer ON TOP of OAuth 2.0
      - OAuth = Authorization (What can this app do?)
      - OIDC = Authentication (Who is this user?)
      - "Login with Google" uses OIDC, not just OAuth

2020s: OAuth 2.1 (draft) - Consolidating best practices
```

### What are RFCs?

**RFC = Request for Comments**, managed by **IETF** (Internet Engineering Task Force) — the folks who standardize how the internet works!

Fun Trivia:
- **RFC 1** (1969) — The very first RFC, about ARPANET host software
- **RFC 2616** — HTTP/1.1 (you use this every day!)
- **RFC 1149** — "IP over Avian Carriers" — Yes, sending internet packets via pigeons! (April Fools' joke actually tested in 2001 — 55% packet loss)
- **RFC 2324** — Hyper Text Coffee Pot Control Protocol (HTCPCP) — Another April Fools' RFC!

> RFCs are never deleted — they get "obsoleted" by newer RFCs. The internet's history is preserved forever!

---

## OAuth vs OIDC — The Car Analogy

| | OAuth 2.0 = Car Keys | OIDC = Driver's License |
|---|---|---|
| **What it is** | "Here are my **car keys**. You can drive my car." | "Here's my **driver's license**. I am Sumit Mishra." |
| **Purpose** | Grants **permission** to do something | Proves **identity** (who you are) |
| **Key Point** | Doesn't tell you WHO the person is | Built on top of OAuth 2.0 |
| **Implication** | Anyone with these keys can drive! | Confirms you're allowed to drive |

### Key Insight

> Just because you have a **driver's license** (OIDC/identity) doesn't mean you can drive my car — you still need the **keys** (OAuth/permission)!
>
> And just because you have my **car keys** doesn't prove WHO you are — anyone with the keys can drive!

**"Login with Google"** = OIDC (you want to know WHO the user is — like checking their license)

**"Let app access my photos"** = OAuth (you want to grant PERMISSION — like handing over keys)

---

## OAuth vs Authentication

```
IMPORTANT DISTINCTION
═════════════════════

OAuth 2.0 is for AUTHORIZATION, not AUTHENTICATION!

┌─────────────────────────────┐    ┌─────────────────────────────┐
│      OAuth 2.0 Answers:     │    │   Authentication Answers:   │
│                             │    │                             │
│  "What can this app access?"│    │    "Who is this user?"      │
│                             │    │                             │
│   Authorization = Permissions    │    For this, use OIDC       │
│                             │    │   (built on top of OAuth)   │
└─────────────────────────────┘    └─────────────────────────────┘
```

**OpenID Connect (OIDC)** adds an ID Token (a JWT) that contains user identity information. That's what "Login with Google" actually uses!

---

## What is OAuth 2.0?

OAuth 2.0 is an **authorization framework** that enables applications to obtain limited access to user accounts on third-party services. It's the protocol behind "Login with Google/Facebook/GitHub".

---

## OAuth vs Sessions vs JWT: Different Problems!

**Key Insight:** OAuth solves a DIFFERENT problem than sessions or JWT. They're not replacements for each other!

| Technology | What Problem It Solves | Who Uses It |
|------------|----------------------|-------------|
| **Sessions** | "Remember that this user logged in to MY site" | Your server remembers your users |
| **JWT** | "Verify this user's identity without DB lookup" | Your server issues tokens to your users |
| **OAuth** | "Let a third-party app access MY user's data safely" | Google lets YOUR app access its users' data |

```
THE DIFFERENCE VISUALIZED
═════════════════════════

SESSIONS / JWT:
┌──────────┐                    ┌──────────┐
│   User   │ ──── Login ─────► │ Your App │
│ (Gokula) │ ◄─── Session ──── │          │
└──────────┘                    └──────────┘
Gokula creates account ON your app.
Your app authenticates Gokula directly.


OAUTH:
┌──────────┐     ┌──────────┐     ┌──────────┐
│   User   │     │ Your App │     │  Google  │
│ (Gokula) │     │          │     │          │
└──────────┘     └──────────┘     └──────────┘
     │                │                │
     │ 1. Click "Login with Google"    │
     │───────────────►│                │
     │                │ 2. Redirect    │
     │◄───────────────│───────────────►│
     │                │                │
     │ 3. "Allow PhotoApp to see your email?"
     │◄────────────────────────────────│
     │ 4. Click Allow                  │
     │────────────────────────────────►│
     │                │                │
     │                │ 5. Access Token│
     │                │◄───────────────│
     │                │                │
     │ 6. Welcome Gokula!             │
     │◄───────────────│                │

Gokula's account is at GOOGLE.
Your app gets PERMISSION to access Gokula's Google data.
```

---

## The Problem OAuth Solves

```
WITHOUT OAUTH (The Bad Old Days)
════════════════════════════════

You want App X to access your Google Photos.

Old way:
1. App X asks for your Google password
2. You give App X your password (yikes!)
3. App X logs into Google AS YOU
4. App X has FULL access to your account

Problems:
❌ App X has your password
❌ App X can do ANYTHING as you
❌ To revoke access, you must change password
❌ No granular permissions
```

```
WITH OAUTH 2.0 (The Right Way)
══════════════════════════════

You want App X to access your Google Photos.

OAuth way:
1. App X redirects you to Google
2. Google asks: "Allow App X to view your photos?"
3. You click "Allow"
4. Google gives App X a LIMITED token
5. App X can ONLY view photos (nothing else)

Benefits:
✅ App X NEVER sees your password
✅ App X has LIMITED access (photos only)
✅ Revoke access anytime without changing password
✅ Granular permissions (scopes)
```

---

## Why Do We Need OAuth After Sessions/Tokens?

| Use Case | Description | Can Sessions/JWT Do This? |
|----------|-------------|---------------------------|
| **Social Login** | Let users login with existing Google/GitHub accounts instead of creating new passwords | No |
| **API Access** | Let third-party apps access your users' data with their permission (like apps posting to Twitter) | No |
| **Granular Permissions** | Give limited access (read email but not send, view photos but not delete) | No |
| **No Password Sharing** | Apps never see or store user passwords. Revoke access without changing password | No |

---

## Key Terminology

| Term | Description | Real-World Example |
|------|-------------|-------------------|
| **Resource Owner** | The user who owns the data | You (own your Google photos) |
| **Client** | App wanting access | A photo printing app |
| **Authorization Server** | Issues tokens after user consent | accounts.google.com |
| **Resource Server** | Holds the protected data | Google Photos API |
| **Access Token** | Key to access resources | The token given to the app |
| **Refresh Token** | Used to get new access tokens | Long-lived token for renewal |
| **Scope** | What permissions are granted | `photos.readonly`, `email` |

---

## OAuth 2.0 Flows (Grant Types)

### 1. Authorization Code Flow (Most Common)
**Use for:** Server-side web apps, mobile apps

```
USER          CLIENT (App)      AUTH SERVER       RESOURCE SERVER
 │                 │                 │                   │
 │── Click login ─►│                 │                   │
 │                 │                 │                   │
 │◄── Redirect to Auth Server ──────►│                   │
 │                 │                 │                   │
 │── Login + Consent ───────────────►│                   │
 │                 │                 │                   │
 │◄── Redirect with AUTH CODE ───────│                   │
 │                 │                 │                   │
 │── AUTH CODE ───►│                 │                   │
 │                 │── Exchange code for token ─────────►│
 │                 │◄── ACCESS TOKEN + REFRESH TOKEN ───│
 │                 │                 │                   │
 │                 │── API request + ACCESS TOKEN ─────────────────►│
 │                 │◄── Protected resource ─────────────────────────│
 │◄── Show data ───│                 │                   │
```

### 2. Client Credentials Flow
**Use for:** Server-to-server (no user involved)

```
CLIENT (Backend)     AUTH SERVER       RESOURCE SERVER
     │                    │                   │
     │── client_id + ────►│                   │
     │   client_secret    │                   │
     │◄── ACCESS TOKEN ───│                   │
     │                    │                   │
     │── API request + token ────────────────►│
     │◄── Data ──────────────────────────────│
```

### 3. PKCE Flow (Authorization Code + PKCE)
**Use for:** Mobile apps, SPAs (public clients)

```
Same as Authorization Code, but with:
- code_verifier: Random string generated by client
- code_challenge: SHA256 hash of code_verifier

This prevents authorization code interception attacks.
```

---

## Scopes: Granular Permissions

```
OAUTH SCOPES EXAMPLE
════════════════════

App requests: scope=email photos.readonly

What user sees:
┌─────────────────────────────────────┐
│  Photo Print App wants to:          │
│                                     │
│  ✓ View your email address          │
│  ✓ View your photos                 │
│                                     │
│  [Allow]         [Deny]             │
└─────────────────────────────────────┘

What app can do:
✅ Read email
✅ View photos
❌ Delete photos (not requested)
❌ Access Drive (not requested)
❌ Send emails (not requested)
```

**Least Privilege:** Apps should only request the scopes they actually need. Users are more likely to approve minimal permissions.

---

## Access Token vs Refresh Token

| Aspect | Access Token | Refresh Token |
|--------|--------------|---------------|
| **Purpose** | Access APIs | Get new access tokens |
| **Lifetime** | Short (15-60 min) | Long (days to months) |
| **Sent to** | Resource server | Authorization server only |
| **Storage** | Memory (if possible) | Secure storage |
| **If stolen** | Limited damage (expires) | Can get new access tokens |

## Token Refresh Flow

```
ACCESS TOKEN EXPIRED
════════════════════

Client              Auth Server
  │                      │
  │── API Request ──────►│  (Access token expired)
  │◄── 401 Unauthorized ─│
  │                      │
  │── Refresh Token ────►│
  │◄── New Access Token ─│
  │                      │
  │── API Request ──────►│  (New access token)
  │◄── 200 OK ───────────│
```

---

## Common OAuth Providers

| Provider | Authorization Endpoint | Token Endpoint |
|----------|----------------------|----------------|
| Google | accounts.google.com/o/oauth2/v2/auth | oauth2.googleapis.com/token |
| GitHub | github.com/login/oauth/authorize | github.com/login/oauth/access_token |
| Facebook | facebook.com/v12.0/dialog/oauth | graph.facebook.com/v12.0/oauth/access_token |

---

## Security Best Practices

1. **Always use HTTPS**
2. **Validate redirect_uri** - Prevent open redirect attacks
3. **Use state parameter** - Prevent CSRF attacks
4. **Store tokens securely** - Never in localStorage for sensitive apps
5. **Use PKCE for public clients** - Mobile apps, SPAs
6. **Implement token rotation** - New refresh token on each use
7. **Validate all tokens server-side** - Never trust client validation

---

## Real-World Example: "Login with Google"

```python
# 1. Redirect user to Google
redirect_url = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    "client_id=YOUR_CLIENT_ID&"
    "redirect_uri=https://yourapp.com/callback&"
    "response_type=code&"
    "scope=email profile&"
    "state=random_csrf_token"
)

# 2. Google redirects back with code
# https://yourapp.com/callback?code=AUTH_CODE&state=random_csrf_token

# 3. Exchange code for tokens
response = requests.post(
    "https://oauth2.googleapis.com/token",
    data={
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "code": "AUTH_CODE",
        "grant_type": "authorization_code",
        "redirect_uri": "https://yourapp.com/callback"
    }
)
tokens = response.json()
# {"access_token": "...", "refresh_token": "...", "id_token": "..."}

# 4. Use access token to get user info
user_info = requests.get(
    "https://www.googleapis.com/oauth2/v2/userinfo",
    headers={"Authorization": f"Bearer {tokens['access_token']}"}
).json()
# {"email": "user@gmail.com", "name": "John Doe", ...}
```

---

## Real-World Examples You Use Daily

| Service | What OAuth Enables |
|---------|-------------------|
| **Login with Google** | Sign into apps using your Google account |
| **Login with GitHub** | Authorize apps to access your repos |
| **Login with Facebook** | Share profile info with third-party apps |
| **Spotify + Last.fm** | Last.fm tracks your Spotify listening |
| **CRED + Banks** | CRED reads your credit card statements |
| **Buffer + Twitter** | Buffer posts tweets on your behalf |
