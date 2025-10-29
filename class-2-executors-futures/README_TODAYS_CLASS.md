# Today's Class: Executors, GIL, and Futures

## Quick Revision from Last Class

### Key Concepts Recap
- **Thread**: Lightweight unit of execution within a process
- **CPU-bound**: Tasks that require heavy computation (e.g., sorting, calculations)
- **I/O-bound**: Tasks that wait for external resources (e.g., file read, network calls)
- **Concurrency**: Multiple tasks making progress (not necessarily at same instant)
- **Parallelism**: Multiple tasks executing at the exact same instant (needs multiple cores)

### Context Switching States
1. **Sequential** (1 core, no switching): 1 thread partially complete, 1 in progress
2. **Concurrent** (1 core, with switching): >1 thread partially complete, 1 in progress
3. **Parallel** (multi-core, with switching): >1 thread partially complete, >1 in progress

---

## Today's Topics

### 1. GIL (Global Interpreter Lock)

**What is GIL?**
- A mutex (lock) in Python's CPython interpreter
- Only ONE thread can execute Python bytecode at a time
- Makes Python thread-safe for memory management

**Key Point**: 
- Java CAN run threads in true parallel
- Python CANNOT run threads in true parallel (due to GIL)
- Python threads are good for **I/O-bound** tasks only
- For **CPU-bound** tasks, use **Processes** instead

**Why does GIL exist?**
- Simplifies memory management
- Protects Python's reference counting mechanism
- Prevents race conditions in CPython

---

### 2. Executors

**Why do we need Executors?**
- Managing threads/processes manually is complex
- Executors provide a high-level interface
- Automatic resource management (thread/process pools)
- Cleaner code with context managers

**Two Types**:
1. **ThreadPoolExecutor** - Pool of threads (for I/O-bound)
2. **ProcessPoolExecutor** - Pool of processes (for CPU-bound)

---

### 3. ThreadPoolExecutor

**When to use**: I/O-bound tasks (file operations, network calls, database queries)

**How it works**:
- Creates a pool of worker threads
- Submits tasks to the pool
- Threads are reused (no overhead of creating/destroying)
- Returns `Future` objects

**Key Methods**:
- `submit(function, *args)` - Submit a single task, returns Future
- `map(function, iterable)` - Submit multiple tasks, returns results in order
- `shutdown(wait=True)` - Clean shutdown

---

### 4. ProcessPoolExecutor

**When to use**: CPU-bound tasks (calculations, data processing, sorting)

**Why use Processes?**
- Each process has its own Python interpreter
- Each process has its own GIL
- True parallelism on multi-core systems

**Important**: 
- Must use `if __name__ == "__main__":` guard
- Prevents infinite process creation on Windows
- Required for process spawning

---

### 5. ThreadPoolExecutor vs ProcessPoolExecutor

| Feature | ThreadPoolExecutor | ProcessPoolExecutor |
|---------|-------------------|---------------------|
| Best for | I/O-bound tasks | CPU-bound tasks |
| GIL Impact | Yes, shares GIL | No, separate GIL per process |
| Memory | Shared memory | Separate memory space |
| Overhead | Low | High |
| True Parallelism | No | Yes |
| Speed for I/O | Fast | Slower (overhead) |
| Speed for CPU | Slow (GIL) | Fast |

---

### 6. Futures and Callables

**Callable**:
- Any object that can be called like a function
- Functions, methods, classes with `__call__`

**Future**:
- Represents the result of an asynchronous operation
- Think of it as a "promise" for a future result
- You get it immediately, but result comes later

**Key Future Methods**:
- `result()` - Get the result (blocks until ready)
- `done()` - Check if task is complete (returns True/False)
- `cancel()` - Attempt to cancel the task

**Important**: `as_completed()` function iterates over futures as they complete

---

## Summary

1. Python threads **cannot** run in parallel (GIL limitation)
2. Use **ThreadPoolExecutor** for I/O-bound tasks
3. Use **ProcessPoolExecutor** for CPU-bound tasks
4. Executors manage resources automatically
5. `submit()` returns a `Future` object
6. Use `result()` on Future to get the actual result
