"""
Example 1: GIL Doesn't Prevent Race Conditions
Demonstrates why we need locks even with GIL
"""
from threading import Thread
import time

class Counter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        # This LOOKS like one operation, but it's actually THREE:
        # 1. Load count value
        # 2. Add 1
        # 3. Store back
        self.count += 1
    
    def decrement(self):
        self.count -= 1

class Adder(Thread):
    def __init__(self, counter, iterations):
        super().__init__()
        self.counter = counter
        self.iterations = iterations
    
    def run(self):
        for _ in range(self.iterations):
            self.counter.increment()

class Subtractor(Thread):
    def __init__(self, counter, iterations):
        super().__init__()
        self.counter = counter
        self.iterations = iterations
    
    def run(self):
        for _ in range(self.iterations):
            self.counter.decrement()

if __name__ == "__main__":
    print("=" * 60)
    print("Adder-Subtractor WITHOUT Locks")
    print("=" * 60)
    
    # Try with different iteration counts
    for iterations in [100, 1000, 10000, 100000]:
        counter = Counter()
        
        adder = Adder(counter, iterations)
        subtractor = Subtractor(counter, iterations)
        
        adder.start()
        subtractor.start()
        
        adder.join()
        subtractor.join()
        
        print(f"Iterations: {iterations:6d} | Expected: 0 | Actual: {counter.count:6d}")
    
    print("\n" + "=" * 60)
    print("KEY OBSERVATION:")
    print("=" * 60)
    print("• Expected result: 0 (always)")
    print("• Actual result: NOT 0 (usually)")
    print("• GIL is active but race condition still occurs!")
    print("\n💡 WHY?")
    print("• count += 1 is THREE bytecode instructions")
    print("• GIL can switch threads BETWEEN these instructions")
    print("• Result: Lost updates (race condition)")
    print("\n🔒 SOLUTION: We need LOCKS to protect our code!")
