"""
REVISION: ThreadPool, ProcessPool & MergeSort
Quick recap before today's synchronization class
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

# ============================================================
# Quick MergeSort Recap
# ============================================================
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

# ============================================================
# Revision Examples
# ============================================================

def revision_threadpool():
    print("=" * 60)
    print("REVISION: ThreadPoolExecutor (for I/O tasks)")
    print("=" * 60)
    
    def download_file(file_id):
        print(f"Downloading file {file_id}...")
        time.sleep(1)
        return f"file_{file_id}.txt"
    
    start = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        files = list(range(1, 4))
        results = list(executor.map(download_file, files))
    elapsed = time.time() - start
    
    print(f"Downloaded: {results}")
    print(f"Time: {elapsed:.2f}s")
    print("✓ ThreadPool good for I/O-bound tasks")

def revision_processpool():
    print("\n" + "=" * 60)
    print("REVISION: ProcessPoolExecutor (for CPU tasks)")
    print("=" * 60)
    
    def cpu_task(n):
        total = 0
        for i in range(5_000_000):
            total += i * i
        return total
    
    start = time.time()
    with ProcessPoolExecutor(max_workers=2) as executor:
        numbers = [1, 2]
        results = list(executor.map(cpu_task, numbers))
    elapsed = time.time() - start
    
    print(f"Results: {len(results)} tasks completed")
    print(f"Time: {elapsed:.2f}s")
    print("✓ ProcessPool achieves true parallelism")

def revision_gil():
    print("\n" + "=" * 60)
    print("REVISION: The GIL Problem")
    print("=" * 60)
    print("""
Key Points from Last Class:
─────────────────────────────
1. GIL = Global Interpreter Lock
2. Only ONE thread executes Python bytecode at a time
3. Python threads CANNOT run in true parallel (for CPU tasks)
4. Java CAN run threads in parallel (no GIL)

When to use what:
─────────────────────────────
I/O-bound tasks → ThreadPoolExecutor
  • File operations
  • Network calls
  • Database queries

CPU-bound tasks → ProcessPoolExecutor
  • Calculations
  • Data processing
  • Sorting (like MergeSort)

Remember: Each process has its own GIL!
    """)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QUICK REVISION: Last Class")
    print("=" * 60)
    
    revision_gil()
    revision_threadpool()
    revision_processpool()
    
    print("\n" + "=" * 60)
    print("Now let's move to TODAY'S TOPIC:")
    print("=" * 60)
    print("""
If GIL locks threads, why do we still need Mutex?
↓
Because GIL locks INTERPRETER, not your DATA!
↓
Context switching can still cause race conditions!
↓
Let's see examples...
    """)
