# 🚨 Emergency Guide: All Proxies Failed

When you see this error:
```
❌ ERROR: No working Bangladeshi proxy found!
⚠️  Please set BANGLADESHI_PROXY in GitHub Secrets
Error: Process completed with exit code 1.
```

It means all built-in proxies are down or unreachable.

---

## ⚡ Quick Fix (5 minutes)

### Step 1: Find a Fresh Bangladesh Proxy

Go to **[free-proxy-list.net](https://free-proxy-list.net)** and:
1. Look for country filter/dropdown
2. Search for "Bangladesh" or filter by country
3. Sort by "Speed" (fastest first)
4. Copy a proxy like: `103.x.x.x:8080`

### Step 2: Test Your Proxy Locally

Open terminal and run:

```bash
# For Windows (PowerShell)
curl.exe -proxy http://103.x.x.x:8080 http://api.ipify.org

# For Mac/Linux
curl --proxy http://103.x.x.x:8080 http://api.ipify.org

# Replace 103.x.x.x:8080 with your actual proxy
```

If successful, you'll see an IP address returned.

### Step 3: Verify It's Bangladesh

Replace `YOUR_IP` with the IP from Step 2:

```bash
curl -s http://ip-api.com/json/YOUR_IP | grep countryCode
# Should show: "countryCode":"BD"
```

### Step 4: Add to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `BANGLADESHI_PROXY`
5. Value: `http://103.x.x.x:8080` (your working proxy)
6. Click **Add secret**

### Step 5: Trigger Workflow

1. Go to **Actions** tab
2. Click "IPTV Auto Merge - Bangladesh Filter"
3. Click **Run workflow** button
4. Should now work! ✅

---

## 🧪 Test Locally First (Recommended)

Before updating GitHub, test the script locally:

```bash
# Step 1: Export proxy
export HTTP_PROXY="http://your-proxy:port"

# Step 2: Run test
python proxy_test.py
# Should show: ✅ BANGLADESH IP VERIFIED!

# Step 3: Run script
python merge.py
# Should complete successfully
```

If it works locally, add to GitHub Secrets.

---

## 🔄 Batch Testing (Find Multiple Proxies)

To test many proxies at once:

```bash
python batch_proxy_test.py
# Shows all working proxies with IPs
# Pick one and use it
```

---

## 📋 Proxy Websites (Bookmark These!)

Use these to find fresh Bangladesh proxies:

1. **[free-proxy-list.net](https://free-proxy-list.net)**
   - Filter by Bangladesh
   - Usually reliable
   - Updated daily

2. **[proxy-list.download](https://proxy-list.download)**
   - Separate Bangladesh page
   - Good uptime
   - Multiple format options

3. **[freeproxylists.net](https://www.freeproxylists.net)**
   - Easy to use
   - Sort by country
   - Basic filtering

4. **[proxyscrape.com](https://proxyscrape.com)**
   - API available
   - Real-time updates
   - Advanced filtering

---

## 🎯 Quick Bangladesh IP Ranges

When searching proxy websites, look for these IP ranges (Bangladesh ISPs):

```
103.0.x.x       - Grameenphone
103.48.x.x      - Banglalink  
103.56.x.x      - Banglalink
103.64.x.x      - Banglalink
103.106.x.x     - Various ISPs
103.140.x.x     - Various ISPs
103.141.x.x     - Various ISPs
103.144.x.x     - Various ISPs
180.163.x.x     - Teletalk/Others
```

Proxies in these ranges are likely Bangladesh IPs!

---

## ✅ Step-by-Step Troubleshooting

### Issue: Found proxy but it fails

```
❌ Proxy failed or timeout
```

**Solutions:**
1. Proxy might be down - try another from the list
2. Port might be wrong - check format: `http://ip:port`
3. Your ISP might block it - try different proxy
4. Test with: `python proxy_test.py http://ip:port`

### Issue: Proxy works locally but fails on GitHub

**Solutions:**
1. GitHub might have different network rules
2. Proxy might be blocking GitHub's IP range
3. Try different proxy
4. Some proxies only work from Bangladesh IP range (catch-22!)

### Issue: Can't find ANY working proxies

**Solutions:**
1. **Use paid VPN** ($5-15/month) - Most reliable
   - ExpressVPN (supports Bangladesh)
   - NordVPN (supports Bangladesh)
   - Surfshark (cheap, Bangladesh support)
   
2. **Try different proxy sites**
   - Proxyscrape might have different proxies
   - Wait 24 hours - new proxies appear
   
3. **Use a rotating proxy service**
   - Bright.com
   - Oxylabs
   - Scraperapi

### Issue: GitHub Actions still fails after adding secret

**Troubleshooting:**
1. Make sure secret is named exactly: `BANGLADESHI_PROXY`
2. Test proxy locally first: `python proxy_test.py`
3. Check workflow logs for specific error
4. Try triggering workflow manually: Actions → Run workflow

---

## 🛠️ Tools Available

You have these tools to find and test proxies:

```bash
# Test single proxy
python proxy_test.py http://ip:port

# Test from environment variable
export HTTP_PROXY="http://ip:port"
python proxy_test.py

# Batch test many proxies at once
python batch_proxy_test.py

# Batch test with custom thread count
python batch_proxy_test.py --threads 10

# Run with single thread (more stable)
python batch_proxy_test.py --quick
```

---

## 📈 When Proxies Frequently Go Down

If you're constantly having this issue:

### Recommended: Use Paid VPN
- **Cost:** $5-15/month
- **Reliability:** 99%+ uptime
- **No hassle:** Set and forget
- **Best options:** ExpressVPN, NordVPN, Surfshark

### If Using Free Proxies:
- Keep 3-5 backup proxies
- Test weekly: `python proxy_test.py --list`
- Update secret when one fails
- Have batch test ready to find new ones

---

## 💾 Recent Working Proxies (Apr 2026)

Try these if currently down:

```bash
python proxy_test.py http://103.106.233.226:80
python proxy_test.py http://103.106.239.108:80
python proxy_test.py http://103.148.48.65:80
python proxy_test.py http://180.163.220.66:3128
```

---

## 🚀 Your Action Plan

1. **Right now (5 min):**
   - Go to free-proxy-list.net
   - Filter for Bangladesh
   - Copy a proxy
   - Test locally: `python proxy_test.py http://proxy:port`

2. **Within 30 min:**
   - Add working proxy to GitHub Secrets
   - Trigger workflow manually
   - Verify it works

3. **This week:**
   - Find 2-3 backup proxies
   - Test and document them
   - Keep list updated

4. **Next month:**
   - Consider switching to paid VPN
   - Never worry about proxy again
   - Guaranteed Bangladesh IP

---

## 📞 Still Having Issues?

Check these files:
- **[FIND_PROXIES.md](FIND_PROXIES.md)** - Comprehensive proxy finding guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Full setup instructions
- **[README.md](README.md)** - Overview and troubleshooting

Or try:
```bash
python batch_proxy_test.py
```

---

## 🎉 You Got This!

The solution is simple:
1. Find a Bangladesh proxy
2. Test it works
3. Add to GitHub or use locally
4. Done!

**Good luck! 🇧🇩**
