"""
Example 5: Semaphore - Allowing N Threads
When you need more than 1 thread but not unlimited
"""
from threading import Thread, Semaphore, Lock
import time

# ============================================================
# Comparison: Lock vs Semaphore
# ============================================================
def compare_lock_vs_semaphore():
    print("=" * 60)
    print("Lock vs Semaphore Comparison")
    print("=" * 60)
    
    # Using Lock (only 1 thread at a time)
    print("\n1. Using Lock (max 1 thread):")
    print("-" * 60)
    
    lock = Lock()
    
    def task_with_lock(thread_id):
        with lock:
            print(f"  [Thread {thread_id}] Working...")
            time.sleep(1)
            print(f"  [Thread {thread_id}] Done")
    
    start = time.time()
    threads = [Thread(target=task_with_lock, args=(i,)) for i in range(1, 4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    lock_time = time.time() - start
    
    print(f"Time taken: {lock_time:.2f}s (sequential - one at a time)")
    
    # Using Semaphore (allow N threads)
    print("\n2. Using Semaphore (max 2 threads):")
    print("-" * 60)
    
    semaphore = Semaphore(2)  # Allow 2 threads
    
    def task_with_semaphore(thread_id):
        with semaphore:
            print(f"  [Thread {thread_id}] Working...")
            time.sleep(1)
            print(f"  [Thread {thread_id}] Done")
    
    start = time.time()
    threads = [Thread(target=task_with_semaphore, args=(i,)) for i in range(1, 4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    sem_time = time.time() - start
    
    print(f"Time taken: {sem_time:.2f}s (2 at a time)")

# ============================================================
# Real-World Example: Database Connection Pool
# ============================================================
def database_pool_example():
    print("\n" + "=" * 60)
    print("Real Example: Database Connection Pool")
    print("=" * 60)
    print("Scenario: Only 3 database connections available")
    print("-" * 60)
    
    # Semaphore allows max 3 concurrent database connections
    db_pool = Semaphore(3)
    
    def access_database(user_id):
        print(f"[User {user_id}] Requesting database access...")
        
        with db_pool:  # Wait if all 3 connections are busy
            print(f"[User {user_id}] ✓ Got connection! Querying database...")
            time.sleep(2)  # Simulate database query
            print(f"[User {user_id}] Query complete, releasing connection")
    
    # 5 users trying to access database, but only 3 connections available
    threads = [Thread(target=access_database, args=(i,)) for i in range(1, 6)]
    
    start = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    total_time = time.time() - start
    
    print(f"\n✓ All users served in {total_time:.2f}s")
    print("Notice: Max 3 users at a time (semaphore limit)")

# ============================================================
# Visualizing Semaphore
# ============================================================
def visualize_semaphore():
    print("\n" + "=" * 60)
    print("How Semaphore Works")
    print("=" * 60)
    
    print("""
Semaphore(3) = 3 permits available

Timeline:
─────────────────────────────────────────
Thread 1: [Working...] (permit 1)
Thread 2: [Working...] (permit 2)
Thread 3: [Working...] (permit 3)
Thread 4: [Waiting...] (no permits available)
Thread 5: [Waiting...] (no permits available)
─────────────────────────────────────────
[Thread 1 finishes] (permit 1 released)
Thread 4: [Working...] (got permit 1)
─────────────────────────────────────────

Key Points:
• Semaphore(N) allows N threads simultaneously
• Threads wait if all N permits are taken
• When thread finishes, permit is released
• Next waiting thread gets the permit
    """)

if __name__ == "__main__":
    compare_lock_vs_semaphore()
    database_pool_example()
    visualize_semaphore()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    print("""
Lock vs Semaphore:
┌─────────────┬──────────────┬────────────────┐
│ Feature     │ Lock         │ Semaphore(N)   │
├─────────────┼──────────────┼────────────────┤
│ Max threads │ 1            │ N              │
│ Use case    │ Mutual excl. │ Limited access │
│ Example     │ Shared var   │ Connection pool│
└─────────────┴──────────────┴────────────────┘

When to use Semaphore:
✓ Database connection pools (limited connections)
✓ API rate limiting (max N requests/second)
✓ Resource pools (max N file handles)
✓ Throttling (limit concurrent operations)

Remember:
• Lock = Semaphore(1)
• Semaphore(N) = Allow N threads max
• Use Lock for data protection
• Use Semaphore for resource limiting
    """)
