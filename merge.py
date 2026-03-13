import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
TIMEOUT = 8  # Seconds to wait for response
MAX_WORKERS = 30

# Simple headers that mimic VLC or IPTV player
PLAYER_HEADERS = {
    'User-Agent': 'VLC/3.0.18 LibVLC/3.0.18',
    'Accept': '*/*'
}

# Skip patterns
SKIP_PATTERNS = [
    "Welcome to PlayZ TV",
    "Sponsored",
    "promo/intro",
]

def stream_responds(url):
    """Simple check: does the stream URL respond like in VLC?"""
    try:
        # Just like VLC, we try to connect and see if we get any response
        response = requests.get(
            url, 
            headers=PLAYER_HEADERS,
            timeout=TIMEOUT,
            stream=True  # Don't download full content
        )
        
        # Read just the first few bytes to confirm connection works
        next(response.iter_content(chunk_size=1))
        response.close()
        
        # Any 2xx response means it's working
        return response.status_code < 400
        
    except Exception:
        return False

def should_skip(extinf_line):
    """Check if channel should be skipped"""
    for pattern in SKIP_PATTERNS:
        if pattern.lower() in extinf_line.lower():
            return True
    return False

def process_playlist(url):
    """Process a single playlist file"""
    working_entries = []
    entries_to_check = []
    
    try:
        print(f"📡 Fetching: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        lines = response.text.splitlines()
        
        # Collect all entries
        for i in range(len(lines)-1):
            if lines[i].startswith("#EXTINF"):
                if not should_skip(lines[i]):  # Skip unwanted channels
                    entries_to_check.append({
                        'info': lines[i],
                        'url': lines[i+1].strip()
                    })
        
        print(f"   Found {len(entries_to_check)} channels")
        
        # Check which ones respond
        working_count = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_entry = {
                executor.submit(stream_responds, entry['url']): entry 
                for entry in entries_to_check
            }
            
            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]
                if future.result():
                    working_entries.append(entry['info'])
                    working_entries.append(entry['url'])
                    working_count += 1
        
        print(f"   ✅ {working_count} working channels")
        return working_entries
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

def main():
    # Read source URLs
    with open(SOURCE_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print("=" * 60)
    print("🎯 IPTV MERGER - Simple Channel Checker")
    print("=" * 60)
    print(f"Sources: {len(urls)}")
    print("=" * 60)
    
    all_channels = []
    total_working = 0
    
    # Process each source
    for i, url in enumerate(urls, 1):
        print(f"\n📁 Source {i}/{len(urls)}")
        channels = process_playlist(url)
        all_channels.extend(channels)
        total_working += len(channels) // 2
    
    # Save results
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        f.write(f"# Merged: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Working channels: {total_working}\n\n")
        
        for line in all_channels:
            f.write(line + '\n')
    
    print("\n" + "=" * 60)
    print("✅ DONE!")
    print(f"Working channels: {total_working}")
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()
