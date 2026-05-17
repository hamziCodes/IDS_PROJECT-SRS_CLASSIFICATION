# CI/CD Infrastructure Overview

This directory contains all CI/CD configurations and documentation for automated TestFlight deployment.

## 📁 Directory Structure

```
CI_CD/
├── TESTFLIGHT_SETUP.md          # Complete setup guide (START HERE)
├── SECRETS_SETUP.md             # GitHub secrets configuration
├── CI_CD_OVERVIEW.md            # This file
├── TROUBLESHOOTING.md           # Common issues and solutions
├── scripts/
│   ├── validate-setup.sh        # Verify setup is correct
│   └── local-build-test.sh      # Test build locally
└── examples/
    └── ExportOptions.plist      # iOS export configuration template
```

## 🚀 Quick Start

1. **First Time Setup?**
   - Read: `TESTFLIGHT_SETUP.md` (complete guide)
   - Then: `SECRETS_SETUP.md` (configure GitHub secrets)

2. **Need to Troubleshoot?**
   - Check: `TROUBLESHOOTING.md`

3. **Want to Test Locally?**
   - Run: `scripts/local-build-test.sh`

4. **Verify Everything is Set Up?**
   - Run: `scripts/validate-setup.sh`

## 📋 What Gets Automated

The CI/CD workflow (`.github/workflows/ios-testflight.yml`) does:

1. ✅ Automatically builds your iOS app when you push to `main`
2. ✅ Signs the app with your Apple certificate
3. ✅ Uploads to TestFlight automatically
4. ✅ Notifies you when done (Slack notifications optional)
5. ✅ Archives build artifacts for 30 days

## 🔑 Key Files

### Workflow File
- **Location:** `.github/workflows/ios-testflight.yml`
- **Triggers:** Push to main, manual trigger
- **Runtime:** ~15-25 minutes
- **Cost:** Free (GitHub Actions)

### iOS Configuration
- **Location:** `vertex_app/ios/ExportOptions.plist`
- **Purpose:** Tells Xcode how to export the build
- **Required:** Yes, must be created

### Flutter Configuration
- **Location:** `vertex_app/pubspec.yaml`
- **Important Fields:**
  - `version: 1.0.0+1` (must increment build number)
  - Bundle identifier must match App Store Connect

## 🔐 Security

- All secrets stored in GitHub encrypted storage
- `.p8` file never committed to git
- API key has minimal required permissions
- Workflow runs only on `main` branch
- All builds logged and auditable

## 📊 Monitoring

**View Build Status:**
- GitHub repository → Actions tab
- Click "iOS TestFlight Deployment"
- View logs for each workflow run

**Expected Times:**
- Setup: 30 minutes
- First build: 20-25 minutes
- Subsequent builds: 15-20 minutes
- TestFlight availability: 5-10 minutes after upload

## 🔄 Workflow

```
You push code to main
    ↓
GitHub Actions triggers
    ↓
macOS runner starts
    ↓
Flutter builds iOS IPA
    ↓
App gets signed with your certificate
    ↓
Uploaded to TestFlight
    ↓
5-10 min later, testers can access build
    ↓
Get feedback and iterate
```

## 📱 Testing Your App

1. **Internal TestFlight (Fastest)**
   - Automatic once workflow completes
   - For team members & yourself
   - No review process

2. **External TestFlight (With Review)**
   - After testing internally
   - For beta testers outside your team
   - Requires App Store review (~24-48 hours)

3. **App Store Production**
   - Final submission when ready
   - Requires full App Store review

## 🛠️ Common Tasks

### Trigger a New Build
```
Push to main branch OR
GitHub → Actions → Run workflow manually
```

### Increment Build Version
Edit `vertex_app/pubspec.yaml`:
```yaml
version: 1.0.1+2  # Major.Minor.Patch+BuildNumber
```

### Check Build Logs
GitHub → Actions → iOS TestFlight Deployment → Click run → Scroll to see logs

### Stop a Running Build
GitHub → Actions → Running workflow → Cancel workflow

### Re-run a Failed Build
GitHub → Actions → Failed workflow → Re-run jobs

## 📞 Getting Help

1. **Build failed?** → See TROUBLESHOOTING.md
2. **Secrets not working?** → See SECRETS_SETUP.md
3. **First time setup?** → See TESTFLIGHT_SETUP.md
4. **Xcode issues?** → See TESTFLIGHT_SETUP.md → Step 4-5

## 📚 Additional Resources

- [Apple App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flutter iOS Deployment](https://docs.flutter.dev/deployment/ios)
- [Xcode Build Settings](https://developer.apple.com/documentation/xcode/build-settings-reference)

## ✅ Setup Checklist

Before running the workflow, ensure:

- [ ] You have an Apple Developer Account (paid)
- [ ] Your app is created in App Store Connect
- [ ] You have generated API key in App Store Connect
- [ ] All GitHub secrets are configured
- [ ] ExportOptions.plist is created
- [ ] Bundle ID matches App Store Connect
- [ ] Version in pubspec.yaml is set

Once completed, you can push to main and let CI/CD handle the rest!

## 📝 Environment Info

- **Runner OS:** macOS (latest)
- **Flutter Version:** 3.24.0 (configurable in workflow)
- **Xcode:** Latest available
- **iOS Minimum:** iOS 11.0 (default Flutter)
- **Platform:** iOS only (Android uses different workflow)

## 🎯 Next Steps

1. ✅ Read TESTFLIGHT_SETUP.md completely
2. ✅ Follow SECRETS_SETUP.md to configure secrets
3. ✅ Create ExportOptions.plist
4. ✅ Test with manual workflow trigger
5. ✅ Invite testers to TestFlight
6. ✅ Iterate on feedback

Good luck with your iOS deployment! 🚀
