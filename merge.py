import requests
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
CHECK_TIMEOUT = 5
MAX_WORKERS = 20   # adjust for speed vs. system load

def get_ip_info():
    """Get local IP info to confirm environment (Bangladeshi ISP if run locally)."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return f"Local IP: {local_ip} (Filtering depends on this environment)"
    except:
        return "Could not determine local IP"

def is_stream_available(url):
    """Check if stream is available, only filtering out 403 errors."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.google.com/',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        response = requests.head(url, timeout=CHECK_TIMEOUT, headers=headers, allow_redirects=True)

        if response.status_code == 403:
            print(f"🚫 Filtering out 403 Forbidden: {url}")
            return False

        if response.status_code != 200:
            print(f"⚠️ Keeping non-200 (HTTP {response.status_code}) stream: {url}")

        return True

    except requests.exceptions.Timeout:
        print(f"⏱️ Timeout but KEEPING (may work in player): {url}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"🔌 Connection error but KEEPING (may work in player): {url}")
        return True
    except Exception as e:
        print(f"⚠️ Error but KEEPING stream: {url} - {e}")
        return True

def process_playlist(playlist_url):
    """Fetch and process a single playlist, return entries and counts."""
    entries = []
    skipped_count = 0
    forbidden_count = 0
    kept_count = 0

    try:
        print(f"\n📡 Fetching playlist: {playlist_url}")
        text = requests.get(playlist_url, timeout=15).text
        lines = text.splitlines()

        i = 0
        while i < len(lines) - 1:
            if lines[i].startswith("#EXTINF"):
                channel_name_line = lines[i]
                stream_url = lines[i+1]

                if "Welcome to PlayZ TV" in channel_name_line and "playztv.pages.dev/promo" in stream_url:
                    print(f"⏭️ Removing PlayZ sponsored entry")
                    skipped_count += 1
                    i += 2
                    continue

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

    return entries, skipped_count, forbidden_count, kept_count

def merge_playlists():
    all_entries = []
    total_skipped = 0
    total_forbidden = 0
    total_kept = 0

    with open(SOURCE_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    # Run playlists in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_playlist, url): url for url in urls}
        for future in as_completed(futures):
            entries, skipped, forbidden, kept = future.result()
            all_entries.extend(entries)
            total_skipped += skipped
            total_forbidden += forbidden
            total_kept += kept

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in all_entries:
            f.write(entry + "\n")

    print("\n" + "="*60)
    print("✅ MERGE COMPLETED!")
    print("="*60)
    print(f"📺 Total channels kept: {total_kept}")
    print(f"🚫 403 Forbidden channels removed: {total_forbidden}")
    print(f"⏭️ PlayZ sponsored entries removed: {total_skipped}")
    print(f"📊 Total entries in final playlist: {len(all_entries)//2}")
    print("="*60)
    print(f"📁 Output saved to: {OUTPUT_FILE}")
    print("\n📝 Note: Only 403 Forbidden errors were filtered.")
    print("   All other channels (timeouts, connection errors, etc.) were KEPT.")
    print("="*60)
    print(get_ip_info())
    print("⚠️ Reminder: Run this script on your Bangladeshi ISP for correct filtering.")
    print("="*60)

if __name__ == "__main__":
    merge_playlists()
