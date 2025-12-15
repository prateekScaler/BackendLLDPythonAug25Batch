#!/usr/bin/env python3
"""
Demonstrate concurrent booking - multiple users booking same seats simultaneously
"""
import requests
import threading
import time
from collections import defaultdict

BASE_URL = "http://localhost:8000"
AUTH = ("pvijay", "password123")

# Seats to test concurrency on
BOOKING_DATA = {
    "show_id": "show-1",
    "seat_ids": [
        "show-1-pvr-delhi-1-screen-1-A5",
        "show-1-pvr-delhi-1-screen-1-A6"
    ],
    "payment_mode": "UPI",
    "coupon_code": ""
}

results = []
results_lock = threading.Lock()

def make_booking_request(user_id):
    """Simulate a user making a booking request"""
    try:
        print(f"User {user_id}: Sending booking request...")
        start_time = time.time()

        response = requests.post(
            f"{BASE_URL}/api/book/",
            json=BOOKING_DATA,
            auth=AUTH,
            headers={"Content-Type": "application/json"}
        )

        elapsed = time.time() - start_time

        with results_lock:
            results.append({
                'user_id': user_id,
                'status_code': response.status_code,
                'response': response.json(),
                'elapsed': elapsed
            })

        if response.status_code == 201:
            print(f"✅ User {user_id}: SUCCESS! Booking confirmed in {elapsed:.2f}s")
        else:
            error = response.json().get('non_field_errors', response.json())
            print(f"❌ User {user_id}: FAILED - {error}")

    except Exception as e:
        print(f"❌ User {user_id}: ERROR - {e}")

def test_concurrent_booking(num_users=5):
    """Test concurrent booking with multiple users"""
    print(f"\n{'='*70}")
    print(f"Testing Concurrent Booking: {num_users} users booking same seats")
    print(f"Seats: {', '.join(BOOKING_DATA['seat_ids'])}")
    print(f"{'='*70}\n")

    # Create threads for concurrent requests
    threads = []
    for i in range(1, num_users + 1):
        thread = threading.Thread(target=make_booking_request, args=(i,))
        threads.append(thread)

    # Start all threads at roughly the same time
    print("Starting concurrent requests...\n")
    start_time = time.time()

    for thread in threads:
        thread.start()

    # Wait for all to complete
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time

    # Analyze results
    print(f"\n{'='*70}")
    print("RESULTS SUMMARY")
    print(f"{'='*70}")

    successes = [r for r in results if r['status_code'] == 201]
    failures = [r for r in results if r['status_code'] != 201]

    print(f"Total requests: {len(results)}")
    print(f"Successful bookings: {len(successes)}")
    print(f"Failed bookings: {len(failures)}")
    print(f"Total time: {total_time:.2f}s")

    if len(successes) == 1:
        print("\n✅ CONCURRENCY CONTROL WORKING!")
        print("   Only 1 user succeeded, others got 'seats not available'")
        winner = successes[0]
        print(f"   Winner: User {winner['user_id']}")
    elif len(successes) > 1:
        print("\n⚠️  WARNING: Multiple users booked same seats!")
        print("   This indicates a race condition issue")
    else:
        print("\n❌ No successful bookings - check if seats are available")

    print(f"{'='*70}\n")

if __name__ == "__main__":
    # Run the test
    test_concurrent_booking(num_users=5)
