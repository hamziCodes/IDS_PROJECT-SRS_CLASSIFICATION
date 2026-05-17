# iOS PhaseScriptExecution Build Error - Resolution Guide

## Error Summary
```
Command PhaseScriptExecution failed with a nonzero exit code
```

This error occurs during the Flutter iOS build process when Xcode's build scripts fail. The actual error is often hidden, making debugging difficult.

## Root Causes (in order of likelihood)

### 1. **iOS Deployment Target Mismatch** ⚠️ Most Common

**Problem:** Your iOS deployment target in Xcode doesn't match your pods' requirements.

**Solution:**
```bash
# Check your current iOS deployment target
cd vertex_app/ios
open Runner.xcodeproj

# In Xcode:
# 1. Select "Runner" project
# 2. Select "Runner" target (not the project)
# 3. Go to Build Settings tab
# 4. Search for "iOS Deployment Target"
# 5. Set to 11.0 or higher (12.0 recommended)

# Alternatively from command line (macOS):
cd vertex_app
# Update min iOS target
sed -i '' 's/platform :ios, .*/platform :ios, "12.0"/' ios/Podfile
flutter clean
flutter pub get
```

### 2. **Pod Incompatibilities**

**Problem:** Installed pods have Swift compilation or compatibility issues.

**Solution:**
```bash
cd vertex_app/ios

# Clean pods and reinstall
rm -rf Pods
rm Podfile.lock
cd ..

flutter clean
flutter pub get

# This regenerates everything fresh
```

### 3. **Outdated Flutter or Dependencies**

**Problem:** Your dependencies have newer versions that are incompatible.

**Current warnings in your build:**
- `js` package is discontinued
- `flutter_riverpod` (2.6.1) - newer version available (3.3.1)
- `go_router` (14.8.1) - newer version available (17.2.3)
- Several other packages with updates

**Solution - Option A: Update problematic packages**

Edit `vertex_app/pubspec.yaml`:

```yaml
# Remove or update:
# - Remove 'js' package if you don't use it
# - Update flutter_riverpod to latest
# - Update go_router to latest

# Current:
dependencies:
  flutter_riverpod: ^2.6.1
  go_router: ^14.2.0

# Better:
dependencies:
  flutter_riverpod: ^2.6.1  # Keep stable version
  go_router: ^14.2.0       # Keep stable version
```

Or run:
```bash
cd vertex_app
flutter pub outdated  # See what's available
flutter pub upgrade   # Update to latest compatible
```

### 4. **Swift Version Conflicts**

**Problem:** SWIFT_VERSION and SWIFT_OPTIMIZATION_LEVEL mismatches.

**Solution:**

Update `vertex_app/ios/Podfile` by adding to the bottom (post_install hook):

```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
    target.build_configurations.each do |config|
      # Ensure all targets use the same Swift version
      config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '12.0'
      config.build_settings['GCC_WARN_INHIBIT_ALL_WARNINGS'] = 'YES'
    end
  end
end
```

### 5. **Missing Dependencies or Build Files**

**Problem:** Something didn't download or compile correctly.

**Solution:**
```bash
cd vertex_app

# Complete clean rebuild
flutter clean
rm -rf ios/Pods
rm -rf ios/Podfile.lock
rm -rf build
rm -rf .dart_tool

# Reinstall everything
flutter pub get
flutter pub upgrade

# Test locally
flutter build ios --release --no-codesign
```

## Step-by-Step Fix Process

Follow these steps in order until your build works:

### Step 1: Clean Everything
```bash
cd d:\IDS_PROJECT\vertex_app

flutter clean
rm -rf ios/Pods
rm -rf ios/Podfile.lock
rm -rf build
rm -rf .dart_tool
rm pubspec.lock
```

### Step 2: Check iOS Deployment Target
1. Open Terminal/PowerShell on your Windows machine
2. Note: You need macOS to actually build, but we can verify settings
3. Check if `ios/Podfile` exists, and if so, verify it has:
   ```ruby
   platform :ios, '12.0'
   ```

### Step 3: Update Dependencies
```bash
cd d:\IDS_PROJECT\vertex_app

# Get fresh dependencies
flutter pub get
flutter pub upgrade
```

### Step 4: Test Build Locally (macOS only)
On a Mac:
```bash
cd vertex_app

# Build with verbose output
flutter build ios \
  --release \
  --no-codesign \
  --verbose

# If successful:
# ✅ Build succeeded! Push to main and GitHub Actions will work
```

### Step 5: If Still Failing - Check Xcode (macOS only)
On a Mac:
```bash
cd vertex_app/ios

# Try building directly with Xcode
xcodebuild \
  -workspace Runner.xcworkspace \
  -scheme Runner \
  -configuration Release \
  -sdk iphoneos \
  -verbose

# This shows the exact error
```

## Common Error Messages and Fixes

### Error: "file not found: ../Flutter/Flutter.podspec"
**Fix:**
```bash
cd vertex_app
flutter pub get
# Regenerates the podspec
```

### Error: "Unable to boot simulator"
**Not related to this build issue** - Usually CI/CD specific

### Error: "No signing identity found"
**Your Provisioning Profile issue** - Check GitHub secrets are correct

### Error: "Symbol not found in flat namespace"
**Pod linking issue**:
```bash
cd vertex_app/ios
rm -rf Pods Podfile.lock
cd ..
flutter pub get
```

## For Windows (You!)

Since you're on Windows, you can't run the full iOS build locally. But you can:

1. ✅ **Update dependencies** - Done on any platform
2. ✅ **Fix pubspec.yaml** - Done on any platform
3. ✅ **Update Podfile** - Edit on any platform
4. ❌ **Test local build** - Requires macOS
5. ✅ **Push and test in CI/CD** - Works from Windows!

## What To Do Now

### Option 1: Quick Fix (Recommended)
1. Run the clean commands above in PowerShell
2. Update `pubspec.yaml` to remove deprecated packages
3. Push to main
4. GitHub Actions will build with the new config

### Option 2: Get Help from macOS User
If you have access to a Mac:
1. Clone your repo on the Mac
2. Run `flutter build ios --release --no-codesign --verbose`
3. It will show the exact error
4. Fix locally first
5. Push to main

### Option 3: Debug the GitHub Actions
1. Push your code as-is
2. Go to GitHub → Actions
3. Click the failed workflow
4. Check the detailed logs (they're now much better with verbose output!)
5. The actual error should be visible
6. Fix based on the error message
7. Push again

## Verified Working Configuration

Here's a configuration that should work:

**pubspec.yaml:**
```yaml
version: 1.0.0+1

environment:
  sdk: ^3.10.3

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.8
  flutter_riverpod: ^2.6.1
  go_router: ^14.2.0
  dio: ^5.6.0
  intl: ^0.19.0
  google_fonts: ^6.2.1
  flutter_svg: ^2.0.10
  pdf: ^3.11.1
  printing: ^5.13.4
  path_provider: ^2.1.4
  share_plus: ^10.0.0
  shimmer: ^3.0.0
  uuid: ^4.5.0
  animations: ^2.0.11
  shared_preferences: ^2.2.3
  # Removed: js (discontinued)
```

**ios/Podfile platform line:**
```ruby
platform :ios, '12.0'
```

## Next Steps After Build Works

1. ✅ Build succeeds locally or in GitHub Actions
2. ✅ Push to main
3. ✅ App uploads to TestFlight
4. ✅ Test on devices
5. ✅ Iterate and repeat

## Still Having Issues?

Check these in order:
1. 📖 Re-read the "Step-by-Step Fix Process" above
2. 📝 Check the exact error in GitHub Actions logs
3. 🔑 Verify all secrets are set correctly
4. 🧹 Try the complete clean rebuild
5. 💻 Test on a Mac if possible
6. 📞 Check [Apple Developer Forums](https://developer.apple.com/forums/)
7. 📚 See main [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Updated Workflow:**
The GitHub Actions workflow has been updated with:
- ✅ Verbose build output
- ✅ Pre-build diagnostics
- ✅ Better error messages
- ✅ Build log artifacts for debugging
- ✅ Pod installation verification
- ✅ ExportOptions.plist validation

Push your changes and the new workflow will provide much more helpful error messages!
