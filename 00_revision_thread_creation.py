"""
Revision: Basic Thread Creation
Shows the fundamentals of creating and using threads in Python
"""
from threading import Thread
import time

# ============================================================
# Example 1: Simple Thread Creation
# ============================================================
def print_numbers():
    """Simple function to print numbers"""
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(0.5)

print("=" * 60)
print("Example 1: Basic Thread Creation")
print("=" * 60)

# Create a thread
t = Thread(target=print_numbers)

# Start the thread
t.start()

# # Wait for thread to complete
t.join()

print("Thread completed!\n")


# ============================================================
# Example 2: Thread with Arguments
# ============================================================
def greet(name, times):
    """Function that takes arguments"""
    for i in range(times):
        print(f"Hello {name}! (#{i+1})")
        time.sleep(0.3)

print("=" * 60)
print("Example 2: Thread with Arguments")
print("=" * 60)

# Create thread with arguments using 'args' tuple
t = Thread(target=greet, args=("Alice", 3))
t.start()
t.join()

print("Thread completed!\n")


# ============================================================
# Example 3: Multiple Threads
# ============================================================
def task(task_id):
    """Simple task that prints its ID"""
    print(f"Task {task_id} started")
    time.sleep(1)
    print(f"Task {task_id} finished")

print("=" * 60)
print("Example 3: Multiple Threads Running Concurrently")
print("=" * 60)

start = time.time()

# Create and start multiple threads
threads = []
for i in range(1, 4):
    t = Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

end = time.time()
print(f"\nTotal time: {end - start:.2f} seconds")
print("Notice: All 3 tasks ran concurrently, took ~1 second total")