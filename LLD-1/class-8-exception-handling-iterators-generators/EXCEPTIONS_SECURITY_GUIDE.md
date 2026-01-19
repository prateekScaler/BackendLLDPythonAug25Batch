# Exception Security Risks 🔒

## ⚠️ Unhandled Exceptions Leak Sensitive Information

Exceptions expose: file paths, database credentials, SQL queries, API keys, business logic, internal IPs.

---

## 🔓 Example 1: File Path Disclosure

### Unhandled
```python
def get_config(user_id):
    with open(f"/var/www/app/configs/{user_id}.json") as f:
        return f.read()
```

**Output:**
```
FileNotFoundError: [Errno 2] No such file or directory: 
'/var/www/app/configs/123.json'
```

**Leaked:** App path, directory structure, file naming pattern.

### Handled
```python
def get_config(user_id):
    try:
        with open(f"/var/www/app/configs/{user_id}.json") as f:
            return f.read()
    except FileNotFoundError:
        return None  # or {"error": "Not found"}
```

**Output:** `None` - No information leaked.

---

## 🔓 Example 2: Database Credentials

### Unhandled
```python
conn = psycopg2.connect(
    host="db.internal.company.com",
    user="app_admin",
    password="SecretPass123"
)
```

**Output:**
```
psycopg2.OperationalError: connection refused
    Host: db.internal.company.com (10.0.1.50)
    User: app_admin
    Database: production_db
```

**Leaked:** DB host, internal IP, username, database name.

### Handled
```python
try:
    conn = get_db_connection()
except psycopg2.OperationalError:
    logger.critical("DB connection failed")
    return {"error": "Service unavailable"}, 503
```

**Output:** `{"error": "Service unavailable"}` - Generic message.

---

## 🔓 Example 3: SQL Query Structure

### Unhandled
```python
query = f"SELECT * FROM users WHERE email='{email}'"
db.execute(query)
```

**Output:**
```
sqlite3.OperationalError: near "OR": syntax error
Query: SELECT * FROM users WHERE email='' OR '1'='1'
```

**Leaked:** SQL injection vulnerability, table name, column names.

### Handled
```python
try:
    query = "SELECT * FROM users WHERE email=?"
    db.execute(query, (email,))  # Parameterized
except db.Error:
    return {"error": "Invalid input"}, 400
```

**Output:** `{"error": "Invalid input"}` - No query details.

---

## 🔓 Example 4: API Keys

### Unhandled
```python
headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.post(url, headers=headers)
```

**Output:**
```
ConnectionError: Max retries exceeded
Headers: {'Authorization': 'Bearer sk_live_51H8xKJ...'}
```

**Leaked:** API key exposed.

### Handled
```python
try:
    response = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"})
except requests.RequestException:
    logger.error("API call failed")
    return {"error": "Request failed"}, 500
```

**Output:** `{"error": "Request failed"}` - Key protected.

---

## 🔓 Example 5: Business Logic

### Unhandled
```python
def calculate_discount(user, total):
    if user.is_premium and total > 100:
        return total * 0.20
    elif user.referrals > 5:
        return total * 0.15
```

**Output:**
```
AttributeError: 'NoneType' object has no attribute 'is_premium'
File: /app/pricing.py, line 45
Logic: premium + $100 → 20% off, 5+ referrals → 15% off
```

**Leaked:** Pricing logic, discount thresholds.

### Handled
```python
try:
    if not user:
        raise ValueError("Invalid user")
    return calculate_discount_internal(user, total)
except (AttributeError, ValueError):
    return total  # No discount on error
```

**Output:** Original price - Logic hidden.

---

## 📊 What Gets Leaked?

| Information | Risk | Example |
|------------|------|---------|
| File paths | High | `/var/www/app/src/` |
| DB credentials | Critical | `user:pass@host:5432` |
| SQL queries | High | `SELECT * FROM users` |
| API keys | Critical | `sk_live_xxxx` |
| IPs | Medium | `10.0.1.50` |
| Business logic | High | Discount rules |
| Stack traces | Medium | Code structure |

---

## ✅ Security Best Practices

### 1. Handle All Exceptions at Boundaries
```python
@app.errorhandler(Exception)
def handle_error(e):
    logger.exception("Error occurred")
    return {"error": "Internal error"}, 500
```

### 2. Generic Messages to Users, Full Logs Internally
```python
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", extra={"user_id": user_id})
    return {"error": "Operation failed"}, 500  # Generic
```

### 3. Sanitize Error Messages
```python
def sanitize_error(error):
    patterns = [r'/home/\w+/', r'password.*', r'\d+\.\d+\.\d+\.\d+']
    msg = str(error)
    for pattern in patterns:
        msg = re.sub(pattern, '[REDACTED]', msg)
    return msg
```

### 4. Different Config for Dev/Prod
```python
if app.debug:
    raise e  # Show full trace in dev
else:
    return {"error": "Error occurred"}  # Generic in prod
```

---

## 🎯 Why This Matters

### Without Handling:
- ❌ Attackers map your infrastructure
- ❌ Credentials exposed
- ❌ Business logic revealed
- ❌ GDPR/PCI-DSS violations
- ❌ Security vulnerabilities

### With Handling:
- ✅ Information protected
- ✅ Compliance adherence
- ✅ Professional appearance
- ✅ Better user experience
- ✅ Easier debugging (internal logs)

---

## 🔗 Compliance Standards

- **OWASP:** Improper Error Handling
- **CWE-209:** Information Exposure Through Error Message
- **GDPR Article 32:** Security of Processing
- **PCI-DSS 6.5.5:** Improper Error Handling

---

## ⚡ Quick Checklist

- [ ] Handle exceptions at API boundaries
- [ ] Never expose stack traces to users
- [ ] Log full details internally only
- [ ] Use generic error messages
- [ ] Sanitize logs before external systems
- [ ] Different configs for dev/prod
- [ ] Use monitoring tools (Sentry)
- [ ] Test error cases explicitly

---

## 💡 Remember

**"Every unhandled exception is a potential security breach!"**

Treat exception handling as a security requirement, not just good practice.