# GitHub Actions Setup Guide

## Quick Setup (2 minutes)

### Step 1: Add GitHub Secret

1. Go to your repository on GitHub
2. Click **Settings** tab
3. In left sidebar: **Secrets and variables** → **Actions**
4. Click **New repository secret** button
5. Create secret with:
   - **Name:** `BANGLADESHI_PROXY`
   - **Value:** `http://proxy-ip:port`
   
   Example: `http://103.125.31.222:80`

6. Click **Add secret**

### Step 2: Done!

The workflow will automatically:
- ✅ Test your proxy on every run
- ✅ Verify it's from Bangladesh
- ✅ Filter channels from Bangladesh
- ✅ Update `merged.m3u` every 6 hours

---

## Detailed Workflow Explanation

## Detailed Workflow Explanation

The updated `.github/workflows/merge.yml` does this:

```
1. On Schedule (every 6 hours) or Manual Trigger
   ↓
2. Setup Python 3.10
   ↓
3. Install requests package
   ↓
4. Test Bangladeshi Proxies:
   - Try built-in proxy list (18 fresh proxies)
   - If none work, try GitHub secret BANGLADESHI_PROXY
   - Verify each proxy returns Bangladesh IP
   ↓
5. If proxy found and verified:
   - Export HTTP_PROXY and HTTPS_PROXY env vars
   - Verify env vars are set (FIXED!)
   - Test proxy connection
   ↓
6. Run merge.py:
   - Script receives proxy via environment
   - Verifies Bangladesh IP again
   - Filters channels by Bangladesh availability
   ↓
7. If successful:
   - Commit merged.m3u
   - Push to repository
   ↓
8. If failed:
   - Show detailed error message
   - Don't update repository
```

### Important: Proxy Fix Applied ⚠️

**The workflow has been fixed** to properly pass proxy variables to merge.py.

**If you're seeing "proxy failed error":** → See [GITHUB_ACTIONS_PROXY_FIX.md](GITHUB_ACTIONS_PROXY_FIX.md)

### What Each Step Does

#### Step 1: Configure Bangladeshi Proxy
```yaml
- name: Configure Bangladeshi Proxy
```
- Tests 4 free Bangladesh proxies
- Uses your GitHub secret if available
- Only proceeds if Bangladesh IP confirmed

#### Step 2: Run Merge Script
```yaml
- name: Run merge script
```
- Runs merge.py with validated proxy
- Script verifies Bangladesh IP again
- Filters channels

#### Step 3: Commit and Push
```yaml
- name: Commit and push
```
- Saves merged.m3u if changes detected
- Commits with timestamp
- Pushes to repository

---

## Using Built-in Proxies (No Secret Needed)

The workflow includes 4 tested Bangladesh proxies:

```
http://103.125.31.222:80
http://103.144.182.1:3128
http://103.105.187.38:8080
http://180.163.200.242:3128
```

If ANY of these work, the workflow will use them automatically. **No GitHub secret needed!**

To use:
1. Just enable GitHub Actions
2. Workflow will test proxies on first run
3. If one works, you're done!

---

## Using Your Own Proxy

If the built-in proxies don't work in your location:

1. Find a working Bangladesh proxy
   - Test with: `python proxy_test.py http://your-proxy:port`
   - Or test manually: `curl --proxy http://your-proxy:port http://api.ipify.org`

2. Add GitHub Secret
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `BANGLADESHI_PROXY`
   - Value: `http://your-proxy:port`

3. That's it! Workflow will use your secret.

---

## Monitoring the Workflow

### View Workflow Status

1. Go to **Actions** tab in your repository
2. See list of workflow runs
3. Click on a run to see details

### Check if Successful

✅ **Success indicators:**
- Workflow shows green checkmark
- Log shows: "✅ ✓ Using BANGLADESHI IP"
- merged.m3u was updated

❌ **Failure indicators:**
- Workflow shows red X
- Log shows proxy test failed
- merged.m3u not updated

### View Detailed Logs

1. Click on the failed workflow
2. Click on "Configure Bangladeshi Proxy" step
3. See proxy test results
4. Look for error message

---

## Schedule Configuration

### Default Schedule
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'
```
- Runs every 6 hours
- At minute 0 of every 6th hour (0:00, 6:00, 12:00, 18:00)

### Change Schedule

Edit `.github/workflows/merge.yml`:

**Every 12 hours:**
```yaml
- cron: '0 */12 * * *'
```

**Every 3 hours:**
```yaml
- cron: '0 */3 * * *'
```

**Specific time (daily at 2 AM UTC):**
```yaml
- cron: '0 2 * * *'
```

**Multiple times:**
```yaml
schedule:
  - cron: '0 0 * * *'   # Every day at 00:00
  - cron: '0 12 * * *'  # Every day at 12:00
```

---

## Manual Trigger

You can run the workflow manually anytime:

1. Go to **Actions** tab
2. Select "IPTV Auto Merge - Bangladesh Filter"
3. Click **Run workflow** button
4. Choose branch and click "Run workflow"

Useful for:
- Testing immediately
- Force update of merged.m3u
- Checking if proxy is working

---

## Troubleshooting

### Issue: Workflow Failed - "No working Bangladeshi proxy found"

**Cause:** All proxies timed out or failed

**Solutions:**
1. Add working proxy to GitHub secret `BANGLADESHI_PROXY`
2. Built-in proxies might be down - try later
3. Check if your GitHub runner has internet access

### Issue: Workflow Failed - "Not using Bangladeshi IP"

**Cause:** Proxy doesn't return Bangladesh IP

**Solutions:**
1. Use different proxy
2. Test proxy first: `python proxy_test.py http://proxy:port`
3. Add new proxy to GitHub secret

### Issue: Workflow Succeeds but merged.m3u Not Updated

**Cause:** No changes detected (same channels as before)

**This is normal!** Git only commits if content changed.

**To force update:**
1. Edit sources.txt (add/remove a URL)
2. Run workflow manually
3. Git will detect change and commit

### Issue: Workflow Never Triggers

**Causes:**
1. GitHub Actions might be disabled
2. Schedule might be incorrect
3. Repository might be archived

**Solutions:**
1. Check Actions tab - is it enabled?
2. Click "Run workflow" to test manually
3. Check cron syntax on [crontab.guru](https://crontab.guru)

### Issue: Seeing Old merged.m3u

**Workflow might not have run yet:**
1. Wait for scheduled time (every 6 hours)
2. Or trigger manually: Actions → "Run workflow"
3. Check Actions tab for log

---

## Security Notes

### About GitHub Secrets

- ✅ Secrets are encrypted and hidden
- ✅ Never shown in logs
- ✅ Safe to use with proxies
- ✅ Can only be read by workflows

### Best Practices

1. **Use a reliable proxy**
   - Free proxies can be unstable
   - Consider paid VPN with proxy support

2. **Monitor runs**
   - Check workflow logs occasionally
   - Make sure it's working

3. **Update when needed**
   - If proxy stops working, update secret
   - Test new proxies first locally

---

## Advanced Configuration

### Increase Timeout (if proxies are slow)

Edit `merge.py`:
```python
CHECK_TIMEOUT = 10  # Instead of 5 (seconds)
```

Higher = slower but catches more timeouts

### Add More Proxies to Workflow

Edit `.github/workflows/merge.yml`:

```yaml
env:
  PROXY_LIST: |
    http://proxy1:port
    http://proxy2:port
    http://proxy3:port
```

### Disable Auto-Commit on No Changes

Edit `.github/workflows/merge.yml`:

```yaml
- name: Commit and push
  run: |
    git config --global user.name "github-actions[bot]"
    git config --global user.email "github-actions@github.com"
    git add merged.m3u
    
    # Always commit (even if no changes)
    git commit -m "Auto update [$(date +'%Y-%m-%d %H:%M')]" || true
    git push
```

---

## Example Workflow Output

### Successful Run
```
✅ Proxy working! IP: 103.125.31.222
✅ Country: Bangladesh (BD)
✅ ✓ Using BANGLADESHI IP - Ready to filter channels

📋 Found 3 playlist sources
📡 Fetching playlist: https://...
   ✅ Playlist fetched, processing streams...
📊 Progress: Checked 50 streams | Kept: 28
📊 Progress: Checked 100 streams | Kept: 45
...

✅ MERGE COMPLETED - BANGLADESHI CHANNELS ONLY
📺 Total channels kept: 245
🚫 403 Forbidden: 89
🌐 504 Gateway Timeout: 12
⏱️ Timeouts: 34
```

### Failed Run
```
❌ ERROR: Bangladesh IP verification failed!
❌ Proxy not responding: http://proxy:port

Testing GitHub secrets proxy...
❌ Not from Bangladesh: Country code US
```

---

## Success Checklist

- [ ] GitHub Actions enabled (Actions tab shows green)
- [ ] `BANGLADESHI_PROXY` secret added (Settings → Secrets)
- [ ] `.github/workflows/merge.yml` exists and updated
- [ ] `sources.txt` has valid M3U8 URLs
- [ ] First workflow run succeeds (check Actions tab)
- [ ] `merged.m3u` updated with channels
- [ ] Workflow runs on schedule (check next run time)

---

## Next Steps

1. ✅ Add `BANGLADESHI_PROXY` secret
2. ✅ Enable GitHub Actions
3. ✅ Run workflow manually to test
4. ✅ Check merged.m3u for channels
5. ✅ Configure your IPTV player with merged.m3u URL

---

## Support

For issues:
1. Check workflow logs (Actions tab)
2. Test proxy locally: `python proxy_test.py`
3. See SETUP_GUIDE.md for manual setup
4. See README.md for overview

Enjoy your Bangladesh IPTV! 🇧🇩
