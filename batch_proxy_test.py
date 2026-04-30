#!/usr/bin/env python3
"""
Batch Proxy Tester for Bangladesh IPs
Tests multiple proxies at once to find working ones
"""

import requests
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Extended list of Bangladesh proxies to test
PROXIES_TO_TEST = [
    # Fresh Bangladesh IP ranges (March-April 2026)
    "http://103.106.233.226:80",
    "http://103.106.239.108:80",
    "http://103.148.48.65:80",
    "http://180.163.220.66:3128",
    "http://180.163.220.67:3128",
    "http://103.55.36.107:80",
    "http://103.55.36.108:80",
    "http://103.140.201.22:80",
    "http://103.140.201.23:80",
    "http://103.141.100.78:80",
    "http://103.144.202.188:80",
    "http://103.109.177.247:8080",
    "http://103.109.177.248:8080",
    
    # Popular Bangladesh proxies
    "http://103.125.31.222:80",
    "http://103.144.182.1:3128",
    "http://103.105.187.38:8080",
    "http://180.163.200.242:3128",
]

def test_single_proxy(proxy_url):
    """Test a single proxy and return result"""
    try:
        # Test connectivity
        response = requests.get(
            'http://api.ipify.org',
            proxies={'http': proxy_url},
            timeout=5
        )
        
        if response.status_code != 200:
            return proxy_url, False, "Wrong status code"
        
        ip = response.text.strip()
        
        # Verify Bangladesh
        try:
            loc_response = requests.get(
                f'http://ip-api.com/json/{ip}?fields=countryCode',
                timeout=5
            )
            data = loc_response.json()
            country_code = data.get('countryCode', '').upper()
            
            if country_code == 'BD':
                return proxy_url, True, ip
            else:
                return proxy_url, False, f"Not BD: {country_code}"
        except:
            return proxy_url, False, "Could not verify country"
            
    except requests.exceptions.Timeout:
        return proxy_url, False, "Timeout"
    except requests.exceptions.ConnectionError:
        return proxy_url, False, "Connection error"
    except Exception as e:
        return proxy_url, False, str(e)[:30]

def test_proxies_batch(proxies=None, num_threads=5):
    """Test multiple proxies in parallel"""
    
    if proxies is None:
        proxies = PROXIES_TO_TEST
    
    print("="*70)
    print("🔍 BATCH BANGLADESH PROXY TESTER")
    print("="*70)
    print(f"Testing {len(proxies)} proxies with {num_threads} threads...\n")
    
    working_proxies = []
    failed_proxies = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all tasks
        future_to_proxy = {executor.submit(test_single_proxy, proxy): proxy for proxy in proxies}
        
        completed = 0
        for future in as_completed(future_to_proxy):
            completed += 1
            proxy_url, is_working, result = future.result()
            
            if is_working:
                working_proxies.append((proxy_url, result))
                print(f"✅ WORKING: {proxy_url}")
                print(f"   IP: {result}\n")
            else:
                failed_proxies.append((proxy_url, result))
                print(f"❌ Failed: {proxy_url}")
                print(f"   Reason: {result}")
                print()
            
            # Show progress
            if completed % 5 == 0:
                print(f"📊 Progress: {completed}/{len(proxies)} tested, {len(working_proxies)} working\n")
    
    # Summary
    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70)
    print(f"✅ Working proxies: {len(working_proxies)}")
    print(f"❌ Failed proxies: {len(failed_proxies)}")
    print()
    
    if working_proxies:
        print("🎉 WORKING PROXIES (Ready to Use):\n")
        for proxy, ip in working_proxies:
            print(f"export HTTP_PROXY='{proxy}'")
            print(f"# IP: {ip}\n")
        
        print("Quick start:")
        print(f"export HTTP_PROXY='{working_proxies[0][0]}'")
        print("python merge.py\n")
    else:
        print("😞 No working proxies found from built-in list")
        print("\nTry:")
        print("1. Visit free-proxy-list.net and filter for Bangladesh")
        print("2. Add proxies here or use: python proxy_test.py http://ip:port")
        print("3. Update PROXIES_TO_TEST list below this script\n")
    
    print("="*70)
    
    return working_proxies, failed_proxies

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Usage:")
            print("  python batch_proxy_test.py              # Test default list")
            print("  python batch_proxy_test.py --threads N  # Use N threads (default: 5)")
            print("  python batch_proxy_test.py --quick      # Quick single-threaded test")
            return
        
        if sys.argv[1] == '--quick':
            print("\n🐢 Running single-threaded test (slower but more stable)...\n")
            test_proxies_batch(num_threads=1)
            return
        
        if sys.argv[1] == '--threads' and len(sys.argv) > 2:
            try:
                threads = int(sys.argv[2])
                test_proxies_batch(num_threads=threads)
                return
            except:
                print("Invalid thread count")
                return
    
    # Default: fast parallel test with 5 threads
    test_proxies_batch()

if __name__ == "__main__":
    main()
