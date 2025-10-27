"""
Example 11: Why if __name__ == "__main__" is Required
Demonstrates what happens without the guard
"""
from concurrent.futures import ProcessPoolExecutor

def simple_task(n):
    """Simple task for demonstration"""
    return n * n

# ❌ BAD - Without guard (commented out to prevent infinite loop)
# def bad_example():
#     """This will create infinite processes on Windows!"""
#     with ProcessPoolExecutor(max_workers=2) as executor:
#         results = list(executor.map(simple_task, [1, 2, 3]))
#     print(results)
#
# bad_example()  # DO NOT RUN! Will cause infinite spawning

# ✅ GOOD - With guard
if __name__ == "__main__":
    print("=" * 60)
    print("Running with proper if __name__ == '__main__' guard")
    print("=" * 60)
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(simple_task, [1, 2, 3, 4, 5]))
    
    print(f"\nResults: {results}")
    print("\n✓ Worked perfectly!")
    
    print("\n" + "=" * 60)
    print("WHY IS THE GUARD NEEDED?")
    print("=" * 60)
    print("""
When you start a new process:
1. Python imports the script in the new process
2. Without the guard, it will start ANOTHER ProcessPool
3. That pool will spawn MORE processes
4. Those processes import the script again
5. Infinite loop! 💥

The guard prevents this:
- In main process: __name__ == "__main__" → True → Runs code
- In child processes: __name__ == "script_name" → False → Skips code

RULE: Always use if __name__ == "__main__" with ProcessPoolExecutor!
    """)
