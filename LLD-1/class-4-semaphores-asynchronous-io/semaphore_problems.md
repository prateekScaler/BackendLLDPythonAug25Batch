# Semaphore Practice Problems

## LeetCode-Style Problems

---

### Problem 1: Print in Order (Easy)
**LeetCode #1114** : https://leetcode.com/problems/print-in-order/

```python
"""
Three threads print "first", "second", "third" in order.
Use semaphores to ensure correct order.
"""

class Foo:
    def __init__(self):
        # Your code here
        pass
    
    def first(self):
        print("first", end="")
    
    def second(self):
        print("second", end="")
    
    def third(self):
        print("third", end="")
```

**Expected Output:** `firstsecondthird`

---

### Problem 2: Print FooBar Alternately (Medium)
**LeetCode #1115**: https://leetcode.com/problems/print-foobar-alternately/description/

```python
"""
Two threads print "foo" and "bar" alternately n times.
Output: foobarfoobarfoobar...
"""

class FooBar:
    def __init__(self, n):
        self.n = n
        # Your code here
    
    def foo(self):
        for i in range(self.n):
            print("foo", end="")
    
    def bar(self):
        for i in range(self.n):
            print("bar", end="")
```

**Expected Output (n=3):** `foobarfoobarfoobar`

---

### Problem 3: Bounded Blocking Queue (Medium)
**LeetCode #1188**: https://leetcode.com/problems/design-bounded-blocking-queue/description/

```python
"""
Implement a thread-safe bounded blocking queue.
- enqueue() blocks when full
- dequeue() blocks when empty
"""

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        # Your code here
        pass
    
    def enqueue(self, element: int) -> None:
        # Block if queue is full
        pass
    
    def dequeue(self) -> int:
        # Block if queue is empty
        pass
    
    def size(self) -> int:
        pass
```

**Hint:** Use 2 semaphores (empty, full) + 1 lock

---

### Problem 4: The Dining Philosophers (Hard)
**LeetCode #1226**: https://leetcode.com/problems/the-dining-philosophers/description/

```python
"""
5 philosophers sit at a round table.
Each needs 2 forks to eat.
Prevent deadlock!
"""

class DiningPhilosophers:
    def __init__(self):
        # Your code here
        pass
    
    def wantsToEat(self, philosopher: int,
                   pickLeftFork, pickRightFork,
                   eat, putLeftFork, putRightFork):
        # Implement without deadlock
        pass
```

**Challenge:** No philosopher should starve

---

### Problem 5: Traffic Light Controlled Intersection (Hard)
**LeetCode #1279**: https://leetcode.com/problems/traffic-light-controlled-intersection/description/

```python
"""
Intersection with 4 roads (N, S, E, W).
Cars from perpendicular directions can't cross simultaneously.
"""

class TrafficLight:
    def __init__(self):
        # Your code here
        pass
    
    def carArrived(self, carId: int, roadId: int,
                   direction: int,
                   turnGreen, crossCar):
        # roadId: 1=North, 2=East, 3=South, 4=West
        # direction: 1=straight, 2=right, 3=left
        pass
```

---

### Problem 6: Building H2O (Medium)
**LeetCode #1117**

```python
"""
H and O threads form water molecules (H2O).
Every 2 H threads and 1 O thread make one molecule.
"""

class H2O:
    def __init__(self):
        # Your code here
        pass
    
    def hydrogen(self):
        print("H", end="")
    
    def oxygen(self):
        print("O", end="")
```

**Expected Output:** `HHO` or `HOH` or `OHH` (order within molecule varies)

**Hint:** Use semaphores to count H and O atoms

---

### Problem 7: Fizz Buzz Multithreaded (Medium)
**LeetCode #1195**

```python
"""
4 threads print FizzBuzz sequence:
Thread A: Numbers divisible by 3 and 5 → "fizzbuzz"
Thread B: Numbers divisible by 3 only → "fizz"
Thread C: Numbers divisible by 5 only → "buzz"
Thread D: Other numbers → number itself
"""

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        # Your code here
    
    def fizz(self):
        # Print "fizz"
        pass
    
    def buzz(self):
        # Print "buzz"
        pass
    
    def fizzbuzz(self):
        # Print "fizzbuzz"
        pass
    
    def number(self, x: int):
        # Print number
        pass
```

---

### Problem 8: Rate Limiter (Custom)

```python
"""
Implement a rate limiter using semaphores:
- Max N requests per second
- Requests exceeding limit should wait
"""

class RateLimiter:
    def __init__(self, max_per_second: int):
        # Your code here
        pass
    
    def acquire(self):
        # Wait if rate limit exceeded
        pass
```

**Test:**
```python
limiter = RateLimiter(3)
# Make 5 requests quickly
# First 3 succeed, next 2 wait 1 second
```

---

## Practice Tips

1. **Start simple:** Try Print in Order first
2. **Visualize:** Draw state diagrams
3. **Test edge cases:** Single thread, many threads
4. **Think deadlock:** Check for circular wait
5. **Use context managers:** `with semaphore:`

---

## Key Patterns to Learn

### Pattern 1: Sequential Execution
```python
sem1 = Semaphore(0)
sem2 = Semaphore(0)

# Thread 1
task1()
sem1.release()

# Thread 2
sem1.acquire()
task2()
sem2.release()

# Thread 3
sem2.acquire()
task3()
```

### Pattern 2: Alternating Execution
```python
sem_A = Semaphore(1)
sem_B = Semaphore(0)

# Thread A
while True:
    sem_A.acquire()
    print("A")
    sem_B.release()

# Thread B
while True:
    sem_B.acquire()
    print("B")
    sem_A.release()
```

### Pattern 3: Bounded Buffer
```python
empty = Semaphore(capacity)
full = Semaphore(0)
mutex = Lock()

# Producer
empty.acquire()
with mutex:
    buffer.append(item)
full.release()

# Consumer
full.acquire()
with mutex:
    item = buffer.pop()
empty.release()
```

---

Good luck! 🚀
