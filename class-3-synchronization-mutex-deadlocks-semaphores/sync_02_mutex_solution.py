"""
Example 2: Solving Race Condition with Mutex Lock
Shows how Lock() fixes the adder/subtractor problem
"""
from threading import Thread, Lock
import time

class Count:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
    
    def decrement(self):
        self.value -= 1
    
    def get_value(self):
        return self.value

class AdderWithLock(Thread):
    def __init__(self, count, lock, iterations):
        super().__init__()
        self.count = count
        self.lock = lock
        self.iterations = iterations
    
    def run(self):
        for i in range(self.iterations):
            self.lock.acquire()  # Get the lock
            self.count.increment()
            self.lock.release()  # Release the lock

class SubtractorWithLock(Thread):
    def __init__(self, count, lock, iterations):
        super().__init__()
        self.count = count
        self.lock = lock
        self.iterations = iterations
    
    def run(self):
        for i in range(self.iterations):
            self.lock.acquire()  # Get the lock
            self.count.decrement()
            self.lock.release()  # Release the lock

if __name__ == "__main__":
    print("=" * 60)
    print("SOLUTION: Using Mutex Lock")
    print("=" * 60)
    
    test_cases = [100, 1000, 10000, 100000]
    
    for iterations in test_cases:
        count = Count()
        lock = Lock()  # Create a lock
        
        adder = AdderWithLock(count, lock, iterations)
        subtractor = SubtractorWithLock(count, lock, iterations)
        
        adder.start()
        subtractor.start()
        
        adder.join()
        subtractor.join()
        
        final_value = count.get_value()
        expected = 0
        
        print(f"\nIterations: {iterations:,}")
        print(f"Expected: {expected}")
        print(f"Actual:   {final_value}")
        
        if final_value == expected:
            print("✓ Correct!")
        else:
            print(f"✗ Wrong! Difference: {abs(final_value - expected)}")
    
    print("\n" + "=" * 60)
    print("HOW LOCK WORKS:")
    print("=" * 60)
    print("""
lock.acquire() - Thread gets the lock (waits if someone else has it)
lock.release() - Thread releases the lock (others can now get it)

Only ONE thread can hold the lock at a time!

Example with lock:
  Thread A: acquire() → LOAD → ADD → STORE → release()
  Thread B: [waiting...] → acquire() → LOAD → SUB → STORE → release()
  
No interruption during critical section!
Result is always correct!

KEY: Lock protects the CRITICAL SECTION (shared data access)
    """)
