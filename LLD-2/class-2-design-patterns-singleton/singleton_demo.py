"""
Singleton Pattern - Practical Implementations
Demonstrates all methods and common pitfalls
"""

print("=" * 60)
print("SINGLETON PATTERN - IMPLEMENTATIONS")
print("=" * 60)

# ============================================================================
# Method 1: Using __new__ (Classic Approach)
# ============================================================================

print("\n--- Method 1: __new__ Implementation ---")


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("  Creating new instance...")
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            print("  Initializing connection...")
            self.connection_string = "postgresql://localhost:5432"
            self._initialized = True


db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(f"Same instance? {db1 is db2}")
print(f"Connection: {db1.connection_string}")

# ============================================================================
# Method 2: Using Decorator (Elegant)
# ============================================================================

print("\n--- Method 2: Decorator Implementation ---")


def singleton(cls):
    """Decorator to make a class Singleton"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            print(f"  Creating {cls.__name__} instance...")
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:
    def __init__(self):
        self.logs = []
        print("  Logger initialized")

    def log(self, message):
        self.logs.append(message)
        print(f"  Log: {message}")


log1 = Logger()
log1.log("First log")
log2 = Logger()
log2.log("Second log")
print(f"Same instance? {log1 is log2}")
print(f"Total logs: {len(log1.logs)}")

# ============================================================================
# Method 3: Using Metaclass (Advanced)
# ============================================================================

print("\n--- Method 3: Metaclass Implementation ---")


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"  Creating {cls.__name__} via metaclass...")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    def __init__(self):
        self.debug = True
        self.api_key = "secret123"
        print("  Config initialized")


config1 = AppConfig()
config2 = AppConfig()
print(f"Same instance? {config1 is config2}")
print(f"Debug mode: {config1.debug}")

# ============================================================================
# Method 4: Module-Level (Pythonic)
# ============================================================================

print("\n--- Method 4: Module-Level (Most Pythonic) ---")


class _Cache:
    def __init__(self):
        self._data = {}
        print("  Cache initialized")

    def set(self, key, value):
        self._data[key] = value

    def get(self, key):
        return self._data.get(key)


# Create single instance at module level
cache = _Cache()

# Usage
cache.set("user_1", "Alice")
cache.set("user_2", "Bob")
print(f"User 1: {cache.get('user_1')}")
print("Note: Import 'cache' from this module - it's already a singleton!")

# ============================================================================
# Thread-Safe Singleton
# ============================================================================

print("\n--- Thread-Safe Implementation ---")

import threading


class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-check locking
                if cls._instance is None:
                    print("  Creating thread-safe instance...")
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            print("  Initializing thread-safe singleton...")
            self.value = 42
            self._initialized = True


# Test thread safety
def create_singleton():
    s = ThreadSafeSingleton()
    print(f"  Thread {threading.current_thread().name}: {id(s)}")


threads = [threading.Thread(target=create_singleton) for _ in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# ============================================================================
# Practical Use Cases
# ============================================================================

print("\n" + "=" * 60)
print("PRACTICAL USE CASES")
print("=" * 60)

# Use Case 1: Connection Pool
print("\n--- Use Case 1: Connection Pool ---")


@singleton
class ConnectionPool:
    def __init__(self):
        self.max_connections = 5
        self.active = []
        print("  Connection pool created")

    def acquire(self):
        if len(self.active) < self.max_connections:
            conn_id = len(self.active) + 1
            self.active.append(conn_id)
            print(f"  Connection {conn_id} acquired")
            return conn_id
        print("  Pool exhausted!")
        return None

    def release(self, conn_id):
        if conn_id in self.active:
            self.active.remove(conn_id)
            print(f"  Connection {conn_id} released")


pool = ConnectionPool()
c1 = pool.acquire()
c2 = pool.acquire()
print(f"Active connections: {len(pool.active)}")
pool.release(c1)

# Use Case 2: Configuration Manager
print("\n--- Use Case 2: Configuration Manager ---")


@singleton
class Config:
    def __init__(self):
        self.settings = {
            "db_host": "localhost",
            "db_port": 5432,
            "debug": True,
            "api_timeout": 30
        }
        print("  Configuration loaded")

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value


config_obj = Config()
print(f"DB Host: {config_obj.get('db_host')}")
config_obj.set("debug", False)

# Use Case 3: Application Logger
print("\n--- Use Case 3: Application Logger ---")


@singleton
class AppLogger:
    def __init__(self):
        self.entries = []
        print("  Logger initialized")

    def info(self, message):
        entry = f"[INFO] {message}"
        self.entries.append(entry)
        print(f"  {entry}")

    def error(self, message):
        entry = f"[ERROR] {message}"
        self.entries.append(entry)
        print(f"  {entry}")


logger = AppLogger()
logger.info("Application started")
logger.error("Something went wrong")
print(f"Total log entries: {len(logger.entries)}")

# ============================================================================
# Breaking Singleton (Pitfalls)
# ============================================================================

print("\n" + "=" * 60)
print("BREAKING SINGLETON - COMMON PITFALLS")
print("=" * 60)

# Pitfall 1: Subclassing
print("\n--- Pitfall 1: Subclassing ---")


class SingletonBase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class SubSingleton(SingletonBase):
    pass


base = SingletonBase()
sub = SubSingleton()
print(f"Different types? {type(base) != type(sub)}")
print("Problem: Subclass creates different instance!")

# Fix: Store per class
print("\nFix: Store instance per class")


class FixedSingleton:
    _instances = {}

    def __new__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


# Pitfall 2: __init__ called multiple times
print("\n--- Pitfall 2: __init__ Multiple Calls ---")


class BadSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        print("  __init__ called!")  # Called every time!
        self.value = 0


s1 = BadSingleton()
s1.value = 42
s2 = BadSingleton()  # __init__ called again!
print(f"Value reset? {s2.value}")

# ============================================================================
# Best Practices
# ============================================================================

print("\n" + "=" * 60)
print("BEST PRACTICES")
print("=" * 60)

print("""
✅ DO:
  • Use module-level for simple singletons
  • Add thread-safety for concurrent apps
  • Document why Singleton is needed
  • Use for resource managers (pools, caches)

❌ DON'T:
  • Make everything Singleton
  • Use for domain objects (User, Order)
  • Hide dependencies (use DI instead)
  • Use as global state dumping ground

🎯 PREFER:
  • Dependency Injection for testability
  • Module-level variables for simplicity
  • Context managers for scoped resources
""")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
Singleton ensures ONE instance of a class.

Methods:
  1. __new__ - Classic, clear
  2. Decorator - Clean, reusable
  3. Metaclass - Advanced control
  4. Module-level - Most Pythonic

Use for: Connection pools, caches, loggers, config
Avoid for: Domain objects, utilities, testability

Remember: Pattern is a tool, not a rule!
""")