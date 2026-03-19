import requests
import os
import time

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
CHECK_TIMEOUT = 5

# Bangladeshi proxy on port 8080
PROXY = "http://103.239.253.66:8080"
proxies = {
    'http': PROXY,
    'https': PROXY
}

def verify_ip():
    """Verify we're using the Bangladeshi proxy."""
    try:
        # Test IP through proxy
        response = requests.get(
            'https://api.ipify.org', 
            proxies=proxies, 
            timeout=10
        )
        ip = response.text
        
        # Get location
        loc_response = requests.get(
            f'http://ip-api.com/json/{ip}',
            timeout=5
        )
        loc_data = loc_response.json()
        
        print("="*70)
        print("🔍 PROXY VERIFICATION")
        print("="*70)
        print(f"🌍 Proxy: {PROXY}")
        print(f"📡 IP through proxy: {ip}")
        print(f"📍 Country: {loc_data.get('country', 'Unknown')}")
        print(f"🏙️  City: {loc_data.get('city', 'Unknown')}")
        print(f"📡 ISP: {loc_data.get('isp', 'Unknown')}")
        
        if loc_data.get('country') == 'Bangladesh':
            print("✅ Using Bangladeshi IP - FILTERING WILL BE ACCURATE")
            return True
        else:
            print("⚠️ WARNING: Not using Bangladeshi IP!")
            return False
            
    except Exception as e:
        print(f"❌ Proxy verification failed: {e}")
        print("⚠️ Running without proxy verification")
        return False

def is_stream_available(url):
    """Check if stream is available through proxy."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.google.com/',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        # Use proxy for the request
        response = requests.head(
            url, 
            timeout=CHECK_TIMEOUT, 
            headers=headers, 
            allow_redirects=True,
            proxies=proxies
        )

        # Filter 403 and 504
        if response.status_code == 403:
            return False, "403"
        if response.status_code == 504:
            return False, "504"
            
        return True, str(response.status_code)

    except requests.exceptions.ProxyError as e:
        print(f"🔄 Proxy error for: {url[:50]}... - {str(e)[:50]}")
        return True, "proxy_error"  # Keep on proxy error
    except requests.exceptions.Timeout:
        return True, "timeout"
    except requests.exceptions.ConnectionError:
        return True, "connection_error"
    except Exception as e:
        return True, "error"

def merge_playlists():
    entries = []
    skipped_count = 0
    forbidden_count = 0
    gateway_count = 0
    kept_count = 0
    total_checked = 0

    print("\n" + "="*70)
    print("🚀 IPTV MERGER WITH BANGLADESHI PROXY (103.239.253.66:8080)")
    print("="*70)
    
    # Verify proxy
    proxy_working = verify_ip()
    
    if not proxy_working:
        print("\n⚠️ Continuing without proxy verification...")
    
    print("="*70)

    # Read source URLs
    try:
        with open(SOURCE_FILE, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"📋 Found {len(urls)} playlist sources")
    except FileNotFoundError:
        print(f"❌ {SOURCE_FILE} not found!")
        return

    # Process each playlist
    for playlist_url in urls:
        try:
            print(f"\n📡 Fetching playlist: {playlist_url}")
            # Use proxy for playlist fetch too
            response = requests.get(
                playlist_url, 
                timeout=30,
                proxies=proxies
            )
            lines = response.text.splitlines()
            print(f"   ✅ Playlist fetched, processing streams...")

            i = 0
            while i < len(lines) - 1:
                if lines[i].startswith("#EXTINF"):
                    channel_name_line = lines[i]
                    stream_url = lines[i+1]
                    total_checked += 1

                    # Skip PlayZ sponsored
                    if "Welcome to PlayZ TV" in channel_name_line and "playztv.pages.dev/promo" in stream_url:
                        skipped_count += 1
                        i += 2
                        continue

                    # Check stream
                    available, status = is_stream_available(stream_url)
                    
                    if available:
                        entries.append(channel_name_line)
                        entries.append(stream_url)
                        kept_count += 1
                    else:
                        if status == "403":
                            forbidden_count += 1
                        elif status == "504":
                            gateway_count += 1

                    # Show progress every 50 streams
                    if total_checked % 50 == 0:
                        print(f"📊 Progress: Checked {total_checked} streams...")

                    i += 2
                else:
                    i += 1

            print(f"   ✅ Finished playlist: {playlist_url}")

        except Exception as e:
            print(f"❌ Error processing playlist {playlist_url}: {e}")

    # Write final playlist
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in entries:
            f.write(entry + "\n")

    # Print summary
    print("\n" + "="*70)
    print("✅ MERGE COMPLETED!")
    print("="*70)
    print(f"📺 Total channels kept: {kept_count}")
    print(f"🚫 403 Forbidden removed: {forbidden_count}")
    print(f"🌐 504 Gateway Timeout removed: {gateway_count}")
    print(f"⏭️ PlayZ sponsored removed: {skipped_count}")
    print(f"📊 Total streams checked: {total_checked}")
    print(f"📊 Final playlist entries: {len(entries)//2}")
    print("="*70)
    print(f"🔌 Proxy used: {PROXY}")
    print("="*70)
    print(f"📁 Output saved to: {OUTPUT_FILE}")
    print("="*70)

if __name__ == "__main__":
    merge_playlists()
