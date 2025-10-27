"""
Example 7: ThreadPoolExecutor vs ProcessPoolExecutor
Direct comparison on CPU-bound task
"""
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def calculate_sum_of_squares(n):
    """CPU-intensive calculation"""
    total = 0
    for i in range(10_000_000):
        total += i * i
    return total

if __name__ == "__main__":
    numbers = [1, 2, 3, 4]
    
    print("=" * 60)
    print("Testing CPU-Bound Task: Sum of Squares")
    print("=" * 60)
    
    # Method 1: ThreadPoolExecutor
    print("\n1. ThreadPoolExecutor (Affected by GIL)")
    print("-" * 60)
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(calculate_sum_of_squares, numbers))
    thread_time = time.time() - start
    print(f"Time taken: {thread_time:.2f} seconds")
    
    # Method 2: ProcessPoolExecutor
    print("\n2. ProcessPoolExecutor (TRUE Parallelism)")
    print("-" * 60)
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(calculate_sum_of_squares, numbers))
    process_time = time.time() - start
    print(f"Time taken: {process_time:.2f} seconds")
    
    # Comparison
    print("\n" + "=" * 60)
    print("COMPARISON:")
    print("=" * 60)
    print(f"ThreadPool:  {thread_time:.2f}s (GIL prevents parallelism)")
    print(f"ProcessPool: {process_time:.2f}s (True parallelism)")
    print(f"ProcessPool is {thread_time/process_time:.2f}x FASTER")
    
    print("\n📌 KEY TAKEAWAY:")
    print("   For CPU-bound tasks → Use ProcessPoolExecutor")
    print("   For I/O-bound tasks → Use ThreadPoolExecutor")
