# Synchronization in Python - Complete Guide

## 📚 Class Structure

### Part 1: Revision (10 min)
- Quick recap of Executors and Futures
- **THE KEY QUESTION**: Why do we need locks if GIL exists?

### Part 2: Understanding the Problem (15 min)
- Race conditions in action
- Why GIL doesn't protect your code
- Critical sections

### Part 3: Mutex Locks (20 min)
- Basic lock usage
- acquire() and release()
- Context managers (with statement)

### Part 4: Deadlocks (15 min)
- What is deadlock?
- How it occurs
- Prevention strategies

### Part 5: Semaphores (15 min)
- When locks aren't enough
- Controlling N threads
- Real-world use cases

---

## 🔑 Key Concepts

### Critical Section
Code that accesses shared resource
```python
def increment(self):
    self.count += 1  # ← Critical section
```

### Race Condition
Multiple threads accessing critical section simultaneously
```
Thread A: Read count (0) → Add 1 → Write (1)
Thread B: Read count (0) → Add 1 → Write (1)
Result: 1 (should be 2!)
```

### Mutex (Lock)
Ensures only ONE thread in critical section
```python
with lock:
    self.count += 1  # Only one thread here
```

### Deadlock
Threads waiting for each other forever
```
Thread A: Has Lock1, wants Lock2
Thread B: Has Lock2, wants Lock1
→ Both wait forever
```

### Semaphore
Allows N threads simultaneously
```python
semaphore = Semaphore(3)  # Allow 3 threads
```

---

## 🤔 GIL vs Locks - THE CONFUSION

### The Question Everyone Asks:
**"If GIL allows only one thread at a time, why do we need locks?"**

### The Answer:

**GIL operates at BYTECODE level, not statement level!**

#### Your Code:
```python
count += 1
```

#### Bytecode (what actually runs):
```
1. LOAD_FAST (count)
2. LOAD_CONST (1)
3. BINARY_ADD
4. STORE_FAST (count)
```

**GIL can switch threads BETWEEN these instructions!**

#### Timeline:
```
Thread A: LOAD count (0)
Thread A: ADD 1
[GIL SWITCHES TO Thread B]
Thread B: LOAD count (0)  ← Still sees 0!
Thread B: ADD 1
Thread B: STORE (1)
[GIL SWITCHES TO Thread A]
Thread A: STORE (1)  ← Overwrites B's work!
```

### Summary:
- **GIL** protects Python's internals (memory management)
- **Locks** protect YOUR data
- **Both are needed!**

---

## 🔒 Mutex Lock Usage

### Basic Pattern:
```python
from threading import Lock

lock = Lock()

# Acquire and release manually
lock.acquire()
try:
    # critical section
finally:
    lock.release()
```

### Better: Context Manager
```python
with lock:
    # critical section
    # automatically released
```

### Properties:
- ✓ Only ONE thread can hold lock
- ✓ Other threads wait (blocking)
- ✓ Automatically released with 'with'
- ✓ Prevents race conditions

---

## 💀 Deadlocks

### How They Occur:
```python
# Thread 1
with lock_A:
    with lock_B:  # Wants lock_B
        # work
        
# Thread 2
with lock_B:
    with lock_A:  # Wants lock_A
        # work
```

**Result**: Both threads wait forever!

### Prevention Strategies:

#### 1. Lock Ordering (BEST)
Always acquire locks in same order
```python
locks = sorted([lock_A, lock_B], key=id)
with locks[0]:
    with locks[1]:
        # work
```

#### 2. Lock Timeout
```python
if lock.acquire(timeout=5):
    try:
        # work
    finally:
        lock.release()
else:
    print("Couldn't get lock")
```

#### 3. Avoid Nested Locks
Use single lock when possible

#### 4. Lock Hierarchy
Define order: lock1 always before lock2

---

## 🚦 Semaphores

### When to Use:
- Limited resources (database connections, printer slots)
- Want to allow N threads, not just 1

### Lock vs Semaphore:
```
Lock:      [Thread] → Only 1 allowed
Semaphore: [Thread][Thread][Thread] → N allowed
```

### Example:
```python
from threading import Semaphore

# Allow 3 threads
semaphore = Semaphore(3)

with semaphore:
    # Up to 3 threads can be here
    use_database_connection()
```

### Common Use Cases:
- Database connection pools
- Rate limiting
- Resource pools
- Printer queues

---

## 📊 Comparison Table

| Feature | Lock (Mutex) | Semaphore |
|---------|-------------|-----------|
| Threads allowed | 1 | N (configurable) |
| Use case | Protect variable | Limit resources |
| Example | Counter | Connection pool |
| Syntax | `Lock()` | `Semaphore(N)` |

---

## ✅ Properties of Good Synchronization

1. **Mutual Exclusion**: Only one thread in critical section
2. **Progress**: Threads eventually enter critical section
3. **Bounded Waiting**: No thread waits forever
4. **No Busy Waiting**: Threads sleep, not spin
5. **Fairness**: All threads get equal opportunity

---

## 🎯 Decision Tree

```
Do multiple threads access shared data?
├─ No → No synchronization needed
└─ Yes → Need synchronization
    │
    ├─ Protecting a variable?
    │  └─ Use LOCK (Mutex)
    │
    └─ Limiting resource access?
       └─ Use SEMAPHORE
```

---

## 💡 Best Practices

### DO:
✓ Use `with` statement for locks  
✓ Keep critical sections small  
✓ Always acquire locks in same order  
✓ Use semaphores for resource pools  
✓ Test with many iterations  

### DON'T:
✗ Forget to release locks  
✗ Acquire locks in different orders  
✗ Hold locks longer than needed  
✗ Use shared data without locks  
✗ Ignore race conditions  

---

## 🔍 Debugging Tips

### Finding Race Conditions:
- Run with many iterations (100,000+)
- Check if result varies across runs
- Look for shared mutable data

### Finding Deadlocks:
- Program hangs
- Threads in "waiting" state
- Check for nested locks
- Check lock acquisition order

---

## 📝 Quick Reference

```python
# Lock
from threading import Lock
lock = Lock()
with lock:
    # critical section

# Semaphore
from threading import Semaphore
sem = Semaphore(3)
with sem:
    # up to 3 threads

# Check if lock is locked
if lock.locked():
    print("Lock is held")
```

---

## 🎓 Remember

1. **GIL ≠ Your locks** (different purposes)
2. **Always use locks** for shared data
3. **Context managers** are your friend
4. **Lock ordering** prevents deadlocks
5. **Semaphores** for limited resources

---