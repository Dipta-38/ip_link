#!/usr/bin/env python3
"""
IPTV M3U Merger Script
Fetches and merges multiple M3U/M3U8 playlists from sources.txt
Filters out unwanted channels (Live BDIX, Welcome to PlayZ)
"""

import requests
import os
import sys
import re
from pathlib import Path
from typing import Set, List, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
SCRIPT_DIR = Path(__file__).parent
SOURCES_FILE = SCRIPT_DIR / "sources.txt"
OUTPUT_FILE = SCRIPT_DIR / "merged.m3u"
TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# Keywords to filter out (case-insensitive)
FILTER_KEYWORDS = [
    "[LIVE] BDIX",
    "welcome to playz",
    "playz tv",
    "playztv"
]

def should_filter_channel(extinf_line: str, url_line: str) -> bool:
    """
    Check if channel should be filtered out.
    Returns True if channel should be removed.
    """
    combined = (extinf_line + " " + url_line).lower()
    
    for keyword in FILTER_KEYWORDS:
        if keyword in combined:
            logger.debug(f"Filtered out: {keyword} - {extinf_line[:100]}")
            return True
    return False

def read_sources(sources_file: Path) -> List[str]:
    """Read URLs from sources.txt file."""
    try:
        with open(sources_file, 'r', encoding='utf-8') as f:
            sources = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        logger.info(f"Found {len(sources)} sources in {sources_file}")
        return sources
    except FileNotFoundError:
        logger.error(f"Sources file not found: {sources_file}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading sources file: {e}")
        sys.exit(1)

def fetch_playlist(url: str, retries: int = MAX_RETRIES) -> Tuple[bool, str]:
    """
    Fetch a single playlist from URL with retry logic.
    Returns tuple (success: bool, content: str)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(retries):
        try:
            logger.debug(f"Fetching {url} (attempt {attempt + 1}/{retries})")
            response = requests.get(url, timeout=TIMEOUT, headers=headers)
            response.raise_for_status()
            return True, response.text
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout fetching {url} (attempt {attempt + 1}/{retries})")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error fetching {url} (attempt {attempt + 1}/{retries})")
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error {e.response.status_code} for {url}")
            return False, ""
        except Exception as e:
            logger.warning(f"Error fetching {url}: {e} (attempt {attempt + 1}/{retries})")
    
    logger.error(f"Failed to fetch {url} after {retries} attempts")
    return False, ""

def parse_m3u_content(content: str) -> Tuple[List[str], List[str]]:
    """
    Parse M3U content and extract channels.
    Returns tuple (extinf_lines: List[str], url_lines: List[str])
    """
    lines = content.split('\n')
    extinf_lines = []
    url_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('#EXTINF:'):
            extinf_lines.append(line)
            # Next non-empty line should be the URL
            i += 1
            while i < len(lines):
                url_line = lines[i].strip()
                if url_line and not url_line.startswith('#'):
                    url_lines.append(url_line)
                    break
                i += 1
        i += 1
    
    return extinf_lines, url_lines

def merge_playlists(sources: List[str]) -> Tuple[List[str], List[str]]:
    """
    Fetch and merge all playlists from sources.
    Filters out unwanted channels.
    Returns tuple (extinf_lines, url_lines)
    """
    all_extinf = []
    all_urls = []
    seen_urls: Set[str] = set()
    filtered_count = 0
    
    logger.info("Starting playlist merge process with filtering...")
    logger.info(f"Filtering keywords: {', '.join(FILTER_KEYWORDS)}")
    
    for source_url in sources:
        logger.info(f"Processing: {source_url}")
        success, content = fetch_playlist(source_url)
        
        if not success or not content:
            logger.warning(f"Skipped: {source_url}")
            continue
        
        extinf_lines, url_lines = parse_m3u_content(content)
        logger.info(f"  Found {len(url_lines)} channels in this source")
        
        # Add unique channels (filtering unwanted ones)
        for extinf, url in zip(extinf_lines, url_lines):
            if url not in seen_urls:
                # Check if channel should be filtered
                if should_filter_channel(extinf, url):
                    filtered_count += 1
                    continue
                
                seen_urls.add(url)
                all_extinf.append(extinf)
                all_urls.append(url)
    
    logger.info(f"Total unique channels merged: {len(all_urls)}")
    logger.info(f"Total channels filtered out: {filtered_count}")
    return all_extinf, all_urls

def save_merged_playlist(extinf_lines: List[str], url_lines: List[str], output_file: Path):
    """Save merged playlist to output file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            
            for extinf, url in zip(extinf_lines, url_lines):
                f.write(extinf + "\n")
                f.write(url + "\n")
        
        logger.info(f"Merged playlist saved to: {output_file}")
        logger.info(f"Total channels: {len(url_lines)}")
        return True
    except Exception as e:
        logger.error(f"Error saving merged playlist: {e}")
        return False

def main():
    """Main function."""
    try:
        # Read sources
        sources = read_sources(SOURCES_FILE)
        
        if not sources:
            logger.warning("No sources found in sources.txt")
            sys.exit(1)
        
        # Merge playlists
        extinf_lines, url_lines = merge_playlists(sources)
        
        if not url_lines:
            logger.error("No channels were merged successfully")
            sys.exit(1)
        
        # Save merged playlist
        success = save_merged_playlist(extinf_lines, url_lines, OUTPUT_FILE)
        
        if success:
            logger.info("Merge completed successfully!")
            sys.exit(0)
        else:
            logger.error("Failed to save merged playlist")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
