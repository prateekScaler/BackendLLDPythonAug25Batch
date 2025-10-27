"""
Sequential Merge Sort (No Threading/Multiprocessing)
Basic implementation for comparison
"""
import time
import random


def merge(left, right):
    """Merge two sorted arrays into one sorted array"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    """Recursively sort array using merge sort"""
    # Base case: array with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr

    # Divide array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # Merge the sorted halves
    return merge(left_sorted, right_sorted)


if __name__ == "__main__":
    # Create random array
    size = 100_000
    arr = [random.randint(1, 1000) for _ in range(size)]

    print("=" * 60)
    print(f"Sorting {size:,} elements using Sequential Merge Sort")
    print("=" * 60)

    # Sort
    start = time.time()
    sorted_arr = merge_sort(arr.copy())
    end = time.time()

    # Verify correctness
    is_correct = sorted_arr == sorted(arr)

    print(f"\nTime taken: {end - start:.3f} seconds")
    print(f"Correctly sorted: {is_correct}")

    # Show first and last few elements
    print(f"\nFirst 10 elements: {sorted_arr[:10]}")
    print(f"Last 10 elements: {sorted_arr[-10:]}")