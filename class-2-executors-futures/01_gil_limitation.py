"""
Example 1: GIL Limitation - CPU Bound Task with Threads
Demonstrates why threads are BAD for CPU-bound tasks
"""
import time
from threading import Thread

def cpu_bound_task(n):
    """A CPU-intensive task - calculating sum of squares"""
    print(f"Starting task {n}")
    total = 0
    for i in range(10_000_000):  # 10 million iterations
        total += i * i
    print(f"Task {n} finished. Result: {total}")
    return total

if __name__ == "__main__":
    print("=" * 50)
    print("Sequential Execution (No Threads)")
    print("=" * 50)
    
    start = time.time()
    cpu_bound_task(1)
    cpu_bound_task(2)
    end = time.time()
    sequential_time = end - start
    print(f"Time taken: {sequential_time:.2f} seconds\n")
    
    print("=" * 50)
    print("With Threads (Should be similar time due to GIL)")
    print("=" * 50)
    
    start = time.time()
    t1 = Thread(target=cpu_bound_task, args=(1,))
    t2 = Thread(target=cpu_bound_task, args=(2,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    end = time.time()
    threaded_time = end - start
    print(f"Time taken: {threaded_time:.2f} seconds\n")
    
    print("=" * 50)
    print("CONCLUSION:")
    print("=" * 50)
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Threaded:   {threaded_time:.2f}s")
    print(f"Speedup:    {sequential_time/threaded_time:.2f}x")
    print("\nNotice: NO speedup! Threads don't help CPU-bound tasks due to GIL")
