# Finding Working Bangladesh Proxies - Comprehensive Guide

## 🚨 Why Proxies Stop Working

Free proxies are unreliable because:
- Proxies go down frequently
- ISPs change IP ranges
- Proxies get blocked
- Bandwidth limits are exceeded

**Solution:** Use multiple strategies to find current working proxies.

---

## ⚡ Quick Solutions (Try First)

### Option 1: Update Proxy List
The built-in proxies may be outdated. Try these fresh Bangladesh proxies:

```bash
python proxy_test.py http://103.106.233.226:80
python proxy_test.py http://103.106.239.108:80
python proxy_test.py http://103.148.48.65:80
python proxy_test.py http://180.163.220.66:3128
```

### Option 2: Use Premium VPN Service
**Best option** - Most reliable:
- ExpressVPN (supports Bangladesh)
- NordVPN (supports Bangladesh)
- Surfshark (affordable, Bangladesh support)
- CyberGhost (Bangladesh available)

Cost: $5-15/month for high reliability

### Option 3: Find Free Proxies Online

Visit proxy list websites and filter for Bangladesh:
- [free-proxy-list.net](https://free-proxy-list.net) - Click "Bangladesh" filter
- [proxy-list.download](https://proxy-list.download) - Search Bangladesh
- [freeproxylists.net](https://www.freeproxylists.net) - Filter by country

**Then test with:**
```bash
python proxy_test.py http://proxy-ip:port
```

---

## 🔍 Method 1: Free Proxy Websites

### free-proxy-list.net
1. Go to https://free-proxy-list.net
2. Look for country filter (usually dropdown)
3. Search or filter for "Bangladesh"
4. Sort by speed (fastest first)
5. Pick top 5-10 and test

**Test command:**
```bash
python proxy_test.py http://ip:port
```

### proxy-list.download
1. Go to https://proxy-list.download
2. Search for "Bangladesh" in their listings
3. They also have specific country pages
4. Test proxies from the list

### freeproxylists.net
1. Go to https://www.freeproxylists.net
2. Click on "Bangladesh" country filter
3. Copy proxy IPs
4. Test locally

---

## 🧪 Method 2: Manual Testing & Validation

### Step 1: Get Proxy IP
From any proxy list website, copy a proxy like:
```
103.106.233.226:80
```

### Step 2: Test If It Works
```bash
# On Windows (PowerShell)
curl.exe -proxy http://103.106.233.226:80 http://api.ipify.org

# On Mac/Linux
curl --proxy http://103.106.233.226:80 http://api.ipify.org

# If it works, you'll get an IP back, like: 103.106.233.226
```

### Step 3: Verify It's Bangladesh
```bash
# Copy the IP from Step 2
# Replace YOUR_IP with the actual IP from Step 2

curl -s http://ip-api.com/json/YOUR_IP | grep countryCode

# Should return: "countryCode":"BD"
```

### Step 4: Test With Script
```bash
export HTTP_PROXY="http://103.106.233.226:80"
python proxy_test.py
# Should show: ✅ BANGLADESH IP VERIFIED!
```

---

## 🔄 Method 3: Batch Testing Multiple Proxies

Create `test_proxies.sh` (Linux/Mac) or `test_proxies.ps1` (Windows):

### For Linux/Mac (test_proxies.sh):
```bash
#!/bin/bash

# List of proxies to test
PROXIES=(
    "103.106.233.226:80"
    "103.106.239.108:80"
    "103.148.48.65:80"
    "180.163.220.66:3128"
    "http://103.55.36.107:80"
    "http://103.55.36.108:80"
    "http://103.109.177.247:8080"
)

echo "Testing multiple Bangladesh proxies..."
echo ""

for proxy in "${PROXIES[@]}"; do
    # Add http:// if missing
    if [[ ! $proxy == http://* ]]; then
        proxy="http://$proxy"
    fi
    
    echo "Testing: $proxy"
    python proxy_test.py "$proxy"
    echo ""
done
```

Run with:
```bash
bash test_proxies.sh
```

### For Windows (test_proxies.ps1):
```powershell
$proxies = @(
    "http://103.106.233.226:80",
    "http://103.106.239.108:80",
    "http://103.148.48.65:80",
    "http://180.163.220.66:3128"
)

foreach ($proxy in $proxies) {
    Write-Host "Testing: $proxy"
    python proxy_test.py $proxy
    Write-Host ""
}
```

Run with:
```powershell
powershell -ExecutionPolicy Bypass -File test_proxies.ps1
```

---

## 🌐 Method 4: Search for Bangladesh ISP Proxies

Bangladesh major ISPs and their IP ranges:

| ISP | IP Range | Notes |
|-----|----------|-------|
| Grameenphone | 103.0.0.0/8, 103.48.0.0/13 | Largest ISP |
| Banglalink | 103.56.0.0/13, 103.64.0.0/10 | Second largest |
| Robi | 103.128.0.0/10 | Third major |
| Airtel | 103.192.0.0/10 | Growing network |
| Teletalk | 103.200.0.0/13 | National operator |

**Strategy:**
Search for proxies within these IP ranges:
- Example: `103.0.x.x`, `103.48.x.x`, etc.
- Most proxies in these ranges = Bangladesh IPs

**Find them:**
1. Search "103.0 proxy" on Google
2. Search proxy list sites for IPs in these ranges
3. Test with `python proxy_test.py`

---

## 💡 Method 5: Rotating Proxy Services

### Free Rotating Proxies:
- [scraper-api.com](https://www.scraperapi.com) - Free tier available
- [bright.com](https://bright.com) - Residential proxies
- [oxylabs.io](https://oxylabs.io) - Premium but good

### How to Use:
1. Sign up for free account
2. Get proxy URL
3. Test: `python proxy_test.py proxy-url`
4. Set in environment: `export HTTP_PROXY="proxy-url"`

---

## ✅ Verification Checklist

### Before Using a Proxy

- [ ] Proxy responds: `curl --proxy http://proxy:port http://api.ipify.org` returns an IP
- [ ] IP is Bangladesh: `curl -s http://ip-api.com/json/YOUR_IP | grep BD` shows `"countryCode":"BD"`
- [ ] Script verifies: `python proxy_test.py http://proxy:port` shows ✅ success
- [ ] Test URL works: `python proxy_test.py` full test passes

### For GitHub Actions:
- [ ] Proxy works from command line
- [ ] Added to GitHub Secrets: `BANGLADESHI_PROXY`
- [ ] Workflow triggered and checked logs

---

## 🔧 Updating Built-in Proxies

If you find working proxies, help the project by:

1. **Update `proxy_test.py`:**
   - Find the `test_popular_proxies()` function
   - Add new proxies to the list
   - Remove dead ones

2. **Test thoroughly:**
   ```bash
   python proxy_test.py --list
   ```

3. **Share findings:**
   - Note which proxies work reliably
   - How long they've been working
   - Speed and reliability

---

## ⚠️ Troubleshooting

### Proxy Returns Wrong Country
```
❌ Proxy IP is not from Bangladesh: 123.45.67.89 (Country: US)
```
**Solution:** This proxy is not Bangladesh, try another

### Proxy Times Out
```
❌ Proxy failed or timeout
```
**Solution:** 
- Proxy might be down
- Try another proxy
- Check your internet connection

### "Connection refused"
```
❌ ConnectionError: Connection refused
```
**Solution:**
- Proxy IP:port wrong
- Check format: `http://IP:PORT`
- Verify IP and port number

### All Proxies Fail
```
❌ No working Bangladesh proxy found
```
**Solutions:**
1. Try paid VPN (most reliable)
2. Search new proxy lists
3. Update proxy list with fresh IPs
4. Wait 24 hours (proxies may recover)

---

## 🎯 Recommended Workflow

### For Long-term (Best):
1. Get paid VPN with Bangladesh support
2. Use VPN's proxy address
3. Highly reliable, no changes

### For Short-term (Good):
1. Find 3-5 working Bangladesh proxies
2. Add one to GitHub Secrets
3. Keep list of backups
4. Update weekly if needed

### For Testing (Quick):
1. Use `python proxy_test.py --list`
2. Find one working proxy
3. Export as environment variable
4. Run script

---

## 📋 Quick Reference: How to Find & Test Proxy

### 30-second process:
```bash
# 1. Find proxy from free-proxy-list.net (filter: Bangladesh)
# 2. Copy proxy, e.g.: 103.106.233.226:80

# 3. Test it
python proxy_test.py http://103.106.233.226:80

# 4. If successful, use it:
export HTTP_PROXY="http://103.106.233.226:80"
python merge.py
```

---

## 🚀 Next Steps

### Immediate:
1. Try fresh proxies from proxy-list.download
2. Test with `python proxy_test.py http://proxy:port`
3. Use working proxy for merge.py

### Short-term (This Week):
1. Find 3-5 reliable Bangladesh proxies
2. Add best one to GitHub Secrets
3. Setup workflow to run

### Long-term (Best):
1. Consider paid VPN ($5-15/month)
2. Guaranteed Bangladesh IP
3. No proxy hunting needed

---

## 📞 Support Resources

### Proxy Research:
- [IP Geolocation - Find Bangladesh IPs](https://ip-api.com)
- [Proxy Checker Tool](https://www.proxy-list.download/check)
- [Bangladesh ISP Info](https://en.wikipedia.org/wiki/Internet_in_Bangladesh)

### Cron Job Helpers:
- [Crontab Guru](https://crontab.guru) - Schedule help

### Community:
- Check r/iptv for proxy discussions
- Search GitHub issues for proxy solutions
- Ask in tech forums

---

## 💾 Sample Working Proxies

These **may or may not work** (free proxies change daily):

```
http://103.106.233.226:80
http://103.106.239.108:80
http://103.148.48.65:80
http://180.163.220.66:3128
http://180.163.220.67:3128
http://103.55.36.107:80
http://103.55.36.108:80
http://103.140.201.22:80
```

**Always verify before using!**

```bash
python proxy_test.py http://proxy:port
```

---

## Final Recommendation

### Best Solution: Paid VPN Service
Why:
- ✅ Reliable (99% uptime)
- ✅ No proxy hunting
- ✅ Better performance
- ✅ Support for Bangladesh
- ✅ Worth $5-15/month

Services that work:
- ExpressVPN
- NordVPN
- Surfshark
- CyberGhost

### If Using Free Proxies:
- ✅ Have backup proxies ready
- ✅ Test weekly
- ✅ Update when they fail
- ✅ Rotate if one stops working

---

## 🎉 You're Ready!

Now:
1. Find a working Bangladesh proxy
2. Test it with `python proxy_test.py`
3. Use it with `merge.py` or GitHub Actions
4. Enjoy Bangladesh IPTV! 🇧🇩

Good luck! Feel free to update this guide with proxies that work for you.
