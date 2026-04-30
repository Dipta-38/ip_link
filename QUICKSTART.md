# Quick Start Guide: Bangladesh IP IPTV Filter

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Bangladesh Proxy
Choose ONE option:

#### Option A: Use Free Proxy (Unreliable)
```bash
# Find a Bangladesh proxy at:
# https://free-proxy-list.com/
# Filter country = BD
```

#### Option B: Use SurfShark VPN (Easiest)
```bash
# Linux:
sudo apt install surfshark-vpn
surfshark-cli auth
surfshark-cli connect -l Bangladesh

# Then run:
python merge.py
```

#### Option C: Setup HTTP Proxy
```bash
export BD_PROXY_HTTP="http://your-proxy-ip:port"
export BD_PROXY_HTTPS="http://your-proxy-ip:port"
export USE_BD_PROXY="true"
python merge.py
```

### Step 3: Run Script
```bash
python merge.py
```

### Step 4: Find Output
- `merged.m3u` - Use in your IPTV player
- `sources.txt` - Channel information

---

## 🐙 GitHub Actions Setup (10 minutes)

### Step 1: Get Bangladesh Proxy/VPN
Choose a provider:
- **SurfShark**: $2.49/month - Easiest setup
- **ExpressVPN**: $6.67/month - Most reliable
- **BrightData**: $15+/month - Best for automation
- **Oxylabs**: Custom pricing - Enterprise solution

Get proxy URL in format: `http://ip:port` or `http://user:pass@ip:port`

### Step 2: Add GitHub Secrets
1. Go to your repository
2. **Settings → Secrets and variables → Actions**
3. Click **New repository secret**

Add these secrets:
```
Name: BD_PROXY_HTTP
Value: http://your-proxy-ip:port

Name: BD_PROXY_HTTPS  
Value: http://your-proxy-ip:port
```

### Step 3: Done!
- GitHub Actions will run every 6 hours automatically
- Updated `merged.m3u` will be committed to repository
- Releases created with each update
- Artifacts available for download

---

## 📊 How It Works

1. **Find Files**: Scans directory for M3U8 files
2. **Extract Channels**: Reads all channel information
3. **Remove Duplicates**: Keeps only unique streams
4. **Filter by BD IP**: Tests each channel using Bangladesh proxy
5. **Output Results**: Creates merged.m3u with available channels

---

## 🔧 Advanced Configuration

### Local .env File
Create `.env` file based on `.env.example`:
```bash
cp .env.example .env
# Edit .env with your proxy settings
python merge.py
```

### Custom Proxy
```bash
export BD_PROXY_HTTP="http://user:password@proxy.com:8080"
python merge.py
```

### Local VPN Connection
```bash
# Connect VPN first (SurfShark, ExpressVPN, etc.)
# Then:
python merge.py
```

---

## ⚠️ Troubleshooting

### "No channels available for Bangladesh"
```bash
# Test if proxy is really from Bangladesh:
curl -x http://your-proxy:port https://api.country.is/
# Should show: "country":"BD"
```

### "Connection timeout"
```bash
# Check proxy availability:
curl -x http://your-proxy:port --connect-timeout 10 https://example.com
# If fails, proxy is down or wrong
```

### "Proxy error in GitHub Actions"
1. Check secrets are correctly set
2. Verify proxy IP/port format: `http://ip:port`
3. Test proxy locally first
4. Use residential proxy, not datacenter
5. Check proxy provider supports your traffic

---

## 💡 Tips & Best Practices

✅ **Do:**
- Test proxy locally first before using in GitHub Actions
- Use paid proxy for production (more reliable)
- Monitor GitHub Actions logs for errors
- Keep proxy credentials in GitHub Secrets
- Test channel availability periodically

❌ **Don't:**
- Use free proxies for automated systems (unreliable)
- Hardcode proxy IP in workflow files
- Use datacenter proxies (more likely to be blocked)
- Run too many parallel requests
- Leave VPN/proxy info in commit history

---

## 📈 Example: Setting up SurfShark for GitHub Actions

### 1. Buy SurfShark (Optional - can test free)
- Go to: https://surfshark.com
- Cost: $2.49/month with 2-year plan
- Enable "OpenVPN" in settings

### 2. Download OpenVPN Config
- In SurfShark app: Settings → Manage VPN extensions
- Download OpenVPN config for Bangladesh
- Or use: https://api.surfshark.com/v3/server/openvpn/country/bd

### 3. Create GitHub Secrets
```
Secret Name: OPENVPN_CONFIG
Value: [base64 encoded .ovpn file content]

Get via: base64 -w 0 < your-bd.ovpn | pbcopy
```

### 4. Workflow automatically uses it
The workflow will detect and setup OpenVPN automatically!

---

## 📱 Using Merged M3U File

### VLC Media Player
```
File → Open File → merged.m3u
```

### Kodi
```
Add-ons → Install from file → Select merged.m3u
```

### IPTV Smarters
```
Settings → Manage Playlists → Add → File → merged.m3u
```

### Other Players
Most IPTV players support direct M3U file input. Just point to `merged.m3u`

---

## 🔄 Automatic Updates

GitHub Actions will:
- ✅ Run every 6 hours automatically
- ✅ Update channels based on BD IP availability
- ✅ Commit new versions to repository
- ✅ Create releases with each update
- ✅ Keep 30-day artifact history

Customize frequency in `.github/workflows/merge.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # Change to:
  # - cron: '0 */4 * * *'  # Every 4 hours
  # - cron: '0 0 * * *'    # Daily
```

---

## 📞 Getting Help

**Script not working?**
1. Check Python version: `python --version` (need 3.8+)
2. Check proxy: `curl -x proxy https://api.ipify.org`
3. Check Bangladesh IP: `curl -x proxy https://api.country.is/`
4. Review script output messages

**GitHub Actions failing?**
1. Check workflow logs: Actions → Your workflow → Latest run
2. Verify secrets are set correctly
3. Test proxy with: `curl -x proxy https://api.ipify.org`
4. Enable debug logging if needed

**Proxy issues?**
- Contact proxy provider support
- Try different proxy from same provider
- Switch to different VPN provider
- Check if proxy supports your region

---

**More details?** See:
- `SETUP_BANGLADESH_PROXY.md` - Detailed proxy setup
- `BD_PROXY_CONFIG.md` - Provider comparison and costs
- `.env.example` - Configuration options
- `merge.py` - Source code with comments

---

**Happy streaming!** 🎬
