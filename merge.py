#!/usr/bin/env python3
"""
IPTV M3U8 Merger with Bangladeshi IP Filtering
Merges multiple M3U8 files and filters channels available in Bangladesh
"""

import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse
import socket
from typing import List, Tuple
import time

# Bangladeshi IP/Proxy configurations
BD_PROXIES = {
    'http': os.getenv('BD_PROXY_HTTP', 'http://proxy.example.com:8080'),
    'https': os.getenv('BD_PROXY_HTTPS', 'http://proxy.example.com:8080'),
}

# Use environment variable for proxy or fallback
USE_BD_PROXY = os.getenv('USE_BD_PROXY', 'true').lower() == 'true'

class M3U8Merger:
    def __init__(self, use_proxy=USE_BD_PROXY, timeout=10):
        self.channels = {}
        self.use_proxy = use_proxy
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure proxy if enabled
        if self.use_proxy:
            self.session.proxies.update(BD_PROXIES)
        
        # Set a user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def read_m3u8_file(self, file_path: str) -> List[Tuple[str, str]]:
        """Read M3U8 file and extract channels"""
        channels = []
        
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            return channels
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Look for EXTINF lines (channel info)
                if line.startswith('#EXTINF:'):
                    info = line
                    # Get channel name from EXTINF line
                    match = re.search(r'tvg-name="([^"]*)"', info)
                    channel_name = match.group(1) if match else f"Channel {len(channels)}"
                    
                    # Get URL from next line
                    if i + 1 < len(lines):
                        url = lines[i + 1].strip()
                        if url and not url.startswith('#'):
                            channels.append((channel_name, url))
                
                i += 1
            
            print(f"✓ Loaded {len(channels)} channels from {os.path.basename(file_path)}")
        except Exception as e:
            print(f"✗ Error reading {file_path}: {e}")
        
        return channels

    def check_channel_availability(self, url: str) -> bool:
        """Check if channel is accessible (simulating Bangladesh IP check)"""
        if not url.strip():
            return False
        
        try:
            # Only check HTTP/HTTPS URLs
            if not url.startswith(('http://', 'https://', '//')):
                return True  # Local streams are assumed available
            
            # Perform HEAD request to check availability
            response = self.session.head(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                verify=False
            )
            
            # Check if response is successful (2xx or 3xx)
            return 200 <= response.status_code < 400
        
        except requests.exceptions.Timeout:
            print(f"  ⏱️  Timeout: {url}")
            return False
        except requests.exceptions.ProxyError:
            print(f"  🔴 Proxy error for: {url}")
            return False
        except requests.exceptions.ConnectionError:
            print(f"  ✗ Connection error: {url}")
            return False
        except Exception as e:
            print(f"  ⚠️  Error checking {url}: {str(e)[:50]}")
            return False

    def merge_files(self, file_list: List[str], filter_bd: bool = True) -> int:
        """Merge multiple M3U8 files and filter for Bangladesh availability"""
        all_channels = []
        
        # Read all M3U8 files
        for file_path in file_list:
            channels = self.read_m3u8_file(file_path)
            all_channels.extend(channels)
        
        print(f"\n📊 Total channels found: {len(all_channels)}")
        
        # Remove duplicates (keep first occurrence)
        seen_urls = set()
        unique_channels = []
        for name, url in all_channels:
            if url not in seen_urls:
                unique_channels.append((name, url))
                seen_urls.add(url)
        
        print(f"📊 After removing duplicates: {len(unique_channels)}")
        
        # Filter channels by Bangladesh availability
        if filter_bd:
            print(f"\n🔍 Filtering channels for Bangladesh IP access...")
            print(f"   Using proxy: {self.use_proxy}")
            
            available_channels = []
            for idx, (name, url) in enumerate(unique_channels, 1):
                print(f"  [{idx}/{len(unique_channels)}] Checking {name[:30]:<30}...", end=" ")
                
                if self.check_channel_availability(url):
                    print("✓")
                    available_channels.append((name, url))
                else:
                    print("✗")
                
                # Rate limiting
                time.sleep(0.2)
            
            print(f"\n✓ Available channels in Bangladesh: {len(available_channels)}/{len(unique_channels)}")
            self.channels = available_channels
        else:
            self.channels = unique_channels
            print(f"✓ Total channels to merge: {len(self.channels)}")
        
        return len(self.channels)

    def write_m3u8(self, output_file: str):
        """Write merged channels to M3U8 file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write M3U header
                f.write("#EXTM3U\n")
                
                # Write channels
                for idx, (name, url) in enumerate(self.channels, 1):
                    f.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
                    f.write(f'{url}\n')
            
            print(f"\n✓ Merged M3U8 written to: {output_file}")
            print(f"  Total channels: {len(self.channels)}")
        except Exception as e:
            print(f"✗ Error writing file: {e}")

    def write_sources(self, sources_file: str):
        """Write sources information"""
        try:
            with open(sources_file, 'w', encoding='utf-8') as f:
                f.write("# IPTV Sources\n")
                f.write(f"# Generated with Bangladesh IP filtering\n")
                f.write(f"# Total channels: {len(self.channels)}\n\n")
                
                for name, url in self.channels:
                    f.write(f"{name} | {url}\n")
            
            print(f"✓ Sources information written to: {sources_file}")
        except Exception as e:
            print(f"✗ Error writing sources: {e}")


def get_m3u8_files() -> List[str]:
    """Get all M3U8 files in current directory"""
    current_dir = Path('.')
    m3u8_files = []
    
    # Find M3U and M3U8 files (excluding merged output)
    for ext in ['*.m3u', '*.m3u8']:
        for file in current_dir.glob(ext):
            if not file.name.startswith('merged'):
                m3u8_files.append(str(file))
    
    return sorted(m3u8_files)


def main():
    print("=" * 60)
    print("🎬 IPTV M3U8 Merger - Bangladesh IP Filter")
    print("=" * 60)
    
    # Get all M3U8 files
    m3u8_files = get_m3u8_files()
    
    if not m3u8_files:
        print("❌ No M3U8 files found in current directory!")
        return
    
    print(f"\n📁 Found {len(m3u8_files)} M3U8 file(s):")
    for file in m3u8_files:
        print(f"   - {file}")
    
    # Check for Bangladeshi proxy configuration
    use_proxy = USE_BD_PROXY or os.getenv('BD_PROXY_HTTP') or os.getenv('BD_PROXY_HTTPS')
    
    if use_proxy:
        print(f"\n✓ Using Bangladeshi proxy/IP for filtering")
    else:
        print(f"\n⚠️  No proxy configured - using default connection")
        print(f"   Set BD_PROXY_HTTP or BD_PROXY_HTTPS environment variables")
    
    # Create merger instance
    merger = M3U8Merger(use_proxy=bool(use_proxy))
    
    # Merge and filter channels
    merger.merge_files(m3u8_files, filter_bd=True)
    
    # Write output files
    if merger.channels:
        merger.write_m3u8('merged.m3u')
        merger.write_sources('sources.txt')
        print("\n✓ Merge complete!")
    else:
        print("\n❌ No channels available for Bangladesh!")


if __name__ == '__main__':
    main()
