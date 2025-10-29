# Deadlocks - Quick Guide

## What is a Deadlock?

**When two or more threads wait for each other forever, none can proceed.**

```
Thread A: Has Lock1, wants Lock2
Thread B: Has Lock2, wants Lock1
→ Both wait forever = DEADLOCK
```

---

## Simple Example

```python
# Thread 1
with lock_A:
    with lock_B:  # Wants B
        work()

# Thread 2  
with lock_B:
    with lock_A:  # Wants A
        work()
```



**Timeline:**
```
Thread 1: Gets A → Wants B (waiting...)
Thread 2: Gets B → Wants A (waiting...)
DEADLOCK! 💥
```

---

## When Do Deadlocks Occur?

### Four Conditions (ALL must be true):

1. **Mutual Exclusion**: Only one thread can hold a lock
2. **Hold and Wait**: Thread holds lock while waiting for another
3. **No Preemption**: Locks can't be forcibly taken away
4. **Circular Wait**: Thread 1 waits for Thread 2, Thread 2 waits for Thread 1

**Break ANY one condition → No deadlock!**

---

## Common Scenarios

### 1. Bank Transfer (Most Common)
```python
# Transfer from A to B
with account_A.lock:
    with account_B.lock:
        transfer()

# Transfer from B to A (at same time)
with account_B.lock:
    with account_A.lock:  # DEADLOCK!
        transfer()
```

### 2. Resource Allocation
```python
# Thread 1: Needs Printer then Scanner
with printer_lock:
    with scanner_lock:
        work()

# Thread 2: Needs Scanner then Printer
with scanner_lock:
    with printer_lock:  # DEADLOCK!
        work()
```

### 3. Nested Function Calls
```python
def func_a():
    with lock_a:
        func_b()  # Calls func_b which needs lock_b

def func_b():
    with lock_b:
        func_a()  # Calls func_a which needs lock_a
        # DEADLOCK!
```

---

## Prevention Strategies

### 1. **Lock Ordering** (BEST) ⭐
Always acquire locks in same order

```python
# BAD - Different order
Thread 1: lock_A → lock_B
Thread 2: lock_B → lock_A  # DEADLOCK

# GOOD - Same order
Thread 1: lock_A → lock_B
Thread 2: lock_A → lock_B  # No deadlock
```

**Implementation:**
```python
# Sort locks by ID
locks = sorted([lock_A, lock_B], key=id)
with locks[0]:
    with locks[1]:
        work()
```

### 2. **Lock Timeout**
Don't wait forever

```python
if lock.acquire(timeout=5):
    try:
        work()
    finally:
        lock.release()
else:
    print("Couldn't get lock, try again")
```

### 3. **Avoid Nested Locks**
Use single lock when possible

```python
# Instead of multiple locks
with lock_A:
    with lock_B:
        work()

# Use one lock
with single_lock:
    work()
```

### 4. **Lock Hierarchy**
Define order: Lock1 always before Lock2

```python
# Rule: account_lock always before transaction_lock
with account_lock:
    with transaction_lock:
        work()
```

### 5. **Use Lock-Free Structures**
Atomic operations, queues

```python
from queue import Queue
q = Queue()  # Thread-safe, no locks needed
```

---

## Detection in Code

### Signs of Potential Deadlock:
- ✗ Nested locks
- ✗ Multiple locks in different order
- ✗ Lock acquired in one function, released in another
- ✗ Locks held while calling external code

### Safe Patterns:
- ✓ Single lock per operation
- ✓ Consistent lock ordering
- ✓ Short critical sections
- ✓ Use context managers (`with`)

---

## Real-World Example: Bank Transfer

### ❌ Deadlock-Prone
```python
def transfer(from_acc, to_acc, amount):
    with from_acc.lock:
        with to_acc.lock:
            from_acc.balance -= amount
            to_acc.balance += amount

# Thread 1: transfer(A, B, 100)  # Locks: A, then B
# Thread 2: transfer(B, A, 50)   # Locks: B, then A
# DEADLOCK!
```

### ✅ Deadlock-Free
```python
def transfer(from_acc, to_acc, amount):
    # Always lock in ID order
    first, second = sorted([from_acc, to_acc], key=id)
    
    with first.lock:
        with second.lock:
            from_acc.balance -= amount
            to_acc.balance += amount

# Both threads lock in SAME order
# No deadlock!
```

---

## Quick Checklist

**Before writing code with multiple locks:**

- [ ] Can I use just ONE lock?
- [ ] Am I acquiring locks in consistent order?
- [ ] Am I using context managers (`with`)?
- [ ] Do I have timeout on locks?
- [ ] Is critical section as short as possible?

---

## Summary

**Deadlock = Threads waiting for each other forever**

**Occurs when:**
- Multiple locks
- Acquired in different order
- Hold and wait

**Prevention:**
1. **Lock ordering** (best)
2. Lock timeout
3. Avoid nested locks
4. Use hierarchy

**Remember:** Break any one of the four conditions → No deadlock!

---

## Visual Summary

```
DEADLOCK:
Thread 1: [Lock A] → wants Lock B ⏸️
Thread 2: [Lock B] → wants Lock A ⏸️
Result: Both stuck forever

NO DEADLOCK (Same Order):
Thread 1: [Lock A] → [Lock B] ✓
Thread 2: waits for A → [Lock A] → [Lock B] ✓
Result: Both complete sequentially
```