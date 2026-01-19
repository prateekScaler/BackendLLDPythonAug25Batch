"""
Example 3: Context Manager for Locks
Shows the cleaner 'with' statement approach
"""
from threading import Thread, Lock

class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1

# ============================================================
# OLD WAY: Manual acquire/release
# ============================================================
class AdderManual(Thread):
    def __init__(self, counter, lock, iterations):
        super().__init__()
        self.counter = counter
        self.lock = lock
        self.iterations = iterations
    
    def run(self):
        for _ in range(self.iterations):
            self.lock.acquire()
            try:
                self.counter.increment()
            finally:
                self.lock.release()  # Must release even if error!

# ============================================================
# NEW WAY: Context Manager (with statement)
# ============================================================
class AdderWithContext(Thread):
    def __init__(self, counter, lock, iterations):
        super().__init__()
        self.counter = counter
        self.lock = lock
        self.iterations = iterations
    
    def run(self):
        for _ in range(self.iterations):
            with self.lock:  # Automatically acquires and releases!
                self.counter.increment()

class SubtractorWithContext(Thread):
    def __init__(self, counter, lock, iterations):
        super().__init__()
        self.counter = counter
        self.lock = lock
        self.iterations = iterations
    
    def run(self):
        for _ in range(self.iterations):
            with self.lock:
                self.counter.decrement()

if __name__ == "__main__":
    print("=" * 60)
    print("Context Manager (with statement) for Locks")
    print("=" * 60)
    
    iterations = 100000
    counter = Counter()
    lock = Lock()
    
    adder = AdderWithContext(counter, lock, iterations)
    subtractor = SubtractorWithContext(counter, lock, iterations)
    
    adder.start()
    subtractor.start()
    
    adder.join()
    subtractor.join()
    
    print(f"Iterations: {iterations:6d}")
    print(f"Expected: 0")
    print(f"Actual: {counter.count}")
    
    print("\n" + "=" * 60)
    print("BENEFITS OF CONTEXT MANAGER:")
    print("=" * 60)
    print("✓ Cleaner code (with lock:)")
    print("✓ Automatic release (even if exception occurs)")
    print("✓ No need for try-finally blocks")
    print("✓ Less chance of forgetting to release")
    
    print("\n" + "=" * 60)
    print("COMPARISON:")
    print("=" * 60)
    print("\nManual (OLD):")
    print("  lock.acquire()")
    print("  try:")
    print("      # critical section")
    print("  finally:")
    print("      lock.release()")
    
    print("\nContext Manager (NEW):")
    print("  with lock:")
    print("      # critical section")
    
    print("\n💡 Always prefer 'with' statement!")
