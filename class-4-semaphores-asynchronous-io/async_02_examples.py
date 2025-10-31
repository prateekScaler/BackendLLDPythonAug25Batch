"""
Async I/O - Practical Examples
When async shines vs threads
"""
import asyncio
import time
from threading import Thread
import aiohttp  # pip install aiohttp (for demo purposes)

# ============================================================
# Example 1: Fetching Multiple URLs
# ============================================================

print("=" * 60)
print("Example 1: Fetching 10 URLs")
print("=" * 60)

# With threads
def fetch_url_thread(url_id):
    time.sleep(0.5)  # Simulate network delay
    return f"Data from URL {url_id}"

def fetch_all_threads():
    print("\nUSING THREADS:")
    start = time.time()
    
    threads = []
    for i in range(10):
        t = Thread(target=fetch_url_thread, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Time: {time.time() - start:.2f}s")
    print("✓ Works, but 10 threads created")

# With async
async def fetch_url_async(url_id):
    await asyncio.sleep(0.5)  # Simulate network delay
    return f"Data from URL {url_id}"

async def fetch_all_async():
    print("\nUSING ASYNC:")
    start = time.time()
    
    tasks = [fetch_url_async(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    
    print(f"Time: {time.time() - start:.2f}s")
    print("✓ Same speed, SINGLE thread!")

# ============================================================
# Example 2: Chat Server (Async Advantage)
# ============================================================

print("\n" + "=" * 60)
print("Example 2: Chat Server Scenario")
print("=" * 60)

async def handle_client(client_id):
    """Each client connection"""
    print(f"Client {client_id} connected")
    
    # Wait for messages (I/O operation)
    for i in range(3):
        await asyncio.sleep(0.5)  # Waiting for message
        print(f"Client {client_id}: Message {i}")
    
    print(f"Client {client_id} disconnected")

async def chat_server():
    print("\nSimulating 5 concurrent chat clients:")
    
    # Handle 5 clients concurrently on single thread!
    clients = [handle_client(i) for i in range(5)]
    await asyncio.gather(*clients)
    
    print("\n✓ Handled 5 clients on SINGLE thread!")
    print("With threads: Would need 5 threads")
    print("With async: Can handle 10,000+ clients on 1 thread!")

# ============================================================
# Example 3: Database Queries (When Async Shines)
# ============================================================

print("\n" + "=" * 60)
print("Example 3: Multiple Database Queries")
print("=" * 60)

async def query_database(query_id):
    """Simulate async database query"""
    print(f"  Query {query_id}: Executing...")
    await asyncio.sleep(0.3)  # Simulates query time
    print(f"  Query {query_id}: Done")
    return f"Result {query_id}"

async def run_queries():
    print("\nRunning 20 database queries concurrently:")
    
    start = time.time()
    
    # Run 20 queries concurrently
    queries = [query_database(i) for i in range(20)]
    results = await asyncio.gather(*queries)
    
    elapsed = time.time() - start
    
    print(f"\n✓ 20 queries in {elapsed:.2f}s on SINGLE thread!")
    print(f"Sequential would take: {20 * 0.3:.1f}s")
    print(f"Speedup: {(20 * 0.3) / elapsed:.1f}x")

# ============================================================
# Example 4: File I/O (Async advantage)
# ============================================================

print("\n" + "=" * 60)
print("Example 4: Processing Multiple Files")
print("=" * 60)

async def process_file(file_id):
    """Simulate async file processing"""
    print(f"  File {file_id}: Reading...")
    await asyncio.sleep(0.2)  # Simulate file I/O
    
    print(f"  File {file_id}: Processing...")
    await asyncio.sleep(0.1)
    
    print(f"  File {file_id}: Done")
    return f"Processed {file_id}"

async def process_files():
    print("\nProcessing 15 files concurrently:")
    
    start = time.time()
    
    files = [process_file(i) for i in range(15)]
    results = await asyncio.gather(*files)
    
    elapsed = time.time() - start
    
    print(f"\n✓ 15 files in {elapsed:.2f}s")
    print("Single thread handled all file I/O!")

# ============================================================
# When Async DOESN'T Help
# ============================================================

print("\n" + "=" * 60)
print("When Async DOESN'T Help:")
print("=" * 60)

print("""
❌ CPU-bound tasks:
   async def compute():
       result = sum(range(10_000_000))  # CPU work
       # No 'await' = blocks event loop!

❌ Blocking libraries:
   with open('file.txt') as f:  # Blocking I/O
       data = f.read()  # Blocks entire event loop!
   
   # Should use: aiofiles library

❌ Simple scripts:
   If you only have 2-3 I/O operations,
   threads are simpler!

✓ Use threads/processes for CPU-bound
✓ Use async for I/O-bound high-concurrency
""")

# ============================================================
# Quick Decision Matrix
# ============================================================

print("\n" + "=" * 60)
print("DECISION MATRIX:")
print("=" * 60)

print("""
┌────────────────────┬──────────┬──────────┬──────────┐
│ Scenario           │ Threads  │ Async    │ Processes│
├────────────────────┼──────────┼──────────┼──────────┤
│ 10 HTTP requests   │ ✓ Good   │ ✓✓ Best  │ ✗ Overkill│
│ 10,000 requests    │ ✗ Too many│✓✓ Best  │ ✗ Too many│
│ CPU + I/O mixed    │ ✓✓ Best  │ ✗ Blocks │ ✓ Good   │
│ Pure CPU work      │ ✗ No help│ ✗ Blocks │ ✓✓ Best  │
│ Simple script      │ ✓✓ Best  │ ✗ Complex│ ✗ Overkill│
│ Web server (1000s) │ ✗ Memory │ ✓✓ Best  │ ✗ Memory │
└────────────────────┴──────────┴──────────┴──────────┘
""")

# Run all examples
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RUNNING DEMOS:")
    print("=" * 60)
    
    fetch_all_threads()
    asyncio.run(fetch_all_async())
    
    asyncio.run(chat_server())
    asyncio.run(run_queries())
    asyncio.run(process_files())
    
    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("=" * 60)
    print("1. Async = Single thread, many tasks")
    print("2. Perfect for I/O-heavy, high-concurrency")
    print("3. Use 'await' at I/O points to yield control")
    print("4. Event loop switches between tasks efficiently")
    print("5. Can handle 10,000+ concurrent operations!")
    print("=" * 60)
