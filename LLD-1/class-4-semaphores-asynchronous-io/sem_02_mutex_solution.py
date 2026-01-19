"""
Producer-Consumer with Mutex (Lock)
Works correctly but inefficient!
"""
from threading import Thread, Lock
import time

buffer = []
MAX_SIZE = 3
lock = Lock()

# ============================================================
# WITH MUTEX - CORRECT BUT INEFFICIENT
# ============================================================

def producer(id):
    """Producer with lock - works but wasteful"""
    for i in range(3):
        item = f"P{id}-{i}"

        # BUSY WAITING - keeps trying until success
        while True:
            with lock:
                if len(buffer) < MAX_SIZE:
                    buffer.append(item)
                    print(f"Producer {id}: ✓ Added {item} | Buffer: {len(buffer)}")
                    break
            # Buffer full, wait and retry
            time.sleep(0.01)

        time.sleep(0.02)

def consumer(id):
    """Consumer with lock - works but wasteful"""
    for i in range(3):
        # BUSY WAITING - keeps trying until success
        while True:
            with lock:
                if len(buffer) > 0:
                    item = buffer.pop(0)
                    print(f"Consumer {id}: ✓ Consumed {item} | Buffer: {len(buffer)}")
                    break
            # Buffer empty, wait and retry
            time.sleep(0.01)

        time.sleep(0.02)

if __name__ == "__main__":
    print("=" * 60)
    print("PRODUCER-CONSUMER WITH MUTEX")
    print(f"Buffer max size: {MAX_SIZE}")
    print("=" * 60)
    print()

    start = time.time()

    # 5 producers, 5 consumers
    threads = []

    for i in range(1, 6):
        threads.append(Thread(target=producer, args=(i,)))

    for i in range(1, 6):
        threads.append(Thread(target=consumer, args=(i,)))

    # Start all
    for t in threads:
        t.start()

    # Wait all
    for t in threads:
        t.join()

    elapsed = time.time() - start

    print()
    print("=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print(f"✓ All done! Time: {elapsed:.2f}s")
    print(f"✓ Final buffer: {buffer}")
    print(f"✓ Correct! No overflow, no crashes")

    print()
    print("=" * 60)
    print("BUT PROBLEMS WITH MUTEX:")
    print("=" * 60)
    print("✗ BUSY WAITING (while True loop)")
    print("✗ Threads constantly checking lock")
    print("✗ Wasteful CPU usage")
    print("✗ Only ONE thread can access at a time")
    print()
    print("💡 Need better solution: SEMAPHORES!")