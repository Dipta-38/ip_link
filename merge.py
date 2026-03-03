import requests

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"

def merge_playlists():
    channels = set()

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        try:
            print(f"Fetching {url}")
            response = requests.get(url, timeout=15)
            text = response.text

            for line in text.splitlines():
                if line and not line.startswith("#"):
                    channels.add(line.strip())

        except Exception as e:
            print(f"Error fetching {url}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in sorted(channels):
            f.write(ch + "\n")

    print("Playlist merged successfully!")

if __name__ == "__main__":
    merge_playlists()