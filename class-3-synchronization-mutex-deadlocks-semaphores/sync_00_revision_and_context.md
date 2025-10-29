# Quick Revision: Executors + Today's Topic Introduction

## Previous Class Quick Recap (5 mins)

### What We Learned
- **GIL**: Only one thread executes Python bytecode at a time
- **ThreadPoolExecutor**: For I/O-bound tasks
- **ProcessPoolExecutor**: For CPU-bound tasks (true parallelism)
- **Futures**: Promise for future result

### Key Decision
```
Is it CPU-bound or I/O-bound?
├─ CPU-bound → ProcessPoolExecutor
└─ I/O-bound → ThreadPoolExecutor
```

---

















## 🤔 THE CONFUSING QUESTION

**"If GIL allows only ONE thread at a time, why do we need locks?"**

This is THE most confusing part! Let's clarify:

### GIL vs Locks - They Solve DIFFERENT Problems

#### What GIL Does:
• Protects Python's internal memory management
• Ensures only ONE thread executes Python bytecode at a time
• Works at the **bytecode instruction level**

#### What GIL Does NOT Do:
• Does NOT prevent race conditions in YOUR code
• Does NOT make YOUR code thread-safe
• Does NOT protect YOUR shared variables

---

## 💥 THE PROBLEM: GIL Doesn't Help Your Code

### Example: `count += 1` 

**Your Python code:**
```python
count += 1
```

**This becomes MULTIPLE bytecode instructions:**
```
1. LOAD count value
2. ADD 1 to it
3. STORE back to count
```

**What happens with 2 threads:**
```
Thread A: LOAD count (count = 0)
Thread B: LOAD count (count = 0)  ← GIL switches here!
Thread A: ADD 1 (result = 1)
Thread B: ADD 1 (result = 1)
Thread A: STORE (count = 1)
Thread B: STORE (count = 1)      ← Should be 2, but it's 1!
```

### Key Point:
• GIL switches between threads **between bytecode instructions**
• NOT between Python statements
• So `count += 1` can be interrupted mid-execution!

---

## 📊 Visual: GIL vs Locks

```
WITHOUT LOCKS (only GIL):
Thread A: [LOAD] [ADD] [STORE]
Thread B:        [LOAD] [ADD] [STORE]  ← Interference!
         ↑ GIL can switch here

WITH LOCKS:
Thread A: [LOCK][LOAD][ADD][STORE][UNLOCK]
Thread B:                          [LOCK][LOAD][ADD][STORE][UNLOCK]
         ↑ Thread B waits for lock
```

---

## 🎯 Simple Answer

**GIL** = Protects Python's internals  
**Locks** = Protects YOUR data  

**Both are needed!**

---

## Today's Class: Synchronization

### Why We Need It
• Multiple threads accessing shared data = chaos
• Need to coordinate thread access
• Prevent race conditions

### What We'll Cover
1. **Mutex Locks** - Basic synchronization
2. **Context Managers** - Clean lock usage
3. **Deadlocks** - When locks go wrong
4. **Semaphores** - Advanced control

### Real Example We'll Use
• Adder/Subtractor problem
• MergeSort with synchronization

---

## Key Terminology (Today)

**Critical Section**: Code that accesses shared resource  
**Race Condition**: Multiple threads accessing critical section simultaneously  
**Mutex**: Lock that ensures only one thread in critical section  
**Deadlock**: Threads waiting for each other forever  
**Semaphore**: Lock that allows N threads simultaneously  

---

## Remember for Today

```
GIL protects Python
Locks protect YOUR code
```
