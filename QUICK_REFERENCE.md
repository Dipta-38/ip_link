# Quick Reference Card

## 🚨 Proxy Problem? Do This NOW

```
1️⃣  Run: python batch_proxy_test.py
2️⃣  Copy a working proxy from output
3️⃣  Run: export HTTP_PROXY="http://proxy:port"
4️⃣  Run: python merge.py
5️⃣  Done! ✅
```

**Total time:** 5-10 minutes

---

## 🛠️ Essential Commands

```bash
# Find working proxies (automatic)
python batch_proxy_test.py

# Test single proxy
python proxy_test.py http://ip:port

# Paste proxies from list
python import_proxies.py

# Run script with proxy
export HTTP_PROXY="http://ip:port"
python merge.py

# Test from environment
export HTTP_PROXY="http://ip:port"
python proxy_test.py
```

---

## 🔗 Key URLs

| Site | Link | Notes |
|------|------|-------|
| Free Proxies | https://free-proxy-list.net | Filter: Bangladesh |
| Free Proxies 2 | https://proxy-list.download | Bangladesh section |
| IP Checker | https://ip-api.com | Check if Bangladesh |
| Cron Helper | https://crontab.guru | Schedule syntax |

---

## 📚 Documentation Quick Links

| Problem | Solution |
|---------|----------|
| "No proxy found" | Read: [PROXY_EMERGENCY_GUIDE.md](PROXY_EMERGENCY_GUIDE.md) |
| "How to find proxy" | Read: [FIND_PROXIES.md](FIND_PROXIES.md) |
| "How to setup" | Read: [SETUP_GUIDE.md](SETUP_GUIDE.md) |
| "GitHub Actions" | Read: [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) |
| All solutions | Read: [PROXY_SOLUTIONS.md](PROXY_SOLUTIONS.md) |

---

## ✅ Verification Steps

1. **Find proxy** → `python batch_proxy_test.py` ✅
2. **Test proxy** → `python proxy_test.py http://ip:port` ✅
3. **Set proxy** → `export HTTP_PROXY="http://ip:port"` ✅
4. **Run script** → `python merge.py` ✅
5. **Check output** → `cat merged.m3u` ✅

---

## 🇧🇩 Bangladesh IP Check

```bash
# Get your IP through proxy
curl --proxy http://ip:port http://api.ipify.org

# Replace YOUR_IP with result from above
# Should show: "countryCode":"BD"
curl -s http://ip-api.com/json/YOUR_IP
```

---

## 🎯 Bangladesh Proxy IP Ranges

Search for these in proxy lists:
```
103.0.x.x       103.106.x.x     103.140.x.x
103.48.x.x      103.141.x.x     103.144.x.x
103.56.x.x      180.163.x.x     103.148.x.x
```

---

## 💾 Recent Working Proxies (Try These First)

```bash
python proxy_test.py http://103.106.233.226:80
python proxy_test.py http://103.106.239.108:80
python proxy_test.py http://103.148.48.65:80
python proxy_test.py http://180.163.220.66:3128
python proxy_test.py http://103.140.201.22:80
```

---

## ⏱️ Setup Time Estimates

| Task | Time | Tools |
|------|------|-------|
| Find proxy | 5 min | batch_proxy_test.py |
| Test locally | 2 min | proxy_test.py |
| Run script | 5-30 min | merge.py |
| GitHub setup | 5 min | GitHub website |
| **TOTAL** | **20-50 min** | **All local** |

---

## 🆘 Emergency Solutions

| Issue | Solution |
|-------|----------|
| All proxies down | Use paid VPN ($5-15/mo) |
| Proxy test fails | Try: `python import_proxies.py` |
| Can't find proxy | Visit: free-proxy-list.net |
| Proxy is slow | Change timeout: `CHECK_TIMEOUT = 10` |
| GitHub Actions fails | Test proxy locally first |
| Few channels in output | Normal! Only verified ones kept |

---

## 🚀 GitHub Actions Quick Setup

1. Add secret: `BANGLADESHI_PROXY` = `http://ip:port`
2. Go to Actions → Run workflow
3. Done! ✅
4. Runs every 6 hours automatically

---

## 📞 Common Questions

**Q: Do I need to be in Bangladesh?**
A: No, just need Bangladesh IP proxy

**Q: Why does proxy keep failing?**
A: Free proxies change/go down - use paid VPN for stability

**Q: How often does it update?**
A: Every 6 hours (configurable)

**Q: Why so few channels?**
A: By design - only verified Bangladesh channels

**Q: Is this legal?**
A: Script tests availability. Use legal channels only.

---

## 🎯 Next Steps

### Immediate (Do This Now):
```bash
python batch_proxy_test.py
```

### Then:
```bash
export HTTP_PROXY="[proxy from above]"
python merge.py
```

### Optional (Automation):
Add `BANGLADESHI_PROXY` to GitHub Secrets

---

## 💡 Pro Tips

- Keep 2-3 backup proxies handy
- Test proxies weekly
- Consider paid VPN for reliability
- Use `batch_proxy_test.py` to find multiple
- Import proxies with `import_proxies.py`
- Check logs: `cat merged.m3u`

---

## 📋 File Reference

```
merge.py                      - Main script
merged.m3u                   - Output (auto-generated)
sources.txt                  - Input URLs (edit this)
proxy_test.py               - Test single proxy
batch_proxy_test.py         - Test many proxies
import_proxies.py           - Paste & test list
setup.sh                    - Automated setup
README.md                   - Overview
PROXY_EMERGENCY_GUIDE.md    - When proxies fail
FIND_PROXIES.md             - How to find proxies
SETUP_GUIDE.md              - Detailed setup
```

---

## 🎉 You're Ready!

**Running Bangladesh IPTV merger!**

1. ✅ Find proxy: `python batch_proxy_test.py`
2. ✅ Use proxy: `export HTTP_PROXY="..."`
3. ✅ Run script: `python merge.py`
4. ✅ Enjoy: `merged.m3u` ready!

---

**Questions?** See [PROXY_SOLUTIONS.md](PROXY_SOLUTIONS.md)
