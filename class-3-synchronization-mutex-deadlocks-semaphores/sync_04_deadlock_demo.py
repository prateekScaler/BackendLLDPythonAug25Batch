"""
Example 4: Deadlock - Simple Bank Transfer Example
Shows deadlock with account names (easy to understand)
"""
from threading import Thread, Lock
import time

# Create accounts with locks
class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.lock = Lock()

# ============================================================
# DEADLOCK SCENARIO - Locking accounts in different order
# ============================================================
def transfer_bad(from_account, to_account, amount):
    """This can cause DEADLOCK!"""
    print(f"  {from_account.name} trying to transfer ${amount} to {to_account.name}")

    # Lock from_account first
    with from_account.lock:
        print(f"    {from_account.name}: Got my account lock")
        time.sleep(0.1)  # Simulate some processing

        # Then lock to_account
        with to_account.lock:
            print(f"    {from_account.name}: Got {to_account.name}'s lock")
            from_account.balance -= amount
            to_account.balance += amount
            print(f"    ✓ Transfer complete: {from_account.name} → {to_account.name}")

def deadlock_demo():
    print("=" * 60)
    print("DEADLOCK SCENARIO")
    print("=" * 60)

    alice = Account("Alice", 1000)
    bob = Account("Bob", 1000)

    # Alice sends $100 to Bob (locks: Alice, then Bob)
    t1 = Thread(target=transfer_bad, args=(alice, bob, 100))

    # Bob sends $50 to Alice (locks: Bob, then Alice) - OPPOSITE ORDER!
    t2 = Thread(target=transfer_bad, args=(bob, alice, 50))

    t1.start()
    t2.start()

    # Wait with timeout
    t1.join(timeout=2)
    t2.join(timeout=2)

    if t1.is_alive() or t2.is_alive():
        print("\n💥 DEADLOCK OCCURRED!")
        print("Both transfers are stuck!")

    print("\n" + "=" * 60)
    print("WHAT HAPPENED:")
    print("=" * 60)
    print("Thread 1 (Alice→Bob): Has Alice's lock, wants Bob's lock")
    print("Thread 2 (Bob→Alice): Has Bob's lock, wants Alice's lock")
    print("Both waiting for each other → DEADLOCK!")

# ============================================================
# SOLUTION: Always lock accounts in ALPHABETICAL ORDER
# ============================================================
def transfer_good(from_account, to_account, amount):
    """NO deadlock - locks in alphabetical order by name"""
    print(f"  {from_account.name} transferring ${amount} to {to_account.name}")

    # Always lock in alphabetical order of account names
    if from_account.name < to_account.name:
        first, second = from_account, to_account
    else:
        first, second = to_account, from_account

    with first.lock:
        print(f"    Got {first.name}'s lock first")
        with second.lock:
            print(f"    Got {second.name}'s lock second")
            from_account.balance -= amount
            to_account.balance += amount
            print(f"    ✓ Transfer complete: {from_account.name} → {to_account.name}")

def no_deadlock_demo():
    print("\n" + "=" * 60)
    print("NO DEADLOCK - Alphabetical Lock Order")
    print("=" * 60)

    alice = Account("Alice", 1000)
    bob = Account("Bob", 1000)

    # Both transfers will lock in alphabetical order (Alice, then Bob)
    t1 = Thread(target=transfer_good, args=(alice, bob, 100))
    t2 = Thread(target=transfer_good, args=(bob, alice, 50))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"\n✓ Final balances:")
    print(f"  Alice: ${alice.balance}")
    print(f"  Bob: ${bob.balance}")

if __name__ == "__main__":
    print("\n🔴 WARNING: First demo will deadlock (by design)")
    print("Press Ctrl+C to stop if it hangs\n")

    try:
        deadlock_demo()
    except KeyboardInterrupt:
        print("\n\nStopped by user")

    no_deadlock_demo()

    print("\n" + "=" * 60)
    print("KEY LESSON:")
    print("=" * 60)
    print("Always lock accounts in ALPHABETICAL ORDER")
    print("  Alice → Bob: Lock Alice first, then Bob")
    print("  Bob → Alice: Lock Alice first, then Bob (same order!)")
    print("\nThis ensures no deadlock can occur!")