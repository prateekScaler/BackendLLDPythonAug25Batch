"""
Example 4: ThreadPoolExecutor - submit() and as_completed()
Shows how to handle multiple tasks and process results as they complete
"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(user_id):
    """Simulates fetching user data from API"""
    wait_time = user_id % 3 + 1  # Different wait times
    print(f"Fetching user {user_id}... (will take {wait_time}s)")
    time.sleep(wait_time)
    print(f"User {user_id} data fetched!")
    return {"id": user_id, "name": f"User{user_id}", "wait_time": wait_time}

if __name__ == "__main__":
    print("=" * 60)
    print("Processing results AS THEY COMPLETE (not in order)")
    print("=" * 60)
    
    start = time.time()
    user_ids = [1, 2, 3, 4, 5]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks and store futures
        futures = {executor.submit(fetch_data, uid): uid for uid in user_ids}
        
        print(f"\nSubmitted {len(futures)} tasks to the pool\n")
        
        # Process results as they complete (not in submission order!)
        for future in as_completed(futures):
            user_id = futures[future]
            try:
                result = future.result()
                print(f"✓ Processed: {result}")
            except Exception as e:
                print(f"✗ User {user_id} failed: {e}")
    
    end = time.time()
    print(f"\n{'='*60}")
    print(f"Total time: {end - start:.2f} seconds")
    print("Notice: Results came as they completed, not in order!")
