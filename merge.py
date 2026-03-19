import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"

# OPTIMIZED SETTINGS FOR 4000 STREAMS WITH 5 SECOND TIMEOUT
CHECK_TIMEOUT = 5           # 5 seconds - best balance for reliability
MAX_WORKERS = 50            # Check 50 streams simultaneously
STREAM_CHECK_ENABLED = True
VERBOSE_LOGGING = False     # Keep False to avoid console spam
BATCH_SIZE = 200            # Process in batches to manage memory

# Thread-safe counters
entries = []
entries_lock = threading.Lock()
skipped_count = 0
forbidden_count = 0
kept_count = 0
stats_lock = threading.Lock()
start_time = time.time()

def print_progress(current, total, playlist_name=""):
    """Show progress bar."""
    percentage = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current // total)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    elapsed = time.time() - start_time
    streams_per_second = current / elapsed if elapsed > 0 else 0
    eta = (total - current) / streams_per_second if streams_per_second > 0 else 0
    
    print(f"\r📊 Progress: |{bar}| {current}/{total} ({percentage:.1f}%) | {streams_per_second:.1f} streams/s | ETA: {eta:.0f}s", end='')

def is_stream_available(url):
    """Quick check for 403 errors only with 5 second timeout."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.google.com/',
            'Connection': 'close'
        }
        
        # Quick HEAD request with 5 second timeout
        response = requests.head(
            url, 
            timeout=CHECK_TIMEOUT, 
            headers=headers, 
            allow_redirects=True,
            stream=False
        )
        
        # Only filter 403
        if response.status_code == 403:
            return False, "403"
        return True, str(response.status_code)
        
    except requests.exceptions.Timeout:
        return True, f"timeout>{CHECK_TIMEOUT}s"  # Keep timeouts
    except requests.exceptions.ConnectionError:
        return True, "connection_error"  # Keep connection errors
    except Exception:
        return True, "other_error"  # Keep all other errors

def process_stream(channel_line, stream_url):
    """Process a single stream entry."""
    global skipped_count, forbidden_count, kept_count
    
    # Skip PlayZ sponsored
    if "Welcome to PlayZ TV" in channel_line and "playztv.pages.dev/promo" in stream_url:
        with stats_lock:
            skipped_count += 1
        return None
    
    # Check stream if enabled
    if STREAM_CHECK_ENABLED:
        available, status = is_stream_available(stream_url)
        if not available:  # Only 403 Forbidden
            with stats_lock:
                forbidden_count += 1
            if VERBOSE_LOGGING:
                print(f"\n🚫 403: {stream_url[:50]}...")
            return None
        elif VERBOSE_LOGGING and status != "200":
            print(f"\n  ⚠️ {status}: {stream_url[:50]}...")
    
    with stats_lock:
        kept_count += 1
    
    return (channel_line, stream_url)

def process_playlist(playlist_url):
    """Fetch and parse a playlist."""
    local_entries = []
    
    try:
        print(f"\n📡 Fetching: {playlist_url}")
        response = requests.get(playlist_url, timeout=30)
        lines = response.text.splitlines()
        
        # Collect all stream pairs
        stream_pairs = []
        i = 0
        while i < len(lines) - 1:
            if lines[i].startswith("#EXTINF"):
                stream_pairs.append((lines[i], lines[i+1]))
                i += 2
            else:
                i += 1
        
        total_streams = len(stream_pairs)
        print(f"   Found {total_streams} streams to check")
        
        # Process in batches to show progress
        for batch_start in range(0, total_streams, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, total_streams)
            batch = stream_pairs[batch_start:batch_end]
            
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [executor.submit(process_stream, ch, url) for ch, url in batch]
                
                for i, future in enumerate(as_completed(futures)):
                    result = future.result()
                    if result:
                        local_entries.append(result[0])
                        local_entries.append(result[1])
                    
                    # Show progress
                    current = batch_start + i + 1
                    print_progress(current, total_streams, playlist_url)
        
        print()  # New line after progress
        
    except Exception as e:
        print(f"\n❌ Error with {playlist_url}: {e}")
    
    return local_entries

def merge_playlists():
    global start_time
    start_time = time.time()
    
    print("\n" + "="*70)
    print("🚀 OPTIMIZED FOR 4000 STREAMS (5 SECOND TIMEOUT)")
    print("="*70)
    print(f"⚙️ Configuration:")
    print(f"  ⏱️  Timeout: {CHECK_TIMEOUT}s per stream - BEST BALANCE")
    print(f"  🔄 Parallel workers: {MAX_WORKERS}")
    print(f"  📦 Batch size: {BATCH_SIZE}")
    print(f"  🔍 Stream checking: {'ENABLED' if STREAM_CHECK_ENABLED else 'DISABLED'}")
    print("="*70)

    # Read source URLs
    with open(SOURCE_FILE, "r") as f:
        playlist_urls = [line.strip() for line in f if line.strip()]
    
    print(f"\n📋 Found {len(playlist_urls)} playlist sources")
    print("="*70)

    # Process each playlist
    all_entries = []
    for playlist_url in playlist_urls:
        playlist_entries = process_playlist(playlist_url)
        all_entries.extend(playlist_entries)

    # Write final playlist
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in all_entries:
            f.write(entry + "\n")

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    # Print summary
    print("\n" + "="*70)
    print("✅ MERGE COMPLETED!")
    print("="*70)
    print(f"📺 Total channels kept: {kept_count}")
    print(f"🚫 403 Forbidden removed: {forbidden_count}")
    print(f"⏭️ PlayZ sponsored removed: {skipped_count}")
    print(f"📊 Final playlist entries: {len(all_entries)//2}")
    print("="*70)
    print(f"⏱️  Total time: {minutes}m {seconds}s")
    print(f"⚡ Average speed: {kept_count/elapsed_time:.1f} streams/second")
    print("="*70)
    print(f"📁 Output: {OUTPUT_FILE}")
    print("="*70)

if __name__ == "__main__":
    merge_playlists()
