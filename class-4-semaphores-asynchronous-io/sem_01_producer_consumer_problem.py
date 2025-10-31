"""
Producer-Consumer Problem - The Issue
Simple demonstration of race conditions
"""
from threading import Thread
import time

buffer = []
MAX_SIZE = 3

# ============================================================
# WITHOUT SYNCHRONIZATION - CHAOS!
# ============================================================

def producer(id):
    """Add items to buffer"""
    for i in range(3):
        item = f"P{id}-{i}"

        if len(buffer) < MAX_SIZE:
            print(f"Producer {id}: Checking... Buffer has space")
            time.sleep(0.01)  # Simulates work - RACE WINDOW!
            buffer.append(item)
            print(f"Producer {id}: ✓ Added {item} | Buffer size: {len(buffer)}")
        else:
            print(f"Producer {id}: ✗ Buffer full, dropped {item}")

        time.sleep(0.02)

def consumer(id):
    """Remove items from buffer"""
    for i in range(3):
        if len(buffer) > 0:
            print(f"Consumer {id}: Checking... Buffer has items")
            time.sleep(0.01)  # Simulates work - RACE WINDOW!
            item = buffer.pop(0)
            print(f"Consumer {id}: ✓ Consumed {item} | Buffer size: {len(buffer)}")
        else:
            print(f"Consumer {id}: ✗ Buffer empty, nothing to consume")

        time.sleep(0.02)

if __name__ == "__main__":
    print("=" * 60)
    print("PRODUCER-CONSUMER WITHOUT LOCKS")
    print(f"Buffer max size: {MAX_SIZE}")
    print("=" * 60)
    print()

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

    print()
    print("=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print(f"Final buffer: {buffer}")
    print(f"Final size: {len(buffer)}")

    print()
    print("PROBLEMS:")
    print("• Buffer overflow (size > 3)")
    print("• Lost items (multiple threads add/remove)")
    print("• IndexError (pop from empty buffer)")
    print()
    print("WHY? Race condition between CHECK and ACTION!")