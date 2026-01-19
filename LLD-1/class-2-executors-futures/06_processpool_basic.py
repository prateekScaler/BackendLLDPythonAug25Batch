"""
Example 6: ProcessPoolExecutor for CPU-Bound Tasks
Shows how to use processes for TRUE parallelism
"""
import time
from concurrent.futures import ProcessPoolExecutor

def cpu_intensive_task(n):
    """Heavy computation - finding sum of squares"""
    print(f"Process {n} started")
    total = 0
    for i in range(10_000_000):  # 10 million iterations
        total += i * i
    print(f"Process {n} finished")
    return total

if __name__ == "__main__":
    # IMPORTANT: if __name__ == "__main__" is REQUIRED for processes
    # Prevents infinite process creation on Windows
    
    print("=" * 50)
    print("Sequential Execution")
    print("=" * 50)
    
    start = time.time()
    result1 = cpu_intensive_task(1)
    result2 = cpu_intensive_task(2)
    result3 = cpu_intensive_task(3)
    end = time.time()
    sequential_time = end - start
    print(f"Time: {sequential_time:.2f}s\n")
    
    print("=" * 50)
    print("ProcessPoolExecutor (True Parallelism)")
    print("=" * 50)
    
    start = time.time()
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(cpu_intensive_task, i) for i in range(1, 4)]
        results = [f.result() for f in futures]
    end = time.time()
    parallel_time = end - start
    print(f"Time: {parallel_time:.2f}s\n")
    
    print("=" * 50)
    print("COMPARISON:")
    print("=" * 50)
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Parallel:   {parallel_time:.2f}s")
    print(f"Speedup:    {sequential_time/parallel_time:.2f}x")
    print("\nNotice: Significant speedup! Processes achieve TRUE parallelism")
