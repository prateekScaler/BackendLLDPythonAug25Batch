"""
BONUS: Real-World Example - Image Processing Pipeline
Shows when to use ThreadPool vs ProcessPool in same application
"""
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import random

# Simulate image operations
def download_image(image_id):
    """I/O-bound: Download image from server"""
    print(f"📥 Downloading image {image_id}...")
    time.sleep(1)  # Simulates network delay
    print(f"✓ Image {image_id} downloaded")
    return f"image_{image_id}_data"

def process_image(image_data):
    """CPU-bound: Apply filters, resize, etc."""
    image_id = image_data.split("_")[1]
    print(f"🎨 Processing {image_data}...")
    
    # Simulate CPU-intensive work
    total = 0
    for i in range(5_000_000):
        total += i * i
    
    print(f"✓ {image_data} processed")
    return f"{image_data}_processed"

def upload_image(processed_data):
    """I/O-bound: Upload processed image"""
    image_id = processed_data.split("_")[1]
    print(f"📤 Uploading {processed_data}...")
    time.sleep(1)  # Simulates network delay
    print(f"✓ {processed_data} uploaded")
    return f"{processed_data}_uploaded"

# ============================================================
# APPROACH 1: Sequential (Baseline)
# ============================================================
def sequential_pipeline(num_images):
    """Process images one by one"""
    print("\n" + "=" * 60)
    print("SEQUENTIAL APPROACH")
    print("=" * 60)
    
    start = time.time()
    
    for i in range(1, num_images + 1):
        # Download
        image_data = download_image(i)
        # Process
        processed = process_image(image_data)
        # Upload
        upload_image(processed)
    
    elapsed = time.time() - start
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    return elapsed

# ============================================================
# APPROACH 2: Mixed Executors (Optimal)
# ============================================================
def optimized_pipeline(num_images):
    """Use ThreadPool for I/O, ProcessPool for CPU"""
    print("\n" + "=" * 60)
    print("OPTIMIZED APPROACH (Mixed Executors)")
    print("=" * 60)
    
    start = time.time()
    
    # Step 1: Download all images (I/O-bound → ThreadPool)
    print("\n[STEP 1: Downloading with ThreadPool]")
    with ThreadPoolExecutor(max_workers=5) as executor:
        image_ids = range(1, num_images + 1)
        downloaded = list(executor.map(download_image, image_ids))
    
    # Step 2: Process all images (CPU-bound → ProcessPool)
    print("\n[STEP 2: Processing with ProcessPool]")
    with ProcessPoolExecutor(max_workers=4) as executor:
        processed = list(executor.map(process_image, downloaded))
    
    # Step 3: Upload all images (I/O-bound → ThreadPool)
    print("\n[STEP 3: Uploading with ThreadPool]")
    with ThreadPoolExecutor(max_workers=5) as executor:
        uploaded = list(executor.map(upload_image, processed))
    
    elapsed = time.time() - start
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    return elapsed

# ============================================================
# APPROACH 3: Wrong Choice (ThreadPool for CPU)
# ============================================================
def wrong_approach(num_images):
    """Using ThreadPool for everything (BAD for CPU tasks)"""
    print("\n" + "=" * 60)
    print("WRONG APPROACH (ThreadPool for CPU tasks)")
    print("=" * 60)
    
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Download
        print("\n[STEP 1: Downloading]")
        image_ids = range(1, num_images + 1)
        downloaded = list(executor.map(download_image, image_ids))
        
        # Process (WRONG: using threads for CPU task!)
        print("\n[STEP 2: Processing - Using ThreadPool ❌]")
        processed = list(executor.map(process_image, downloaded))
        
        # Upload
        print("\n[STEP 3: Uploading]")
        uploaded = list(executor.map(upload_image, processed))
    
    elapsed = time.time() - start
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    return elapsed

if __name__ == "__main__":
    NUM_IMAGES = 4
    
    print("=" * 60)
    print("IMAGE PROCESSING PIPELINE COMPARISON")
    print("=" * 60)
    print(f"Processing {NUM_IMAGES} images")
    
    # Run all approaches
    seq_time = sequential_pipeline(NUM_IMAGES)
    opt_time = optimized_pipeline(NUM_IMAGES)
    wrong_time = wrong_approach(NUM_IMAGES)
    
    # Final comparison
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    print(f"Sequential:         {seq_time:.2f}s (baseline)")
    print(f"Optimized (mixed):  {opt_time:.2f}s ({seq_time/opt_time:.2f}x faster)")
    print(f"Wrong (all thread): {wrong_time:.2f}s ({seq_time/wrong_time:.2f}x faster)")
    
    print("\n" + "=" * 60)
    print("KEY LESSONS:")
    print("=" * 60)
    print("1. Use ThreadPool for I/O operations (download/upload)")
    print("2. Use ProcessPool for CPU operations (image processing)")
    print("3. Mixing executors appropriately gives BEST results")
    print("4. Using wrong executor (threads for CPU) limits speedup")
    print("\n📌 REMEMBER: Match the executor to the task type!")
