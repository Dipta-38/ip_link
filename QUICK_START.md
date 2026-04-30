# IPTV Bangladesh Filter - Quick Reference Guide

## 📚 Documentation Index

### Getting Started
- **[README.md](README.md)** - Start here! Overview and quick start
- **[QUICK_START.md](QUICK_START.md)** - This file
- **[CHANGES.md](CHANGES.md)** - What was modified and why

### Setup & Configuration
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions (5-10 min read)
- **[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)** - GitHub Actions specific setup
- **[setup.sh](setup.sh)** - Automated setup script (Linux/Mac)

### Tools & Utilities
- **[proxy_test.py](proxy_test.py)** - Test if proxy works
- **[merge.py](merge.py)** - Main script (Bangladesh filtered)

### Source Configuration
- **[sources.txt](sources.txt)** - Edit this to add playlist URLs

---

## 🚀 Quick Start (Choose Your Path)

### Path 1: GitHub Actions (Automated)
Time: 2 minutes

```
1. Add GitHub Secret
2. Enable Actions
3. Done - runs automatically every 6 hours
```

**→ Go to: [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)**

---

### Path 2: Local Setup (Windows/Mac/Linux)
Time: 10 minutes

```bash
# 1. Find proxy
python proxy_test.py --list

# 2. Set proxy
export HTTP_PROXY="http://proxy:port"

# 3. Run script
python merge.py
```

**→ Go to: [SETUP_GUIDE.md](SETUP_GUIDE.md)**

---

### Path 3: Automated Setup (Linux/Mac)
Time: 5 minutes

```bash
bash setup.sh
```

Interactive setup that guides you through everything.

---

## 🔍 Which Documentation to Read?

| Need | Read |
|------|------|
| Want quick overview | [README.md](README.md) |
| Setting up GitHub Actions | [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) |
| Local setup with details | [SETUP_GUIDE.md](SETUP_GUIDE.md) |
| Understand what changed | [CHANGES.md](CHANGES.md) |
| Troubleshoot proxy | Run: `python proxy_test.py` |
| Automate local setup | Run: `bash setup.sh` |
| Configure playlists | Edit: `sources.txt` |

---

## ⚡ TL;DR (Super Quick)

### Local Quick Start:
```bash
# Install dependencies
pip install requests

# Test proxy
python proxy_test.py --list

# Use a proxy
export HTTP_PROXY="http://103.125.31.222:80"

# Run
python merge.py

# Get output
cat merged.m3u
```

### GitHub Actions Quick Start:
1. Go to GitHub repo Settings
2. Add Secret: `BANGLADESHI_PROXY` = `http://proxy:port`
3. That's it! Runs every 6 hours

---

## 🎯 What This Script Does

**Before:** Merged IPTV channels from anywhere
**After:** Only merges channels available in **Bangladesh**

**Process:**
1. Uses Bangladeshi IP proxy
2. Tests each channel
3. Keeps only channels available in Bangladesh
4. Removes: 403 Forbidden, 504 errors, timeouts
5. Creates filtered `merged.m3u`

**Result:** Quality playlist with only working Bangladesh channels

---

## 📝 Key Changes Made

### Modified:
- ✅ `merge.py` - Added Bangladesh IP requirement
- ✅ `README.md` - Updated documentation
- ✅ `.github/workflows/merge.yml` - Enhanced workflow

### Created:
- ✅ `SETUP_GUIDE.md` - Detailed setup
- ✅ `GITHUB_ACTIONS_SETUP.md` - Actions guide
- ✅ `CHANGES.md` - Change summary
- ✅ `proxy_test.py` - Proxy testing tool
- ✅ `setup.sh` - Automated setup
- ✅ `QUICK_START.md` - This file

---

## ⚠️ Important: Bangladesh IP Required!

This script **requires** a Bangladeshi IP proxy to work.

**Script will refuse to run if:**
- No proxy is configured
- Proxy doesn't return Bangladesh IP
- Proxy is from a different country

**To fix:**
1. Find Bangladesh proxy
2. Test with: `python proxy_test.py http://proxy:port`
3. Should see: `"countryCode":"BD"`

---

## 🆘 Troubleshooting Quick Links

### Problem | Solution
---|---
"No proxy configured" | Set `HTTP_PROXY` env variable
"Not Bangladesh IP" | Use different proxy
Very few channels | Normal - geo-restricted channels removed
Proxy timeout | Increase `CHECK_TIMEOUT` in merge.py
GitHub Actions fails | Check proxy in secret, test manually

---

## 📱 Usage Guide

### Using Output Playlist

The `merged.m3u` file can be used with:
- VLC media player
- Kodi
- IPTV Smarters
- Smart TV apps
- Any M3U8 compatible player

Just import/open the `merged.m3u` file.

---

## 🔧 Common Configurations

### Change Schedule (GitHub Actions)
Edit `.github/workflows/merge.yml`:
```yaml
- cron: '0 */3 * * *'  # Every 3 hours instead of 6
```

### Increase Timeout
Edit `merge.py`:
```python
CHECK_TIMEOUT = 10  # More lenient, slower
```

### Add Playlist Sources
Edit `sources.txt`:
```
https://example.com/playlist1.m3u8
https://example.com/playlist2.m3u8
```

---

## 💾 File Structure

```
ip_link/
├── merge.py                    # Main script
├── merged.m3u                  # Output (auto-generated)
├── sources.txt                 # Input URLs (edit this)
├── requirements.txt            # Python dependencies
├── proxy_test.py              # Proxy testing tool
├── setup.sh                   # Automated setup
├── README.md                  # Overview
├── QUICK_START.md             # This file
├── SETUP_GUIDE.md             # Detailed setup
├── GITHUB_ACTIONS_SETUP.md    # Actions guide
├── CHANGES.md                 # What changed
└── .github/workflows/
    └── merge.yml              # GitHub Actions workflow
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] `requests` package installed (`pip install requests`)
- [ ] Bangladesh proxy found and tested
- [ ] `sources.txt` has M3U8 URLs
- [ ] Script runs without proxy error
- [ ] `merged.m3u` generated with channels
- [ ] GitHub Actions configured (optional)

---

## 🎓 Learning Resources

### Finding Bangladesh Proxies:
- [free-proxy-list.net](https://free-proxy-list.net)
- [proxy-list.download](https://proxy-list.download)
- Search: "Bangladesh proxy"

### Testing Proxies:
```bash
curl --proxy http://ip:port http://api.ipify.org
```

### M3U Format:
- [M3U Specification](https://en.wikipedia.org/wiki/M3U)

---

## 🎉 Next Steps

1. **Choose setup method**
   - GitHub Actions → Read GITHUB_ACTIONS_SETUP.md
   - Local → Read SETUP_GUIDE.md

2. **Find Bangladesh proxy**
   - Run: `python proxy_test.py --list`
   - Or: Find online at proxy-list websites

3. **Test proxy**
   - Run: `python proxy_test.py http://your-proxy:port`

4. **Configure sources**
   - Edit: `sources.txt`
   - Add M3U8 playlist URLs

5. **Run script**
   - Local: `python merge.py`
   - GitHub: Workflow runs automatically

6. **Enjoy!**
   - Import `merged.m3u` to your IPTV player

---

## 📞 FAQ

**Q: Do I need to be in Bangladesh?**
A: No, just need a Bangladeshi IP proxy.

**Q: Can I use free proxies?**
A: Yes, but they may be less reliable. Paid VPNs are more stable.

**Q: How often does it update?**
A: Every 6 hours (configurable).

**Q: Why so few channels?**
A: By design - only truly working Bangladesh channels kept.

**Q: Is this legal?**
A: Script tests channel availability. Use only legal channels.

---

## 📖 Reading Order

Recommended reading order based on your needs:

### First Time Setup:
1. This file (QUICK_START.md) - 5 min
2. README.md - 5 min
3. Your chosen guide (GitHub or Local) - 10 min
4. Run setup or script - 5 min

### Troubleshooting:
1. Check error message
2. Run `python proxy_test.py`
3. Read relevant section in SETUP_GUIDE.md
4. Try solution

### Learning More:
1. CHANGES.md - Understanding what changed
2. SETUP_GUIDE.md - Advanced setup
3. GITHUB_ACTIONS_SETUP.md - Automation details

---

## 🚀 Get Started Now!

Choose your path:

- **GitHub Actions?** → [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)
- **Local Setup?** → [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Need Help?** → Run `python proxy_test.py --list`

---

Happy IPTV streaming! 🇧🇩 📺

*For detailed info, see the documentation files in this folder*
