# IPTV Merge with Bangladesh IP Filter

This project automatically merges multiple IPTV M3U8 playlist files and filters channels to only include those accessible from Bangladeshi IP addresses.

## Features

✅ **Automatic Bangladesh IP Filtering** - Only includes channels accessible from Bangladesh IPs
✅ **Multi-file Support** - Merges multiple M3U8 files
✅ **Duplicate Removal** - Removes duplicate streams
✅ **GitHub Actions Integration** - Automatic scheduled updates
✅ **Availability Checking** - Verifies channel accessibility
✅ **Proxy Support** - Configurable proxy for Bangladesh region

## Setup Instructions

### 1. **Bangladeshi Proxy Configuration**

You have several options to set up Bangladeshi IP/proxy access:

#### Option A: Using a Bangladeshi VPN Service (Recommended)

Install a VPN with Bangladesh servers:
- **SurfShark** - Affordable, fast Bangladesh servers
- **ExpressVPN** - Reliable, good for streaming
- **Hotspot Shield** - Free tier available
- **ProtonVPN** - Free tier with server options

#### Option B: Using a Bangladeshi Proxy

1. Find a Bangladesh proxy service:
   ```
   - http://bd-proxy.example.com:8080
   - Use dedicated proxy providers
   - Check for free proxy lists (note: less reliable)
   ```

2. Set environment variables:
   ```bash
   export BD_PROXY_HTTP="http://proxy.bd.example:8080"
   export BD_PROXY_HTTPS="http://proxy.bd.example:8080"
   export USE_BD_PROXY="true"
   ```

#### Option C: For GitHub Actions - Use GitHub Secrets

1. Go to your repository: **Settings → Secrets and variables → Actions**
2. Add new secrets:
   - `BD_PROXY_HTTP` = Your Bangladesh proxy HTTP URL
   - `BD_PROXY_HTTPS` = Your Bangladesh proxy HTTPS URL
   - `VPN_PROVIDER_CONFIG` = VPN configuration (optional)

3. Update `.github/workflows/merge.yml` to use secrets:
   ```yaml
   - name: Configure Bangladesh Proxy
     env:
       BD_PROXY_HTTP: ${{ secrets.BD_PROXY_HTTP }}
       BD_PROXY_HTTPS: ${{ secrets.BD_PROXY_HTTPS }}
     run: |
       export BD_PROXY_HTTP=${{ secrets.BD_PROXY_HTTP }}
       export BD_PROXY_HTTPS=${{ secrets.BD_PROXY_HTTPS }}
   ```

### 2. **Local Setup**

Install dependencies:
```bash
pip install -r requirements.txt
```

Create `requirements.txt`:
```
requests>=2.31.0
pysocks>=1.7.1
```

### 3. **Running Locally**

With proxy:
```bash
export BD_PROXY_HTTP="http://your-bangladesh-proxy:8080"
export BD_PROXY_HTTPS="http://your-bangladesh-proxy:8080"
export USE_BD_PROXY="true"
python merge.py
```

Without proxy (test mode):
```bash
python merge.py
```

### 4. **GitHub Actions Setup**

The workflow runs automatically:
- **Every 6 hours** (configurable via cron)
- **On push to main/master branch**
- **Manual trigger** (via workflow_dispatch)

To configure:

1. **Using Secrets (Recommended):**
   ```yaml
   env:
     BD_PROXY_HTTP: ${{ secrets.BD_PROXY_HTTP }}
     BD_PROXY_HTTPS: ${{ secrets.BD_PROXY_HTTPS }}
   ```

2. **Using Direct Proxy:**
   Edit `.github/workflows/merge.yml` and set:
   ```yaml
   - name: Get Bangladesh Proxy
     run: |
       echo "BD_PROXY=http://your-proxy:8080" >> $GITHUB_ENV
   ```

3. **Using Docker with VPN:**
   Add to workflow:
   ```yaml
   - name: Setup VPN Container
     uses: myoung34/docker-container@0
     with:
       image: dperson/openvpn-client
       # ... VPN configuration
   ```

## Bangladesh Proxy Providers

### Free Options (Less Reliable):
- [Free Proxy List](https://www.freeproxylists.net/)
- [ProxyMesh](https://proxymesh.com/) - Trial available
- [Oxylabs](https://oxylabs.io/) - Free trial

### Paid Options (Recommended):
- **SurfShark VPN** - $2.49/month (best value)
- **ExpressVPN** - $6.67/month (most reliable)
- **Bright Data** - Residential proxies with BD IPs
- **Oxylabs** - Premium proxy service with Bangladesh nodes

## Environment Variables

```bash
# Required
BD_PROXY_HTTP       # Bangladesh HTTP proxy URL
BD_PROXY_HTTPS      # Bangladesh HTTPS proxy URL
USE_BD_PROXY        # Set to 'true' to enable proxy filtering

# Optional
TIMEOUT             # Connection timeout in seconds (default: 10)
```

## Output Files

- `merged.m3u` - Merged and filtered M3U8 playlist
- `sources.txt` - Channel information and source URLs

## Troubleshooting

### "No channels available for Bangladesh"
- Check proxy configuration is correct
- Verify proxy can access the internet
- Test proxy manually: `curl -x your-proxy https://example.com`
- Try with a different proxy service

### Workflow fails in GitHub Actions
- Add `BD_PROXY_HTTP` and `BD_PROXY_HTTPS` secrets
- Check proxy is reachable from GitHub's IP range
- Use a residential proxy (datacenter proxies may be blocked)
- Check workflow logs for specific error messages

### Channels still not filtered correctly
- Ensure proxy is actually from Bangladesh
- Verify with: `curl -x proxy https://api.ipify.org`
- Check channel URLs are accessible
- Increase timeout if connections are slow

## Script Details

### merge.py

The merge script:
1. Reads all M3U8 files in the current directory
2. Extracts channel information and URLs
3. Removes duplicates based on URL
4. Filters channels by testing accessibility via Bangladesh proxy
5. Writes filtered results to `merged.m3u` and `sources.txt`

Features:
- Configurable proxy support
- Connection timeout handling
- Progress indicators
- Error logging
- User-agent rotation for blocking prevention

## Examples

### Running with SurfShark VPN

```bash
# Connect VPN first via SurfShark app
# Then run:
python merge.py
```

### Running with ExpressVPN

```bash
# Via command line (ExpressVPN CLI):
expressvpn connect Bangladesh
python merge.py
expressvpn disconnect
```

### Running with HTTP Proxy

```bash
export BD_PROXY_HTTP="http://bangladesh-proxy.example.com:8080"
export BD_PROXY_HTTPS="http://bangladesh-proxy.example.com:8080"
export USE_BD_PROXY="true"
python merge.py
```

## Notes

- The script respects `.gitignore` for temporary files
- Channels are validated by attempting HTTP HEAD requests
- Rate limiting is applied during checking (0.2s between requests)
- Local streams (non-HTTP) are assumed available
- Proxy support is optional - works without proxy but may not filter correctly

## License

This project is provided as-is for educational and personal use.

## Support

For issues with:
- **Script errors** - Check Python version >= 3.8
- **Proxy issues** - Verify proxy credentials and availability
- **GitHub Actions** - Check workflow logs and secrets configuration
- **Channel filtering** - Ensure Bangladesh proxy/VPN is active

---

**Last Updated:** 2024
