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

            for i in range(len(lines)-1):
                if lines[i].startswith("#EXTINF"):
                    # Skip if this is the Welcome to PlayZ TV entry
                    if "Welcome to PlayZ TV" in lines[i] and "playztv.pages.dev/promo" in lines[i+1]:
                        print("Skipping PlayZ TV promo entry")
                        continue
                    
                    entries.append(lines[i])
                    entries.append(lines[i+1])

        except Exception as e:
            print(f"Error with {url}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in entries:
            f.write(entry + "\n")

    print(f"Merge completed! Total entries: {len(entries)//2}")

if __name__ == "__main__":
    merge_playlists()
