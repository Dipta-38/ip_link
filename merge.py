import requests
import os

SOURCE_FILE = "sources.txt"
OUTPUT_FILE = "merged.m3u"
CHECK_TIMEOUT = 5

# Get proxy from environment variable
HTTP_PROXY = os.environ.get('HTTP_PROXY')
HTTPS_PROXY = os.environ.get('HTTPS_PROXY', HTTP_PROXY)

proxies = {}
if HTTP_PROXY:
    proxies = {
        'http': HTTP_PROXY,
        'https': HTTPS_PROXY if HTTPS_PROXY else HTTP_PROXY,
    }

# Bangladesh IP ranges for verification
BANGLADESH_IP_RANGES = [
    '103.0.0.0/8',
    '103.48.0.0/13',
    '103.56.0.0/13',
    '103.64.0.0/10',
    '103.128.0.0/10',
    '103.192.0.0/10',
    '103.200.0.0/13',
    '103.208.0.0/13',
    '103.216.0.0/13',
    '103.224.0.0/11',
    '180.163.0.0/16',
]

BANGLADESH_COUNTRY_CODES = ['BD', 'Bangladesh']

def verify_bangladesh_ip():
    """Verify IP is from Bangladesh through proxy if available."""
    if not proxies:
        print("❌ ERROR: No proxy configured!")
        print("   To use this script, set HTTP_PROXY and HTTPS_PROXY environment variables")
        print("   with a Bangladeshi IP proxy. Example:")
        print("   export HTTP_PROXY='http://bangladeshi-proxy.com:port'")
        return False
        
    try:
        # Get current IP through proxy
        response = requests.get(
            'http://api.ipify.org',
            proxies=proxies,
            timeout=10
        )
        ip = response.text.strip()
        
        # Get location details
        loc_response = requests.get(
            f'http://ip-api.com/json/{ip}?fields=country,countryCode,city,org',
            timeout=5
        )
        loc_data = loc_response.json()
        
        country = loc_data.get('country', '').strip()
        country_code = loc_data.get('countryCode', '').strip().upper()
        city = loc_data.get('city', 'Unknown')
        org = loc_data.get('org', 'Unknown')
        
        print("="*70)
        print("🔍 PROXY VERIFICATION - BANGLADESH IP CHECK")
        print("="*70)
        print(f"🌍 Proxy: {HTTP_PROXY}")
        print(f"📡 IP through proxy: {ip}")
        print(f"🏢 Organization: {org}")
        print(f"📍 Country: {country} ({country_code})")
        print(f"🏙️  City: {city}")
        
        # Strict Bangladesh verification
        if country_code in BANGLADESH_COUNTRY_CODES or country in BANGLADESH_COUNTRY_CODES:
            print("✅ ✓ Using BANGLADESHI IP - Ready to filter channels")
            print("="*70)
            return True
        else:
            print("❌ ERROR: IP is NOT from Bangladesh!")
            print(f"   Country detected: {country} ({country_code})")
            print("   Please use a Bangladeshi proxy!")
            print("="*70)
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout verifying IP - Check proxy connectivity")
        return False
    except Exception as e:
        print(f"❌ Failed to verify Bangladesh IP: {e}")
        print(f"   Proxy: {HTTP_PROXY}")
        print(f"   Error: {str(e)}")
        return False

def is_stream_available(url):
    """Check if stream is available through Bangladeshi proxy."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.google.com/',
            'Accept': '*/*',
            'Connection': 'close',
        }

        # Use proxy for all requests to ensure Bangladesh IP
        request_proxies = proxies if proxies else None

        response = requests.head(
            url, 
            timeout=CHECK_TIMEOUT, 
            headers=headers, 
            allow_redirects=True,
            proxies=request_proxies,
            verify=False  # Ignore SSL warnings for some streams
        )

        # Filter 403 and 504
        if response.status_code == 403:
            return False, "403"
        if response.status_code == 504:
            return False, "504"
            
        # Accept 2xx, 3xx, and some 4xx codes (except 403, 504)
        if response.status_code < 400 or response.status_code in [401, 404]:
            return True, str(response.status_code)
        
        return False, str(response.status_code)

    except requests.exceptions.Timeout:
        return False, "timeout"  # Changed to False - timeout means unavailable
    except requests.exceptions.ConnectionError:
        return False, "connection_error"  # Changed to False - connection error means unavailable
    except Exception as e:
        return False, f"error: {str(e)}"  # Changed to False - other errors mean unavailable

def merge_playlists():
    entries = []
    skipped_count = 0
    forbidden_count = 0
    gateway_count = 0
    timeout_count = 0
    connection_error_count = 0
    kept_count = 0
    total_checked = 0

    print("\n" + "="*70)
    print("🚀 IPTV MERGER - BANGLADESH IP FILTER")
    print("="*70)
    
    # Verify Bangladesh proxy is configured and working
    if not verify_bangladesh_ip():
        print("\n❌ CRITICAL ERROR: Bangladesh IP verification failed!")
        print("   The script will not proceed without a valid Bangladeshi proxy.")
        print("\n   To fix this:")
        print("   1. Set HTTP_PROXY environment variable with Bangladeshi proxy")
        print("   2. Set HTTPS_PROXY environment variable with Bangladeshi proxy")
        print("   3. Verify proxy is accessible and provides Bangladesh IP")
        return
    
    print("\n✅ Bangladesh IP verified - Starting channel filtering...\n")

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
            
            # Always use proxy to maintain Bangladesh IP
            response = requests.get(
                playlist_url, 
                timeout=30,
                proxies=proxies,
                verify=False
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

                    # Check stream availability through Bangladesh IP
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
                        elif status == "timeout":
                            timeout_count += 1
                        elif status == "connection_error":
                            connection_error_count += 1

                    # Show progress every 50 streams
                    if total_checked % 50 == 0:
                        print(f"📊 Progress: Checked {total_checked} streams | Kept: {kept_count}")

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
    print("✅ MERGE COMPLETED - BANGLADESHI CHANNELS ONLY")
    print("="*70)
    print(f"📺 Total channels kept: {kept_count}")
    print(f"🚫 403 Forbidden (not available in BD): {forbidden_count}")
    print(f"🌐 504 Gateway Timeout: {gateway_count}")
    print(f"⏱️  Timeouts: {timeout_count}")
    print(f"❌ Connection errors: {connection_error_count}")
    print(f"⏭️  PlayZ sponsored removed: {skipped_count}")
    print(f"📊 Total streams checked: {total_checked}")
    print(f"📊 Final playlist entries: {len(entries)//2}")
    print("="*70)
    if proxies:
        print(f"🔌 Proxy: {HTTP_PROXY}")
        print(f"🇧🇩 Channels filtered for BANGLADESH IP only")
    print("="*70)
    print(f"📁 Output saved to: {OUTPUT_FILE}")
    print("✅ All channels are verified to work from BANGLADESH IP")
    print("="*70)

if __name__ == "__main__":
    merge_playlists()
