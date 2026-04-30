# IPTV Bangladesh Filter - Setup Guide

## Quick Start

### ⚡ Minimum Requirements

1. **Bangladeshi IP Proxy**: Required for script to work
2. **Python 3.8+**: Local testing
3. **GitHub Account**: For automated workflow

### 🚀 Quick Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set proxy environment variables
export HTTP_PROXY="http://bangladeshi-proxy-ip:port"
export HTTPS_PROXY="http://bangladeshi-proxy-ip:port"

# 3. Run script
python merge.py

# 4. Check output
cat merged.m3u
```

---

## Detailed Setup

### Step 1: Find a Bangladesh Proxy

**Option A: Free Proxy Sites**
- [free-proxy-list.net](https://free-proxy-list.net) - Filter by Bangladesh
- [proxy-list.download](https://proxy-list.download) - Search Bangladesh proxies
- [proxyscrape.com](https://proxyscrape.com) - Filter by country

**Option B: Test an IP directly**
```bash
# Replace IP_ADDRESS:PORT with actual proxy
curl --proxy http://IP_ADDRESS:PORT http://api.ipify.org
# Should return an IP (if working)

# Then verify it's Bangladesh
IP=$(curl -s --proxy http://IP_ADDRESS:PORT http://api.ipify.org)
curl -s "http://ip-api.com/json/$IP" | grep countryCode
# Should show: "countryCode":"BD"
```

**Option C: Use Paid VPN Services**
- ExpressVPN, NordVPN, Surfshark - Most support Bangladesh
- Usually more reliable than free proxies

### Step 2: Test Your Proxy

```bash
#!/bin/bash
# Save as test_proxy.sh and run: bash test_proxy.sh

PROXY="http://103.125.31.222:80"  # Replace with your proxy

echo "Testing proxy: $PROXY"

# Test connectivity
IP=$(curl -s --max-time 5 --proxy "$PROXY" http://api.ipify.org)
echo "IP through proxy: $IP"

# Verify it's Bangladesh
COUNTRY=$(curl -s "http://ip-api.com/json/$IP?fields=country,countryCode,city,org")
echo "Location details: $COUNTRY"

# Check for Bangladesh
if echo "$COUNTRY" | grep -q '"countryCode":"BD"'; then
  echo "✅ Proxy is from Bangladesh!"
else
  echo "❌ Proxy is NOT from Bangladesh"
fi
```

### Step 3: Configure sources.txt

Edit `sources.txt` with playlist URLs (one per line):

```
https://iptvcat.com/my_list.m3u8
https://example.com/playlist.m3u8
https://another-site.com/iptv.m3u
```

### Step 4: Run Locally (Optional)

```bash
# Set proxy
export HTTP_PROXY="http://your-proxy:port"
export HTTPS_PROXY="http://your-proxy:port"

# Run
python merge.py

# Check results
ls -la merged.m3u
head -20 merged.m3u  # Preview output
```

### Step 5: Setup GitHub Actions

#### For GitHub Secrets (Recommended):

1. Go to repository: **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Create secret: `BANGLADESHI_PROXY`
   - Value: `http://your-proxy-ip:port`

#### For Built-in Proxies:

No setup needed! Workflow tests built-in proxies automatically.

---

## Detailed Configuration

### merge.py Options

Edit `merge.py` to customize:

```python
SOURCE_FILE = "sources.txt"      # Input playlist file
OUTPUT_FILE = "merged.m3u"       # Output filename
CHECK_TIMEOUT = 5                # Timeout in seconds
```

### Proxy Configuration

**Environment Variables:**
```bash
HTTP_PROXY="http://ip:port"      # HTTP proxy
HTTPS_PROXY="http://ip:port"     # HTTPS proxy (optional)
```

**For SOCKS5 Proxy:**
```bash
HTTP_PROXY="socks5://ip:port"
HTTPS_PROXY="socks5://ip:port"
```

---

## Understanding the Output

### Summary Report

```
✅ MERGE COMPLETED - BANGLADESHI CHANNELS ONLY
📺 Total channels kept: 245
🚫 403 Forbidden (not available in BD): 89
🌐 504 Gateway Timeout: 12
⏱️  Timeouts: 34
❌ Connection errors: 15
⏭️  PlayZ sponsored removed: 5
📊 Total streams checked: 400
📊 Final playlist entries: 245
```

### What Each Metric Means

- **channels kept**: ✅ Channels available in Bangladesh
- **403 Forbidden**: Channels blocked outside specific countries (removed)
- **504 Gateway Timeout**: Server errors (removed)
- **Timeouts**: Too slow to load (removed)
- **Connection errors**: Network issues (removed)

### merged.m3u Format

```
#EXTM3U
#EXTINF:-1 tvg-id="bnt.bd" tvg-name="BNT" tvg-logo="...",BNT
http://stream.bnt.com.bd/live/stream
#EXTINF:-1 tvg-id="ntv.bd" tvg-name="NTV" tvg-logo="...",NTV
http://stream.ntv.com.bd/live/stream
...
```

---

## Advanced Setup

### Custom Proxy Script

Create `find_proxy.sh` to automatically find working proxy:

```bash
#!/bin/bash

PROXIES=(
    "http://103.125.31.222:80"
    "http://103.144.182.1:3128"
    "http://103.105.187.38:8080"
    "http://180.163.200.242:3128"
)

echo "Finding working Bangladesh proxy..."

for proxy in "${PROXIES[@]}"; do
    echo -n "Testing $proxy ... "
    IP=$(timeout 3 curl -s --proxy "$proxy" http://api.ipify.org)
    
    if [ $? -eq 0 ] && [ ! -z "$IP" ]; then
        COUNTRY=$(curl -s "http://ip-api.com/json/$IP?fields=countryCode" | grep -o '"countryCode":"[^"]*"' | cut -d'"' -f4)
        
        if [ "$COUNTRY" = "BD" ]; then
            echo "✅ FOUND: $proxy"
            echo "export HTTP_PROXY=$proxy"
            echo "export HTTPS_PROXY=$proxy"
            exit 0
        fi
    fi
    echo "❌"
done

echo "No working Bangladesh proxy found"
exit 1
```

### Docker Usage

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY merge.py .
COPY sources.txt .

ENV HTTP_PROXY=""
ENV HTTPS_PROXY=""

CMD ["python", "merge.py"]
```

Build and run:
```bash
docker build -t iptv-merger .
docker run -e HTTP_PROXY="http://proxy:port" iptv-merger
```

---

## Troubleshooting

### Issue: "Bangladesh IP verification failed"

```
❌ ERROR: Bangladesh IP verification failed!
   The script will not proceed without a valid Bangladeshi proxy.
```

**Solutions:**
1. Check proxy is set: `echo $HTTP_PROXY`
2. Test proxy works: `curl --proxy $HTTP_PROXY http://api.ipify.org`
3. Verify it's Bangladesh: See "Test Your Proxy" section above

### Issue: GitHub Actions Keeps Failing

Check the workflow log:
1. Go to **Actions** tab
2. Click latest workflow run
3. Look for error in logs

**Common causes:**
- Proxy stopped working
- Network issues
- Invalid `sources.txt`

**Fix:**
- Update `BANGLADESHI_PROXY` secret with working proxy
- Test proxy manually first

### Issue: Very Few Channels in Output

This is **expected**! The script:
- Only keeps channels available FROM Bangladesh
- Many channels are geo-restricted
- Some servers block automated access

**Why:** You're getting ONLY channels that truly work in Bangladesh.

### Issue: Script Takes Too Long

**Solutions:**
- Increase `CHECK_TIMEOUT` in merge.py
- Reduce number of sources in `sources.txt`
- Run during off-peak hours

### Issue: "No proxy configured"

**For Local:**
```bash
export HTTP_PROXY="http://proxy-ip:port"
python merge.py
```

**For GitHub Actions:**
Add `BANGLADESHI_PROXY` secret (Settings → Secrets)

---

## Performance Tips

### Speed Up Script

1. **Increase timeout** (faster rejection of slow channels):
   ```python
   CHECK_TIMEOUT = 3  # Instead of 5
   ```

2. **Use faster proxy** (lower latency)

3. **Limit sources** (fewer URLs to process)

### Reduce false positives

1. **Decrease timeout** (more lenient):
   ```python
   CHECK_TIMEOUT = 7  # Instead of 5
   ```

2. **Use faster internet connection**

---

## Additional Resources

### IPTV Resources
- [IPTVCAT](https://iptvcat.com) - Large playlist database
- [M3U8 Format Spec](https://en.wikipedia.org/wiki/M3U) - Playlist format

### Proxy Resources
- [FreeProxyList](https://www.freeproxylists.net) - Proxy lists
- [ip-api.com](https://ip-api.com) - IP location lookup
- [ipify.org](https://api.ipify.org) - IP detection

### GitHub Resources
- [GitHub Actions Docs](https://docs.github.com/actions)
- [GitHub Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets)
- [Cron Syntax](https://crontab.guru) - Schedule syntax

---

## Support & FAQ

**Q: Can I use a VPN instead of proxy?**
A: Yes! Set `HTTP_PROXY` to your VPN's proxy address if available.

**Q: How often should I run this?**
A: Every 6 hours (default). Channels change, servers go down.

**Q: Will this work with all M3U8 files?**
A: Yes! Any standard M3U8 playlist format works.

**Q: Can I run multiple instances?**
A: Yes, but use different `sources.txt` and `OUTPUT_FILE`.

**Q: Is this legal?**
A: Script tests channel availability. Use only legal, authorized channels.

---

## Success Checklist

- [ ] Found working Bangladesh proxy
- [ ] Proxy tested and verified (returns BD country code)
- [ ] `sources.txt` contains valid M3U8 URLs
- [ ] `requirements.txt` installed (`pip install -r requirements.txt`)
- [ ] Script runs without "Bangladesh IP verification failed" error
- [ ] `merged.m3u` generated with channels
- [ ] GitHub Actions workflow enabled (if using automation)
- [ ] `BANGLADESHI_PROXY` secret added (if using workflow)

---

## Next Steps

1. ✅ Set up proxy
2. ✅ Configure `sources.txt`
3. ✅ Run `python merge.py`
4. ✅ Verify `merged.m3u` output
5. ✅ Import into IPTV player
6. ✅ Setup GitHub Actions (optional, for automation)

Enjoy your filtered IPTV playlist! 📺
