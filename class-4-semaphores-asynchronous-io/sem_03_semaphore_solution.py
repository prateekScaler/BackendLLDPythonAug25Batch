"""
Producer-Consumer with Semaphores
Elegant and efficient solution!
"""
from threading import Thread, Semaphore, Lock
import time

buffer = []
MAX_SIZE = 3

# Semaphores for synchronization
empty = Semaphore(MAX_SIZE)  # Counts empty slots (initially 3)
full = Semaphore(0)          # Counts items (initially 0)
mutex = Lock()               # Protects buffer access

# ============================================================
# WITH SEMAPHORES - EFFICIENT & CORRECT
# ============================================================

def producer(id):
    """Producer using semaphores - no busy waiting!"""
    for i in range(3):
        item = f"P{id}-{i}"

        # Wait for empty slot (BLOCKS if full - no busy waiting!)
        empty.acquire()

        # Add to buffer (mutex protects this)
        with mutex:
            buffer.append(item)
            print(f"Producer {id}: ✓ Added {item} | Buffer: {len(buffer)}")

        # Signal: buffer has one more item
        full.release()

        time.sleep(0.02)

def consumer(id):
    """Consumer using semaphores - no busy waiting!"""
    for i in range(3):
        # Wait for item (BLOCKS if empty - no busy waiting!)
        full.acquire()

        # Remove from buffer (mutex protects this)
        with mutex:
            item = buffer.pop(0)
            print(f"Consumer {id}: ✓ Consumed {item} | Buffer: {len(buffer)}")

        # Signal: buffer has one more empty slot
        empty.release()

        time.sleep(0.02)

if __name__ == "__main__":
    print("=" * 60)
    print("PRODUCER-CONSUMER WITH SEMAPHORES")
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
    print(f"✓ No busy waiting!")

    print()
    print("=" * 60)
    print("HOW IT WORKS:")
    print("=" * 60)
    print("empty = Semaphore(3)  # Tracks empty slots")
    print("full  = Semaphore(0)  # Tracks items")
    print()
    print("Producer:")
    print("  1. empty.acquire() → Wait for space (blocks if full)")
    print("  2. Add item")
    print("  3. full.release()  → Signal item added")
    print()
    print("Consumer:")
    print("  1. full.acquire()  → Wait for item (blocks if empty)")
    print("  2. Remove item")
    print("  3. empty.release() → Signal space freed")

    print()
    print("=" * 60)
    print("WHY SEMAPHORES WIN:")
    print("=" * 60)
    print("✓ No busy waiting (threads sleep when blocked)")
    print("✓ Automatic coordination between producers/consumers")
    print("✓ Producer blocks ONLY when buffer full")
    print("✓ Consumer blocks ONLY when buffer empty")
    print("✓ Efficient CPU usage")

    print()
    print("KEY: Semaphore = Counting lock")
    print("  • Lock allows 1 thread")
    print("  • Semaphore(N) allows N threads")