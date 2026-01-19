# Quick Reference: Synchronization in Python

## The Big Question Answer

**Q: If GIL locks threads, why do we need Mutex?**

**A: GIL locks INTERPRETER execution, Mutex locks DATA access**

```
GIL:   WHO can execute Python bytecode
Mutex: WHAT data can be accessed

Even with GIL, context switching breaks atomicity!
```

---

## Key Concepts

### 1. Race Condition
**What:** Multiple threads accessing shared data → wrong results
**Fix:** Use locks

### 2. Critical Section
**What:** Code that accesses shared resource
**Fix:** Protect with lock

### 3. Atomic Operation
**What:** Operation that completes without interruption
**Problem:** `count += 1` is NOT atomic (3 bytecode steps)

---

## Lock Templates

### Basic Lock (DON'T USE)
```python
lock = Lock()
lock.acquire()  # Get lock
# critical section
lock.release()  # Release lock
```
❌ Risky: If exception occurs, lock never released!

### Context Manager (ALWAYS USE)
```python
lock = Lock()
with lock:
    # critical section
    pass
```
✓ Safe: Auto-releases even on exceptions
✓ Cleaner code
✓ Pythonic way

---

## Full Example Template

```python
from threading import Thread, Lock

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = Lock()
    
    def increment(self):
        with self.lock:  # Protect critical section
            self.count += 1
    
    def get_count(self):
        with self.lock:
            return self.count

# Usage
counter = Counter()
threads = [Thread(target=counter.increment) for _ in range(100)]
for t in threads: t.start()
for t in threads: t.join()
print(counter.get_count())  # Always 100!
```

---

## Deadlock Prevention

### Problem: Circular Wait
```python
# Thread A
with lock1:
    with lock2:
        pass

# Thread B
with lock2:  # Different order!
    with lock1:
        pass
# Result: DEADLOCK!
```

### Solution: Same Order
```python
# Thread A
with lock1:
    with lock2:
        pass

# Thread B
with lock1:  # Same order!
    with lock2:
        pass
# Result: No deadlock ✓
```

### Prevention Rules
1. **Lock Ordering:** Always acquire locks in same order
2. **Single Lock:** Use one lock for related data
3. **Timeout:** Use `lock.acquire(timeout=1)`
4. **Avoid Nesting:** Minimize nested locks

---

## Semaphore

### When to Use
- Limit concurrent access to N threads
- Examples: connection pools, rate limiting

### Template
```python
from threading import Semaphore

# Allow max 3 threads
semaphore = Semaphore(3)

def task():
    with semaphore:  # Wait if 3 threads already using
        # Do work
        pass
```

### Lock vs Semaphore
```
Lock           = Semaphore(1)  → Only 1 thread
Semaphore(N)   = Allow N threads
```

---

## Decision Chart

```
Do you have shared data?
│
├─ No  → No lock needed
│
└─ Yes → Do multiple threads access it?
    │
    ├─ No  → No lock needed
    │
    └─ Yes → Need synchronization!
        │
        ├─ Only 1 thread should access?
        │   └─→ Use Lock
        │
        └─ Allow N threads?
            └─→ Use Semaphore(N)
```

---

## Common Patterns

### Pattern 1: Shared Counter
```python
lock = Lock()
count = 0

with lock:
    count += 1
```

### Pattern 2: Shared List
```python
lock = Lock()
items = []

with lock:
    items.append(item)
```

### Pattern 3: Database Pool
```python
db_pool = Semaphore(5)  # Max 5 connections

with db_pool:
    # Use database connection
    pass
```

---

## Key Reminders

### Always Remember
- ✓ Use `with lock:` not acquire/release
- ✓ Keep critical sections small
- ✓ Consistent lock ordering
- ✓ Lock only what you need

### Common Mistakes
- ❌ Forgetting to release lock
- ❌ Different lock order (deadlock)
- ❌ Locking too much code
- ❌ Using acquire/release directly

---

## GIL vs Mutex Summary

| Feature | GIL | Mutex |
|---------|-----|-------|
| Locks | Interpreter | Data |
| Scope | All Python code | Your variables |
| Automatic | Yes (built-in) | No (you add) |
| Purpose | Memory safety | Data consistency |
| One per | Process | Critical section |

**Key:** Need BOTH for thread-safe code!

---

## Quick Troubleshooting

**Problem:** Count not correct after threads finish
→ **Fix:** Add lock around increment/decrement

**Problem:** Program hangs forever
→ **Fix:** Check for deadlock (lock order)

**Problem:** Lock never released (program stuck)
→ **Fix:** Use `with lock:` instead of acquire/release

**Problem:** Too many threads using resource
→ **Fix:** Use Semaphore(N) to limit

---

## Syntax Cheat Sheet

```python
# Import
from threading import Lock, Semaphore, Thread

# Create
lock = Lock()
sem = Semaphore(3)

# Use (context manager - ALWAYS)
with lock:
    # critical section
    pass

# Thread with lock
class Worker(Thread):
    def __init__(self, lock):
        super().__init__()
        self.lock = lock
    
    def run(self):
        with self.lock:
            # safe code here
            pass

# Create and run
lock = Lock()
threads = [Worker(lock) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
```

---

## One-Liner Rules

1. **Shared data + Multiple threads = Need Lock**
2. **Always use `with lock:` never acquire/release**
3. **Same lock order = No deadlock**
4. **Lock = 1 thread, Semaphore(N) = N threads**
5. **GIL locks interpreter, Mutex locks data**
6. **Critical section = Code accessing shared data**
7. **count += 1 is NOT atomic (3 bytecode ops)**
8. **Context manager = Auto-release on error**

---

## Final Checklist

Before writing multithreaded code:
- [ ] Identified shared data?
- [ ] Added Lock/Semaphore?
- [ ] Using context manager (`with`)?
- [ ] Checked lock ordering?
- [ ] Kept critical sections small?
- [ ] Tested with many iterations?

If all ✓ → Your code is thread-safe! 🎉
