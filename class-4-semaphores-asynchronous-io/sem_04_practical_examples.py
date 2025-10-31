"""
Part 4: Practical Semaphore Examples
Real-world scenarios where semaphores shine
"""
from threading import Thread, Semaphore
import time
import random

# ============================================================
# Example 1: Connection Pool (Most Common)
# ============================================================

class DatabaseConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = Semaphore(max_connections)
        self.max_connections = max_connections
    
    def execute_query(self, user_id, query):
        print(f"User {user_id}: Requesting connection...")
        
        # Wait for available connection
        self.semaphore.acquire()
        
        try:
            print(f"User {user_id}: ✓ Got connection! Executing: {query}")
            time.sleep(random.uniform(0.5, 1.5))  # Simulate query
            print(f"User {user_id}: Query done, releasing connection")
        finally:
            # Always release!
            self.semaphore.release()

def connection_pool_demo():
    print("=" * 60)
    print("Example 1: DATABASE CONNECTION POOL")
    print("=" * 60)
    print("Pool has 2 connections, 5 users want to query\n")
    
    pool = DatabaseConnectionPool(max_connections=2)
    
    threads = []
    queries = ["SELECT * FROM users", "UPDATE products", "INSERT INTO orders", 
               "DELETE FROM cache", "SELECT COUNT(*)"]
    
    for i in range(1, 6):
        t = Thread(target=pool.execute_query, args=(i, queries[i-1]))
        threads.append(t)
        t.start()
        time.sleep(0.1)  # Stagger starts
    
    for t in threads:
        t.join()
    
    print("\n✓ All queries completed!")

# ============================================================
# Example 2: Rate Limiter (API calls)
# ============================================================

class RateLimiter:
    def __init__(self, max_per_second):
        self.semaphore = Semaphore(max_per_second)
        self.max_per_second = max_per_second
    
    def make_request(self, user_id, endpoint):
        print(f"User {user_id}: Attempting API call to {endpoint}")
        
        if self.semaphore.acquire(blocking=False):  # Non-blocking!
            try:
                print(f"User {user_id}: ✓ API call allowed")
                time.sleep(0.5)  # Simulate API call
                return "Success"
            finally:
                # Release after 1 second (rate limit window)
                Thread(target=self._delayed_release).start()
        else:
            print(f"User {user_id}: ✗ Rate limit exceeded! Try later")
            return "Rate limited"
    
    def _delayed_release(self):
        time.sleep(1)  # 1 second window
        self.semaphore.release()

def rate_limiter_demo():
    print("\n" + "=" * 60)
    print("Example 2: API RATE LIMITER")
    print("=" * 60)
    print("Limit: 3 requests per second\n")
    
    limiter = RateLimiter(max_per_second=3)
    
    # Burst of 5 requests
    for i in range(1, 6):
        limiter.make_request(i, "/api/data")
        time.sleep(0.1)
    
    print("\n✓ Rate limiting enforced!")



if __name__ == "__main__":
    connection_pool_demo()
    rate_limiter_demo()
    download_manager_demo()
    
    print("\n" + "=" * 60)
    print("WHEN TO USE SEMAPHORES:")
    print("=" * 60)
    print("✓ Limited resources (connections, threads, slots)")
    print("✓ Rate limiting (API calls, requests)")
    print("✓ Controlling concurrency level")
    print("✓ Resource pools")
    print("")
    print("Real-world examples:")
    print("  • Database connection pools")
    print("  • Thread pools")
    print("  • API rate limiters")
    print("  • Print job queues")
    print("  • Parking lot management")
