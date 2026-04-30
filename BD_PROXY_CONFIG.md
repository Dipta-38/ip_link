# Bangladesh Proxy/VPN Configuration Guide
# This file helps you configure the merge.py script with Bangladesh IP access

## QUICK START OPTIONS

### Option 1: Using SurfShark VPN (Recommended for ease)
# Cost: ~$2.49/month
# Installation:
#   Windows: Download from https://surfshark.com
#   Linux: sudo apt install surfshark-vpn
#   macOS: brew install surfshark

# Usage:
# 1. Install SurfShark
# 2. Connect to Bangladesh server
# 3. Run: python merge.py

# Command line (Linux/Mac):
# surfshark-cli connect -l Bangladesh
# python merge.py
# surfshark-cli disconnect


### Option 2: Using ExpressVPN
# Cost: $6.67/month
# Better for reliability and speed
# https://www.expressvpn.com

# Usage:
# 1. Install ExpressVPN
# 2. Connect to Bangladesh
# 3. Run: python merge.py


### Option 3: Free Proxy (Unreliable but works)
# Many free proxies available at:
# - https://www.freeproxylists.net/
# - https://free-proxy-list.com/
# Filter for Bangladesh (BD) proxies

# Usage in .env file:
# BD_PROXY_HTTP=http://188.166.211.200:8080
# BD_PROXY_HTTPS=http://188.166.211.200:8080
# USE_BD_PROXY=true


### Option 4: Paid Datacenter Proxy (Most Reliable)
# - BrightData (formerly Luminati)
# - Oxylabs
# - Smartproxy
# - ScraperAPI

# These provide:
# ✓ 99.9% uptime
# ✓ Residential IPs (less likely to be blocked)
# ✓ Rotating proxies
# ✓ 24/7 support


### Option 5: GitHub Actions with Secrets (Automated)
# 1. Get proxy from any paid provider
# 2. Go to GitHub: Settings → Secrets and variables → Actions
# 3. Add secrets:
#    - BD_PROXY_HTTP=http://your-proxy:port
#    - BD_PROXY_HTTPS=http://your-proxy:port
# 4. GitHub Actions will automatically use them


## DETAILED SETUP GUIDES

### SurfShark VPN Setup
# Linux:
sudo apt update
sudo apt install surfshark-vpn
surfshark-cli auth
surfshark-cli connect -l Bangladesh
python merge.py
surfshark-cli disconnect

# Windows (PowerShell as Admin):
# Download from https://surfshark.com/download
# Run installer
# Open SurfShark GUI → Bangladesh → Connect
# Open PowerShell → python merge.py

# macOS:
brew install surfshark
surfshark-cli auth
surfshark-cli connect -l Bangladesh
python merge.py


### OpenVPN Setup (For stored certificates)
# Linux:
sudo apt install openvpn
# Place your OpenVPN .ovpn config file in current directory
# Then run:
sudo openvpn --config your-bd-config.ovpn --daemon
python merge.py
sudo killall openvpn


### WireGuard Setup (Fast, modern VPN)
# Linux:
sudo apt install wireguard
# Create /etc/wireguard/wg0.conf with your Bangladesh server config
sudo wg-quick up wg0
python merge.py
sudo wg-quick down wg0


## GITHUB ACTIONS CONFIGURATION

### Step 1: Choose Your VPN Provider
# Option A: HTTP/HTTPS Proxy
#   - Get proxy URL from provider
#   - Format: http://ip:port or http://user:pass@ip:port

# Option B: OpenVPN (More complex but very reliable)
#   - Export your .ovpn file
#   - Base64 encode it
#   - Store in GitHub Secret

# Option C: WireGuard (Fastest VPN option)
#   - Export WireGuard config
#   - Base64 encode it
#   - Store in GitHub Secret


### Step 2: Add GitHub Secrets
# Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions

# For HTTP Proxy:
# Name: BD_PROXY_HTTP
# Value: http://your-proxy-ip:port

# Name: BD_PROXY_HTTPS
# Value: http://your-proxy-ip:port


# For OpenVPN:
# Name: OPENVPN_CONFIG
# Value: (base64 encoded .ovpn file)
# Get via: cat your-bd.ovpn | base64


# For WireGuard:
# Name: WIREGUARD_CONFIG
# Value: (base64 encoded wg0.conf)
# Get via: cat /etc/wireguard/wg0.conf | base64


### Step 3: Workflow will automatically use these secrets


## TESTING YOUR PROXY

### Test proxy connectivity:
curl -x http://your-proxy:port https://api.ipify.org
# Should show: Your IP address

### Verify Bangladesh IP:
curl -x http://your-proxy:port https://api.country.is/
# Should show: "country":"BD"

### Test with merge.py:
export BD_PROXY_HTTP="http://your-proxy:port"
export BD_PROXY_HTTPS="http://your-proxy:port"
export USE_BD_PROXY="true"
python merge.py


## RECOMMENDED PROVIDERS FOR GITHUB ACTIONS

### 1. **SurfShark (Easiest)**
   - Cost: $2.49/month
   - Setup: Very easy via CLI
   - Speed: Excellent
   - Supports: OpenVPN, IKEv2
   - Bangladesh: Yes
   - Visit: https://surfshark.com

### 2. **ExpressVPN**
   - Cost: $6.67/month
   - Setup: Medium
   - Speed: Very good
   - Supports: OpenVPN, IKEv2, L2TP
   - Bangladesh: Yes
   - Visit: https://expressvpn.com

### 3. **BrightData (Proxies)**
   - Cost: $15-50/month
   - Setup: Easy
   - Speed: Excellent
   - Supports: HTTP, SOCKS5, Residential
   - Bangladesh: Yes (residential)
   - Visit: https://brightdata.com

### 4. **Oxylabs**
   - Cost: Custom pricing
   - Setup: Easy
   - Speed: Excellent
   - Supports: HTTP, SOCKS5
   - Bangladesh: Yes
   - Visit: https://oxylabs.io

### 5. **Smartproxy**
   - Cost: $7.50/month
   - Setup: Very easy
   - Speed: Good
   - Supports: HTTP, SOCKS5
   - Bangladesh: Yes
   - Visit: https://smartproxy.com


## TROUBLESHOOTING

### Problem: "No channels available for Bangladesh"
Solution:
1. Verify proxy is actually from Bangladesh
2. Test: curl -x proxy https://api.country.is/ | grep BD
3. Try different proxy or VPN provider
4. Check if websites are accessible through proxy

### Problem: Proxy connection timeout
Solution:
1. Check proxy IP and port are correct
2. Verify proxy credentials if authentication required
3. Try: curl -x proxy --connect-timeout 10 https://example.com
4. Test proxy in different environment

### Problem: "Connection error" in workflow
Solution:
1. Verify secret values are correct in GitHub settings
2. Check proxy works from your local machine first
3. Some proxies may block GitHub IP ranges
4. Try residential proxy instead of datacenter
5. Check firewall/security rules

### Problem: Slow channel filtering
Solution:
1. Reduce number of channels to filter
2. Increase timeout in merge.py (default 10s)
3. Use faster proxy provider
4. Run during off-peak hours


## COST COMPARISON

| Provider | Cost | Setup | Speed | Reliability |
|----------|------|-------|-------|------------|
| Free Proxy | $0 | Easy | Slow | Very Low |
| SurfShark | $2.49/mo | Easy | Good | High |
| ExpressVPN | $6.67/mo | Medium | Very Good | Very High |
| BrightData | $15-50/mo | Easy | Excellent | Very High |
| Oxylabs | Custom | Easy | Excellent | Very High |
| Smartproxy | $7.50/mo | Very Easy | Good | High |


## BEST PRACTICE RECOMMENDATIONS

### For GitHub Actions:
- Use paid proxy/VPN service
- Store credentials in GitHub Secrets
- Test locally before using in Actions
- Monitor workflow logs for issues
- Schedule runs during off-peak hours

### For Local Use:
- Use VPN app (SurfShark, ExpressVPN)
- Or use proxy environment variables
- Always verify Bangladesh IP before running
- Test network connection first

### For Production:
- Use residential proxies (less blocking)
- Implement retry logic
- Monitor channel availability
- Log all requests/errors
- Use multiple proxy sources for redundancy


## GETTING HELP

If proxy setup isn't working:
1. Test proxy manually with curl
2. Verify Bangladesh IP location
3. Check proxy provider support
4. Review merge.py debug output
5. Check GitHub Actions logs
6. Test with different proxy provider

Contact proxy provider support if:
- Proxy IP is not responding
- Connection keeps timing out
- IP location verification fails
- Authentication issues occur


---

**Last Updated:** 2024
**For issues, check:** https://github.com/YOUR_REPO/issues
