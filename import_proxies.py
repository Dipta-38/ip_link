#!/usr/bin/env python3
"""
Simple proxy import and test tool
Paste proxy list and test them all
"""

import sys

def prompt_for_proxies():
    """Prompt user to enter proxies"""
    print("="*70)
    print("📋 PROXY LIST IMPORTER & TESTER")
    print("="*70)
    print("\nEnter proxies (one per line).")
    print("Format: http://ip:port or ip:port (http:// will be added)")
    print("Paste proxies, then press Enter twice when done:")
    print()
    
    proxies = []
    empty_count = 0
    
    while True:
        try:
            line = input().strip()
            
            if not line:
                empty_count += 1
                if empty_count >= 1:
                    break
                continue
            
            empty_count = 0
            
            # Add http:// if missing
            if not line.startswith('http'):
                line = 'http://' + line
            
            proxies.append(line)
            print(f"✅ Added: {line}")
        
        except KeyboardInterrupt:
            print("\n\nCancelled")
            return []
        except EOFError:
            break
    
    return proxies

def test_proxies(proxies):
    """Test list of proxies"""
    if not proxies:
        print("No proxies to test")
        return
    
    import requests
    
    print("\n" + "="*70)
    print("🧪 TESTING PROXIES")
    print("="*70 + "\n")
    
    working = []
    failed = []
    
    for i, proxy in enumerate(proxies, 1):
        print(f"[{i}/{len(proxies)}] Testing: {proxy}")
        
        try:
            response = requests.get(
                'http://api.ipify.org',
                proxies={'http': proxy, 'https': proxy},
                timeout=5
            )
            
            ip = response.text.strip()
            
            # Check country
            loc_response = requests.get(
                f'http://ip-api.com/json/{ip}?fields=countryCode',
                timeout=5
            )
            country = loc_response.json().get('countryCode', 'XX')
            
            if country == 'BD':
                print(f"  ✅ WORKING - IP: {ip} (Bangladesh)")
                working.append((proxy, ip))
            else:
                print(f"  ⚠️  Working but not Bangladesh: {ip} ({country})")
                failed.append((proxy, f"Not BD: {country}"))
        
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout")
            failed.append((proxy, "Timeout"))
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Connection error")
            failed.append((proxy, "Connection error"))
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:40]}")
            failed.append((proxy, str(e)[:40]))
        
        print()
    
    # Summary
    print("="*70)
    print("📊 RESULTS")
    print("="*70)
    print(f"✅ Working Bangladesh proxies: {len(working)}")
    print(f"❌ Failed or wrong country: {len(failed)}")
    print()
    
    if working:
        print("🎉 WORKING PROXIES:\n")
        for proxy, ip in working:
            print(f"{proxy}")
            print(f"  IP: {ip}\n")
        
        print("Use in bash:")
        for proxy, _ in working:
            print(f"export HTTP_PROXY='{proxy}'")
        print()
        
        print("Use in GitHub Actions:")
        for proxy, _ in working[:1]:
            print(f"BANGLADESHI_PROXY={proxy}")
        print()
    
    if failed:
        print("❌ FAILED PROXIES:\n")
        for proxy, reason in failed:
            print(f"{proxy} - {reason}")
        print()

def main():
    import requests
    
    try:
        print("Checking internet connection...", end=' ')
        requests.get('http://api.ipify.org', timeout=3)
        print("✅\n")
    except:
        print("❌\nNo internet connection!")
        return
    
    proxies = prompt_for_proxies()
    
    if proxies:
        test_proxies(proxies)
    else:
        print("No proxies entered")

if __name__ == "__main__":
    main()
