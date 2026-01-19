# Creating Threads: Function vs Class Approach

## Two Ways to Create Threads

### Method 1: Function with args (What you know)
```python
from threading import Thread


def task(name, count):
    for i in range(count):
        print(f"{name}: {i}")


t = Thread(target=task, args=("Worker", 5))
t.start()
t.join()
```

### Method 2: Extending Thread Class (NEW)
```python
from threading import Thread


class MyThread(Thread):
    def __init__(self, name, count):
        super().__init__()
        self.name = name
        self.count = count

    def run(self):
        for i in range(self.count):
            print(f"{self.name}: {i}")


t = MyThread("Worker", 5)
t.start()
t.join()
```

---

## Key Differences

| Feature | Function Approach | Class Approach |
| --------- | ------------------ | ---------------- |
| Simplicity | ✓ Simpler | More code |
| Organization | All in function | Data + logic together |
| Reusability | Less | ✓ More reusable |
| State Management | Need to pass everything | ✓ Store as attributes |
| Override behavior | ✗ Can't | ✓ Can override |

---

## When to Use Class Approach

### ✓ Use Class When:
- Thread needs **multiple methods**
- Thread has **complex state** (many variables)
- Need to **override** thread behavior
- Building **reusable** thread types
- Thread logic is **complex**

### ✓ Use Function When:
- Simple, one-time task
- Few parameters
- No state to maintain
- Quick and simple

---

## Real Example: Adder with Both Approaches

### Function Approach
```python
from threading import Thread


def adder(counter, lock, iterations):
    for _ in range(iterations):
        with lock:
            counter.count += 1


# Usage
t = Thread(target=adder, args=(counter, lock, 1000))
t.start()
```

**Problems:**
- Have to pass 3 arguments
- Can't add helper methods
- Hard to extend

### Class Approach
```python
from threading import Thread


class Adder(Thread):
    def __init__(self, counter, lock, iterations):
        super().__init__()
        self.counter = counter
        self.lock = lock
        self.iterations = iterations

    def run(self):
        for _ in range(self.iterations):
            self.increment()

    def increment(self):
        with self.lock:
            self.counter.count += 1


# Usage
t = Adder(counter, lock, 1000)
t.start()
```

**Benefits:**
- ✓ Data stored as attributes
- ✓ Can have helper methods (`increment`)
- ✓ Clear structure
- ✓ Easy to extend

---

## Important: The run() Method

### Must Override run()
```python
class MyThread(Thread):
    def run(self):  # ← MUST be named "run"
        # Your code here
        pass
```

- When you call `t.start()`, it automatically calls `run()`
- **DON'T** call `run()` directly, always use `start()`

---

## Example: Download Manager

### Function Approach (Messy)
```python
def download(url, save_path, callback, retry_count):
    # Download logic
    pass


t = Thread(target=download, args=(url, path, callback, 3))
```

### Class Approach (Clean)
```python
class Downloader(Thread):
    def __init__(self, url, save_path, retry_count=3):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.retry_count = retry_count
        self.status = "pending"

    def run(self):
        for attempt in range(self.retry_count):
            if self.try_download():
                self.status = "success"
                return
        self.status = "failed"

    def try_download(self):
        # Download logic
        pass

    def get_status(self):
        return self.status


# Usage
d = Downloader("http://example.com/file.zip", "/downloads/")
d.start()
d.join()
print(d.get_status())
```

---

## super().__init__() - Why Needed?

```python
class MyThread(Thread):
    def __init__(self, name):
        super().__init__()  # ← Initialize Thread's internals
        self.name = name
```

**What it does:**
- Calls Thread class's `__init__`
- Sets up internal thread machinery
- **Must be called** before thread can start

---

## Complete Comparison Example

```python
from threading import Thread


# FUNCTION APPROACH
def worker_function(worker_id, tasks):
    for task in tasks:
        print(f"Worker {worker_id} doing {task}")


t1 = Thread(target=worker_function, args=(1, ["A", "B"]))


# CLASS APPROACH
class Worker(Thread):
    def __init__(self, worker_id, tasks):
        super().__init__()
        self.worker_id = worker_id
        self.tasks = tasks
        self.completed = []

    def run(self):
        for task in self.tasks:
            self.do_task(task)

    def do_task(self, task):
        print(f"Worker {self.worker_id} doing {task}")
        self.completed.append(task)

    def get_completed(self):
        return self.completed


t2 = Worker(2, ["C", "D"])
t2.start()
t2.join()
print(t2.get_completed())  # Can access results!
```

---

## Quick Rules

1. **Simple task** → Use function approach
2. **Complex logic** → Use class approach
3. **Always call** `super().__init__()`
4. **Override** `run()` method
5. **Use** `start()`, not `run()`

---

## Summary

**Function Approach:**
- Quick and simple
- Good for one-off tasks
- Less code

**Class Approach:**
- Better organization
- Reusable and extendable
- More features (methods, state)
- **Preferred for production code**

---

## In Your Adder-Subtractor Example

This is why we use class approach:

```python
class Adder(Thread):
    def __init__(self, counter, lock):
        super().__init__()
        self.counter = counter
        self.lock = lock

    def run(self):
        for i in range(100):
            with self.lock:
                self.counter.increment()
```

**Benefits:**
- Clear what data thread needs
- Can add methods later
- Easy to understand
- Professional code structure