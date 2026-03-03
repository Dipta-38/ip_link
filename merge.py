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
                    entries.append(lines[i])
                    entries.append(lines[i+1])

        except Exception as e:
            print(e)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in entries:
            f.write(entry + "\n")

    print("Merge completed!")

if __name__ == "__main__":
    merge_playlists()
