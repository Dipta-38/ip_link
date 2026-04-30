#!/usr/bin/env python3
"""
IPTV Playlist Merger and IP Filter
Merges multiple IPTV playlists and filters channels by IP address.
"""

import requests
import re
from pathlib import Path
from urllib.parse import urlparse
import yaml
from datetime import datetime

class IPTVMerger:
    def __init__(self, config_file='merge.yml'):
        """Initialize with configuration file."""
        self.config = self.load_config(config_file)
        self.target_ip = self.config.get('target_ip', '103.73.185.62')
        self.sources_file = self.config.get('sources_file', 'sources.txt')
        self.output_file = self.config.get('output_file', 'merged.m3u')
        self.timeout = self.config.get('timeout', 10)
        self.merged_channels = []
        
    def load_config(self, config_file):
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Using defaults.")
            return {}
        
    def load_sources(self):
        """Load source URLs from sources.txt."""
        sources = []
        try:
            with open(self.sources_file, 'r', encoding='utf-8') as f:
                sources = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"Sources file {self.sources_file} not found.")
        return sources
    
    def download_playlist(self, url):
        """Download a playlist from URL."""
        try:
            print(f"Downloading: {url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return ""
    
    def is_channel_compatible(self, url):
        """Check if channel URL is compatible with target IP."""
        # Check if URL contains the target IP
        if self.target_ip in url:
            return True
        
        # Check for common BDIX/IPTV patterns that work with the IP
        bdix_patterns = [
            r'103\.\d+\.\d+\.\d+',  # Any IP in 103.x.x.x range (BDIX)
            r'192\.168\.',           # Local network
            r'10\.\d+\.',            # Private network
        ]
        
        for pattern in bdix_patterns:
            if re.search(pattern, url):
                return True
        
        # Check for relative URLs or stream paths
        parsed = urlparse(url)
        if not parsed.netloc or parsed.netloc.startswith('localhost'):
            return True
        
        return False
    
    def parse_m3u(self, content):
        """Parse M3U playlist content."""
        channels = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for EXTINF lines
            if line.startswith('#EXTINF:'):
                extinf = line
                # Next line should be the URL
                if i + 1 < len(lines):
                    url = lines[i + 1].strip()
                    if url and not url.startswith('#'):
                        channels.append({
                            'extinf': extinf,
                            'url': url
                        })
                    i += 2
                else:
                    i += 1
            else:
                i += 1
        
        return channels
    
    def filter_channels(self, channels):
        """Filter channels by IP compatibility."""
        filtered = []
        for channel in channels:
            if self.is_channel_compatible(channel['url']):
                filtered.append(channel)
        return filtered
    
    def merge_playlists(self):
        """Merge and filter playlists."""
        sources = self.load_sources()
        
        if not sources:
            print("No sources found!")
            return
        
        print(f"\n{'='*60}")
        print(f"IPTV Playlist Merger - Filtering for IP: {self.target_ip}")
        print(f"{'='*60}\n")
        
        all_channels = []
        unique_urls = set()
        
        for source_url in sources:
            content = self.download_playlist(source_url)
            if content:
                channels = self.parse_m3u(content)
                # Filter channels by IP
                filtered = self.filter_channels(channels)
                
                # Avoid duplicates
                for channel in filtered:
                    if channel['url'] not in unique_urls:
                        all_channels.append(channel)
                        unique_urls.add(channel['url'])
                
                print(f"✓ Found {len(filtered)} compatible channels from {len(channels)} total")
        
        print(f"\n{'='*60}")
        print(f"Total unique channels: {len(all_channels)}")
        print(f"{'='*60}\n")
        
        self.merged_channels = all_channels
        return all_channels
    
    def save_playlist(self):
        """Save merged playlist to M3U file."""
        if not self.merged_channels:
            print("No channels to save!")
            return
        
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTM3U url-tvg=\"\" refresh=\"3600\" max-conn=\"1\"\n")
                f.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Filtered for IP: {self.target_ip}\n")
                f.write(f"# Total channels: {len(self.merged_channels)}\n\n")
                
                for channel in self.merged_channels:
                    f.write(channel['extinf'] + '\n')
                    f.write(channel['url'] + '\n')
            
            print(f"✓ Playlist saved to: {self.output_file}")
            print(f"  Total channels: {len(self.merged_channels)}")
        except IOError as e:
            print(f"Error saving playlist: {e}")
    
    def run(self):
        """Run the complete merge and filter process."""
        self.merge_playlists()
        self.save_playlist()


def main():
    merger = IPTVMerger()
    merger.run()


if __name__ == '__main__':
    main()
