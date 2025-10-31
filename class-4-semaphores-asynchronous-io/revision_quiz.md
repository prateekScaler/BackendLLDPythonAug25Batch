# 🧠 Threading & Synchronization Quiz
## Test Your Knowledge!

---

## Question 1: The GIL Gotcha 🤔

```python
counter = 0
# Two threads both do: counter += 1
# 1000 times each
```

**Q: Final value with GIL active?**

A) Always 2000

B) Always less than 2000

C) Could be anywhere from 2 to 2000

D) Python will throw an error

---

## Answer 1: C 🎯

**GIL doesn't prevent race conditions in YOUR code!**

```
counter += 1  →  LOAD, ADD, STORE (3 bytecode ops)
GIL can switch between these!
```

**Remember:** GIL ≠ Thread safety for your variables!

---

## Question 2: ThreadPoolExecutor Mystery 🕵️

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)
executor.submit(task, 1)
executor.submit(task, 2)
executor.submit(task, 3)
# Program ends here
```

**Q: What's the problem?**

A) max_workers should be higher

B) Tasks may not complete before program exits

C) Need to call executor.start()

D) submit() is the wrong method

---

## Answer 2: B 🚨

**No waiting for tasks to complete!**

```python
# BAD - tasks may be interrupted
executor.submit(task)
# program exits immediately!

# GOOD - wait for completion
with ThreadPoolExecutor() as executor:
    executor.submit(task)
# automatically waits

# OR
future = executor.submit(task)
future.result()  # waits for completion
```

---

## Question 3: Future or Result? 🔮

```python
with ThreadPoolExecutor() as executor:
    result = executor.submit(calculate, 10)
    print(result + 5)
```

**Q: What happens?**

A) Prints the calculated value + 5

B) TypeError: unsupported operand type

C) Waits forever

D) Returns Future object address

---

## Answer 3: B 💥

**submit() returns a Future, not the result!**

```python
# WRONG
result = executor.submit(calculate, 10)
print(result + 5)  # Can't add to Future!

# RIGHT
future = executor.submit(calculate, 10)
result = future.result()  # Get actual value
print(result + 5)
```

**Remember:** Future ≠ Result. Call `.result()` to get value!

---

## Question 4: Deadlock Detective 🔍

```python
# Thread 1
with lock_A:
    time.sleep(0.1)
    with lock_B:
        work()

# Thread 2
with lock_B:
    time.sleep(0.1)
    with lock_A:
        work()
```

**Q: Will this ALWAYS deadlock?**

A) Yes, every time

B) No, never

C) Sometimes (race condition)

D) Only on multi-core CPUs

---

## Answer 5: C 🎲

**Deadlock is a race condition itself!**

If Thread 1 gets BOTH locks before Thread 2 starts:
→ No deadlock!

If both get first lock simultaneously:
→ DEADLOCK! 💥

**Lesson:** Don't rely on luck. Use lock ordering!

---

## Question 5: Context Manager Trap

```python
lock = Lock()

with lock:
    with lock:  # Nested!
        print("Safe?")
```

**Q: What happens?**

A) Works fine

B) Deadlock!

C) Exception raised

D) Second lock ignored

---

## Answer 5: B 💀

**Thread deadlocks ITSELF!**

```
First 'with': Acquires lock ✓
Second 'with': Tries to acquire same lock...
              But it's already held!
              Waits forever for itself! 😵
```

**Solution:** Use `RLock()` (Reentrant Lock)

---

## Question 6: The Sneaky Bug 🐛

```python
class Counter:
    count = 0  # Class variable!
    
c1 = Counter()
c2 = Counter()

# Thread 1 increments c1.count
# Thread 2 increments c2.count
```

**Q: Need locks?**

A) No, different objects

B) Yes! They share class variable

C) Only on Windows

D) Only if count > 1000

---

## Answer 6: B 

**Class variables are SHARED across instances!**

```python
class Counter:
    count = 0  # ← Shared by ALL instances!

c1.count and c2.count point to SAME memory!
```

**Fix:**
```python
class Counter:
    def __init__(self):
        self.count = 0  # Instance variable
```

---

## Question 7: ProcessPool vs ThreadPool

```python
def calculate_pi(digits):
    # Heavy computation
    return compute(digits)

# Which is faster for 4 tasks?
# A) ThreadPoolExecutor(4)
# B) ProcessPoolExecutor(4)
```

**Q: Which executor and why?**

A) ThreadPool (lower overhead)

B) ProcessPool (CPU-bound task)

C) Same speed

D) Depends on number of CPU cores

---

## Answer 7: B

**CPU-bound = Processes win!**

```
ThreadPool:   GIL prevents parallelism
              All 4 threads take turns
              No speedup!

ProcessPool:  Each has own GIL
              True parallel execution
              ~4x faster!
```

**Remember:** CPU → Processes, I/O → Threads

---

## Question 8: The Timeout Trick

```python
if lock.acquire(timeout=5):
    work()
    lock.release()
```

**Q: What's the bug?**

A) Timeout too short

B) Should use 'with' statement

C) If exception in work(), lock never released

D) acquire() doesn't take timeout

---

## Answer 8: C 🔓

**Exception = Lock stays locked forever!**

```python
# GOOD
if lock.acquire(timeout=5):
    try:
        work()
    finally:
        lock.release()  # Always runs!

# BETTER
if lock.acquire(timeout=5):
    with lock:
        work()
```

---

## Question 9: Future.result() Behavior 📞

```python
future = executor.submit(slow_task)  # Takes 5 seconds
print("Submitted!")
result = future.result()
print("Got result!")
```

**Q: When does "Got result!" print?**

A) Immediately after submit

B) After 5 seconds (blocks until complete)

C) Never (need to call future.wait())

D) Raises exception

---

## Answer 9: B ⏳

**result() is BLOCKING!**

```python
future = executor.submit(slow_task)
print("Submitted!")          # Prints immediately
result = future.result()     # WAITS 5 seconds here
print("Got result!")         # Prints after 5 seconds
```

**Check without blocking:**
```python
if future.done():
    result = future.result()  # Won't block
```

---

## Question 10:

```python
lock = Lock()
lock.acquire()
with lock:
    print("Hello")
lock.release()
```

**Q: What happens?**

A) Prints "Hello" twice

B) Deadlock immediately

C) Works fine

D) Prints "Hello" then deadlocks

---

## Answer 10: B 💥

**Timeline:**
```
1. acquire() → Gets lock ✓
2. with lock:
   → Tries to acquire AGAIN
   → But already held!
   → DEADLOCK (waits forever)
3. Never reaches print() or release()
```

**Don't mix manual acquire() with 'with'!**

---


## Question 11: Producer-Consumer Race 🏃

```python
buffer = []

def producer():
    if len(buffer) < 5:
        buffer.append(item)

def consumer():
    if len(buffer) > 0:
        buffer.pop()
```

**Q: What's wrong?**

A) Nothing, len() is thread-safe

B) Race condition between check and action

C) Need to use queue.Queue instead

D) Both B and C

---

## Answer 11: D 🎯

**Classic check-then-act race condition!**

```
Thread 1: if len(buffer) < 5:  ✓ (len=4)
Thread 2: if len(buffer) < 5:  ✓ (len=4)
Thread 1: buffer.append(item)  (len=5)
Thread 2: buffer.append(item)  (len=6) 💥 Overflow!
```

**Solutions:**
- Use locks around check+action
- Better: Use `queue.Queue` (thread-safe!)

---

## 🏆 Scoring

**12/12:** Threading Ninja! 🥷

**9-11:** Pretty solid! 💪

**6-8:** Good effort! Keep learning! 📚

**0-5:** Review the material! You got this! 🎯

---

## Key Takeaways 🎓

✅ GIL ≠ Thread safety for YOUR code

✅ Future ≠ Result (call .result() to get value)

✅ Always wait for executor tasks to complete

✅ Producer-Consumer needs locks or Queue

✅ Lock ordering prevents deadlock

✅ I/O-bound → Threads, CPU-bound → Processes

✅ Context managers (`with`) = Automatic cleanup

✅ Semaphore(N) for limiting N concurrent threads

✅ Always use try-finally with manual acquire()

---

## 🎉 Ready for Today's Class!

**Today:** Semaphores & Async I/O

**Remember:**
- Mutex = 1 thread allowed
- Semaphore = N threads allowed
- Async = Single thread, many tasks!

Let's go! 🚀