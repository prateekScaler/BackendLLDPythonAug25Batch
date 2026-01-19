# Async I/O - Internal Mechanism

## What is Async I/O?

**Single thread managing multiple I/O operations without blocking**

```python
# Threads: Multiple threads, one task each
# Async: Single thread, many tasks
```

---

## The Core: Event Loop

**Event loop = While loop that manages tasks**

```python
# Simplified event loop
while True:
    task = get_next_ready_task()
    run_task_until_it_waits()
    # Task hits 'await' → switches to next task
```

**Key:** Tasks voluntarily yield control (cooperative multitasking)

---

## Internal State

```
Event Loop has:
  • Task queue (ready to run)
  • Waiting tasks (blocked on I/O)
  • Current task (running now)
```

**Visual:**
```
┌─────────────────────────┐
│     Event Loop          │
│                         │
│ Running: Task A         │
│ Ready: [Task B, Task C] │
│ Waiting: [Task D, E]    │
└─────────────────────────┘
```

---

## How await Works

```python
async def download(url):
    data = await fetch(url)  # Pauses here
    return data
```

**Internally:**

```
1. Task hits 'await fetch(url)'
2. fetch() starts I/O operation (non-blocking)
3. Task yields control to event loop
4. Event loop runs next ready task
5. When I/O completes, task moves to ready queue
6. Event loop resumes task after await
```

**Timeline:**
```
Task A: print("start")
Task A: await download()  → Yields control
  ↓
Event Loop: Switch to Task B
  ↓
Task B: print("start")
Task B: await download()  → Yields control
  ↓
Event Loop: Switch to Task C
  ↓
Task C: runs...
  ↓
I/O for Task A completes → Task A back to ready queue
  ↓
Event Loop: Resume Task A after await
```

---

## Detailed Execution Flow

```python
async def task1():
    print("Task 1 started")
    await asyncio.sleep(1)  # I/O operation
    print("Task 1 done")

async def task2():
    print("Task 2 started")
    await asyncio.sleep(1)
    print("Task 2 done")
```

**Step-by-step:**

```
Time 0.0s:
  Event loop: Start task1
  task1: print "Task 1 started"
  task1: await sleep(1) → Registers I/O, yields
  
  Event loop ready queue: [task2]
  Event loop waiting: [task1 (until 1.0s)]

Time 0.0s (same tick):
  Event loop: Start task2
  task2: print "Task 2 started"
  task2: await sleep(1) → Registers I/O, yields
  
  Event loop ready queue: []
  Event loop waiting: [task1 (until 1.0s), task2 (until 1.0s)]

Time 1.0s:
  I/O completes for task1 and task2
  Event loop ready queue: [task1, task2]
  
  Event loop: Resume task1
  task1: print "Task 1 done"
  task1: completes
  
  Event loop: Resume task2
  task2: print "Task 2 done"
  task2: completes
```

**Output:**
```
Task 1 started
Task 2 started
(1 second passes)
Task 1 done
Task 2 done

Total time: ~1 second (not 2!)
```

---

## Event Loop Architecture

```
┌─────────────────────────────────────┐
│          Event Loop                 │
├─────────────────────────────────────┤
│                                     │
│  1. Check ready tasks               │
│  2. Run one task until await        │
│  3. Check I/O completions           │
│  4. Move completed to ready         │
│  5. Repeat                          │
│                                     │
└─────────────────────────────────────┘
           ↓         ↑
           ↓         ↑
    ┌──────────────────────┐
    │   OS (epoll/kqueue)  │
    │   Monitors I/O       │
    └──────────────────────┘
```

---

## How OS Helps: epoll/select

**Async uses OS primitives to monitor I/O:**

```python
# Simplified
while True:
    # Ask OS: "Which I/O operations completed?"
    ready_fds = epoll.poll()  # Non-blocking!
    
    for fd in ready_fds:
        task = tasks[fd]
        mark_ready(task)
    
    # Run ready tasks
    run_ready_tasks()
```

**Key:** Event loop asks OS "what's ready?" instead of blocking on one I/O

---

## Async vs Threads Internals

### Threads
```
OS Kernel manages:
  • Thread 1 → runs until time slice ends
  • Thread 2 → runs until time slice ends
  • Preemptive switching (OS decides)
  • Each thread: 8MB stack
```

### Async
```
Event loop manages:
  • Task 1 → runs until 'await'
  • Task 2 → runs until 'await'
  • Cooperative switching (tasks decide)
  • Each task: 1-2KB (coroutine object)
```

**Memory comparison:**
```
1000 threads = 8GB memory
1000 async tasks = 2MB memory
```

---

## Task States

```
┌─────────┐  await   ┌─────────┐  I/O done  ┌─────────┐
│ RUNNING │ ──────→  │ WAITING │ ─────────→ │  READY  │
└─────────┘          └─────────┘            └─────────┘
     ↑                                            │
     └────────────────────────────────────────────┘
              Event loop schedules
```

**States:**
- **RUNNING**: Currently executing
- **WAITING**: Blocked on I/O (await)
- **READY**: I/O done, waiting for event loop

---

## Why Single Thread?

**No context switching overhead:**
```
Threads:
  - OS switches every ~10ms
  - Save/restore registers
  - Cache invalidation
  - TLB flush

Async:
  - Switch only at 'await'
  - Minimal state save
  - Cache-friendly
  - No OS involvement
```

---

## The Coroutine Object

```python
async def task():
    await something()
```

**Internally:**
```python
# Coroutine = Generator-like object
coro = task()  # Creates coroutine object

# Coroutine has:
  • Current state (where it's paused)
  • Local variables
  • Awaiting what?
  
# Event loop calls:
coro.send(None)  # Resume execution
# Coroutine runs until next 'await'
# Then yields back to event loop
```

---

## asyncio.gather() Internals

```python
results = await asyncio.gather(task1(), task2(), task3())
```

**What happens:**

```
1. Create 3 coroutine objects
2. Submit all to event loop
3. Event loop schedules them
4. All run concurrently (switch on await)
5. Collect results when all done
6. Return list of results
```

**Visual:**
```
Time →
Task1: [───await───]──done
Task2: [──await──]────done
Task3: [────await────]──done
       ↑
       All start together
       Switch between them at 'await'
       All finish around same time
```

---

## Non-Blocking I/O

**Blocking I/O (normal):**
```python
data = file.read()  # Waits here, thread blocked
```

**Non-blocking I/O (async):**
```python
data = await file.read()  # Registers request, yields
# Event loop runs other tasks
# When data ready, resume here
```

**How it works:**
```
1. Call OS: "Start reading, don't wait"
2. OS returns immediately with "in progress"
3. Event loop does other work
4. OS signals "read complete"
5. Event loop resumes task
```

---

## Comparison with Node.js

**Very similar!**

```javascript
// Node.js
async function fetchData() {
    const data = await fetch(url);
    return data;
}
```

```python
# Python
async def fetch_data():
    data = await fetch(url)
    return data
```

**Both use:**
- Event loop (libuv in Node, asyncio in Python)
- Cooperative multitasking
- Non-blocking I/O
- Single-threaded concurrency

---

## When Async Fails

**CPU-bound work blocks event loop:**

```python
async def bad():
    result = sum(range(10_000_000))  # No await!
    # Event loop BLOCKED here
    # No other task can run
    return result
```

**Why:** No `await` = no yielding = event loop stuck

**Solution:**
```python
async def good():
    # Run CPU work in thread/process pool
    result = await loop.run_in_executor(None, heavy_compute)
    return result
```

---

## Summary

**Event Loop:**
- While loop managing tasks
- Runs one task until `await`
- Switches to next ready task

**await:**
- Yields control to event loop
- Task pauses (not blocked)
- Event loop runs other tasks

**Non-blocking I/O:**
- OS primitive (epoll/select)
- Asks "what's ready?" not "wait for this"
- Event loop monitors multiple I/O

**Single thread but concurrent:**
- Tasks switch at `await` points
- No OS thread overhead
- Can handle 10,000+ concurrent I/O operations

**Key difference from threads:**
- Threads: OS decides when to switch (preemptive)
- Async: Tasks decide when to switch (cooperative)