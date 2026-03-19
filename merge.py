import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
CHECK_TIMEOUT = 6
MAX_WORKERS = 20  # speed (increase if needed)

# OPTIONAL: Use Bangladeshi proxy if not running locally
PROXIES = None
# Example:
# PROXIES = {
#     "http": "http://BD_IP:PORT",
#     "https": "http://BD_IP:PORT"
# }

USER_AGENTS = [
    "VLC/3.0.18 LibVLC/3.0.18",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Lavf/58.20.100",
]


def is_stream_available(url):
    """Check if stream is available (filters only real 403 errors)."""
    
    for ua in USER_AGENTS:
        try:
            headers = {
                "User-Agent": ua,
                "Referer": "http://example.com/",
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Icy-MetaData": "1"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=CHECK_TIMEOUT,
                stream=True,
                allow_redirects=True,
                proxies=PROXIES
            )

            # 🚫 True 403 block
            if response.status_code == 403:
                continue

            # 🚫 Soft block detection (some servers fake 200)
            text_sample = ""
            try:
                text_sample = response.text[:200].lower()
            except:
                pass

            if "forbidden" in text_sample or "access denied" in text_sample:
                continue

            # ✅ Accept everything else
            return True

        except requests.exceptions.Timeout:
            return True  # keep
        except requests.exceptions.ConnectionError:
            return True  # keep
        except Exception:
            return True  # keep

    print(f"🚫 403 Forbidden (BD blocked): {url}")
    return False


def process_playlist(playlist_url):
    entries = []
    skipped = 0
    forbidden = 0
    kept = 0

    try:
        print(f"\n📡 Fetching: {playlist_url}")
        text = requests.get(playlist_url, timeout=15).text
        lines = text.splitlines()

        i = 0
        while i < len(lines) - 1:
            if lines[i].startswith("#EXTINF"):
                info = lines[i]
                stream_url = lines[i + 1]

                # Remove PlayZ promo
                if "Welcome to PlayZ TV" in info and "playztv.pages.dev/promo" in stream_url:
                    print("⏭️ Skipped PlayZ promo")
                    skipped += 1
                    i += 2
                    continue

                if is_stream_available(stream_url):
                    entries.append(info)
                    entries.append(stream_url)
                    kept += 1
                else:
                    forbidden += 1

                i += 2
            else:
                i += 1

    except Exception as e:
        print(f"❌ Error: {playlist_url} -> {e}")

    return entries, skipped, forbidden, kept


def merge_playlists():
    all_entries = []
    total_skipped = 0
    total_forbidden = 0
    total_kept = 0

    with open(SOURCE_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_playlist, url) for url in urls]

        for future in as_completed(futures):
            entries, skipped, forbidden, kept = future.result()
            all_entries.extend(entries)
            total_skipped += skipped
            total_forbidden += forbidden
            total_kept += kept

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for line in all_entries:
            f.write(line + "\n")

    # Summary
    print("\n" + "=" * 60)
    print("✅ MERGE COMPLETED")
    print("=" * 60)
    print(f"📺 Channels kept: {total_kept}")
    print(f"🚫 403 (BD blocked) removed: {total_forbidden}")
    print(f"⏭️ Promo skipped: {total_skipped}")
    print(f"📊 Final entries: {len(all_entries)//2}")
    print(f"📁 Saved to: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    merge_playlists()
