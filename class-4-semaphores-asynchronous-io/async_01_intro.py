"""
Async I/O - Introduction
Why async when we have threads?
"""
import asyncio
import time
from threading import Thread

print("=" * 60)
print("ASYNC I/O vs THREADS")
print("=" * 60)

# ============================================================
# The Problem: Too Many Threads
# ============================================================

print("\nTHE PROBLEM WITH THREADS:")
print("-" * 60)
print("""
Imagine 10,000 concurrent I/O operations:
  • Each thread = ~8MB memory
  • 10,000 threads = 80GB memory! 💥
  • Context switching overhead
  • OS thread limit
  
We need: Handle MANY I/O tasks WITHOUT many threads!
""")

# ============================================================
# Example 1: Thread Approach
# ============================================================

def download_with_thread(url_id):
    """Simulate download with thread"""
    print(f"Thread {url_id}: Starting download...")
    time.sleep(1)  # Simulates I/O wait
    print(f"Thread {url_id}: Done!")
    return f"Data from {url_id}"

def thread_approach():
    print("\n1. THREAD APPROACH:")
    print("-" * 60)
    
    start = time.time()
    
    threads = []
    for i in range(5):
        t = Thread(target=download_with_thread, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Time: {time.time() - start:.2f}s")
    print("✓ Fast, but each download = 1 thread")
    print("✗ Doesn't scale to 10,000 downloads!")

# ============================================================
# Example 2: Async Approach
# ============================================================

async def download_with_async(url_id):
    """Simulate download with async"""
    print(f"Async {url_id}: Starting download...")
    await asyncio.sleep(1)  # Simulates I/O wait (non-blocking!)
    print(f"Async {url_id}: Done!")
    return f"Data from {url_id}"

async def async_approach():
    print("\n2. ASYNC APPROACH:")
    print("-" * 60)
    
    start = time.time()
    
    # Create 5 tasks (NOT threads!)
    tasks = [download_with_async(i) for i in range(5)]
    
    # Run all concurrently on SINGLE thread!
    await asyncio.gather(*tasks)
    
    print(f"Time: {time.time() - start:.2f}s")
    print("✓ Fast, single thread handles all!")
    print("✓ Scales to 10,000 downloads easily!")

# ============================================================
# Key Differences
# ============================================================

print("\n" + "=" * 60)
print("THREADS vs ASYNC:")
print("=" * 60)

print("""
┌─────────────────────┬──────────────────┬──────────────────┐
│ Feature             │ Threads          │ Async            │
├─────────────────────┼──────────────────┼──────────────────┤
│ Concurrency Model   │ Preemptive       │ Cooperative      │
│ Switching           │ OS decides       │ You control      │
│ Memory per task     │ ~8MB             │ ~1-2KB           │
│ Max concurrent      │ ~1000s           │ ~100,000s        │
│ Complexity          │ Simple           │ More complex     │
│ Best for            │ I/O + CPU mixed  │ Pure I/O         │
│ GIL Impact          │ Yes (CPU-bound)  │ No (single thread)│
└─────────────────────┴──────────────────┴──────────────────┘
""")

# ============================================================
# When to Use What?
# ============================================================

print("=" * 60)
print("WHEN TO USE ASYNC:")
print("=" * 60)
print("""
✓ Many I/O operations (network, file, database)
✓ Need to handle 10,000+ concurrent operations
✓ All I/O is async-compatible (libraries support it)
✓ Can use async/await syntax

Examples:
  • Web scraping (many URLs)
  • API servers (many clients)
  • Chat servers
  • Microservices
""")

print("=" * 60)
print("WHEN TO USE THREADS:")
print("=" * 60)
print("""
✓ Mixed CPU + I/O work
✓ Need to use blocking libraries (no async support)
✓ Simpler code (no async/await)
✓ Moderate concurrency (< 1000)

Examples:
  • GUI applications
  • Desktop apps
  • Simple scripts
  • Legacy code integration
""")

# ============================================================
# The Event Loop (Async Secret Sauce)
# ============================================================

print("\n" + "=" * 60)
print("HOW ASYNC WORKS: THE EVENT LOOP")
print("=" * 60)

print("""
Event Loop = Traffic Controller for I/O

1. Task 1 starts download → Waiting for response
   ↓ (yield control)
2. Task 2 starts download → Waiting for response
   ↓ (yield control)
3. Task 3 starts download → Waiting for response
   ↓
4. Task 1 response arrives → Resume Task 1 → Process
5. Task 3 response arrives → Resume Task 3 → Process
6. Task 2 response arrives → Resume Task 2 → Process

Key: Single thread switches between tasks at I/O points!
     NOT preemptive like threads (OS switches)
     Cooperative (tasks yield control with 'await')
""")

# ============================================================
# Comparison with Node.js
# ============================================================

print("=" * 60)
print("ASYNC IN OTHER LANGUAGES:")
print("=" * 60)

print("""
Python (asyncio):
  async def fetch():
      await download()
  
  asyncio.run(fetch())

Node.js (similar!):
  async function fetch() {
      await download();
  }
  
  fetch();

JavaScript (browser):
  async function fetch() {
      await fetch('url');
  }

All use same concept: Event loop + async/await!
""")

# Run demos
if __name__ == "__main__":
    thread_approach()
    asyncio.run(async_approach())
    
    print("\n" + "=" * 60)
    print("KEY TAKEAWAY:")
    print("=" * 60)
    print("Async = Single thread handling MANY I/O tasks")
    print("Threads = Multiple threads, each handling ONE task")
    print("\nFor I/O-heavy, high-concurrency: Async wins!")
    print("For simplicity, mixed workload: Threads win!")
    print("=" * 60)
