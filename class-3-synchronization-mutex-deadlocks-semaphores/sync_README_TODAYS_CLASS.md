# Today's Class: Synchronization in Python

## Quick Revision from Last Class

### What We Covered
- **GIL (Global Interpreter Lock)**: Only one thread executes Python bytecode at a time
- **ThreadPoolExecutor**: For I/O-bound tasks
- **ProcessPoolExecutor**: For CPU-bound tasks
- **Futures**: Promise for future results

### Key Takeaway
- GIL prevents **true parallelism** for CPU tasks
- But GIL does NOT prevent **race conditions** in shared data!

---

## THE BIG QUESTION: If GIL locks threads, why do we need Mutex?

### GIL vs Mutex - CRITICAL DIFFERENCE

**What GIL does:**
- Locks Python bytecode execution
- Only one thread executes at a time
- Prevents parallel CPU execution

**What GIL does NOT do:**
- Does NOT lock your data/variables
- Does NOT prevent context switching mid-operation
- Does NOT prevent race conditions

### The Problem Explained

```python
# This looks like ONE operation:
count += 1

# But in Python bytecode it's THREE operations:
1. LOAD count (read value)
2. ADD 1 (calculate new value)  
3. STORE count (write value)
```

**What happens with GIL:**
```
Thread A: LOAD count (value = 5)
Thread A: ADD 1 (result = 6)
[GIL RELEASES - Context Switch]
Thread B: LOAD count (value = 5)  ← Still 5!
Thread B: ADD 1 (result = 6)
Thread B: STORE count (count = 6)
[Context Switch]
Thread A: STORE count (count = 6)  ← Overwrites B's work!
```

**Result:** Both threads tried to increment, but count only went from 5 to 6 (not 7)!

### Key Insight
- **GIL** = Lock on **interpreter** (who can execute code)
- **Mutex** = Lock on **data** (who can access shared variable)
- You need BOTH for thread-safe operations!

---

## Today's Topics

### 1. Race Conditions
**What:** Multiple threads accessing shared data simultaneously
**Problem:** Inconsistent/wrong results
**Example:** Adder/Subtractor both modifying same counter

### 2. Critical Section
**What:** Code that accesses shared resource
**Problem:** Multiple threads entering at same time
**Solution:** Only one thread at a time

### 3. Mutex Locks
**What:** Mutual Exclusion lock
**Purpose:** Ensure only one thread in critical section
**Python:** `threading.Lock()`

### 4. Using Locks in Python
**Methods:**
- `lock.acquire()` - Get the lock (wait if busy)
- `lock.release()` - Release the lock

### 5. Context Managers
**What:** `with lock:` syntax
**Why:** Automatic lock release (even on errors)
**Better than:** Manual acquire/release

### 6. Deadlocks
**What:** Threads waiting for each other forever
**Example:** Thread A has Lock1, wants Lock2; Thread B has Lock2, wants Lock1
**Result:** Both stuck forever

### 7. Deadlock Prevention
**Strategies:**
- Lock ordering (always acquire in same order)
- Timeout on acquire
- Avoid nested locks
- Use single lock when possible

### 8. Semaphores
**What:** Lock that allows N threads (not just 1)
**Use case:** Limit concurrent access (e.g., max 3 database connections)
**Python:** `threading.Semaphore(n)`

---

## GIL vs Mutex - Visual Comparison

```
WITHOUT MUTEX (Only GIL):
─────────────────────────────
Thread A: count = count + 1  [Reads 5]
[Context Switch]
Thread B: count = count + 1  [Reads 5] ← PROBLEM!
Thread B: [Writes 6]
Thread A: [Writes 6] ← Lost B's increment!

Result: count = 6 (should be 7)


WITH MUTEX:
─────────────────────────────
Thread A: lock.acquire()
Thread A: count = count + 1  [Reads 5, Writes 6]
Thread A: lock.release()
[Context Switch]
Thread B: lock.acquire()
Thread B: count = count + 1  [Reads 6, Writes 7]
Thread B: lock.release()

Result: count = 7 ✓ Correct!
```

---

## Why Adder/Subtractor Fails Without Lock

**The Problem:**
```python
# Each operation is NOT atomic:
self.count += 1  # Actually 3 steps!
1. temp = self.count  (LOAD)
2. temp = temp + 1    (ADD)
3. self.count = temp  (STORE)
```

**Race Condition:**
```
Adder:      LOAD (50) → ADD (51) → [SWITCH] → STORE (51)
Subtractor:              [SWITCH] → LOAD (50) → SUB (49) → STORE (49)

Expected: 50 + 1 - 1 = 50
Actual: 49 ← Lost the addition!
```

---

## Key Concepts Summary

| Concept | Purpose | Python |
|---------|---------|--------|
| **GIL** | Lock interpreter execution | Built-in |
| **Mutex** | Lock data access | `Lock()` |
| **Critical Section** | Code accessing shared data | Your code |
| **Race Condition** | Multiple threads, same data | Bug |
| **Context Manager** | Auto lock/unlock | `with lock:` |
| **Deadlock** | Circular wait | Bug |
| **Semaphore** | Allow N threads | `Semaphore(n)` |

---

## Remember This

```
╔════════════════════════════════════════╗
║  GIL locks INTERPRETER                 ║
║  Mutex locks DATA                      ║
║                                        ║
║  You need Mutex even with GIL!        ║
╚════════════════════════════════════════╝
```

**The Rule:**
- Shared data + Multiple threads = Need Mutex
- Even with GIL, context switching breaks atomicity
- Always protect critical sections with locks
