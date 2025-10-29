"""
Example 2: Using Mutex Locks to Fix Race Conditions
Shows how locks ensure correct results
"""
from threading import Thread, Lock
import time

class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1

class AdderWithLock(Thread):
    def __init__(self, counter, lock, iterations):
        super().__init__()
        self.counter = counter
        self.lock = lock
        self.iterations = iterations
    
    def run(self):
        for _ in range(self.iterations):
            self.lock.acquire()  # Get the lock
            self.counter.increment()
            self.lock.release()  # Release the lock

class SubtractorWithLock(Thread):
    def __init__(self, counter, lock, iterations):
        super().__init__()
        self.counter = counter
        self.lock = lock
        self.iterations = iterations
    
    def run(self):
        for _ in range(self.iterations):
            self.lock.acquire()  # Get the lock
            self.counter.decrement()
            self.lock.release()  # Release the lock

if __name__ == "__main__":
    print("=" * 60)
    print("Adder-Subtractor WITH Locks")
    print("=" * 60)
    
    # Try with different iteration counts
    for iterations in [100, 1000, 10000, 100000]:
        counter = Counter()
        lock = Lock()  # Create a lock
        
        adder = AdderWithLock(counter, lock, iterations)
        subtractor = SubtractorWithLock(counter, lock, iterations)
        
        adder.start()
        subtractor.start()
        
        adder.join()
        subtractor.join()
        
        print(f"Iterations: {iterations:6d} | Expected: 0 | Actual: {counter.count:6d}")
    
    print("\n" + "=" * 60)
    print("KEY OBSERVATION:")
    print("=" * 60)
    print("✓ Result is ALWAYS 0 (correct!)")
    print("✓ Locks ensure only ONE thread in critical section")
    print("✓ No race condition")
    
    print("\n" + "=" * 60)
    print("HOW MUTEX LOCK WORKS:")
    print("=" * 60)
    print("1. Thread calls lock.acquire()")
    print("   → If lock is free: Thread gets it, enters critical section")
    print("   → If lock is taken: Thread WAITS")
    print("2. Thread executes critical section")
    print("3. Thread calls lock.release()")
    print("   → Lock becomes free for other threads")
