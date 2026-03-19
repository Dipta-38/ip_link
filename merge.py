import requests

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
CHECK_TIMEOUT = 10

def is_stream_available(url):
    """Check if stream is available, only filtering out 403 errors."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.google.com/',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        
        # Try HEAD request first
        response = requests.head(url, timeout=CHECK_TIMEOUT, headers=headers, allow_redirects=True)
        
        # Check specifically for 403 Forbidden
        if response.status_code == 403:
            print(f"🚫 Filtering out 403 Forbidden: {url}")
            return False
        
        # Keep all other responses (including 404, 500, timeouts, etc.)
        # For non-200 responses, we'll still keep them as they might work in some players
        if response.status_code != 200:
            print(f"⚠️ Keeping non-200 (HTTP {response.status_code}) stream: {url}")
        
        return True
        
    except requests.exceptions.Timeout:
        print(f"⏱️ Timeout but KEEPING (may work in player): {url}")
        return True  # Keep timeouts - they might work in actual player
    except requests.exceptions.ConnectionError:
        print(f"🔌 Connection error but KEEPING (may work in player): {url}")
        return True  # Keep connection errors - they might work in actual player
    except Exception as e:
        print(f"⚠️ Error but KEEPING stream: {url} - {e}")
        return True  # Keep all other errors

def merge_playlists():
    entries = []
    skipped_count = 0
    forbidden_count = 0
    kept_count = 0

    with open(SOURCE_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for playlist_url in urls:
        try:
            print(f"\n📡 Fetching playlist: {playlist_url}")
            text = requests.get(playlist_url, timeout=15).text
            lines = text.splitlines()

            i = 0
            while i < len(lines) - 1:
                if lines[i].startswith("#EXTINF"):
                    channel_name_line = lines[i]
                    stream_url = lines[i+1]
                    
                    # Skip the specific PlayZ sponsored entry
                    if "Welcome to PlayZ TV" in channel_name_line and "playztv.pages.dev/promo" in stream_url:
                        print(f"⏭️ Removing PlayZ sponsored entry")
                        skipped_count += 1
                        i += 2
                        continue
                    
                    # Check if stream is available (only filters 403)
                    if is_stream_available(stream_url):
                        entries.append(channel_name_line)
                        entries.append(stream_url)
                        kept_count += 1
                    else:
                        forbidden_count += 1
                    
                    i += 2
                else:
                    i += 1

        except Exception as e:
            print(f"❌ Error processing playlist {playlist_url}: {e}")

    # Write the merged playlist
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in entries:
            f.write(entry + "\n")

    # Print summary
    print("\n" + "="*60)
    print("✅ MERGE COMPLETED!")
    print("="*60)
    print(f"📺 Total channels kept: {kept_count}")
    print(f"🚫 403 Forbidden channels removed: {forbidden_count}")
    print(f"⏭️ PlayZ sponsored entries removed: {skipped_count}")
    print(f"📊 Total entries in final playlist: {len(entries)//2}")
    print("="*60)
    print(f"📁 Output saved to: {OUTPUT_FILE}")
    print("\n📝 Note: Only 403 Forbidden errors were filtered.")
    print("   All other channels (timeouts, connection errors, etc.) were KEPT.")
    print("="*60)

if __name__ == "__main__":
    merge_playlists()
