"""
Example 8: Understanding Futures
Shows what a Future is and how to use it
"""
import time
from concurrent.futures import ThreadPoolExecutor

def slow_task(task_id, duration):
    """A task that takes some time"""
    print(f"Task {task_id} started (will take {duration}s)")
    time.sleep(duration)
    print(f"Task {task_id} completed!")
    return f"Result from task {task_id}"

if __name__ == "__main__":
    print("=" * 60)
    print("Understanding Futures")
    print("=" * 60)
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit returns a Future immediately
        print("\n1. Submitting task...")
        future = executor.submit(slow_task, 1, 3)
        
        print(f"2. Got Future object: {future}")
        print(f"   Type: {type(future)}")
        
        # Check if task is done (non-blocking)
        print(f"\n3. Is task done? {future.done()}")
        
        # Do other work while task runs
        print("4. Doing other work while task runs...")
        time.sleep(1)
        print(f"   Is task done now? {future.done()}")
        
        # Get result (blocks until ready)
        print("\n5. Getting result (this will block until task completes)...")
        result = future.result()
        print(f"   Result: {result}")
        print(f"   Is task done? {future.done()}")
    
    print("\n" + "=" * 60)
    print("KEY POINTS:")
    print("=" * 60)
    print("• Future = Promise for a future result")
    print("• submit() returns Future immediately")
    print("• done() checks if task is complete (non-blocking)")
    print("• result() gets the result (blocks until ready)")
