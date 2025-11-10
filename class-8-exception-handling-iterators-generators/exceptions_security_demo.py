"""
Security Risks of Unhandled Exceptions
Live demonstration of information leakage
"""

import os
import sys

print("=" * 70)
print("🔒 SECURITY DEMONSTRATION: Why Exception Handling Matters")
print("=" * 70)

print("\n" + "=" * 70)
print("Demo 1: File Path Disclosure")
print("=" * 70)

print("\n--- ❌ INSECURE: Unhandled Exception ---")


def get_user_config_insecure(user_id):
    """Exposes internal file structure"""
    config_path = f"/var/www/myapp/configs/users/{user_id}.json"
    with open(config_path) as f:
        return f.read()


print("\nAttempting to access user config...")
try:
    get_user_config_insecure("nonexistent_user")
except FileNotFoundError as e:
    print(f"\n🔓 LEAKED TO ATTACKER:")
    print(f"   Error: {e}")
    print(f"   File: {e.filename}")
    print(f"\n🚨 Attacker now knows:")
    print(f"   ✗ Application root: /var/www/myapp/")
    print(f"   ✗ Config location: /configs/users/")
    print(f"   ✗ File naming pattern: {{user_id}}.json")

print("\n--- ✅ SECURE: Handled Exception ---")


def get_user_config_secure(user_id):
    """Protects internal details"""
    try:
        config_path = f"/var/www/myapp/configs/users/{user_id}.json"
        with open(config_path) as f:
            return f.read()
    except FileNotFoundError:
        # Log internally (not shown to user)
        # logger.error(f"Config not found: {user_id}")
        return None


print("\nAttempting to access user config...")
result = get_user_config_secure("nonexistent_user")
print(f"\n🔒 USER SEES: None")
print(f"✓ No sensitive information leaked")
print(f"✓ Internal paths hidden")

print("\n" + "=" * 70)
print("Demo 2: Database Connection Info Disclosure")
print("=" * 70)

print("\n--- ❌ INSECURE: Connection Details Exposed ---")


class FakeDatabase:
    def __init__(self, host, port, user, password, database):
        self.connection_string = f"{user}:{password}@{host}:{port}/{database}"
        if "fail" in host:
            raise ConnectionError(
                f"Could not connect to {host}:{port}\n"
                f"Connection string: {self.connection_string}\n"
                f"User: {user}, Database: {database}"
            )


print("\nAttempting database connection...")
try:
    db = FakeDatabase(
        host="db.internal.fail.company.com",
        port=5432,
        user="app_admin",
        password="SuperSecret123!",
        database="production_db"
    )
except ConnectionError as e:
    print(f"\n🔓 LEAKED TO ATTACKER:")
    print(f"{e}")
    print(f"\n🚨 Attacker now knows:")
    print(f"   ✗ Database host: db.internal.fail.company.com")
    print(f"   ✗ Port: 5432 (PostgreSQL)")
    print(f"   ✗ Username: app_admin")
    print(f"   ✗ Password: SuperSecret123!")
    print(f"   ✗ Database: production_db")

print("\n--- ✅ SECURE: Generic Error Message ---")


def connect_db_secure():
    try:
        db = FakeDatabase(
            host="db.internal.fail.company.com",
            port=5432,
            user="app_admin",
            password="SuperSecret123!",
            database="production_db"
        )
        return db
    except ConnectionError as e:
        # Log full error internally
        # logger.critical(f"Database connection failed: {e}")
        # Return generic message to user
        raise ConnectionError("Database temporarily unavailable")


print("\nAttempting database connection...")
try:
    connect_db_secure()
except ConnectionError as e:
    print(f"\n🔒 USER SEES: {e}")
    print(f"✓ No credentials exposed")
    print(f"✓ No internal hosts revealed")

print("\n" + "=" * 70)
print("Demo 3: SQL Query Structure Exposure")
print("=" * 70)

print("\n--- ❌ INSECURE: Query Details Leaked ---")


def search_products_insecure(search_term):
    # Vulnerable query (don't actually run this!)
    query = f"SELECT id, name, price FROM products WHERE name LIKE '%{search_term}%'"

    # Simulate SQL error
    if "'" in search_term:
        raise ValueError(
            f"SQL Syntax Error near '{search_term}'\n"
            f"Query: {query}\n"
            f"Table: products\n"
            f"Columns: id, name, price"
        )


print("\nUser searches for: test' OR '1'='1")
try:
    search_products_insecure("test' OR '1'='1")
except ValueError as e:
    print(f"\n🔓 LEAKED TO ATTACKER:")
    print(f"{e}")
    print(f"\n🚨 Attacker now knows:")
    print(f"   ✗ Vulnerable to SQL injection")
    print(f"   ✗ Table name: products")
    print(f"   ✗ Column names: id, name, price")
    print(f"   ✗ Query structure")

print("\n--- ✅ SECURE: Sanitized Response ---")


def search_products_secure(search_term):
    try:
        # Sanitize input
        if any(char in search_term for char in ["'", '"', ";", "--"]):
            raise ValueError("Invalid search term")

        # Use parameterized query (safe)
        # query = "SELECT id, name, price FROM products WHERE name LIKE ?"
        # results = db.execute(query, (f"%{search_term}%",))
        return []
    except ValueError:
        # Generic error
        return {"error": "Invalid search"}, 400


print("\nUser searches for: test' OR '1'='1")
result = search_products_secure("test' OR '1'='1")
print(f"\n🔒 USER SEES: {result}")
print(f"✓ No query structure exposed")
print(f"✓ No table/column names revealed")

print("\n" + "=" * 70)
print("Demo 4: API Key Exposure")
print("=" * 70)

print("\n--- ❌ INSECURE: Secrets in Error Messages ---")


def send_email_insecure(recipient):
    API_KEY = "sk_live_51H8xKJLkjsdf89sd7f6sd8f76sd8f76"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    if "@" not in recipient:
        raise ValueError(
            f"Invalid email: {recipient}\n"
            f"Request headers: {headers}\n"
            f"API Key: {API_KEY}"
        )


print("\nSending email to: invalid-email")
try:
    send_email_insecure("invalid-email")
except ValueError as e:
    print(f"\n🔓 LEAKED TO ATTACKER:")
    print(f"{e}")
    print(f"\n🚨 Attacker now knows:")
    print(f"   ✗ API Key: sk_live_51H8xKJLkjsdf89sd7f6sd8f76sd8f76")
    print(f"   ✗ Can now use your API for free!")

print("\n--- ✅ SECURE: Secrets Protected ---")


def send_email_secure(recipient):
    try:
        if "@" not in recipient:
            raise ValueError("Invalid email format")

        # API_KEY never in error messages
        # send_via_api(recipient, API_KEY)
        return True
    except ValueError:
        # No secrets in error
        return {"error": "Invalid email"}, 400


print("\nSending email to: invalid-email")
result = send_email_secure("invalid-email")
print(f"\n🔒 USER SEES: {result}")
print(f"✓ API key protected")
print(f"✓ No sensitive data leaked")

print("\n" + "=" * 70)
print("Demo 5: Stack Trace Reveals Code Structure")
print("=" * 70)

print("\n--- ❌ INSECURE: Full Stack Trace ---")


def process_payment_insecure(amount, user):
    # Simulate error with full stack trace visible
    if amount < 0:
        print(f"\n🔓 FULL STACK TRACE TO USER:")
        print(f"Traceback (most recent call last):")
        print(f'  File "{__file__}", line {sys._getframe().f_lineno}')
        print(f"    if amount < 0:")
        print(f"ValueError: Amount cannot be negative")
        print(f"\nFunction: process_payment_insecure")
        print(f"File: {__file__}")
        print(f"Parameters: amount={amount}, user={user}")

        print(f"\n🚨 Attacker now knows:")
        print(f"   ✗ Function name and parameters")
        print(f"   ✗ File structure")
        print(f"   ✗ Code logic (checks for negative)")
        print(f"   ✗ Can craft specific attacks")
        raise ValueError("Amount cannot be negative")


print("\nProcessing payment...")
try:
    process_payment_insecure(-100, {"id": 123, "email": "user@example.com"})
except ValueError:
    pass

print("\n--- ✅ SECURE: Generic Error ---")


def process_payment_secure(amount, user):
    try:
        if amount < 0:
            raise ValueError("Invalid amount")
        # Process payment
        return True
    except ValueError:
        # Log internally only
        # logger.warning(f"Invalid payment attempt: {amount}")
        return {"error": "Payment failed"}, 400


print("\nProcessing payment...")
result = process_payment_secure(-100, {"id": 123})
print(f"\n🔒 USER SEES: {result}")
print(f"✓ No internal details exposed")
print(f"✓ No code structure revealed")

print("\n" + "=" * 70)
print("Demo 6: Environment Variables Leak")
print("=" * 70)

print("\n--- ❌ INSECURE: Environment Details ---")

# Simulate environment variables
os.environ["DATABASE_URL"] = "postgres://admin:pass123@db.internal:5432/prod"
os.environ["SECRET_KEY"] = "django-secret-key-abc123xyz"
os.environ["AWS_ACCESS_KEY"] = "AKIAIOSFODNN7EXAMPLE"


def load_config_insecure():
    try:
        db_url = os.environ["DATABASE_URL"]
        secret = os.environ["SECRET_KEY"]
        aws_key = os.environ["AWS_ACCESS_KEY"]
    except KeyError as e:
        print(f"\n🔓 LEAKED TO ATTACKER:")
        print(f"Missing environment variable: {e}")
        print(f"Available variables:")
        for key in ["DATABASE_URL", "SECRET_KEY", "AWS_ACCESS_KEY"]:
            print(f"   {key} = {os.environ.get(key)}")
        raise


print("\nLoading configuration...")
try:
    os.environ.pop("MISSING_VAR", None)
    os.environ["MISSING_VAR"] = "should_exist"
    os.environ.pop("MISSING_VAR")
    load_config_insecure()
except KeyError:
    print(f"\n🚨 Attacker now knows:")
    print(f"   ✗ Database connection string")
    print(f"   ✗ Secret keys")
    print(f"   ✗ AWS credentials")

print("\n--- ✅ SECURE: Protected Config ---")


def load_config_secure():
    try:
        db_url = os.environ["DATABASE_URL"]
        secret = os.environ["SECRET_KEY"]
        aws_key = os.environ["AWS_ACCESS_KEY"]
        return {"configured": True}
    except KeyError as e:
        # Log internally only
        # logger.critical(f"Missing config: {e}")
        return {"error": "Configuration error"}, 500


print("\nLoading configuration...")
result = load_config_secure()
print(f"\n🔒 USER SEES: {result}")
print(f"✓ No credentials exposed")
print(f"✓ Environment protected")

print("\n" + "=" * 70)
print("KEY TAKEAWAYS")
print("=" * 70)
print("""
🚨 UNHANDLED EXCEPTIONS CAN LEAK:
   ✗ File paths and directory structure
   ✗ Database connection details
   ✗ SQL queries and table structure  
   ✗ API keys and secrets
   ✗ Environment variables
   ✗ Code structure and logic
   ✗ Library versions
   ✗ Internal IP addresses
   ✗ Business logic and rules

🔒 PROPER EXCEPTION HANDLING PROTECTS:
   ✓ Sensitive credentials
   ✓ Internal architecture
   ✓ Business logic
   ✓ User data
   ✓ Company reputation

💡 BEST PRACTICES:
   1. ALWAYS handle exceptions at API boundaries
   2. Log full details INTERNALLY
   3. Show generic messages to USERS
   4. Never expose stack traces in production
   5. Sanitize error messages
   6. Use monitoring tools (Sentry, etc.)
   7. Test error cases explicitly

⚖️ COMPLIANCE:
   • OWASP: Improper Error Handling
   • CWE-209: Information Exposure Through Error Message
   • GDPR Article 32: Security of Processing
   • PCI-DSS Requirement 6.5.5

🎯 REMEMBER: "Unhandled exceptions are security vulnerabilities!"
""")

print("\n" + "=" * 70)
print("Run this demo to show students the security impact!")
print("=" * 70)