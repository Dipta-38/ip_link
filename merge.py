import requests
from urllib.parse import urlparse

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
CHANNEL_TIMEOUT = 7  # Timeout for checking if channel is alive
SKIP_KEYWORDS = ["Welcome to PlayZ TV"]  # Add more keywords to skip if needed

def is_channel_alive(url, timeout=CHANNEL_TIMEOUT):
    """Check if a channel URL is responding"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except requests.Timeout:
        print(f"    ✗ Timeout")
        return False
    except requests.ConnectionError:
        print(f"    ✗ Connection error")
        return False
    except Exception as e:
        print(f"    ✗ Error: {str(e)[:50]}")
        return False

def should_skip_channel(extinf_line):
    """Check if channel should be skipped based on keywords"""
    for keyword in SKIP_KEYWORDS:
        if keyword.lower() in extinf_line.lower():
            return True
    return False

def merge_playlists():
    entries = []
    checked_count = 0
    alive_count = 0
    dead_count = 0
    skipped_count = 0

    with open(SOURCE_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Found {len(urls)} source(s)\n")

    for source_url in urls:
        try:
            print(f"Fetching {source_url}")
            response = requests.get(source_url, timeout=15)
            text = response.text
            lines = text.splitlines()

            for i in range(len(lines)-1):
                if lines[i].startswith("#EXTINF"):
                    extinf_line = lines[i]
                    channel_url = lines[i+1].strip()
                    
                    # Extract channel name for display
                    channel_name = extinf_line.split(",")[-1] if "," in extinf_line else extinf_line
                    
                    # Skip if contains blocked keywords
                    if should_skip_channel(extinf_line):
                        print(f"  ⊘ Skipped (blocked): {channel_name[:60]}")
                        skipped_count += 1
                        continue
                    
                    # Check if channel is alive
                    checked_count += 1
                    print(f"  Checking: {channel_name[:60]}", end=" ")
                    
                    if is_channel_alive(channel_url):
                        print("✓")
                        entries.append(extinf_line)
                        entries.append(channel_url)
                        alive_count += 1
                    else:
                        dead_count += 1

        except requests.Timeout:
            print(f"  ✗ Source timeout: {source_url}")
        except Exception as e:
            print(f"  ✗ Error fetching {source_url}: {e}")

    # Write output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in entries:
            f.write(entry + "\n")

    # Print summary
    print("\n" + "="*60)
    print("MERGE COMPLETED!")
    print("="*60)
    print(f"Channels checked:     {checked_count}")
    print(f"Channels alive:       {alive_count} ✓")
    print(f"Channels dead:        {dead_count} ✗")
    print(f"Channels skipped:     {skipped_count} ⊘")
    print(f"Total in output:      {alive_count}")
    print(f"Output file:          {OUTPUT_FILE}")
    print("="*60)

if __name__ == "__main__":
    merge_playlists()
