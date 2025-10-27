"""
Example 5: ThreadPoolExecutor - map() method
Shows how to use map() for simple parallel operations
"""
import time
from concurrent.futures import ThreadPoolExecutor

def process_order(order_id):
    """Simulates processing an order"""
    print(f"Processing order {order_id}...")
    time.sleep(1)
    return f"Order {order_id} - COMPLETED"

if __name__ == "__main__":
    order_ids = [101, 102, 103, 104, 105]
    
    print("=" * 50)
    print("Using map() method")
    print("=" * 50)
    
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # map() returns results in ORDER (unlike as_completed)
        results = executor.map(process_order, order_ids)
        
        print("\nAll tasks submitted!\n")
        
        # Results come in the same order as input
        for result in results:
            print(f"✓ {result}")
    
    end = time.time()
    print(f"\nTotal time: {end - start:.2f} seconds")
    print("Notice: Results are in ORDER, map() maintains input order!")
