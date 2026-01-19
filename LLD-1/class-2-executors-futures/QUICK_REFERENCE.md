# Quick Reference Guide

## When to Use What?

```
┌─────────────────────────────────────────────────────┐
│                  DECISION TREE                      │
└─────────────────────────────────────────────────────┘

Is your task CPU-bound or I/O-bound?
│
├─ CPU-bound (calculations, sorting, data processing)
│  └─→ Use ProcessPoolExecutor
│      ✓ True parallelism
│      ✓ Each process has own GIL
│      ✗ Higher memory overhead
│
└─ I/O-bound (file ops, network, database)
   └─→ Use ThreadPoolExecutor
       ✓ Low overhead
       ✓ Good for waiting tasks
       ✗ No true parallelism (GIL)
```

---

## Code Templates

### ThreadPoolExecutor Template

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def task(item):
    # Do I/O work here
    return result

with ThreadPoolExecutor(max_workers=5) as executor:
    # Method 1: submit
    futures = [executor.submit(task, item) for item in items]
    results = [f.result() for f in as_completed(futures)]
    
    # Method 2: map (simpler)
    results = list(executor.map(task, items))
```

### ProcessPoolExecutor Template

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_task(item):
    # Do CPU-intensive work here
    return result

if __name__ == "__main__":  # REQUIRED!
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_task, items))
```

---

## Common Methods

### Executor Methods
- `submit(fn, *args)` - Submit single task, returns Future
- `map(fn, iterable)` - Submit multiple tasks, returns results in order
- `shutdown(wait=True)` - Clean shutdown

### Future Methods
- `result()` - Get result (blocks until ready)
- `done()` - Check if complete (non-blocking)
- `cancel()` - Try to cancel task

### Helper Functions
- `as_completed(futures)` - Iterate as tasks complete (unordered)
- `wait(futures)` - Wait for futures to complete

---

## Common Mistakes to Avoid

❌ **Using threads for CPU-bound tasks**
```python
# BAD - No speedup due to GIL
with ThreadPoolExecutor() as executor:
    results = executor.map(heavy_calculation, data)
```

✅ **Use processes for CPU-bound tasks**
```python
# GOOD - True parallelism
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = executor.map(heavy_calculation, data)
```

---

❌ **Forgetting if __name__ == "__main__" with processes**
```python
# BAD - Will cause infinite process spawning on Windows
with ProcessPoolExecutor() as executor:
    ...
```

✅ **Always use the guard**
```python
# GOOD
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        ...
```

---

❌ **Not using context manager**
```python
# BAD - Manual cleanup needed
executor = ThreadPoolExecutor()
executor.submit(task)
executor.shutdown()
```

✅ **Use with statement**
```python
# GOOD - Automatic cleanup
with ThreadPoolExecutor() as executor:
    executor.submit(task)
```

---

## Performance Tips

1. **Thread Pool Size**
   - I/O-bound: workers = 5-10x number of CPU cores
   - CPU-bound: workers = number of CPU cores

2. **Process Pool Size**
   - Usually: workers = number of CPU cores
   - Don't overdo it (process overhead)

3. **When NOT to Use**
   - Very small tasks (overhead > benefit)
   - Tasks that need shared state
   - When sequential is fast enough

---

## Remember

| Feature | ThreadPool | ProcessPool |
|---------|-----------|-------------|
| Best for | I/O-bound | CPU-bound |
| GIL | Affected | Not affected |
| Memory | Shared | Separate |
| Startup | Fast | Slower |
| Parallelism | No | Yes |

---

## Examples by Use Case

**File Processing** → ThreadPoolExecutor
**Image Processing** → ProcessPoolExecutor
**API Calls** → ThreadPoolExecutor
**Data Analysis** → ProcessPoolExecutor
**Database Queries** → ThreadPoolExecutor
**Sorting/Searching** → ProcessPoolExecutor
