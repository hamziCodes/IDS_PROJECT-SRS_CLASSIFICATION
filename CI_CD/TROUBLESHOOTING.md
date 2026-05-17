# Troubleshooting Guide

Common issues and their solutions for the iOS TestFlight CI/CD workflow.

## 🚨 Most Common Issue: PhaseScriptExecution Error

If you're seeing:
```
Command PhaseScriptExecution failed with a nonzero exit code
```

**⚡ See:** [FIX_PHASESCRIPT_ERROR.md](FIX_PHASESCRIPT_ERROR.md) ← **Start here!**

This comprehensive guide covers:
- Root causes and solutions
- Step-by-step fix process
- Common variations and fixes
- What to do on Windows (you!)

---

## Build Issues

### "Certificate not found" Error

**Problem:** Workflow fails when trying to sign the app

**Solutions:**
1. Verify your `.p8` file was downloaded correctly
2. Check that `APPSTORE_API_KEY_P8_BASE64` is properly Base64 encoded
3. Ensure your Team ID in ExportOptions.plist is correct
4. Try regenerating the API key in App Store Connect:
   - Delete the old key
   - Create a new one
   - Update GitHub secrets

**Check:**
```bash
# Verify .p8 file content starts with:
-----BEGIN PRIVATE KEY-----
```

---

### "No provisioning profiles found"

**Problem:** Build fails because provisioning profiles can't be downloaded

**Solutions:**
1. Check Bundle ID exactly matches App Store Connect
2. Verify your app is enabled for iOS in App Store Connect
3. Ensure your API key has correct permissions (Admin or Developer)
4. Try manually building locally first:
   ```bash
   cd vertex_app
   flutter build ipa --release
   ```
5. If local build works, the issue is with CI/CD secrets

**Check:**
```bash
# Verify Bundle ID
grep -r "PRODUCT_BUNDLE_IDENTIFIER" vertex_app/ios/Podfile
```

---

### Build Times Out

**Problem:** Workflow exceeds time limit and fails

**Expected Times:**
- First build: 20-25 minutes
- Subsequent builds: 15-20 minutes
- Special case: 30+ minutes is normal sometimes

**Solutions:**
1. Verify Flutter dependencies are cached (usually automatic)
2. Check for errors in the logs (timeouts often hide real errors)
3. Try re-running the workflow
4. Consider that GitHub macOS runners may be slow

---

### "Invalid export options"

**Problem:** `ExportOptions.plist` format is incorrect

**Solutions:**
1. Verify file location: `vertex_app/ios/ExportOptions.plist`
2. Check file is valid XML (use an XML validator)
3. Ensure all required keys are present:
   - `method` (should be `app-store`)
   - `signingStyle` (should be `automatic`)
   - `teamID` (must be your Team ID)
4. Compare with template in `CI_CD/examples/ExportOptions.plist`

**Check:**
```bash
# Validate XML structure
plutil -lint vertex_app/ios/ExportOptions.plist
```

---

### "Xcode build failed"

**Problem:** Flutter/Xcode compilation fails

**Solutions:**
1. Check the error message in workflow logs carefully
2. Try cleaning and rebuilding locally:
   ```bash
   cd vertex_app
   flutter clean
   flutter pub get
   flutter build ipa --release
   ```
3. If local build fails, fix the code first
4. Check iOS minimum deployment target matches Flutter requirements

**Common Xcode errors:**
- Missing pods: Run `flutter pub get`
- Swift version mismatch: Check Xcode project settings
- Missing dependencies: Run `pod install` in `ios/` directory

---

## GitHub Actions Issues

### "Workflow not triggering"

**Problem:** Pushing to main doesn't trigger the workflow

**Solutions:**
1. Check workflow file exists: `.github/workflows/ios-testflight.yml`
2. Verify you're pushing to the `main` branch (not `master` or other)
3. Ensure the workflow file has correct syntax:
   ```bash
   # Validate YAML
   yamllint .github/workflows/ios-testflight.yml
   ```
4. Try manual trigger:
   - Go to GitHub → Actions
   - Select "iOS TestFlight Deployment"
   - Click "Run workflow"
5. Check branch protection rules aren't blocking the action

---

### "Secret not found" Error

**Problem:** Workflow fails because it can't access GitHub secrets

**Solutions:**
1. Verify secret name exactly matches (case-sensitive):
   - ✅ `APPSTORE_ISSUER_ID`
   - ❌ `appstore_issuer_id` (wrong case)
   - ❌ `APPSTORE_API_KEY` (wrong name)

2. Ensure secrets are in the right repository (not organization-level)

3. Check secrets are not empty:
   - Go to Settings → Secrets → Verify each has a value

4. If recently added, wait 1-2 minutes and re-run workflow

**Check:**
```bash
# List secret names (but not values) - use GitHub UI:
# Settings → Secrets and variables → Actions
```

---

### "Authentication failed"

**Problem:** API calls to App Store Connect are failing

**Solutions:**
1. Verify all API credentials are correct:
   - `APPSTORE_ISSUER_ID`: Should be a UUID
   - `APPSTORE_API_KEY_ID`: Should be 8 characters
   - `APPSTORE_API_PRIVATE_KEY`: Should start with `-----BEGIN`

2. Check API key hasn't expired:
   - Go to App Store Connect
   - Verify key is still listed under Users and Access

3. Regenerate key if unsure:
   - Delete old key
   - Create new one
   - Update all GitHub secrets

4. Ensure API key has correct permissions (Admin or Developer)

---

## TestFlight Issues

### Build doesn't appear in TestFlight

**Problem:** Build uploaded successfully but doesn't show in TestFlight

**Expected timing:** 5-10 minutes after upload completes

**Solutions:**
1. Wait 10 minutes (processing takes time)
2. Refresh App Store Connect page
3. Check if build is in "Processing" state:
   - Go to App Store Connect → Your App → TestFlight → Builds
   - Status should change from "Processing" to "Ready to Test"

4. If stuck on "Processing" for >20 minutes:
   - Go to App Store Connect
   - Check for any warning messages
   - Try uploading build again

---

### "Build rejected by TestFlight"

**Problem:** Build appears then is rejected

**Common reasons:**
1. **Incorrect build number:** Must be unique per version
   - Edit `pubspec.yaml`: Change `version: 1.0.0+2` (increment the `+2` part)
   - Rebuild and push

2. **Binary incompatibilities:** Run local tests
   ```bash
   cd vertex_app
   flutter build ipa --release
   ```

3. **Cryptography issues:** Ensure signing certificate is valid
   - Check ExportOptions.plist has correct teamID
   - Verify API key is not expired

4. **Code compliance:** Review build logs for warnings

**Solution:** Fix issue and increment build number, then re-push to trigger new build

---

### Can't download build on device

**Problem:** Build appears in TestFlight but won't download on test device

**Solutions:**
1. Verify device is registered in App Store Connect:
   - Your App → TestFlight → Testers
   - Add device UDID if not listed

2. Check tester has accepted TestFlight invitation:
   - Send invitation email
   - Tester must tap the TestFlight link

3. Ensure device is running compatible iOS version:
   - Check your Flutter project minimum iOS target
   - Device must have equal or higher iOS version

4. Try on different device:
   - Helps determine if issue is device-specific

5. Sign out and sign back into TestFlight app

---

## Version & Build Number Issues

### "Build number is not higher than previous"

**Problem:** TestFlight rejects build because number wasn't incremented

**Understanding build numbers:**
```
version: 1.0.0+5
         │ │ │ │
    Major Major Minor │ Build Number
                       │
              This must increase each build!
```

**Solutions:**
1. Edit `vertex_app/pubspec.yaml`
2. Increment the build number (after the `+`):
   ```yaml
   # Change from:
   version: 1.0.0+5
   # To:
   version: 1.0.0+6
   ```

3. Push the change to trigger new build

**Remember:** Build number must always increase, even if version stays the same

---

### App version not updating in TestFlight

**Problem:** TestFlight shows old version number

**Solutions:**
1. Verify `pubspec.yaml` has new version
2. Check the uploaded build's build number
3. See "Build number is not higher" section above
4. Try clearing TestFlight app cache on device

---

## Local Testing

### "Flutter not found" when testing locally

**Problem:** Can't run flutter commands locally

**Solutions:**
```bash
# Check Flutter installation
flutter --version

# If not found, install Flutter:
# https://docs.flutter.dev/get-started/install/windows

# Or add to PATH in PowerShell:
$env:Path += ";C:\flutter\bin"
```

---

### Local build succeeds but CI/CD fails

**Problem:** Build works on your machine but fails in GitHub Actions

**Common causes:**
1. Different Flutter version
   - Check workflow: `.github/workflows/ios-testflight.yml`
   - Update your local Flutter to match

2. Missing secrets (can't test locally)
   - Local uses your certificate already installed
   - CI/CD must download from App Store Connect

3. Different Xcode versions
   - Workflow uses latest macOS, you might have older Xcode
   - Update Xcode to latest

**Debug locally:**
```bash
cd vertex_app

# Clean everything
flutter clean

# Get fresh dependencies
flutter pub get

# Try building
flutter build ipa --release
```

---

## Network & Permission Issues

### "Network error" during upload

**Problem:** Upload to TestFlight fails with network error

**Solutions:**
1. Check your internet connection is stable
2. Check if App Store Connect is accessible
3. Try running workflow again (might be temporary)
4. Check GitHub status page for outages

---

### "Permission denied" error

**Problem:** Workflow can't access files or directories

**Solutions:**
1. Check file permissions in `vertex_app/` directory
2. Ensure `ExportOptions.plist` is readable
3. Verify `.p8` file has correct permissions locally (before Base64 encoding)

---

## Getting Help

If you're stuck:

1. **Read error message carefully** - usually contains the issue
2. **Check workflow logs** - GitHub Actions shows detailed output
3. **Search similar issues** - Someone probably had same problem
4. **Try local build** - Helps isolate CI/CD vs code issues
5. **Regenerate API key** - Often fixes authentication issues

## Escalation

If still stuck:
1. Review App Store Connect API docs
2. Check [Flutter documentation](https://docs.flutter.dev/deployment/ios)
3. Contact Apple Developer Support
4. Check GitHub Actions documentation

---

## Quick Reference

| Issue | Check | Fix |
|-------|-------|-----|
| Build timeout | Logs | Wait longer or re-run |
| Secret error | Case sensitivity | Fix secret name |
| Certificate error | API key expiry | Regenerate key |
| No TestFlight build | 10 min wait | Check processing status |
| Build number error | pubspec.yaml | Increment `+` number |
| Local works, CI fails | Flutter version | Match workflow version |
| Can't download app | Device registered | Add to TestFlight testers |

---

Last updated: May 2026
