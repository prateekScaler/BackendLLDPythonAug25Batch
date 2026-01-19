# Revision: Previous Class Notes

## What is a Thread?
- Lightweight unit of execution within a process
- Shares memory space with other threads in same process
- Has its own: program counter, stack, registers
- Cheaper to create than processes

---

## CPU-Bound vs I/O-Bound Tasks

### CPU-Bound Tasks
- Require heavy computation
- Limited by CPU speed
- Examples:
  - Mathematical calculations
  - Data processing
  - Sorting algorithms
  - Image/video processing
  - Machine learning

### I/O-Bound Tasks
- Spend time waiting for external resources
- Limited by I/O speed (not CPU)
- Examples:
  - Reading/writing files
  - Network requests
  - Database queries
  - User input
  - API calls

---

## Benefits of Threads

1. **Responsiveness**: Keep UI responsive while doing background work
2. **Resource Sharing**: Share memory - easier communication
3. **Economy**: Cheaper to create than processes
4. **Scalability**: Utilize multiple cores (in theory)
5. **Concurrency**: Handle multiple tasks "simultaneously"

---

## Single Core vs Multi-Core

### Single Core CPU
- Can run only ONE thread at a time
- Uses time-slicing (context switching) to create illusion of parallelism
- Cannot achieve true parallelism

### Multi-Core CPU
- Can run MULTIPLE threads simultaneously
- Each core can run one thread
- Can achieve true parallelism
- 4 cores = up to 4 threads running at exact same instant

---

## Concurrency vs Parallelism

### Key Difference
- **Concurrency**: Tasks making progress (not necessarily at same instant)
- **Parallelism**: Tasks executing at EXACT same instant

### Three Scenarios

#### 1. Single Core, No Context Switching (Sequential)
```
Time →
Core: [Task1] [Task2] [Task3]

- Threads partially completed: 1
- Threads in progress at any instant: 1
- Type: Sequential (neither concurrent nor parallel)
```

#### 2. Single Core, With Context Switching (Concurrency)
```
Time →
Core: [T1][T2][T1][T3][T2][T1]...

- Threads partially completed: >1
- Threads in progress at any instant: 1
- Type: Concurrent but NOT parallel
```

#### 3. Multi-Core, With Context Switching (Parallelism)
```
Time →
Core1: [T1][T2][T1][T3]...
Core2: [T2][T3][T4][T1]...

- Threads partially completed: >1
- Threads in progress at any instant: >1
- Type: Both concurrent AND parallel
```

---

## Optimal Number of Threads

### Amdahl's Law (Bell Curve)
- Too few threads: Not utilizing resources
- Optimal number: Depends on task type
- Too many threads: Overhead kills performance

### Guidelines
- **CPU-bound**: threads ≈ number of cores
- **I/O-bound**: threads can be much higher (10x+ cores)

### Why Bell Curve?
```
Performance
    ^
    |      /\
    |     /  \
    |    /    \
    |   /      \
    |__/________\___>
      1  Optimal  Many
      Number of Threads
```
- Rising: More parallelism
- Peak: Sweet spot
- Falling: Overhead (context switching, memory)

---

## Creating Threads in Python

### Basic Syntax
```python
from threading import Thread

def task():
    print("Thread running")

# Create thread
t = Thread(target=task)

# Start thread
t.start()

# Wait for completion
t.join()
```

### What does thread.start() do?
1. Allocates resources for the thread
2. Calls the target function
3. Thread begins executing
4. Returns immediately (non-blocking)

### thread.join()
- Waits for thread to complete
- Blocking call
- Main program waits here until thread finishes

### Thread.sleep()
```python
import time
time.sleep(2)  # Sleep for 2 seconds
```
- Pauses current thread
- Allows other threads to run (releases CPU)
- Used to simulate I/O operations

---

## Passing Arguments to Threads

### Using args
```python
def greet(name, age):
    print(f"Hello {name}, you are {age}")

t = Thread(target=greet, args=("Alice", 25))
t.start()
```

### Using kwargs
```python
def greet(name, age):
    print(f"Hello {name}, you are {age}")

t = Thread(target=greet, kwargs={"name": "Bob", "age": 30})
t.start()
```

### Both args and kwargs
```python
t = Thread(target=func, args=(1, 2), kwargs={"key": "value"})
```

---

## Context Switching in Action

### Example showing uncertainty

```python
from threading import Thread

def task(n):
    print(f"Thread {n} started")
    print(f"Thread {n} finished")

# Create multiple threads
threads = []
for i in range(5):
    t = Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

# Wait for all
for t in threads:
    t.join()
```

### Output (unpredictable order):
```
Thread 0 started
Thread 2 started
Thread 1 started
Thread 0 finished
Thread 3 started
Thread 2 finished
...
```

**Why?** Context switching! OS decides which thread runs when.

---

## Key Takeaways from Last Class

1. ✓ Threads share memory within a process
2. ✓ CPU-bound tasks need CPU power
3. ✓ I/O-bound tasks spend time waiting
4. ✓ Single core = concurrency only (no parallelism)
5. ✓ Multi-core = can achieve parallelism
6. ✓ Optimal threads ≠ infinite threads (bell curve)
7. ✓ Context switching creates uncertainty in execution order
8. ✓ Use `thread.start()` to begin, `thread.join()` to wait
9. ✓ Pass arguments using `args` and `kwargs`
10. ✓ `time.sleep()` simulates I/O operations

---

## Questions to Test Understanding

1. What's the difference between concurrency and parallelism?
2. Can a single-core CPU achieve parallelism? Why/why not?
3. Why is there a limit to optimal number of threads?
4. What happens when you call `thread.start()`?
5. Why might thread execution order be unpredictable?
6. When would you use threads vs processes?
