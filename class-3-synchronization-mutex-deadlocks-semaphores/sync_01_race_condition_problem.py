"""
Example 1: Race Condition - Adder & Subtractor Problem
Demonstrates why we need locks even with GIL
"""
from threading import Thread
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

class Adder(Thread):
    def __init__(self, count, iterations):
        super().__init__()
        self.count = count
        self.iterations = iterations
    
    def run(self):
        for i in range(self.iterations):
            self.count.increment()

class Subtractor(Thread):
    def __init__(self, count, iterations):
        super().__init__()
        self.count = count
        self.iterations = iterations
    
    def run(self):
        for i in range(self.iterations):
            self.count.decrement()

if __name__ == "__main__":
    print("=" * 60)
    print("Race Condition Demo: Adder & Subtractor")
    print("=" * 60)
    
    # Test with different iteration counts
    test_cases = [100, 1000, 10000, 100000]
    
    for iterations in test_cases:
        count = Count()
        
        adder = Adder(count, iterations)
        subtractor = Subtractor(count, iterations)
        
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
    print("WHY THIS HAPPENS:")
    print("=" * 60)
    print("""
count += 1 is NOT atomic! It's actually 3 steps:
1. LOAD count    (read current value)
2. ADD 1         (calculate new value)
3. STORE count   (write new value)

GIL allows context switch between these steps!

Example:
  Adder:      LOAD(5) → ADD(6) → [SWITCH] → STORE(6)
  Subtractor:           [SWITCH] → LOAD(5) → SUB(4) → STORE(4)
  
Result: 4 instead of 5 - Lost the addition!

KEY: GIL locks INTERPRETER, NOT your data!
     You need MUTEX to lock your data!
    """)
