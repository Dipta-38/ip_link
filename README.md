# IPTV Bangladesh Filter

Automatically merge and filter IPTV channels that are **available in Bangladesh only**.

## Overview

This script:
- ✅ Fetches IPTV playlists from multiple sources
- ✅ Tests each channel through a **Bangladeshi IP proxy**
- ✅ Removes channels not available in Bangladesh (403 Forbidden, 504 errors, timeouts)
- ✅ Creates a filtered `merged.m3u` playlist with working channels
- ✅ Runs automatically via GitHub Actions every 6 hours

## ⚠️ Important: Bangladesh IP Required

⚠️ **This script REQUIRES a Bangladeshi IP proxy to work correctly.**

Without a Bangladeshi IP, the script cannot determine which channels are available in Bangladesh. The script will refuse to run if a valid Bangladesh IP is not detected.

### Having Proxy Issues?

If you see: `❌ ERROR: No working Bangladeshi proxy found!`

→ **See: [PROXY_EMERGENCY_GUIDE.md](PROXY_EMERGENCY_GUIDE.md)** (Quick fix - 5 minutes)

## Setup Instructions

### 1. Local Testing

To test locally:

```bash
# Set proxy environment variables
export HTTP_PROXY="http://YOUR_BANGLADESH_PROXY:PORT"
export HTTPS_PROXY="http://YOUR_BANGLADESH_PROXY:PORT"

# Run the script
python merge.py
```

### 2. GitHub Actions Workflow

#### Option A: Using GitHub Secrets (Recommended)

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add a secret named: `BANGLADESHI_PROXY`
5. Value: `http://YOUR_PROXY_IP:PORT`

Example: `http://103.125.31.222:80`

#### Option B: Pre-configured Proxies

The workflow includes a list of known Bangladeshi proxies. If one of these works in Bangladesh, no additional setup is needed:

```
http://103.125.31.222:80
http://103.144.182.1:3128
http://103.105.187.38:8080
http://180.163.200.242:3128
```

### 3. Configure Your Playlist Sources

Edit `sources.txt` and add M3U8 playlist URLs (one per line):

```
https://example.com/playlist1.m3u8
https://example.com/playlist2.m3u8
https://example.com/playlist3.m3u8
```

## How It Works

1. **Proxy Verification**: Script verifies the IP is from Bangladesh
   - Uses `api.ipify.org` to get current IP
   - Uses `ip-api.com` to verify country code is `BD`
   - ❌ Stops if IP is not from Bangladesh

2. **Playlist Fetching**: Downloads M3U8 files from `sources.txt`

3. **Channel Testing**: For each channel:
   - Makes HEAD request through Bangladeshi proxy
   - Removes if: 403 Forbidden, 504 Gateway Timeout, Connection Error, or Timeout
   - Keeps if: 200 OK or redirects work

4. **Output**: Creates `merged.m3u` with only Bangladesh-available channels

## File Structure

```
merge.py              # Main script
merged.m3u           # Output playlist (generated)
sources.txt          # Input playlist URLs
requirements.txt     # Python dependencies
.github/workflows/   # GitHub Actions configuration
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Manual Run
```bash
python merge.py
```

### GitHub Actions
- Automatically runs every 6 hours
- Can also trigger manually via **Actions** tab
- Updates `merged.m3u` when changes occur

## Troubleshooting

### Error: "Bangladesh IP verification failed"

**Problem**: Script detected non-Bangladesh IP

**Solution**:
1. Check if proxy is set: `echo $HTTP_PROXY`
2. Verify proxy works: `curl --proxy $HTTP_PROXY http://api.ipify.org`
3. Get proxy country:
   ```bash
   IP=$(curl -s --proxy $HTTP_PROXY http://api.ipify.org)
   curl -s http://ip-api.com/json/$IP
   ```
4. Use a proxy that returns Bangladesh IP

### Script exits without filtering channels

**Problem**: No working Bangladeshi proxy found

**Solution**:
- For GitHub Actions: Add `BANGLADESHI_PROXY` secret with valid Bangladesh proxy
- For local: Set `HTTP_PROXY` to a working Bangladesh proxy

### Few channels in output

This is expected behavior! The script:
- Only keeps channels available FROM Bangladesh
- Removes channels blocked in Bangladesh
- Removes unresponsive or timeout channels
- Result: Only truly accessible channels remain

## Support

### Finding Bangladeshi Proxies

- Search for "Bangladesh proxy lists" online
- Check proxy websites: `proxy-list.download`, `free-proxy-list.net`
- Verify proxy returns Bangladesh IP before using

### Proxy Testing

```bash
# Test if proxy works
curl --proxy http://PROXY_IP:PORT http://api.ipify.org

# Verify it's Bangladesh
curl -s http://ip-api.com/json/RESULT_IP
```

Look for `"countryCode":"BD"` in response.

## License

MIT