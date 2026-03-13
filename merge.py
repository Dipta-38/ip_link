import requests

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"

def merge_playlists():
    entries = []

    with open(SOURCE_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        try:
            print(f"Fetching {url}")
            text = requests.get(url, timeout=15).text

            lines = text.splitlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith("#EXTINF"):
                    # Check both conditions: matching text AND the specific URL
                    if ("Welcome to PlayZ TV" in lines[i] and 
                        i + 1 < len(lines) and 
                        "playztv.pages.dev" in lines[i + 1]):
                        print(f"  Skipping PlayZ TV entry at line {i}")
                        # Skip this entry and its URL (move ahead by 2 lines)
                        i += 2
                        continue
                    
                    # If not the unwanted entry, add it and its URL
                    entries.append(lines[i])
                    if i + 1 < len(lines):
                        entries.append(lines[i + 1])
                    i += 2
                else:
                    i += 1

        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Remove any potential duplicates while preserving order
    seen = set()
    unique_entries = []
    for entry in entries:
        if entry not in seen:
            seen.add(entry)
            unique_entries.append(entry)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in unique_entries:
            f.write(entry + "\n")

    print(f"✓ Merge completed! Output saved to {OUTPUT_FILE}")
    print(f"  Total entries: {len(unique_entries)}")

if __name__ == "__main__":
    merge_playlists()
