import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
TIMEOUT = 5
MAX_WORKERS = 30

def check_stream(url):
    """Check if a stream URL is accessible"""
    try:
        response = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code >= 400:
            response = requests.get(url, timeout=TIMEOUT, stream=True)
            next(response.iter_content(chunk_size=1))
        return response.status_code < 400
    except:
        return False

def process_playlist_concurrent(url):
    """Fetch and parse a single playlist, return entries with working streams"""
    working_entries = []
    entries_to_check = []
    
    try:
        print(f"Fetching {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        text = response.text
        
        lines = text.splitlines()
        
        for i in range(len(lines)-1):
            if lines[i].startswith("#EXTINF"):
                entries_to_check.append({
                    'extinf': lines[i],
                    'url': lines[i+1].strip()
                })
        
        print(f"  Found {len(entries_to_check)} streams in {url}, checking availability...")
        
        # Check streams concurrently
        working_count = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_entry = {executor.submit(check_stream, entry['url']): entry 
                              for entry in entries_to_check}
            
            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]
                if future.result():
                    working_entries.append(entry['extinf'])
                    working_entries.append(entry['url'])
                    working_count += 1
                else:
                    print(f"  ✗ Dead: {entry['url'][:50]}...")
        
        print(f"  ✓ {working_count} working streams found in {url}")
        
    except Exception as e:
        print(f"Error processing {url}: {e}")
    
    return working_entries

def merge_playlists_concurrent():
    all_entries = []
    total_checked = 0
    total_working = 0
    
    with open(SOURCE_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(urls)} playlist sources")
    print("-" * 50)
    
    for url in urls:
        entries = process_playlist_concurrent(url)
        all_entries.extend(entries)
        
        streams_in_playlist = len(entries) // 2
        total_checked += streams_in_playlist
        total_working += streams_in_playlist
        
        print("-" * 50)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Merged playlist generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total working streams: {total_working}\n")
        f.write(f"# Sources: {len(urls)}\n\n")
        
        for entry in all_entries:
            f.write(entry + "\n")
    
    print(f"\n✅ Merge completed!")
    print(f"📊 Statistics:")
    print(f"   - Total streams checked: {total_checked}")
    print(f"   - Working streams kept: {total_working}")
    print(f"   - Dead streams removed: {total_checked - total_working}")
    print(f"📁 Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_playlists_concurrent()
