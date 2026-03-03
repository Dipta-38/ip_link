import requests

# IPTV source URLs
urls = [
    "https://github.com/abusaeeidx/Mrgify-BDIX-IPTV/raw/main/playlist.m3u",
    "https://iptv-org.github.io/iptv/countries/bd.m3u",
    "https://iptv-org.github.io/iptv/countries/in.m3u"
]

output_file = "merged.m3u"

channels = set()

for url in urls:
    try:
        text = requests.get(url, timeout=10).text
        lines = text.splitlines()

        for line in lines:
            if line and not line.startswith("#"):
                channels.add(line)

    except:
        pass

with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for ch in channels:
        f.write(ch + "\n")

print("Merged playlist created!")
