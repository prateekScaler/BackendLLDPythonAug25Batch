# Visual Decision Flow

## When to Use What? - Complete Decision Tree

```
                    START: I have a task
                            |
                            |
                            v
                ┌─────────────────────┐
                │  What type of task? │
                └─────────────────────┘
                            |
              ┌─────────────┴─────────────┐
              |                           |
              v                           v
     ┌─────────────────┐         ┌─────────────────┐
     │  I/O-BOUND      │         │   CPU-BOUND     │
     │                 │         │                 │
     │ - File read/    │         │ - Calculations  │
     │   write         │         │ - Sorting       │
     │ - Network calls │         │ - Data          │
     │ - Database      │         │   processing    │
     │ - API requests  │         │ - Image/video   │
     └─────────────────┘         └─────────────────┘
              |                           |
              v                           v
     ┌─────────────────┐         ┌─────────────────┐
     │ ThreadPool      │         │ ProcessPool     │
     │ Executor        │         │ Executor        │
     │                 │         │                 │
     │ ✓ Low overhead  │         │ ✓ True parallel │
     │ ✓ Shared memory │         │ ✓ No GIL limit  │
     │ ✓ Fast startup  │         │ ✓ Separate GIL  │
     │ ✗ No parallel   │         │ ✗ High overhead │
     └─────────────────┘         └─────────────────┘
              |                           |
              v                           v
     ┌─────────────────┐         ┌─────────────────┐
     │ from            │         │ from            │
     │ concurrent.     │         │ concurrent.     │
     │ futures import  │         │ futures import  │
     │ ThreadPool      │         │ ProcessPool     │
     │ Executor        │         │ Executor        │
     │                 │         │                 │
     │ with ...():     │         │ if __name__     │
     │   executor.     │         │   == "__main__":│
     │   map(fn, data) │         │     with ...(): │
     └─────────────────┘         └─────────────────┘
```

---

## The GIL Impact Visualization

```
WITHOUT GIL (e.g., Java):
┌─────────────────────────────────────┐
│ CPU Core 1  │ CPU Core 2            │
├─────────────────────────────────────┤
│ Thread A    │ Thread B              │
│ [Executing] │ [Executing]           │ ← TRUE PARALLELISM
│             │                       │
└─────────────────────────────────────┘

WITH GIL (Python Threads):
┌─────────────────────────────────────┐
│ CPU Core 1  │ CPU Core 2            │
├─────────────────────────────────────┤
│ Thread A    │ [Idle]                │
│ [Executing] │                       │ ← Only ONE thread at a time
│   (has GIL) │ Thread B (waiting)    │   due to GIL
└─────────────────────────────────────┘

WITH PROCESSES (Python):
┌─────────────────────────────────────┐
│ CPU Core 1  │ CPU Core 2            │
├─────────────────────────────────────┤
│ Process A   │ Process B             │
│ [Executing] │ [Executing]           │ ← TRUE PARALLELISM
│  (own GIL)  │  (own GIL)            │   Each has separate GIL
└─────────────────────────────────────┘
```

---

## Concurrency vs Parallelism - Visual

```
SEQUENTIAL (No concurrency, no parallelism):
Timeline: ──[Task 1]──[Task 2]──[Task 3]──
CPU:      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:   ✓ Simple  ✗ Slow


CONCURRENT (Single core with context switching):
Timeline: ──[T1][T2][T1][T3][T2][T1][T3]──
CPU:      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status:   ✓ Responsive  ~ Medium speed


PARALLEL (Multi-core):
Timeline: ──[Task 1─────]──
          ──[Task 2────]────
          ──[Task 3──────]──
CPU 1:    ━━━━━━━━━━━━━━━━
CPU 2:    ━━━━━━━━━━━━━━━━
CPU 3:    ━━━━━━━━━━━━━━━━
Status:   ✓ Fast  ✗ Complex
```

---

## Thread Pool vs Process Pool - Visual

```
THREAD POOL:
┌──────────────────────────────────┐
│         Main Process             │
│  ┌────────────────────────────┐  │
│  │     ThreadPoolExecutor     │  │
│  │                            │  │
│  │  [Thread 1] [Thread 2]     │  │ ← Threads share memory
│  │  [Thread 3] [Thread 4]     │  │
│  │                            │  │
│  │  Shared Memory Space       │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
• Lightweight
• Shared GIL
• Good for I/O


PROCESS POOL:
┌──────────────────────────────────┐
│      Main Process                │
└──────────────────────────────────┘
        │
        ├─→ ┌──────────────┐
        │   │  Process 1   │ ← Separate memory
        │   │  (own GIL)   │
        │   └──────────────┘
        │
        ├─→ ┌──────────────┐
        │   │  Process 2   │ ← Separate memory
        │   │  (own GIL)   │
        │   └──────────────┘
        │
        └─→ ┌──────────────┐
            │  Process 3   │ ← Separate memory
            │  (own GIL)   │
            └──────────────┘
• Heavyweight
• No shared GIL
• Good for CPU
```

---

## Future Object Lifecycle

```
1. SUBMIT TASK
   ┌──────────────┐
   │ Submit task  │
   └──────┬───────┘
          │
          v
   ┌──────────────┐
   │   Future     │ ← You get this IMMEDIATELY
   │  (pending)   │
   └──────┬───────┘
          │
          v

2. TASK RUNNING
   ┌──────────────┐
   │   Future     │
   │  (running)   │ ← .done() returns False
   └──────┬───────┘
          │
          v

3. TASK COMPLETE
   ┌──────────────┐
   │   Future     │
   │ (finished)   │ ← .done() returns True
   └──────┬───────┘
          │
          v

4. GET RESULT
   ┌──────────────┐
   │  .result()   │ ← Get actual result
   └──────────────┘
```

---

## Common Patterns

### Pattern 1: Submit and Wait
```python
with ThreadPoolExecutor() as executor:
    future = executor.submit(task, arg)
    result = future.result()  # Wait for result
```

### Pattern 2: Submit All, Get All
```python
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, x) for x in data]
    results = [f.result() for f in futures]
```

### Pattern 3: Submit All, Process as Complete
```python
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(task, x) for x in data]
    for future in as_completed(futures):
        result = future.result()  # Process as ready
```

### Pattern 4: Simple Map
```python
with ThreadPoolExecutor() as executor:
    results = list(executor.map(task, data))
```

---

## Memory Model Comparison

```
THREADS (Shared Memory):
┌────────────────────────────────┐
│        Process Memory          │
│                                │
│  [Heap] ← All threads access  │
│  [Data]   same memory         │
│                                │
│  Thread 1: [Stack]            │
│  Thread 2: [Stack]            │
│  Thread 3: [Stack]            │
└────────────────────────────────┘
✓ Easy to share data
✗ Need synchronization


PROCESSES (Separate Memory):
┌───────────────┐  ┌───────────────┐
│  Process 1    │  │  Process 2    │
│               │  │               │
│ [Heap][Data]  │  │ [Heap][Data]  │
│ [Stack]       │  │ [Stack]       │
└───────────────┘  └───────────────┘
✓ No synchronization needed
✗ Hard to share data
```

---

## Performance Characteristics

```
                    I/O Task        CPU Task
                    ────────        ────────
Sequential          ████████        ████████
                    (8 sec)         (8 sec)

ThreadPool          ██              ████████
                    (2 sec)         (8 sec)
                    ↑ 4x faster     ↑ No benefit

ProcessPool         ████            ██
                    (4 sec)         (2 sec)
                    ↑ 2x faster     ↑ 4x faster
                    (overhead)      (true parallel)


KEY INSIGHT:
• I/O: ThreadPool wins (low overhead)
• CPU: ProcessPool wins (true parallel)
```

---

## The Complete Picture

```
YOUR TASK
    ↓
    ├─→ Waits a lot (I/O-bound)?
    │   └─→ ThreadPoolExecutor ✓
    │       • Low overhead
    │       • Shares memory
    │       • Many workers OK (10x cores)
    │
    └─→ Computes a lot (CPU-bound)?
        └─→ ProcessPoolExecutor ✓
            • True parallelism
            • Separate GIL
            • Workers ≈ cores
            • Remember: if __name__ == "__main__"
```

---

## Remember This!

```
╔══════════════════════════════════════╗
║  "Is it CPU or I/O?"                 ║
║                                      ║
║  CPU → ProcessPool                   ║
║  I/O → ThreadPool                    ║
║                                      ║
║  Always ask this first!              ║
╚══════════════════════════════════════╝
```
