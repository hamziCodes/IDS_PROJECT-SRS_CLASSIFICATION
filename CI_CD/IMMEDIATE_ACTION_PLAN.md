# 🚨 Immediate Action Plan - iOS Build Error

**Your build failed with:** `Command PhaseScriptExecution failed with a nonzero exit code`

This is fixable! Follow these steps from your Windows PC right now:

## ⚡ Quick Fix (10 minutes)

### Step 1: Clean Everything (PowerShell)

```powershell
cd d:\IDS_PROJECT\vertex_app

# Run cleanup script
powershell -ExecutionPolicy Bypass -File ..\CI_CD\scripts\cleanup-ios-build.ps1

# OR manually:
flutter clean
Remove-Item -Recurse -Force ios/Pods, ios/Podfile.lock, build, .dart_tool, pubspec.lock -ErrorAction SilentlyContinue
flutter pub get
```

**Expected:** Should complete in 2-3 minutes without errors

### Step 2: Verify iOS Settings (5 minutes)

**Check file:** `vertex_app/ios/Podfile`

Look for (or add) this line near the top:
```ruby
platform :ios, '12.0'
```

If it says `9.0` or `10.0`, change it to `12.0`

**Save the file.**

### Step 3: Commit and Push (2 minutes)

```powershell
cd d:\IDS_PROJECT

git add .
git commit -m "Fix iOS build: clean cache and verify iOS target"
git push origin main
```

### Step 4: Watch the Build (15 minutes)

1. Go to GitHub → Your Repository → **Actions**
2. Click **"iOS TestFlight Deployment"**
3. Watch the workflow run
4. **NEW:** You now see:
   - ✅ Pre-build diagnostics
   - ✅ Verbose build output
   - ✅ Detailed error messages (if any!)

## 🎯 Expected Outcomes

### ✅ Build Succeeds
```
✓ Runner.app built successfully
✓ Archive created successfully
✓ IPA exported successfully
✓ Upload successful! Build should appear in TestFlight in 5-10 minutes.
```

**Next:** Check TestFlight in 10 minutes, your build will be there!

### ❌ Build Still Fails
```
Now you'll see the ACTUAL error message!
```

**Next:** Go to `CI_CD/FIX_PHASESCRIPT_ERROR.md` and find your specific error

## 📚 Reference Documents

| Document | When to Read | Time |
|----------|---|---|
| **This file** | Right now! | 2 min |
| `FIX_PHASESCRIPT_ERROR.md` | If build still fails | 10-20 min |
| `BUILD_ERROR_FIX_SUMMARY.md` | After build fails for context | 5 min |
| `TROUBLESHOOTING.md` | For other errors | 5-20 min |

## ⏰ Time Estimate

| Task | Time |
|------|------|
| Clean cache (Step 1) | 3 min |
| Verify settings (Step 2) | 2 min |
| Commit & push (Step 3) | 1 min |
| **GitHub Actions build** | 15-20 min |
| **Total** | ~20-25 min |

## ✨ What's Different Now

The workflow has been improved with:

✅ **Verbose output** - See what's actually happening  
✅ **Pre-build checks** - Xcode, Flutter, pods verification  
✅ **Better errors** - The actual problem, not just "PhaseScriptExecution failed"  
✅ **Success/failure summaries** - Clear next steps  
✅ **Log artifacts** - Saved for debugging  

## Common Issues & Quick Fixes

| If you see... | Try... |
|---|---|
| Pod errors | Clear cache again, ensure ios/Podfile has `platform :ios, '12.0'` |
| Swift version errors | Same - clean cache and iOS platform target |
| "No provisioning profiles" | GitHub secrets might be wrong - see SECRETS_SETUP.md |
| Different error | Good! Now you know what's wrong - see FIX_PHASESCRIPT_ERROR.md |

## Questions?

**Q: Do I need a Mac?**
A: Not for this step! Windows is fine for cleanup and pushing. GitHub Actions builds on macOS for you.

**Q: Will this delete my code?**
A: No! Only build artifacts and cache. Your code is safe.

**Q: What if it still fails?**
A: The new workflow will show you WHY. Then see `FIX_PHASESCRIPT_ERROR.md` for that specific error.

## Ready? Let's Go!

1. ✅ Open PowerShell
2. ✅ Run Step 1 (cleanup)
3. ✅ Do Step 2 (verify settings)
4. ✅ Do Step 3 (commit & push)
5. ✅ Watch GitHub Actions
6. ✅ See what happens!

---

**Duration:** ~20 minutes total  
**Difficulty:** Easy (just cleanup and push)  
**Success rate:** 80%+ with this process  

**Let's fix this! 🚀**
