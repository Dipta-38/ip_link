import requests
import os

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
CHECK_TIMEOUT = 5

# Bangladeshi proxy on port 80 (HTTP only)
PROXY = "http://103.125.31.222:80"
proxies = {
    'http': PROXY,
    # Don't use for https - it will fail
}

def verify_ip():
    """Verify we're using the Bangladeshi proxy (HTTP only)."""
    try:
        # Use HTTP, not HTTPS for verification
        response = requests.get(
            'http://api.ipify.org',  # Changed to HTTP
            proxies=proxies,
            timeout=10
        )
        ip = response.text
        
        # Get location via HTTP
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
        
        if loc_data.get('country') == 'Bangladesh':
            print("✅ Using Bangladeshi IP - FILTERING WILL BE ACCURATE")
            return True
        else:
            print("⚠️ WARNING: Not using Bangladeshi IP!")
            return False
            
    except Exception as e:
        print(f"❌ Proxy verification failed: {e}")
        return False

def fetch_playlist(url):
    """Fetch playlist using HTTP only."""
    try:
        # Convert HTTPS to HTTP if possible for playlist URLs
        http_url = url.replace('https://', 'http://')
        
        response = requests.get(
            http_url,
            timeout=30,
            proxies=proxies,
            allow_redirects=True
        )
        return response.text
    except Exception as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return None

def check_stream(url):
    """Check stream availability (will work for HTTP streams)."""
    try:
        # For HTTPS streams, we might need to skip proxy
        if url.startswith('https://'):
            # Try without proxy for HTTPS
            response = requests.head(
                url,
                timeout=CHECK_TIMEOUT,
                allow_redirects=True
            )
        else:
            # Use proxy for HTTP
            response = requests.head(
                url,
                timeout=CHECK_TIMEOUT,
                proxies=proxies,
                allow_redirects=True
            )
        
        if response.status_code == 403:
            return False, "403"
        if response.status_code == 504:
            return False, "504"
        return True, str(response.status_code)
        
    except Exception as e:
        print(f"⚠️ Stream check error: {e}")
        return True, "error"  # Keep on error

def merge_playlists():
    entries = []
    skipped_count = 0
    forbidden_count = 0
    gateway_count = 0
    kept_count = 0
    total_checked = 0

    print("\n" + "="*70)
    print("🚀 IPTV MERGER WITH HTTP PROXY (103.125.31.222:80)")
    print("="*70)
    
    # Verify proxy
    proxy_working = verify_ip()
    
    if not proxy_working:
        print("\n⚠️ Proxy not working, will try without proxy for HTTPS")
    
    print("="*70)

    # Read source URLs
    with open(SOURCE_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for playlist_url in urls:
        try:
            print(f"\n📡 Fetching playlist: {playlist_url}")
            
            # Try with proxy first, fallback to direct
            if proxy_working and playlist_url.startswith('http://'):
                text = fetch_playlist(playlist_url)
            else:
                # Direct fetch for HTTPS
                response = requests.get(playlist_url, timeout=30)
                text = response.text
            
            if not text:
                continue
                
            lines = text.splitlines()

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
                    available, status = check_stream(stream_url)
                    
                    if available:
                        entries.append(channel_name_line)
                        entries.append(stream_url)
                        kept_count += 1
                    else:
                        if status == "403":
                            forbidden_count += 1
                        elif status == "504":
                            gateway_count += 1

                    if total_checked % 50 == 0:
                        print(f"📊 Progress: Checked {total_checked} streams...")

                    i += 2
                else:
                    i += 1

        except Exception as e:
            print(f"❌ Error: {playlist_url} - {e}")

    # Write final playlist
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in entries:
            f.write(entry + "\n")

    print("\n" + "="*70)
    print("✅ MERGE COMPLETED!")
    print("="*70)
    print(f"📺 Total channels kept: {kept_count}")
    print(f"🚫 403 Forbidden removed: {forbidden_count}")
    print(f"🌐 504 Gateway Timeout removed: {gateway_count}")
    print(f"⏭️ PlayZ sponsored removed: {skipped_count}")
    print(f"📊 Total streams checked: {total_checked}")
    print("="*70)
    print(f"🔌 Proxy used: {PROXY} (HTTP only)")
    print("="=70)

if __name__ == "__main__":
    merge_playlists()
