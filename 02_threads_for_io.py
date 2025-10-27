"""
Example 2: Threads are GOOD for I/O Bound Tasks
Demonstrates that threads work well when waiting for I/O
"""
import time
from threading import Thread

def io_bound_task(n):
    """Simulates I/O operation (like reading file or network call)"""
    print(f"Task {n} started - waiting for I/O...")
    time.sleep(2)  # Simulates waiting for I/O (network, file, database)
    print(f"Task {n} completed!")
    return n

if __name__ == "__main__":
    print("=" * 50)
    print("Sequential Execution (No Threads)")
    print("=" * 50)
    
    start = time.time()
    io_bound_task(1)
    io_bound_task(2)
    io_bound_task(3)
    end = time.time()
    sequential_time = end - start
    print(f"Time taken: {sequential_time:.2f} seconds\n")
    
    print("=" * 50)
    print("With Threads (Should be MUCH faster)")
    print("=" * 50)
    
    start = time.time()
    threads = []
    for i in range(1, 4):
        t = Thread(target=io_bound_task, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.time()
    threaded_time = end - start
    print(f"Time taken: {threaded_time:.2f} seconds\n")
    
    print("=" * 50)
    print("CONCLUSION:")
    print("=" * 50)
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Threaded:   {threaded_time:.2f}s")
    print(f"Speedup:    {sequential_time/threaded_time:.2f}x")
    print("\nNotice: HUGE speedup! Threads are perfect for I/O-bound tasks")
