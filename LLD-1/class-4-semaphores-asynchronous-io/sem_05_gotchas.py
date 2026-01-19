"""
Part 5: Semaphore Gotchas & Best Practices
Common mistakes and how to avoid them
"""
from threading import Thread, Semaphore
import time

print("=" * 60)
print("SEMAPHORE GOTCHAS & BEST PRACTICES")
print("=" * 60)

# ============================================================
# Gotcha 1: Forgetting to Release
# ============================================================

print("\n1. GOTCHA: Forgetting to Release")
print("-" * 60)

def bad_example_no_release():
    """Don't do this!"""
    sem = Semaphore(2)
    
    def worker(n):
        sem.acquire()
        print(f"Worker {n} working...")
        if n == 2:
            raise Exception("Oops!")  # Never releases!
        sem.release()
    
    for i in range(3):
        Thread(target=worker, args=(i,)).start()

print("❌ BAD:")
print("sem.acquire()")
print("work()  # If error, never releases!")
print("sem.release()")

print("\n✓ GOOD: Use try-finally or context manager")
print("with sem:")
print("    work()  # Always releases!")

# ============================================================
# Gotcha 2: Deadlock with Multiple Semaphores
# ============================================================

print("\n\n2. GOTCHA: Deadlock with Multiple Semaphores")
print("-" * 60)

print("❌ BAD:")
print("# Thread 1")
print("sem_A.acquire()")
print("sem_B.acquire()  # Deadlock if Thread 2 has B!")
print("")
print("# Thread 2")
print("sem_B.acquire()")
print("sem_A.acquire()")

print("\n✓ GOOD: Always acquire in same order")
print("Both threads: sem_A first, then sem_B")

# ============================================================
# Gotcha 3: Initial Value Confusion
# ============================================================

print("\n\n3. GOTCHA: Initial Value Confusion")
print("-" * 60)

print("Semaphore(5) means:")
print("  • 5 threads can acquire simultaneously")
print("  • NOT that semaphore 'has' 5 resources")
print("")
print("For producer-consumer:")
print("  empty = Semaphore(5)   # 5 empty slots")
print("  full = Semaphore(0)    # 0 items initially")

# ============================================================
# Gotcha 4: Semaphore vs Lock Confusion
# ============================================================

print("\n\n4. GOTCHA: Using Semaphore(1) instead of Lock")
print("-" * 60)

print("❌ Confusing:")
print("sem = Semaphore(1)  # Works but unclear intent")
print("")
print("✓ Clear:")
print("lock = Lock()  # Obviously for mutual exclusion")
print("")
print("Use Semaphore(1) only if you might change to Semaphore(N) later!")

# ============================================================
# Gotcha 5: Blocking vs Non-blocking
# ============================================================

print("\n\n5. GOTCHA: Not knowing blocking behavior")
print("-" * 60)

def blocking_demo():
    sem = Semaphore(1)
    
    # Blocking (default)
    sem.acquire()  # Waits forever if not available
    
    # Non-blocking
    if sem.acquire(blocking=False):  # Returns immediately
        print("Got it!")
    else:
        print("Not available")
    
    # With timeout
    if sem.acquire(timeout=2):  # Waits max 2 seconds
        print("Got it!")
    else:
        print("Timeout!")

print("acquire() has 3 modes:")
print("  1. acquire()              # Block forever (default)")
print("  2. acquire(blocking=False) # Return immediately")
print("  3. acquire(timeout=5)     # Wait max 5 seconds")

# ============================================================
# Best Practice Summary
# ============================================================

print("\n\n" + "=" * 60)
print("BEST PRACTICES:")
print("=" * 60)

print("""
✓ Always use context manager (with)
✓ Initialize with correct count
✓ Release in finally block if not using 'with'
✓ Use Lock for mutual exclusion (not Semaphore(1))
✓ Use Semaphore for counting/limiting resources
✓ Consider timeouts for acquire()
✓ Document what semaphore counts/limits
✓ Avoid mixing semaphores and locks unnecessarily

❌ Don't forget to release
❌ Don't acquire in different orders (deadlock)
❌ Don't use Semaphore(1) when Lock is clearer
❌ Don't use blocking acquire() if timeout makes sense
""")

# ============================================================
# Common Patterns
# ============================================================

print("=" * 60)
print("COMMON PATTERNS:")
print("=" * 60)

print("""
1. Resource Pool:
   sem = Semaphore(N)  # N resources available
   with sem:
       use_resource()

2. Rate Limiting:
   sem = Semaphore(max_per_second)
   if sem.acquire(blocking=False):
       make_api_call()
       schedule_release_after_1_second()

3. Producer-Consumer:
   empty = Semaphore(buffer_size)
   full = Semaphore(0)
   mutex = Lock()
   
   Producer: empty.acquire() → add → full.release()
   Consumer: full.acquire() → remove → empty.release()

4. Barrier (wait for all):
   sem = Semaphore(0)
   # N threads call sem.release()
   # Main thread calls sem.acquire() N times
""")

print("=" * 60)
print("REMEMBER:")
print("=" * 60)
print("Semaphore = Counting Lock")
print("  • Lock allows 1")
print("  • Semaphore(N) allows N")
print("  • Use for limiting concurrent access to resources!")
print("=" * 60)
