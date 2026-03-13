import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import re

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
TIMEOUT = 8
MAX_WORKERS = 25
MAX_RETRIES = 2

# Keywords to skip (customize this list)
SKIP_PATTERNS = [
    r"Welcome to PlayZ TV",  # Skip specific channel
    r"Sponsored",            # Skip anything with "Sponsored" in title
    r"promo/intro",          # Skip promo videos
    r"\./intro",             # Skip intro paths
    r"testpattern",          # Skip test patterns
    # Add more patterns as needed
]

# Specific URLs to skip (exact matches or partial)
SKIP_URLS = [
    "https://playztv.pages.dev/promo/intro-2.mp4",
    # Add more URLs to skip
]

def should_skip_entry(extinf_line, url):
    """Check if an entry should be skipped based on patterns"""
    
    # Check if URL is in skip list
    if url in SKIP_URLS:
        return True
    
    # Check for skip patterns in EXTINF line
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, extinf_line, re.IGNORECASE):
            return True
    
    # Skip entries with very long URLs (often ads or trackers)
    if len(url) > 300:
        return True
    
    # Skip entries with suspicious keywords in URL
    suspicious_url_keywords = ['promo', 'advert', 'sponsor', 'intro', 'welcome']
    url_lower = url.lower()
    for keyword in suspicious_url_keywords:
        if keyword in url_lower and len(url_lower) < 100:  # Short promo URLs
            return True
    
    return False

def create_session():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    retry = Retry(
        total=MAX_RETRIES,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def check_stream(url):
    """Check if a stream URL is accessible"""
    try:
        session = create_session()
        response = session.head(url, timeout=TIMEOUT, allow_redirects=True)
        
        if response.status_code >= 400:
            response = session.get(url, timeout=TIMEOUT, stream=True)
            next(response.iter_content(chunk_size=1))
            response.close()
        
        return response.status_code < 400
    except:
        return False

def process_playlist(url, progress_callback=None):
    """Fetch and parse a single playlist, return entries with working streams"""
    working_entries = []
    entries_to_check = []
    skipped_count = 0
    
    try:
        session = create_session()
        print(f"📡 Fetching {url}")
        response = session.get(url, timeout=20)
        response.raise_for_status()
        text = response.text
        
        lines = text.splitlines()
        
        # Parse playlist entries
        for i in range(len(lines)-1):
            if lines[i].startswith("#EXTINF"):
                extinf_line = lines[i]
                stream_url = lines[i+1].strip()
                
                # Check if this entry should be skipped
                if should_skip_entry(extinf_line, stream_url):
                    skipped_count += 1
                    if skipped_count <= 5:  # Show first 5 skipped entries
                        channel_name = extinf_line.split(',')[-1].strip() if ',' in extinf_line else "Unknown"
                        print(f"  ⏭️ Skipped: {channel_name[:50]}...")
                    continue
                
                entries_to_check.append({
                    'extinf': extinf_line,
                    'url': stream_url
                })
        
        total_streams = len(entries_to_check)
        print(f"  Found {total_streams} streams to check ({skipped_count} skipped)")
        
        if total_streams == 0:
            return []
        
        # Check streams concurrently
        working_count = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_entry = {executor.submit(check_stream, entry['url']): entry 
                              for entry in entries_to_check}
            
            completed = 0
            dead_shown = 0
            for future in as_completed(future_to_entry):
                completed += 1
                entry = future_to_entry[future]
                
                if future.result():
                    working_entries.append(entry['extinf'])
                    working_entries.append(entry['url'])
                    working_count += 1
                else:
                    # Show only first few dead streams to avoid clutter
                    if dead_shown < 10:
                        channel_name = entry['extinf'].split(',')[-1].strip() if ',' in entry['extinf'] else "Unknown"
                        print(f"  ✗ Dead: {channel_name[:50]}...")
                        dead_shown += 1
                
                # Show progress every 20 streams
                if completed % 20 == 0:
                    print(f"  Progress: {completed}/{total_streams} checked")
        
        print(f"  ✅ {working_count}/{total_streams} working streams")
        
    except Exception as e:
        print(f"  ❌ Error processing {url}: {e}")
    
    return working_entries

def merge_playlists():
    all_entries = []
    total_checked = 0
    total_working = 0
    total_skipped = 0
    start_time = time.time()
    
    # Read source URLs
    try:
        with open(SOURCE_FILE, "r") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"❌ Error: {SOURCE_FILE} not found!")
        return
    
    print("=" * 60)
    print(f"🔍 IPTV Playlist Merger with Dead Channel Removal")
    print(f"📋 Found {len(urls)} playlist sources")
    print(f"🚫 Skip patterns: {len(SKIP_PATTERNS)} patterns, {len(SKIP_URLS)} specific URLs")
    print("=" * 60)
    
    # Process each playlist
    for idx, url in enumerate(urls, 1):
        print(f"\n[{idx}/{len(urls)}] Processing source")
        entries = process_playlist(url)
        all_entries.extend(entries)
        
        streams_in_playlist = len(entries) // 2
        total_checked += streams_in_playlist
        total_working += streams_in_playlist
        
        print(f"  Running total: {total_working} working streams so far")
    
    # Write merged playlist
    elapsed_time = time.time() - start_time
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Merged playlist generated by IPTV Merger\n")
        f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Sources: {len(urls)}\n")
        f.write(f"# Working streams: {total_working}\n")
        f.write(f"# Dead streams removed: {total_checked - total_working}\n")
        f.write(f"# Filtered entries (sponsored/promo): {total_skipped}\n")
        f.write(f"# Scan time: {elapsed_time:.1f} seconds\n\n")
        
        for entry in all_entries:
            f.write(entry + "\n")
    
    print("\n" + "=" * 60)
    print(f"✅ MERGE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"📊 FINAL STATISTICS:")
    print(f"   • Total streams checked: {total_checked}")
    print(f"   • Working streams kept: {total_working}")
    print(f"   • Dead streams removed: {total_checked - total_working}")
    print(f"   • Filtered entries: {total_skipped}")
    print(f"   • Success rate: {(total_working/total_checked*100):.1f}%")
    print(f"   • Time taken: {elapsed_time:.1f} seconds")
    print(f"📁 Output file: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    merge_playlists()
