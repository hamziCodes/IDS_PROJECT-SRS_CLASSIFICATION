# Quick Start Guide - iOS TestFlight CI/CD

Complete this checklist in order to get TestFlight deployment working.

## ✅ Pre-Requirements (Do these first)

- [ ] You have a paid Apple Developer Account
- [ ] Your app is created in App Store Connect
- [ ] You have administrator access to your GitHub repository
- [ ] Flutter is installed on your development machine

## 📋 Setup Checklist

### Step 1: Create API Key (5 minutes)

- [ ] Go to [App Store Connect](https://appstoreconnect.apple.com/)
- [ ] Click profile → Users and Access → Keys (App Store Connect API)
- [ ] Click **+** to create new key
- [ ] Name it: `GitHub Actions`
- [ ] Set Access level: `Admin`
- [ ] Click **Generate**
- [ ] **Download and save the `.p8` file** (download only once!)
- [ ] Note your **Key ID** (8 characters)
- [ ] Note your **Issuer ID** (UUID)

### Step 2: Configure GitHub Secrets (10 minutes)

- [ ] Open your GitHub repository
- [ ] Go to **Settings** → **Secrets and variables** → **Actions**
- [ ] Create 5 secrets (click "New repository secret" for each):

| Secret Name | Value from |
|---|---|
| `APPSTORE_ISSUER_ID` | App Store Connect → Keys |
| `APPSTORE_API_KEY_ID` | App Store Connect → Keys |
| `APPSTORE_API_PRIVATE_KEY` | Content of downloaded `.p8` file |
| `APPSTORE_API_KEY_P8_BASE64` | Base64 encoded `.p8` file (use `CI_CD/SECRETS_SETUP.md`) |
| `KEYCHAIN_PASSWORD` | Create any strong password |

**How to encode `.p8` to Base64 (Windows PowerShell):**
```powershell
$p8FilePath = "C:\Users\YourName\Downloads\AuthKey_XXXXX.p8"
$bytes = [System.IO.File]::ReadAllBytes($p8FilePath)
$base64 = [System.Convert]::ToBase64String($bytes)
$base64 | Set-Clipboard
# Now paste into GitHub secret APPSTORE_API_KEY_P8_BASE64
```

### Step 3: Update iOS Configuration (10 minutes)

- [ ] Find your **Bundle ID** in App Store Connect (e.g., `com.example.app`)
- [ ] Find your **Team ID** in Apple Developer account (10 characters)
- [ ] Copy `CI_CD/examples/ExportOptions.plist` to `vertex_app/ios/ExportOptions.plist`
- [ ] Edit the file and update:
  - [ ] Replace `YOUR_TEAM_ID_HERE` with your Team ID
  - [ ] Replace `com.example.vertexApp` with your Bundle ID
- [ ] Update `vertex_app/pubspec.yaml`:
  - [ ] Version format should be `X.Y.Z+N` (e.g., `1.0.0+1`)
  - [ ] Increment the `+N` number for each new build

### Step 4: Test Setup Locally (Optional but Recommended)

From your Windows machine:
```powershell
# Navigate to project
cd d:\IDS_PROJECT

# Run validation (optional)
# Requires bash, or use manual checks above

# Or manually verify:
# 1. ExportOptions.plist exists at vertex_app/ios/ExportOptions.plist
# 2. All GitHub secrets are set
# 3. pubspec.yaml has correct version format
```

### Step 5: Trigger First Build (5 minutes)

Option A - Manual trigger (recommended for first test):
- [ ] Go to GitHub → Actions
- [ ] Select "iOS TestFlight Deployment"
- [ ] Click "Run workflow" button

Option B - Automatic trigger:
- [ ] Make a change to your code
- [ ] Push to `main` branch
- [ ] GitHub Actions automatically triggers

### Step 6: Monitor Build

- [ ] Go to GitHub → Actions
- [ ] Click the running workflow to see logs
- [ ] Wait for build to complete (15-25 minutes)
- [ ] Check for any errors in logs

### Step 7: Verify in TestFlight

- [ ] Go to [App Store Connect](https://appstoreconnect.apple.com/)
- [ ] Select your app → TestFlight tab
- [ ] You should see your build appear in 5-10 minutes
- [ ] Status should change from "Processing" to "Ready to Test"

### Step 8: Set Up Testers (Optional)

- [ ] In App Store Connect, go to your app → TestFlight
- [ ] Add testers in "Internal Testers" section
- [ ] Send them invitations
- [ ] They receive email and can download app

## 🎯 Common Next Steps

After successful first build:

1. **Iterate on your app** - Make changes, push to main, new build uploads automatically
2. **Invite external testers** - After internal testing is done
3. **Collect feedback** - Use TestFlight feedback feature
4. **Increment version** - Update `pubspec.yaml` before each build
5. **Submit to App Store** - When ready for production

## 📚 Documentation

If you need help:

| Document | When to Read |
|----------|--------------|
| `CI_CD_OVERVIEW.md` | Overview of the entire setup |
| `TESTFLIGHT_SETUP.md` | Detailed step-by-step guide |
| `SECRETS_SETUP.md` | How to configure GitHub secrets |
| `TROUBLESHOOTING.md` | Common issues and fixes |
| `examples/README.md` | Understanding ExportOptions.plist |

## 🔑 Important Security Notes

⚠️ **CRITICAL:**

- **Never commit your `.p8` file** to Git
- **Never share your secrets** with anyone
- Keep your `.p8` file in a safe location offline
- Use GitHub secrets for all sensitive data
- Review GitHub Actions logs for sensitive information
- Rotate your API key every 6-12 months

## 💡 Pro Tips

1. **Version bumping:** Always increment the build number (`+N` part) before pushing
2. **Testing locally:** Run `cd vertex_app && flutter build ipa --release` to test locally
3. **Fast iterations:** Just push to main, CI/CD handles the rest
4. **Slack notifications:** Add optional `SLACK_WEBHOOK` secret for build status
5. **Check build logs:** If something fails, the logs usually explain why

## ✨ Success!

Once you've completed all steps above:
- ✅ New builds upload automatically when you push to `main`
- ✅ TestFlight is updated automatically
- ✅ Testers can download immediately
- ✅ You can iterate quickly

---

## Quick Commands Reference

```powershell
# View GitHub Actions logs
# Go to: GitHub → Actions → iOS TestFlight Deployment

# View your secrets (safe)
# Go to: GitHub → Settings → Secrets → Actions

# Increment build number
# Edit: vertex_app/pubspec.yaml
# Change: version: 1.0.0+1  →  version: 1.0.0+2

# Clean local Flutter cache
cd vertex_app
flutter clean
flutter pub get
```

## Need Help?

1. **Read the detailed docs** - Start with `TESTFLIGHT_SETUP.md`
2. **Check troubleshooting** - See `TROUBLESHOOTING.md`
3. **Review workflow logs** - GitHub shows exact error messages
4. **Check secrets** - Most issues are missing/wrong secrets

---

**Ready to deploy?** Start with Step 1 above! 🚀
