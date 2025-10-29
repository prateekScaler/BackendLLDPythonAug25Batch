"""
Example 10: MergeSort with ProcessPoolExecutor
Shows parallel merge sort with TRUE parallelism
"""
from concurrent.futures import ProcessPoolExecutor
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

def parallel_sort_chunk(arr):
    """Helper function for process pool - sorts a chunk"""
    return merge_sort_sequential(arr)

def merge_sort_with_processes(arr, num_processes=4):
    """Divide array into chunks, sort in parallel, then merge"""
    if len(arr) <= 1:
        return arr
    
    # Divide into chunks
    chunk_size = len(arr) // num_processes
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    # Sort chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        sorted_chunks = list(executor.map(parallel_sort_chunk, chunks))
    
    # Merge all sorted chunks
    while len(sorted_chunks) > 1:
        merged = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged.append(merge(sorted_chunks[i], sorted_chunks[i + 1]))
            else:
                merged.append(sorted_chunks[i])
        sorted_chunks = merged
    
    return sorted_chunks[0] if sorted_chunks else []

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
    
    # Parallel with ProcessPool
    print("\n2. Parallel MergeSort (ProcessPool)")
    arr_copy = arr.copy()
    start = time.time()
    sorted_arr = merge_sort_with_processes(arr_copy, num_processes=4)
    parallel_time = time.time() - start
    print(f"   Time: {parallel_time:.3f} seconds")
    
    # Verify correctness
    arr_copy = arr.copy()
    python_sorted = sorted(arr_copy)
    is_correct = sorted_arr == python_sorted
    
    # Results
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print(f"Sequential: {seq_time:.3f}s")
    print(f"Parallel:   {parallel_time:.3f}s")
    print(f"Speedup:    {seq_time/parallel_time:.2f}x")
    print(f"Correct:    {is_correct}")
    
    print("\n📌 KEY POINT:")
    print("   ProcessPool achieves TRUE speedup for CPU-bound tasks!")
    print("   Each process runs on a separate core with its own GIL")
