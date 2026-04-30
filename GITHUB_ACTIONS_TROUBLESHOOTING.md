# GitHub Actions - Bangladesh IPTV Filter Troubleshooting

## Quick Diagnostics

### Step 1: Check Workflow Status
1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
2. Find the latest "Merge IPTV" workflow run
3. Click to see full logs

### Step 2: Check Secrets Configuration
1. Go to: **Settings → Secrets and variables → Actions**
2. Verify these secrets exist:
   - `BD_PROXY_HTTP` 
   - `BD_PROXY_HTTPS`
3. If missing, add them!

### Step 3: Common Issues & Solutions

---

## Issue 1: "Secret not found" Error

**Error Message:**
```
Error: Secrets are not passed to workflows triggered from a forked repository
```

**Solution:**
This is normal behavior. To fix:
1. Push changes to your own repository (not a fork)
2. Or ask repository owner to enable workflow secrets for forks

---

## Issue 2: "Proxy Connection Failed"

**Error Message:**
```
ProxyError: Unable to connect to proxy
Connection refused at proxy.example.com:8080
```

**Causes & Solutions:**
1. **Wrong proxy IP/port**
   - Go to Settings → Secrets
   - Click "BD_PROXY_HTTP" → Edit
   - Check format: `http://ip:port` (no https://)
   - Verify credentials if authentication required

2. **Proxy is down**
   - Test locally: `curl -x http://proxy:port https://api.ipify.org`
   - If fails, proxy provider has issues
   - Contact proxy provider or try backup proxy

3. **Proxy IP changed**
   - Some proxies have rotating IPs
   - Update secret with new IP
   - Or use proxy that provides stable URL

4. **GitHub IP blocked**
   - Some proxies don't accept GitHub's IP range
   - Try residential proxy instead
   - Contact proxy provider for GitHub whitelist

---

## Issue 3: "No channels available for Bangladesh"

**Error Message:**
```
✓ Available channels in Bangladesh: 0/1000
```

**Causes & Solutions:**

1. **Proxy is not from Bangladesh**
   - The proxy claims to be Bangladesh but isn't
   - Test locally:
   ```bash
   curl -x http://proxy:port https://api.country.is/
   # Should show: "country":"BD"
   ```
   - If not BD, get different proxy provider

2. **Channel URLs are blocked**
   - Many IPTV streams block datacenter IPs
   - Use **residential proxies** instead
   - Providers: BrightData, Oxylabs, Smartproxy

3. **Timeout during checks**
   - Channels are slow or blocked
   - Increase timeout in merge.py: `timeout = 15`
   - Or reduce number of channels to test

4. **Proxy authentication failing**
   - Format: `http://username:password@proxy:port`
   - Ensure credentials are URL-encoded
   - For special characters, use: `http://user%3Aname:pass%40word@proxy:port`

**Debugging Steps:**
```bash
# In your workflow, add this step to test:
- name: Test Proxy
  run: |
    curl -x ${{ secrets.BD_PROXY_HTTP }} -v https://api.ipify.org
    curl -x ${{ secrets.BD_PROXY_HTTP }} https://api.country.is/
    # Should show Bangladesh IP
```

---

## Issue 4: "No channels merged" or Empty Output

**Causes & Solutions:**

1. **No M3U8 files found**
   - Solution: Add M3U/M3U8 files to repository
   - Files should be in root directory
   - Names like: `playlist.m3u`, `channels.m3u8`

2. **M3U8 files are empty**
   - Solution: Verify M3U8 file contents locally
   - M3U8 format:
   ```
   #EXTM3U
   #EXTINF:-1 tvg-name="Channel Name",Channel Name
   http://stream-url.com/video.ts
   ```

3. **All channels filtered out**
   - Solution: Check proxy is working
   - Add debugging to merge.py
   - Try without filtering first

---

## Issue 5: "Changes not committed/pushed"

**Error Message:**
```
fatal: Permission denied. Could not perform Git operation.
```

**Solution:**
1. Workflow needs permission to push
2. Go to: **Settings → Actions → General**
3. Find: "Workflow permissions"
4. Select: ✓ "Read and write permissions"
5. Click "Save"

---

## Issue 6: Workflow Not Running at All

**Possible Causes:**
1. Cron schedule disabled
2. Workflow file has syntax error
3. File not in correct location

**Solutions:**
1. Check workflow file location:
   ```
   .github/workflows/merge.yml ✓ Correct
   github/workflows/merge.yml ✗ Wrong
   .github/actions/merge.yml ✗ Wrong
   ```

2. Validate YAML syntax:
   - Use: https://www.yamllint.com/
   - Copy contents of merge.yml
   - Check for errors

3. Manually trigger workflow:
   - Go to Actions tab
   - Select "Merge IPTV" workflow
   - Click "Run workflow"
   - Select branch (main/master)
   - Click "Run"

4. Check if branch is correct:
   - Workflow targets: `main` or `master`
   - Make sure your default branch matches

---

## Issue 7: Workflow Runs But No Release Created

**Causes:**
1. No channels found (already covered above)
2. Output files not generated
3. Permission issues

**Solutions:**
1. Check if merge.py actually ran:
   - In logs, look for: "Starting IPTV Merge"
   - Look for output file creation messages

2. Verify Python ran successfully:
   - Check for any Python errors in logs
   - Should see channel counts

3. Check Git permissions:
   - Settings → Actions → General
   - Ensure "Write" permissions enabled

4. Manual check:
   - After workflow runs, check repo
   - Should see: `merged.m3u` and `sources.txt`
   - If missing, files weren't generated

---

## Issue 8: VPN Setup Failed (OpenVPN/WireGuard)

**Error Message:**
```
OpenVPN setup attempted
Could not open VPN connection
```

**Solutions:**
1. Check secret format
   - `OPENVPN_CONFIG` should be base64 encoded .ovpn file
   - Test locally:
   ```bash
   base64 -d <<< "$ENCODED_CONFIG" > test.ovpn
   ```

2. Verify .ovpn file is valid
   - Should start with: `client`
   - Should have: `<ca>`, `<cert>`, `<key>`
   - Should not be corrupted

3. For WireGuard
   - Config file must be valid
   - Permissions must be correct
   - May need elevated privileges

---

## Advanced Debugging

### Enable Debug Logging in Workflow

Add to merge.yml:
```yaml
- name: Enable Debug
  run: |
    export DEBUG=true
    python merge.py
```

### Print Environment Variables

Add step:
```yaml
- name: Debug Info
  run: |
    echo "Proxy: ${{ secrets.BD_PROXY_HTTP }}"
    echo "Python: $(python --version)"
    echo "CWD: $(pwd)"
    ls -la *.m3u *.m3u8 2>/dev/null || echo "No M3U files found"
```

### Test Proxy Directly

```yaml
- name: Test Proxy
  run: |
    python3 << 'EOF'
    import requests
    try:
        proxy = "${{ secrets.BD_PROXY_HTTP }}"
        response = requests.get(
            'https://api.ipify.org?format=json',
            proxies={'http': proxy, 'https': proxy},
            timeout=10
        )
        print(f"Response: {response.json()}")
        
        # Check country
        country = requests.get(
            'https://api.country.is/',
            proxies={'http': proxy, 'https': proxy},
            timeout=10
        ).json()
        print(f"Country: {country}")
    except Exception as e:
        print(f"Error: {e}")
    EOF
```

---

## Testing Locally Before GitHub Actions

Always test locally first:

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set proxy environment
```bash
export BD_PROXY_HTTP="http://your-proxy:port"
export BD_PROXY_HTTPS="http://your-proxy:port"
export USE_BD_PROXY="true"
```

### 3. Verify proxy works
```bash
curl -x http://your-proxy:port https://api.ipify.org
```

### 4. Run script
```bash
python merge.py
```

### 5. Check output
```bash
ls -la merged.m3u sources.txt
```

If all works locally, it should work in GitHub Actions!

---

## Proxy Provider Specific Issues

### SurfShark VPN
- **Issue**: "Daemon not responding"
- **Fix**: Restart daemon: `systemctl restart surfshark-vpn`

### ExpressVPN
- **Issue**: "Connection dropped"
- **Fix**: Reconnect: `expressvpn connect bangladesh`

### BrightData
- **Issue**: "Auth failed"
- **Fix**: Check credentials in proxy URL format

### Oxylabs  
- **Issue**: "Too many requests"
- **Fix**: Reduce concurrent requests or increase delay between requests

### Smartproxy
- **Issue**: "IP rotated"
- **Fix**: Expected behavior - some requests may fail, add retry logic

---

## Performance Optimization

If workflow is slow:

1. **Reduce channels to check**
   - Edit merge.py to skip some channels
   - Or increase timeout

2. **Increase request delay**
   - In merge.py: `time.sleep(0.5)` instead of 0.2

3. **Use faster proxy**
   - Paid proxies are usually faster
   - Residential > Datacenter

4. **Parallel processing**
   - Modify merge.py to check multiple channels at once
   - Use `ThreadPoolExecutor`

5. **Caching**
   - Cache channel availability
   - Skip rechecking unchanged channels

---

## Getting Help

### Check Logs
1. Actions tab → workflow run → Logs
2. Look for error messages
3. Note any URL patterns or proxy info

### Test Command
```bash
# Test if issue is proxy or script
curl -x http://proxy:port https://example.com -v
```

### Contact Support
- **Script issues**: Check merge.py errors
- **Proxy issues**: Contact proxy provider
- **GitHub issues**: Check Actions documentation
- **Workflow issues**: Review merge.yml syntax

---

## Checklist Before Posting for Help

- [ ] Checked GitHub Actions logs
- [ ] Verified secrets are set correctly
- [ ] Tested proxy works locally
- [ ] Confirmed Bangladesh IP: `curl -x proxy https://api.country.is/`
- [ ] Checked M3U8 files exist
- [ ] Verified Python version >= 3.8
- [ ] Tried manual workflow trigger
- [ ] Enabled debug logging

If all checked and still not working, provide:
1. GitHub Actions workflow logs (sanitized)
2. Local test results
3. Proxy provider name
4. Python version
5. Error messages (exact text)

---

**Still having issues?** 
- See `SETUP_BANGLADESH_PROXY.md` for more setup details
- See `BD_PROXY_CONFIG.md` for proxy provider information
- Check `merge.py` for detailed comments
