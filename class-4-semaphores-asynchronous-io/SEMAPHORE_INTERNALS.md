# Semaphores - Internal Mechanism

## What is a Semaphore?

**A counter that controls access to shared resources**

```python
sem = Semaphore(3)  # Internal counter = 3
```

---

## Internal State

```
Semaphore has:
  • Counter (int)
  • Wait queue (list of threads)
```

**Example:**
```python
sem = Semaphore(2)

Internal state:
  counter = 2
  wait_queue = []
```

---

## How acquire() Works

```python
sem.acquire()
```

**Internally:**
```
1. Check counter
   ├─ If counter > 0:
   │    • Decrement counter
   │    • Let thread proceed
   │
   └─ If counter == 0:
        • Add thread to wait_queue
        • BLOCK thread (sleep, not busy wait)
```

**Visual:**
```
Initial: counter=2, queue=[]

Thread A: acquire()
  → counter=1, queue=[], Thread A proceeds ✓

Thread B: acquire()
  → counter=0, queue=[], Thread B proceeds ✓

Thread C: acquire()
  → counter=0, queue=[C], Thread C BLOCKS 😴
```

---

## How release() Works

```python
sem.release()
```

**Internally:**
```
1. Check wait_queue
   ├─ If queue empty:
   │    • Increment counter
   │
   └─ If queue has threads:
        • Wake up first thread in queue
        • Remove it from queue
        • Don't increment counter (thread takes the slot)
```

**Visual:**
```
State: counter=0, queue=[C, D]

Thread A: release()
  → counter=0, queue=[D], Thread C wakes up ✓

Thread B: release()
  → counter=0, queue=[], Thread D wakes up ✓

Thread E: release()
  → counter=1, queue=[] (no one waiting)
```

---

## Producer-Consumer Internals

```python
empty = Semaphore(3)  # counter=3, tracks empty slots
full = Semaphore(0)   # counter=0, tracks items
```

### Producer Flow

```python
empty.acquire()  # Wait for empty slot
buffer.append(item)
full.release()   # Signal item added
```

**Internal timeline:**
```
empty.acquire():
  empty.counter = 2 (was 3)
  Producer proceeds

buffer.append():
  Add item to buffer

full.release():
  full.counter = 1 (was 0)
  OR wake up waiting consumer
```

### Consumer Flow

```python
full.acquire()    # Wait for item
buffer.pop()
empty.release()   # Signal slot freed
```

**Internal timeline:**
```
full.acquire():
  If full.counter > 0:
    full.counter -= 1
    Consumer proceeds
  Else:
    Add consumer to full.wait_queue
    BLOCK (sleep)

buffer.pop():
  Remove item

empty.release():
  empty.counter += 1
  OR wake up waiting producer
```

---

## Complete Example Walkthrough

```python
Buffer: []
empty = Semaphore(2)  # counter=2
full = Semaphore(0)   # counter=0
```

**Step-by-step:**

```
1. Producer P1: empty.acquire()
   → empty.counter=1, P1 proceeds
   
2. Producer P1: adds item
   → Buffer: [item1]
   
3. Producer P1: full.release()
   → full.counter=1
   
4. Consumer C1: full.acquire()
   → full.counter=0, C1 proceeds
   
5. Consumer C1: removes item
   → Buffer: []
   
6. Consumer C1: empty.release()
   → empty.counter=2
   
7. Producer P2: empty.acquire()
   → empty.counter=1, P2 proceeds
   
8. Producer P3: empty.acquire()
   → empty.counter=0, P3 proceeds
   
9. Producer P4: empty.acquire()
   → empty.counter=0, empty.queue=[P4]
   → P4 BLOCKS (buffer full!)
   
10. Consumer C2: full.acquire()
    → full.counter=... waits
    
11. Producer P2: full.release()
    → Wakes C2 from queue
```

---

## Key Differences from Lock

| Feature | Lock | Semaphore |
|---------|------|-----------|
| Counter | Binary (0 or 1) | Integer (0 to N) |
| Threads allowed | 1 | N |
| Use case | Mutual exclusion | Resource counting |

**Under the hood:**
```python
# Lock is essentially:
Semaphore(1)

lock.acquire()  → sem.acquire() (counter: 1→0)
lock.release()  → sem.release() (counter: 0→1)
```

---

## Why No Busy Waiting?

**Without semaphore (busy wait):**
```python
while len(buffer) >= MAX:
    pass  # Keep checking (wastes CPU)
```
- Thread keeps running
- CPU cycles wasted
- Context switching overhead

**With semaphore:**
```python
empty.acquire()  # Blocks here
```
- Thread moved to wait_queue
- Thread state = BLOCKED (not RUNNING)
- OS doesn't schedule blocked threads
- CPU free for other work
- Thread wakes only when released

---

## Implementation Pseudocode

```python
class Semaphore:
    def __init__(self, value):
        self.counter = value
        self.wait_queue = []
        self.lock = Lock()  # Protects counter and queue
    
    def acquire(self):
        with self.lock:
            if self.counter > 0:
                self.counter -= 1
                return  # Proceed immediately
            else:
                # Add current thread to queue
                self.wait_queue.append(current_thread)
        
        # Block thread (OS call)
        block_thread(current_thread)
    
    def release(self):
        with self.lock:
            if self.wait_queue:
                # Wake first waiting thread
                thread = self.wait_queue.pop(0)
                unblock_thread(thread)
            else:
                self.counter += 1
```

---

## Memory View

```
Semaphore object in memory:
┌─────────────────────┐
│ counter: 3          │
│ wait_queue: []      │
│ internal_lock: Lock │
└─────────────────────┘

After 2 acquires:
┌─────────────────────┐
│ counter: 1          │
│ wait_queue: []      │
│ internal_lock: Lock │
└─────────────────────┘

After 3 more acquires:
┌─────────────────────┐
│ counter: 0          │
│ wait_queue: [T4, T5]│ ← Blocked threads
│ internal_lock: Lock │
└─────────────────────┘
```

---

## Summary

**Semaphore = Counter + Wait Queue**

**acquire():**
- Counter > 0 → Decrement and go
- Counter == 0 → Join queue and sleep

**release():**
- Queue empty → Increment counter
- Queue has threads → Wake one thread

**No busy waiting because:**
- Blocked threads don't run
- OS handles scheduling
- CPU available for other work

**Producer-Consumer:**
- Two semaphores track two things
- `empty`: counts available slots
- `full`: counts available items
- Perfect coordination without polling!