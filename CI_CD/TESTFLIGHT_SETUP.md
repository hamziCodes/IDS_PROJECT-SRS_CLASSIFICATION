# iOS TestFlight CI/CD Setup Guide

This guide walks you through setting up automated iOS TestFlight deployment using GitHub Actions. The workflow automatically builds and uploads your Flutter app to TestFlight whenever you push to the `main` branch.

## Prerequisites

- ✅ Flutter project (vertex_app) with iOS target
- ✅ Apple Developer Account (paid)
- ✅ Xcode project properly configured
- ✅ App registered in App Store Connect
- ✅ GitHub repository with Actions enabled

## Step 1: Create App Store Connect API Key

1. Go to [App Store Connect](https://appstoreconnect.apple.com/)
2. Click your profile → **Users and Access** → **Keys** tab
3. Under "App Store Connect API", click the **+** icon
4. Fill in details:
   - **Name:** `GitHub Actions`
   - **Access:** `Admin`
5. Click **Generate**
6. Download the `.p8` file immediately (you can't download it again!)
7. Keep this file safe - you'll need it for GitHub secrets

## Step 2: Get Your App ID Information

1. In App Store Connect, go to **Apps** → Select your app
2. Copy your **Bundle ID** (e.g., `com.example.vertexApp`)
3. Go to **Users and Access** → **Keys** (App Store Connect API section)
4. Find your newly created key and note:
   - **Key ID** (8 character code)
   - **Issuer ID** (40 character UUID)

## Step 3: Configure GitHub Secrets

1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Create these secrets (click **New repository secret** for each):

### Required Secrets:

| Secret Name | Value | Where to get it |
|-------------|-------|-----------------|
| `APPSTORE_ISSUER_ID` | Your Issuer ID | App Store Connect → Users and Access → Keys |
| `APPSTORE_API_KEY_ID` | Your Key ID | App Store Connect → Users and Access → Keys |
| `APPSTORE_API_PRIVATE_KEY` | Content of `.p8` file | App Store Connect (downloaded file) |
| `APPSTORE_API_KEY_P8_BASE64` | Base64 encoded `.p8` file | See below |
| `KEYCHAIN_PASSWORD` | Any secure password | Create one yourself |

### How to create `APPSTORE_API_KEY_P8_BASE64`:

**On Windows PowerShell:**
```powershell
$bytes = [System.IO.File]::ReadAllBytes("C:\path\to\your\AuthKey_*.p8")
$base64 = [System.Convert]::ToBase64String($bytes)
$base64 | Set-Clipboard
# Now paste into GitHub secret
```

**Or on macOS/Linux:**
```bash
base64 -i ~/path/to/AuthKey_*.p8 | pbcopy
# Now paste into GitHub secret
```

### Optional Secrets:

| Secret Name | Value | Purpose |
|-------------|-------|---------|
| `SLACK_WEBHOOK` | Your Slack webhook URL | Get notifications when builds fail |

## Step 4: Update iOS Project Configuration

Your Flutter project needs proper iOS configuration:

### Update `vertex_app/ios/Runner/Info.plist`
Ensure it includes:
```xml
<key>CFBundleIdentifier</key>
<string>com.example.vertexApp</string>
```

### Update `vertex_app/pubspec.yaml`
Make sure your version is set correctly:
```yaml
version: 1.0.0+1
```

## Step 5: Create ExportOptions.plist

Create `vertex_app/ios/ExportOptions.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>compileBitcode</key>
    <false/>
    <key>destination</key>
    <string>upload</string>
    <key>distributionBundleIdentifier</key>
    <string>com.example.vertexApp</string>
    <key>method</key>
    <string>app-store</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>stripSwiftSymbols</key>
    <true/>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>thinning</key>
    <string>&lt;none&gt;</string>
    <key>uploadBitcode</key>
    <true/>
</dict>
</plist>
```

Replace `YOUR_TEAM_ID` with your Apple Team ID (get from Apple Developer account).

## Step 6: Test the Workflow

1. **Manual trigger (recommended for first test):**
   - Push a commit to `main` branch OR
   - Go to GitHub repository → **Actions** → **iOS TestFlight Deployment** → **Run workflow**

2. **Monitor the build:**
   - Click the workflow run to see logs
   - Wait for all steps to complete (typically 15-25 minutes)

3. **Verify in App Store Connect:**
   - Go to App Store Connect → Your App → **TestFlight**
   - Your build should appear in 5-10 minutes

## Step 7: Troubleshooting

### Build fails with "Certificate not found"
- Verify your `.p8` file is correctly encoded to Base64
- Check that your Team ID in ExportOptions.plist matches Apple Developer account

### "No provisioning profiles found"
- Ensure your Bundle ID in Xcode matches App Store Connect
- Run locally with Xcode first to verify signing works

### Build times out
- The first build can take 20+ minutes
- GitHub Actions macOS runners are slower than local Macs
- Check for compilation errors in the workflow logs

### App rejected by TestFlight
- Check iOS build number is incremented
- Update `pubspec.yaml` version/build number
- Review build logs for warnings

## Step 8: Configure Build Triggers (Optional)

The workflow currently triggers on:
- ✅ Push to `main` branch
- ✅ Manual trigger via GitHub UI

To customize, edit `.github/workflows/ios-testflight.yml`:

**Trigger on release tags:**
```yaml
on:
  push:
    tags:
      - 'v*.*.*'
```

**Trigger on pull requests (for testing):**
```yaml
on:
  pull_request:
    branches:
      - main
```

## Step 9: Next Steps

After successful TestFlight build:

1. **Invite testers** in App Store Connect → TestFlight → Internal Testers
2. **Collect feedback** from testers
3. **Iterate** - make changes and push to main
4. **Submit to App Store** when ready for production

## Reference Files

- **Workflow:** `.github/workflows/ios-testflight.yml`
- **Export Config:** `vertex_app/ios/ExportOptions.plist`
- **Flutter Config:** `vertex_app/pubspec.yaml`
- **iOS Info:** `vertex_app/ios/Runner/Info.plist`

## Security Best Practices

⚠️ **IMPORTANT:**

- ✅ Never commit your `.p8` file to version control
- ✅ Use GitHub repository secrets for all sensitive data
- ✅ Rotate your API key periodically (every 6-12 months)
- ✅ Use minimal permissions (don't use Admin unless necessary)
- ✅ Review GitHub Actions logs for sensitive information
- ✅ Enable branch protection rules on `main`

## Quick Reference Commands

```bash
# Navigate to project
cd d:\IDS_PROJECT\vertex_app

# Get Flutter dependencies
flutter pub get

# Build locally for testing
flutter build ipa --release

# Check iOS project
open ios/Runner.xcworkspace

# View workflow logs
# Go to: GitHub → Actions → iOS TestFlight Deployment
```

## Support

For issues:
1. Check workflow logs in GitHub Actions
2. Review `CI_CD/SECRETS_SETUP.md` for secrets configuration
3. Consult [Apple App Store Connect API docs](https://developer.apple.com/documentation/appstoreconnectapi)
4. Check [Flutter iOS build docs](https://docs.flutter.dev/deployment/ios)
