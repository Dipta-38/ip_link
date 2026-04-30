# IPTV Bangladesh Filter - Changes Summary

## 🎯 What Was Changed

Your `merge.py` script has been updated to **enforce Bangladesh IP filtering**. It now:

1. ✅ **Requires** a valid Bangladeshi IP proxy
2. ✅ **Verifies** the IP is actually from Bangladesh
3. ✅ **Refuses to run** if proxy doesn't provide Bangladesh IP
4. ✅ **Routes all requests** through the Bangladeshi proxy (both HTTP and HTTPS)
5. ✅ **Filters strictly** - removes channels that timeout or have errors

---

## 📁 Files Modified/Created

### Modified Files:
1. **`merge.py`** - Enhanced with Bangladesh IP verification
2. **`README.md`** - Updated with Bangladesh filtering documentation
3. **`.github/workflows/merge.yml`** - Enhanced workflow with proxy detection

### New Files Created:
1. **`SETUP_GUIDE.md`** - Complete setup instructions
2. **`proxy_test.py`** - Tool to test if your proxy works
3. **`CHANGES.md`** - This file

---

## 🚀 Quick Start

### For Local Use:

```bash
# 1. Find/test a Bangladesh proxy
python proxy_test.py --list

# 2. Set proxy environment variables
export HTTP_PROXY="http://proxy-ip:port"
export HTTPS_PROXY="http://proxy-ip:port"

# 3. Run script
python merge.py
```

### For GitHub Actions:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `BANGLADESHI_PROXY`
4. Value: `http://proxy-ip:port`
5. Workflow will automatically test and use the proxy

---

## 🔑 Key Changes in merge.py

### Before:
```python
# Old: Optional proxy, not enforced
HTTP_PROXY = os.environ.get('HTTP_PROXY')
proxies = {'http': HTTP_PROXY}  # HTTPS ignored

# Old: Loose verification
def verify_ip():
    # Only checked if proxy was set
    # Accepted any country
```

### After:
```python
# New: Both HTTP and HTTPS proxy support
HTTP_PROXY = os.environ.get('HTTP_PROXY')
HTTPS_PROXY = os.environ.get('HTTPS_PROXY', HTTP_PROXY)
proxies = {
    'http': HTTP_PROXY,
    'https': HTTPS_PROXY if HTTPS_PROXY else HTTP_PROXY,
}

# New: Strict Bangladesh verification
def verify_bangladesh_ip():
    # REQUIRED - script won't run without it
    # Verifies country code is "BD"
    # Refuses to continue if not Bangladesh
```

### Stream Checking:
```python
# Old: Accepted timeouts and errors as "available"
if response.status_code == 403: return False
if response.status_code == 504: return False
return True  # Timeouts/errors were "available"

# New: Stricter - timeouts mean unavailable
if response.status_code == 403: return False, "403"
if response.status_code == 504: return False, "504"
return False, "timeout"  # Timeouts = not available
```

---

## 🔧 Updated Workflow (.github/workflows/merge.yml)

### New Features:
1. **Multiple proxy testing** - Tests 4 built-in Bangladesh proxies
2. **GitHub Secrets support** - Uses `BANGLADESHI_PROXY` secret if available
3. **Country verification** - Confirms each proxy is from Bangladesh
4. **Better error messages** - Clear feedback if no proxy works

### How it works:
```yaml
# 1. Tries built-in proxies
# 2. If none work, tries GitHub secret
# 3. Verifies IP is from Bangladesh
# 4. Only runs script if proxy verified
# 5. Fails clearly if no proxy works
```

---

## 🛠️ New Tools

### proxy_test.py
Test if your proxy works:

```bash
# Test specific proxy
python proxy_test.py http://103.125.31.222:80

# Test from environment variable
export HTTP_PROXY="http://proxy-ip:port"
python proxy_test.py

# Test built-in popular proxies
python proxy_test.py --list
```

---

## 📊 Example Output

### Old (Before):
```
🚀 IPTV MERGER
⚠️ Running without proxy

📺 Total channels kept: 340
🚫 403 Forbidden removed: 15
```
❌ Problems:
- No proxy verification
- Includes channels from anywhere
- Timeouts treated as "working"

### New (After):
```
🚀 IPTV MERGER - BANGLADESH IP FILTER
✅ ✓ Using BANGLADESHI IP - Ready to filter channels

📺 Total channels kept: 120
🚫 403 Forbidden (not available in BD): 89
🌐 504 Gateway Timeout: 12
⏱️  Timeouts: 34
❌ Connection errors: 15
📊 Total streams checked: 400
```
✅ Benefits:
- Verified Bangladesh IP
- Only Bangladesh channels
- Strict availability checking
- Only ~120 channels = high quality

---

## ⚙️ Configuration

### Environment Variables:
```bash
# Required
HTTP_PROXY="http://bangladesh-proxy:port"

# Optional (defaults to HTTP_PROXY if not set)
HTTPS_PROXY="http://bangladesh-proxy:port"
```

### Script Settings (merge.py):
```python
SOURCE_FILE = "sources.txt"      # Input playlists
OUTPUT_FILE = "merged.m3u"       # Output playlist
CHECK_TIMEOUT = 5                # Timeout in seconds
```

---

## ❌ What Happens If No Bangladesh IP?

Script **refuses to run**:

```
❌ ERROR: Bangladesh IP verification failed!
   The script will not proceed without a valid Bangladeshi proxy.

   To fix this:
   1. Set HTTP_PROXY environment variable with Bangladeshi proxy
   2. Set HTTPS_PROXY environment variable with Bangladeshi proxy
   3. Verify proxy is accessible and provides Bangladesh IP
```

---

## ✅ Success Indicators

### Script runs correctly:
- ✅ "Using BANGLADESHI IP - Ready to filter"
- ✅ Creates merged.m3u with channels
- ✅ All channels are from Bangladesh

### Workflow succeeds:
- ✅ GitHub Actions shows green checkmark
- ✅ merged.m3u auto-updated
- ✅ Runs every 6 hours automatically

---

## 🔍 Troubleshooting

### "Bangladesh IP verification failed"
→ Proxy doesn't return Bangladesh IP
→ Use `python proxy_test.py` to find working proxy

### "No proxy configured"
→ Set `HTTP_PROXY` environment variable
→ For GitHub: Add `BANGLADESHI_PROXY` secret

### Very few channels
→ Normal! Only Bangladesh-available channels kept
→ This is the correct behavior

### Workflow keeps failing
→ Check if `BANGLADESHI_PROXY` secret is set
→ Make sure proxy IP is currently working
→ Run `python proxy_test.py` to verify

---

## 📚 Documentation

- **README.md** - Overview and quick start
- **SETUP_GUIDE.md** - Detailed setup instructions
- **CHANGES.md** - This file (what changed)
- **merge.py** - Script with Bangladesh filtering
- **proxy_test.py** - Proxy testing tool

---

## 🎓 Learning More

### Finding Bangladesh Proxies:
- [free-proxy-list.net](https://free-proxy-list.net) - Filter by country
- [proxy-list.download](https://proxy-list.download)
- Search: "Bangladesh proxy list"

### Testing Proxies Manually:
```bash
# Get IP through proxy
curl --proxy http://proxy-ip:port http://api.ipify.org

# Check country
curl -s http://ip-api.com/json/[result-ip]
# Look for: "countryCode":"BD"
```

---

## ⚡ Next Steps

1. **Find a working Bangladesh proxy**
   ```bash
   python proxy_test.py --list
   ```

2. **Test it works**
   ```bash
   export HTTP_PROXY="http://proxy-ip:port"
   python proxy_test.py
   ```

3. **Run script locally**
   ```bash
   python merge.py
   ```

4. **Setup GitHub Actions** (optional)
   - Add `BANGLADESHI_PROXY` secret in GitHub Settings

5. **Monitor results**
   - Check `merged.m3u` has channels
   - Verify workflow runs every 6 hours

---

## 💡 Pro Tips

- **Test multiple proxies** - Some work better than others
- **Use faster proxies** - Speeds up channel checking
- **Monitor workflow** - Check GitHub Actions for success/failures
- **Update sources** - Add new playlist URLs to `sources.txt`
- **Adjust timeout** - Increase if getting many timeouts

---

## ❓ FAQ

**Q: Why does the script require Bangladesh IP?**
A: To ensure you only get channels available in Bangladesh.

**Q: Can I use a VPN?**
A: Yes, if it provides a proxy interface.

**Q: How often does it run?**
A: Every 6 hours (configurable in workflow).

**Q: Why so few channels in output?**
A: By design - only truly available channels from Bangladesh.

---

## 🎉 You're All Set!

Your IPTV merger now properly filters for Bangladesh! 🇧🇩

Next: Find a Bangladesh proxy and run `python merge.py`

Questions? Check SETUP_GUIDE.md or README.md
