"""
Example 9: MergeSort with ThreadPoolExecutor
Shows parallel merge sort implementation
"""
from concurrent.futures import ThreadPoolExecutor
import time

def merge(left, right):
    """Merge two sorted arrays"""
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

def merge_sort_sequential(arr):
    """Traditional sequential merge sort"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_sequential(arr[:mid])
    right = merge_sort_sequential(arr[mid:])
    return merge(left, right)

def merge_sort_parallel(arr, executor, depth=0):
    """Parallel merge sort using ThreadPool"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    
    # Only parallelize at top levels to avoid overhead
    if depth < 3:
        # Submit both halves to thread pool
        left_future = executor.submit(merge_sort_parallel, arr[:mid], executor, depth + 1)
        right_future = executor.submit(merge_sort_parallel, arr[mid:], executor, depth + 1)
        
        left = left_future.result()
        right = right_future.result()
    else:
        # Use sequential for smaller pieces
        left = merge_sort_sequential(arr[:mid])
        right = merge_sort_sequential(arr[mid:])
    
    return merge(left, right)

if __name__ == "__main__":
    import random
    
    # Create large random array
    size = 100_000
    arr = [random.randint(1, 1000) for _ in range(size)]
    
    print("=" * 60)
    print(f"Sorting array of {size:,} elements")
    print("=" * 60)
    
    # Sequential
    print("\n1. Sequential MergeSort")
    arr_copy = arr.copy()
    start = time.time()
    sorted_arr = merge_sort_sequential(arr_copy)
    seq_time = time.time() - start
    print(f"   Time: {seq_time:.3f} seconds")
    
    # Parallel with ThreadPool
    print("\n2. Parallel MergeSort (ThreadPool)")
    arr_copy = arr.copy()
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        sorted_arr = merge_sort_parallel(arr_copy, executor)
    parallel_time = time.time() - start
    print(f"   Time: {parallel_time:.3f} seconds")
    
    # Results
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print(f"Sequential: {seq_time:.3f}s")
    print(f"Parallel:   {parallel_time:.3f}s")
    print(f"Speedup:    {seq_time/parallel_time:.2f}x")
    
    print("\n📌 NOTE: For sorting (CPU-bound), ProcessPool would be better!")
    print("   ThreadPool has limited benefit due to GIL")
