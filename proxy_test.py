#!/usr/bin/env python3
"""
Proxy Testing Tool for Bangladesh IP Verification
Tests if your proxy provides a valid Bangladesh IP
"""

import requests
import sys
import os

def test_proxy(proxy_url):
    """Test if proxy works and returns Bangladesh IP"""
    
    print("="*70)
    print("🔍 BANGLADESH PROXY TEST")
    print("="*70)
    print(f"Testing proxy: {proxy_url}\n")
    
    # Step 1: Test proxy connectivity
    print("Step 1️⃣: Testing proxy connectivity...")
    try:
        response = requests.get(
            'http://api.ipify.org',
            proxies={'http': proxy_url, 'https': proxy_url},
            timeout=5
        )
        ip = response.text.strip()
        print(f"✅ Proxy works! IP through proxy: {ip}\n")
    except requests.exceptions.Timeout:
        print("❌ Timeout - proxy not responding\n")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - proxy unreachable\n")
        return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False
    
    # Step 2: Get IP location
    print("Step 2️⃣: Getting IP location details...")
    try:
        response = requests.get(
            f'http://ip-api.com/json/{ip}?fields=country,countryCode,city,org,isp,proxy',
            timeout=5
        )
        data = response.json()
        
        if response.status_code != 200:
            print(f"❌ Could not get location data\n")
            return False
        
        country = data.get('country', 'Unknown')
        country_code = data.get('countryCode', 'Unknown').upper()
        city = data.get('city', 'Unknown')
        org = data.get('org', 'Unknown')
        isp = data.get('isp', 'Unknown')
        is_proxy = data.get('proxy', False)
        
        print(f"IP:         {ip}")
        print(f"Country:    {country} ({country_code})")
        print(f"City:       {city}")
        print(f"ISP/Org:    {org}")
        print(f"Is Proxy:   {'Yes' if is_proxy else 'No'}\n")
        
    except Exception as e:
        print(f"❌ Error getting location: {e}\n")
        return False
    
    # Step 3: Verify Bangladesh
    print("Step 3️⃣: Verifying Bangladesh IP...")
    if country_code == 'BD' or country == 'Bangladesh':
        print(f"✅ ✅ ✅ BANGLADESH IP VERIFIED! ✅ ✅ ✅\n")
        return True
    else:
        print(f"❌ ❌ ❌ NOT BANGLADESH IP! ❌ ❌ ❌")
        print(f"   Country code: {country_code}")
        print(f"   Country: {country}\n")
        return False


def test_from_env():
    """Test proxy from environment variables"""
    
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    
    if not http_proxy:
        print("❌ ERROR: No proxy found in environment variables!\n")
        print("Set proxy with:")
        print("  export HTTP_PROXY='http://proxy-ip:port'")
        print("  export HTTPS_PROXY='http://proxy-ip:port'\n")
        return False
    
    print(f"Found HTTP_PROXY: {http_proxy}")
    if https_proxy:
        print(f"Found HTTPS_PROXY: {https_proxy}\n")
    
    return test_proxy(http_proxy)


def test_popular_proxies():
    """Test a list of popular Bangladesh proxies"""
    
    proxies = [
        "http://103.125.31.222:80",
        "http://103.144.182.1:3128",
        "http://103.105.187.38:8080",
        "http://180.163.200.242:3128",
        "http://103.141.100.78:80",
        "http://103.144.202.188:80",
    ]
    
    print("="*70)
    print("🔍 TESTING POPULAR BANGLADESH PROXIES")
    print("="*70)
    print("Trying multiple proxies...\n")
    
    working_proxies = []
    
    for proxy in proxies:
        print(f"Testing: {proxy}")
        try:
            response = requests.get(
                'http://api.ipify.org',
                proxies={'http': proxy},
                timeout=3
            )
            ip = response.text.strip()
            
            # Check if Bangladesh
            loc_response = requests.get(
                f'http://ip-api.com/json/{ip}?fields=countryCode',
                timeout=3
            )
            data = loc_response.json()
            country_code = data.get('countryCode', '').upper()
            
            if country_code == 'BD':
                print(f"  ✅ WORKS! IP: {ip} (Bangladesh)\n")
                working_proxies.append(proxy)
            else:
                print(f"  ❌ IP is not Bangladesh: {ip} ({country_code})\n")
        except:
            print(f"  ❌ Failed or timeout\n")
    
    if working_proxies:
        print("="*70)
        print(f"✅ Found {len(working_proxies)} working proxy/proxies:\n")
        for proxy in working_proxies:
            print(f"  export HTTP_PROXY='{proxy}'")
        print("="*70)
        return True
    else:
        print("❌ No working proxies found\n")
        return False


def main():
    print("\n")
    
    if len(sys.argv) > 1:
        # Test specific proxy
        proxy = sys.argv[1]
        success = test_proxy(proxy)
    elif os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy'):
        # Test from environment
        print("Testing proxy from environment variables...\n")
        success = test_from_env()
    else:
        # Show usage and test popular proxies
        print("Usage:")
        print("  python proxy_test.py [proxy_url]")
        print("  python proxy_test.py  # Uses HTTP_PROXY environment variable")
        print("  python proxy_test.py --list  # Tests popular Bangladesh proxies\n")
        
        if len(sys.argv) > 1 and sys.argv[1] == '--list':
            success = test_popular_proxies()
        else:
            print("Examples:")
            print("  python proxy_test.py http://103.125.31.222:80")
            print("  export HTTP_PROXY='http://proxy-ip:port'")
            print("  python proxy_test.py\n")
            print("To test popular proxies:")
            print("  python proxy_test.py --list\n")
            return
    
    print("="*70)
    if success:
        print("✅ READY: Your proxy provides a valid Bangladesh IP!")
        print("   You can now run merge.py")
    else:
        print("❌ PROBLEM: Proxy doesn't provide Bangladesh IP")
        print("   Try another proxy or:")
        print("   python proxy_test.py --list")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
