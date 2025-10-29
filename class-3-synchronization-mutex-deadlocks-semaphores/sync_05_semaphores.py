"""
Example 5: Semaphores - Controlling Multiple Access
Shows when and why to use semaphores instead of locks
"""
from threading import Thread, Semaphore, Lock
import time
import random

# ============================================================
# PROBLEM: Limited Resources (e.g., Database Connections)
# ============================================================

def database_query_with_lock(query_id, lock):
    """Using Lock - only ONE thread at a time"""
    with lock:
        print(f"Query {query_id}: Executing...")
        time.sleep(1)  # Simulate query execution
        print(f"Query {query_id}: Done")

def lock_demo():
    print("=" * 60)
    print("Using LOCK - Only 1 query at a time")
    print("=" * 60)
    
    lock = Lock()
    threads = []
    
    start = time.time()
    
    for i in range(1, 6):
        t = Thread(target=database_query_with_lock, args=(i, lock))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    print(f"\nTotal time: {elapsed:.2f}s")
    print("(All queries ran sequentially)\n")

# ============================================================
# SOLUTION: Semaphore - Allow N threads simultaneously
# ============================================================

def database_query_with_semaphore(query_id, semaphore):
    """Using Semaphore - allow 3 threads at once"""
    with semaphore:
        print(f"Query {query_id}: Executing...")
        time.sleep(1)
        print(f"Query {query_id}: Done")

def semaphore_demo():
    print("=" * 60)
    print("Using SEMAPHORE - Allow 3 queries at a time")
    print("=" * 60)
    
    semaphore = Semaphore(3)  # Allow 3 threads
    threads = []
    
    start = time.time()
    
    for i in range(1, 6):
        t = Thread(target=database_query_with_semaphore, args=(i, semaphore))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    elapsed = time.time() - start
    print(f"\nTotal time: {elapsed:.2f}s")
    print("(Queries ran in batches of 3)\n")

# ============================================================
# REAL EXAMPLE: Connection Pool
# ============================================================

class ConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = Semaphore(max_connections)
        self.max_connections = max_connections
    
    def execute_query(self, user_id):
        print(f"User {user_id}: Requesting connection...")
        
        with self.semaphore:  # Wait for available connection
            print(f"User {user_id}: ✓ Got connection, executing query...")
            time.sleep(random.uniform(0.5, 1.5))  # Simulate query
            print(f"User {user_id}: Query complete, releasing connection")

def connection_pool_demo():
    print("=" * 60)
    print("Real Example: Database Connection Pool")
    print("=" * 60)
    
    pool = ConnectionPool(max_connections=2)
    
    print("Connection pool has 2 connections available\n")
    
    threads = []
    for i in range(1, 6):
        t = Thread(target=pool.execute_query, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.1)  # Stagger starts
    
    for t in threads:
        t.join()
    
    print("\nAll users served!")

if __name__ == "__main__":
    lock_demo()
    semaphore_demo()
    connection_pool_demo()
    
    print("\n" + "=" * 60)
    print("LOCK vs SEMAPHORE:")
    print("=" * 60)
    print("LOCK (Mutex):")
    print("  • Only 1 thread at a time")
    print("  • Use when: Protecting shared variable")
    print("  • Example: Counter, account balance")
    
    print("\nSEMAPHORE:")
    print("  • Allow N threads at a time")
    print("  • Use when: Limited resources (connections, slots)")
    print("  • Example: Database pool, printer queue")
    
    print("\n💡 Semaphore(1) = Lock")
