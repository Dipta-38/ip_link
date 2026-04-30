# GitHub Actions Proxy Issues - Troubleshooting Guide

## Problem
```
GitHub Actions gives: ❌ Proxy failed error
Proxy not being used by default in GitHub Actions
```

## Root Cause
The GitHub Actions runner environment doesn't automatically use HTTP_PROXY/HTTPS_PROXY environment variables unless they are:
1. Explicitly exported
2. Passed as environment variables to the step
3. Properly propagated between steps

---

## ✅ Solution: Updated Workflow

The workflow has been updated to:

1. **Properly test proxy** - With better timeouts (8s instead of 5s)
2. **Export environment variables** - Uses `$GITHUB_ENV` for persistence
3. **Verify proxy is set** - Checks variables are available before running script
4. **Pass proxy to merge.py** - Explicitly sets env vars in step

---

## 🔧 What Was Changed

### Before (Broken):
```yaml
env:
  HTTP_PROXY: ${{ env.HTTP_PROXY }}  # Didn't work reliably
```

### After (Fixed):
```yaml
id: proxy  # Added ID to track step
env:
  HTTP_PROXY: ${{ env.HTTP_PROXY }}  # Still works
  HTTPS_PROXY: ${{ env.HTTPS_PROXY }}  # Added HTTPS
  
# NEW: Verify proxy variables are set
- name: Verify Proxy & Run merge script
  env:
    HTTP_PROXY: ${{ env.HTTP_PROXY }}
    HTTPS_PROXY: ${{ env.HTTPS_PROXY }}
  run: |
    # Check variables are set
    echo "HTTP_PROXY is set: $([ ! -z "$HTTP_PROXY" ] && echo 'YES' || echo 'NO')"
    
    # Exit if not set
    if [ -z "$HTTP_PROXY" ]; then
      echo "❌ ERROR: HTTP_PROXY not set!"
      exit 1
    fi
    
    # Test proxy before running
    curl -s --proxy "$HTTP_PROXY" http://api.ipify.org
    
    # Run merge.py
    python merge.py
```

---

## 🎯 Key Improvements

### 1. Increased Timeout (5s → 8s)
```bash
# Old: timeout 5 curl
# New: timeout 8 curl --max-time 8
```
**Why:** GitHub Actions runners can have higher latency to external networks

### 2. Better Environment Variable Handling
```bash
# Write to $GITHUB_ENV
echo "HTTP_PROXY=$WORKING_PROXY" >> $GITHUB_ENV
echo "HTTPS_PROXY=$WORKING_PROXY" >> $GITHUB_ENV

# Export in current shell
export HTTP_PROXY="$WORKING_PROXY"
export HTTPS_PROXY="$WORKING_PROXY"
```

### 3. Added Step ID
```yaml
- name: Configure Bangladeshi Proxy
  id: proxy  # NEW: Can reference with ${{ steps.proxy.outputs.proxy_url }}
```

### 4. Proxy Verification Step
```yaml
- name: Verify Proxy & Run merge script
  # NEW: Tests that proxy variables are actually set
  # NEW: Tests proxy connection before running merge.py
```

---

## 🧪 How to Test If It Works Now

### Check Workflow Logs:

1. Go to GitHub → **Actions** tab
2. Click latest workflow run
3. Click **Verify Proxy & Run merge script**
4. Look for:

**Success:**
```
✅ Proxy connection verified
✅ STARTING IPTV MERGE
✅ Merge completed successfully
```

**Failure:**
```
❌ ERROR: HTTP_PROXY not set!
```

---

## 🆘 If Still Getting Proxy Errors

### Step 1: Check if BANGLADESHI_PROXY Secret Exists
1. Go to GitHub repo **Settings**
2. **Secrets and variables** → **Actions**
3. Look for `BANGLADESHI_PROXY`
4. If missing → Add it with working Bangladesh proxy

### Step 2: Test Proxy Locally First
```bash
# On your machine
export HTTP_PROXY="http://your-proxy:port"
python proxy_test.py
# Should show: ✅ BANGLADESH IP VERIFIED!
```

### Step 3: Test with Manual Workflow Trigger
1. Go to **Actions** tab
2. Click "IPTV Auto Merge - Bangladesh Filter"
3. Click **Run workflow**
4. Choose **main** branch
5. Click **Run workflow**
6. Check logs for errors

### Step 4: Check Workflow Logs for Details
1. Click the workflow run
2. Click **Verify Proxy & Run merge script**
3. Look for error messages
4. Common errors:
   - `HTTP_PROXY not set` → Proxy detection failed
   - `Connection refused` → Proxy not working
   - `proxy test timeout` → Proxy or network slow (might still work)

---

## 🔍 Debugging Output

The updated workflow now shows:

```
========================================
🔍 VERIFYING PROXY VARIABLES
========================================
HTTP_PROXY is set: YES
HTTPS_PROXY is set: YES

Testing proxy connection...
✅ Proxy connection verified

========================================
🚀 STARTING IPTV MERGE
========================================
✅ ✓ Using BANGLADESHI IP - Ready to filter channels
...
✅ Merge completed successfully
```

---

## 📋 Workflow Checklist

Before running workflow, verify:

- [ ] **Proxy is set correctly**
  ```bash
  python proxy_test.py http://your-proxy:port
  # Should show: ✅ BANGLADESH IP VERIFIED!
  ```

- [ ] **GitHub Secret added** (if using custom proxy)
  - Settings → Secrets → `BANGLADESHI_PROXY` = `http://proxy:port`

- [ ] **sources.txt has URLs**
  ```bash
  cat sources.txt
  # Should show M3U8 playlist URLs
  ```

- [ ] **Git is up to date**
  ```bash
  git push origin main
  # Make sure latest changes are pushed
  ```

- [ ] **Workflow file is valid**
  - Check `.github/workflows/merge.yml` syntax
  - No YAML errors

---

## 🚀 How to Use Updated Workflow

### Option 1: Automatic (Every 6 hours)
- Workflow runs automatically
- No action needed
- Check Actions tab to verify

### Option 2: Manual Trigger
1. Go to **Actions** tab
2. Click **IPTV Auto Merge - Bangladesh Filter**
3. Click **Run workflow**
4. Check logs

### Option 3: With Custom Proxy
1. Go to **Settings** → **Secrets** → **New secret**
2. Name: `BANGLADESHI_PROXY`
3. Value: `http://your-working-proxy:port`
4. Trigger workflow
5. Uses custom proxy + built-in fallbacks

---

## 💡 Why This Works Now

### Before:
- ❌ Environment variables weren't verified
- ❌ Proxy might not be set in merge.py step
- ❌ No feedback if proxy wasn't working
- ❌ Short timeout (5s) caused failures on slow networks

### After:
- ✅ Verifies proxy variables are set
- ✅ Tests proxy connection before running script
- ✅ Better timeout (8s) for GitHub runners
- ✅ Clear error messages if something fails
- ✅ Logs show exactly what's happening

---

## 📞 Still Having Issues?

### Common Error: "HTTP_PROXY not set"
**Cause:** No working proxy found
**Solution:**
1. Check built-in proxy list is up to date
2. Add `BANGLADESHI_PROXY` secret with working proxy
3. Test proxy locally first: `python proxy_test.py http://proxy:port`

### Common Error: "proxy test timeout"
**Cause:** Proxy is slow but might work
**Solution:**
- This is a warning, not fatal
- Script should continue
- If script fails, try different proxy

### Common Error: "Merge script failed"
**Cause:** Multiple possible causes
**Solution:**
1. Check merge.py logs (full output)
2. Verify sources.txt has valid URLs
3. Check if Bangladesh IP was verified
4. Ensure proxy works locally first

### Common Error: "Not using Bangladeshi IP"
**Cause:** Proxy doesn't return Bangladesh IP
**Solution:**
1. Proxy is not from Bangladesh
2. Replace with verified Bangladesh proxy
3. Use: `python proxy_test.py http://proxy:port` locally
4. Must show: `"countryCode":"BD"`

---

## ✅ Verification

After updating, verify:

1. **Workflow file uploaded**
   ```bash
   git push origin main
   ```

2. **Check on GitHub**
   - Go to `.github/workflows/merge.yml`
   - Should have updated code

3. **Test manually**
   - Actions tab → Run workflow
   - Should now show proxy verification
   - Should work with Bangladesh proxy

4. **Check logs**
   - Should show detailed output
   - Should show proxy variables set
   - Should show proxy connection verified

---

## 🎯 Success Indicators

Workflow is working if you see:

```
✅ PROXY VERIFIED: http://xxx.xxx.xxx.xxx:port
✅ Proxy connection verified
✅ STARTING IPTV MERGE
✅ ✓ Using BANGLADESHI IP - Ready to filter channels
✅ Merge completed successfully
```

---

## 📈 What's Better Now

| Issue | Before | After |
|-------|--------|-------|
| Proxy not set | ❌ Silent failure | ✅ Clear error |
| Proxy timeout | ❌ Failed | ✅ 8s timeout (better) |
| Verification | ❌ None | ✅ Shows what's set |
| Debugging | ❌ Hard | ✅ Clear logs |
| Success rate | ❌ Low | ✅ Higher |

---

## 🚀 Next Steps

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Test locally first** (recommended)
   ```bash
   export HTTP_PROXY="http://working-proxy:port"
   python merge.py
   ```

3. **Trigger workflow manually**
   - Actions → Run workflow
   - Check logs

4. **Enjoy!**
   - If successful, workflow runs every 6 hours
   - merged.m3u auto-updates

---

## 📚 Related Files

- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - Full GitHub Actions guide
- [PROXY_SOLUTIONS.md](PROXY_SOLUTIONS.md) - Proxy troubleshooting
- [PROXY_EMERGENCY_GUIDE.md](PROXY_EMERGENCY_GUIDE.md) - Emergency procedures
- [.github/workflows/merge.yml](.github/workflows/merge.yml) - Workflow file (UPDATED)

---

## 🎉 You're All Set!

Workflow now:
✅ Properly detects proxy
✅ Verifies proxy variables
✅ Tests proxy connection
✅ Passes proxy to merge.py
✅ Shows detailed logs
✅ Better error handling
✅ Higher success rate

Go test it! 🚀
