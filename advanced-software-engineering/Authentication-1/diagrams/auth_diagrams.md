# Authentication Diagrams

> View these diagrams on GitHub, VS Code with Mermaid extension, or paste at https://mermaid.live

---

## 1. Authentication vs Authorization Flow

```mermaid
flowchart TD
    A[User Request] --> B{Has Credentials?}
    B -->|No| C[401 Unauthenticated]
    B -->|Yes| D[Authentication Layer]
    D --> E{Valid Credentials?}
    E -->|No| C
    E -->|Yes| F[Identity Verified]
    F --> G[Authorization Layer]
    G --> H{Has Permission?}
    H -->|No| I[403 Forbidden]
    H -->|Yes| J[Access Granted]
    J --> K[Return Resource]

    style C fill:#ff6b6b
    style I fill:#ffa500
    style K fill:#51cf66
```

---

## 2. Password Hashing Evolution

```mermaid
timeline
    title Password Storage Evolution
    1960s-1980s : Plaintext
                : "password123" stored directly
                : Anyone with DB access sees all
    1990s : Simple Hashing (MD5)
          : MD5("password") = "5f4d..."
          : Rainbow tables broke this
    2000s : Salted Hashing (SHA)
          : SHA256(salt + password)
          : Still too fast for GPUs
    2010s : Adaptive Hashing (BCrypt)
          : Intentionally slow
          : Adjustable work factor
    2015+ : Memory-Hard (Argon2)
          : CPU + Memory intensive
          : Resists GPU attacks
```

---

## 3. BCrypt Hashing Process

```mermaid
flowchart LR
    A[Password] --> B[Generate Salt]
    B --> C[Key Setup<br/>EksBlowfish]
    C --> D{Repeat 2^cost times}
    D --> E[Encrypt Magic String]
    E --> D
    D -->|Done| F[Combine Results]
    F --> G["$2b$12$salt...hash"]

    style A fill:#e7f5ff
    style G fill:#d3f9d8
```

---

## 4. JWT Token Structure

```mermaid
flowchart LR
    subgraph Header
        H1["{ alg: HS256, typ: JWT }"]
    end
    subgraph Payload
        P1["{ sub: 123, exp: ..., role: admin }"]
    end
    subgraph Signature
        S1["HMAC-SHA256(header.payload, secret)"]
    end

    Header --> |Base64| A[eyJhbGci...]
    Payload --> |Base64| B[eyJzdWIi...]
    Signature --> |Base64| C[POstGetf...]

    A --> D["eyJhbGci...eyJzdWIi...POstGetf"]
    B --> D
    C --> D

    style D fill:#fff3bf
```

---

## 5. Session vs Token Authentication

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database

    Note over C,DB: Session-Based (Stateful)
    C->>S: Login (username, password)
    S->>DB: Create session record
    DB-->>S: Session ID: abc123
    S-->>C: Set-Cookie: session=abc123
    C->>S: Request + Cookie
    S->>DB: Lookup session abc123
    DB-->>S: User ID: 42
    S-->>C: Response

    Note over C,DB: Token-Based (Stateless)
    C->>S: Login (username, password)
    S->>S: Create signed JWT
    S-->>C: { token: "eyJ..." }
    C->>S: Request + Bearer token
    S->>S: Verify signature
    S-->>C: Response (no DB needed!)
```

---

## 6. Refresh Token Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>S: Login (credentials)
    S-->>C: Access Token (15 min) + Refresh Token (7 days)

    loop Every API call
        C->>S: Request + Access Token
        S-->>C: Response
    end

    Note over C,S: Access token expires
    C->>S: Request + Expired Access Token
    S-->>C: 401 Unauthorized

    C->>S: Refresh (Refresh Token)
    S-->>C: New Access Token

    C->>S: Request + New Access Token
    S-->>C: Response
```

---

## 7. Password Cracking Speed Comparison

```mermaid
xychart-beta
    title "Hashes per Second (RTX 4090)"
    x-axis ["MD5", "SHA-1", "SHA-256", "BCrypt-5", "BCrypt-12", "Argon2"]
    y-axis "Hashes/sec (log scale)" 1 --> 200000000000
    bar [164000000000, 27000000000, 22000000000, 184000, 1400, 1000]
```

---

## 8. Three Factors of Authentication

```mermaid
mindmap
  root((Authentication<br/>Factors))
    Knowledge
      Password
      PIN
      Security Questions
    Possession
      Phone/SMS
      Hardware Token
      Smart Card
    Inherence
      Fingerprint
      Face Recognition
      Voice
      Retina
```

---

## 9. Authentication Flow with MFA

```mermaid
stateDiagram-v2
    [*] --> EnterCredentials
    EnterCredentials --> ValidatePassword: Submit
    ValidatePassword --> Failed: Invalid
    ValidatePassword --> MFARequired: Valid + MFA enabled
    ValidatePassword --> Success: Valid + No MFA

    MFARequired --> EnterOTP
    EnterOTP --> ValidateOTP: Submit
    ValidateOTP --> Failed: Invalid OTP
    ValidateOTP --> Success: Valid OTP

    Failed --> EnterCredentials: Retry
    Success --> [*]

    state Success {
        [*] --> IssueToken
        IssueToken --> CreateSession
        CreateSession --> [*]
    }
```

---

## 10. OAuth 2.0 Authorization Code Flow (Preview)

```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant AS as Auth Server
    participant RS as Resource Server

    U->>A: Click "Login with Google"
    A->>AS: Redirect to /authorize
    AS->>U: Show login page
    U->>AS: Enter credentials
    AS->>A: Redirect with code
    A->>AS: Exchange code for token
    AS-->>A: Access Token
    A->>RS: API Request + Token
    RS-->>A: Protected Data
    A-->>U: Show data
```

---

## 11. Security Attack Comparison

```mermaid
quadrantChart
    title Password Attack Effectiveness
    x-axis Low Effort --> High Effort
    y-axis Low Success --> High Success
    quadrant-1 Dangerous
    quadrant-2 Impractical
    quadrant-3 Minor Threat
    quadrant-4 Moderate Risk
    Rainbow Table (MD5): [0.2, 0.9]
    Brute Force (SHA): [0.5, 0.7]
    Dictionary Attack: [0.3, 0.6]
    Brute Force (BCrypt): [0.9, 0.2]
    Phishing: [0.3, 0.8]
```

---

## 12. Token Storage Options

```mermaid
flowchart TD
    A[Where to Store Tokens?] --> B[localStorage]
    A --> C[sessionStorage]
    A --> D[httpOnly Cookie]
    A --> E[Memory]

    B --> B1[❌ XSS Vulnerable]
    C --> C1[⚠️ XSS Vulnerable<br/>Cleared on tab close]
    D --> D1[✅ Secure from XSS<br/>⚠️ Needs CSRF protection]
    E --> E1[✅ Most Secure<br/>⚠️ Lost on refresh]

    style B1 fill:#ff6b6b
    style C1 fill:#ffa500
    style D1 fill:#51cf66
    style E1 fill:#51cf66
```

---

## Usage

To render these diagrams:

1. **GitHub**: Diagrams render automatically in `.md` files
2. **VS Code**: Install "Markdown Preview Mermaid Support" extension
3. **Online**: Copy code to https://mermaid.live
4. **Export**: Use Mermaid CLI: `mmdc -i diagrams.md -o output.png`

