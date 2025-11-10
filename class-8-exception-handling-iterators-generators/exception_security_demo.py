"""
Exception Security Risks - Concise Demo
Shows what attackers can learn from unhandled exceptions
NOTE: All keys/passwords are fake examples for demonstration only
"""

import os

print("=" * 60)
print("🔒 EXCEPTION SECURITY DEMONSTRATION")
print("=" * 60)

# Demo 1: File Path Disclosure
print("\n--- Demo 1: File Paths ---")

def get_config_insecure(user_id):
    with open(f"/var/www/app/configs/{user_id}.json") as f:
        return f.read()

try:
    get_config_insecure("missing")
except FileNotFoundError as e:
    print("❌ INSECURE - User sees:")
    print(f"   {e}")
    print("   Leaked: /var/www/app/, directory structure")

def get_config_secure(user_id):
    try:
        with open(f"/var/www/app/configs/{user_id}.json") as f:
            return f.read()
    except FileNotFoundError:
        return None

result = get_config_secure("missing")
print("✅ SECURE - User sees:")
print(f"   {result}")
print("   Leaked: Nothing")

# Demo 2: Database Credentials
print("\n--- Demo 2: Database Info ---")

class FakeDB:
    def __init__(self, host, user):
        self.conn_str = f"{user}@{host}"
        if "fail" in host:
            raise ConnectionError(
                f"Connection to {host} failed\n"
                f"User: {user}, Host: {host}"
            )

try:
    db = FakeDB("db.fail.internal", "admin")
except ConnectionError as e:
    print("❌ INSECURE - User sees:")
    print(f"   {e}")
    print("   Leaked: Host, username")

def connect_secure():
    try:
        return FakeDB("db.fail.internal", "admin")
    except ConnectionError:
        raise ConnectionError("Database unavailable")

try:
    connect_secure()
except ConnectionError as e:
    print("✅ SECURE - User sees:")
    print(f"   {e}")
    print("   Leaked: Nothing")

# Demo 3: SQL Query Structure
print("\n--- Demo 3: SQL Queries ---")

def search_insecure(term):
    query = f"SELECT id, email FROM users WHERE name LIKE '%{term}%'"
    if "'" in term:
        raise ValueError(
            f"SQL Error near '{term}'\n"
            f"Query: {query}\n"
            f"Table: users, Columns: id, email"
        )

try:
    search_insecure("test' OR '1'='1")
except ValueError as e:
    print("❌ INSECURE - User sees:")
    print(f"   {e}")
    print("   Leaked: SQL injection, table/column names")

def search_secure(term):
    try:
        if any(c in term for c in ["'", '"', ";"]):
            raise ValueError("Invalid input")
        # Use parameterized query
        return []
    except ValueError:
        return {"error": "Invalid search"}

result = search_secure("test' OR '1'='1")
print("✅ SECURE - User sees:")
print(f"   {result}")
print("   Leaked: Nothing")

# Demo 4: API Keys
print("\n--- Demo 4: API Keys ---")

def send_email_insecure(email):
    # FAKE API KEY for demo - not a real key
    api_key = "demo_key_1234567890abcdef"
    if "@" not in email:
        raise ValueError(
            f"Invalid: {email}\n"
            f"API Key: {api_key}"
        )

try:
    send_email_insecure("invalid")
except ValueError as e:
    print("❌ INSECURE - User sees:")
    print(f"   {e}")
    print("   Leaked: API key exposed")

def send_email_secure(email):
    try:
        if "@" not in email:
            raise ValueError("Invalid email")
        return True
    except ValueError:
        return {"error": "Invalid email"}

result = send_email_secure("invalid")
print("✅ SECURE - User sees:")
print(f"   {result}")
print("   Leaked: Nothing")

# Demo 5: Environment Variables
print("\n--- Demo 5: Environment Variables ---")

# FAKE credentials for demo only
os.environ["DB_URL"] = "postgres://appuser@localhost:5432/mydb"
os.environ["APP_SECRET"] = "fake-secret-for-demo-only"

def load_config_insecure():
    try:
        db = os.environ["DB_URL"]
        key = os.environ["APP_SECRET"]
    except KeyError as e:
        print(f"Missing: {e}")
        print(f"DB_URL: {os.environ['DB_URL']}")
        print(f"APP_SECRET: {os.environ['APP_SECRET']}")
        raise

try:
    os.environ.pop("FAKE_VAR", None)
    load_config_insecure()
except:
    print("❌ INSECURE - Shows all env vars")
    print("   Leaked: DB connection, secrets")

def load_config_secure():
    try:
        db = os.environ["DB_URL"]
        key = os.environ["APP_SECRET"]
        return True
    except KeyError:
        return {"error": "Configuration error"}

result = load_config_secure()
print("✅ SECURE - User sees:")
print(f"   {result}")
print("   Leaked: Nothing")

# Summary
print("\n" + "=" * 60)
print("KEY TAKEAWAYS")
print("=" * 60)
print("""
🚨 UNHANDLED EXCEPTIONS LEAK:
   • File paths & directory structure
   • Database hosts & usernames
   • SQL queries & table structure
   • API keys & tokens
   • Environment variables
   • Code structure & logic

🔒 PROPER HANDLING PROTECTS:
   • Credentials & keys
   • Internal structure
   • Business logic
   • User data
   • Compliance (GDPR, PCI-DSS)

💡 BEST PRACTICES:
   1. Handle at API boundaries
   2. Log internally, generic to users
   3. Never expose stack traces in prod
   4. Use monitoring tools (Sentry)
   5. Test error cases

⚠️  "Unhandled exceptions = Security vulnerabilities"
""")