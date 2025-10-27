"""
Example 3: ThreadPoolExecutor Basics
Shows how to use ThreadPoolExecutor for cleaner thread management
"""
import time
from concurrent.futures import ThreadPoolExecutor

def download_file(file_id):
    """Simulates downloading a file (I/O operation)"""
    print(f"[Thread {file_id}] Starting download...")
    time.sleep(2)  # Simulates download time
    print(f"[Thread {file_id}] Download complete!")
    return f"file_{file_id}.txt"

if __name__ == "__main__":
    print("=" * 50)
    print("ThreadPoolExecutor with 3 Workers")
    print("=" * 50)
    
    start = time.time()
    
    # Create a pool of 3 threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks - returns immediately with Future objects
        future1 = executor.submit(download_file, 1)
        future2 = executor.submit(download_file, 2)
        future3 = executor.submit(download_file, 3)
        
        print("\nAll tasks submitted! Now waiting for results...\n")
        
        # Get results - this blocks until the task is done
        result1 = future1.result()
        result2 = future2.result()
        result3 = future3.result()
        
        print(f"\nResults: {result1}, {result2}, {result3}")
    
    end = time.time()
    print(f"\nTotal time: {end - start:.2f} seconds")
    print("\nNotice: All 3 downloads ran concurrently, took ~2 seconds total")
