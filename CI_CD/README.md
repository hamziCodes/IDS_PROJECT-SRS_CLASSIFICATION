# CI/CD - Automated iOS TestFlight Deployment

Welcome! This directory contains everything you need to automatically build and deploy your Flutter app to TestFlight from Windows.

## 🚀 Quick Start (15 minutes)

1. **[QUICK_START.md](QUICK_START.md)** ← **Start here!** (5-minute checklist)
2. Configure GitHub secrets (5 minutes)
3. Push to main branch (automatic deployment)

## 📚 Complete Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[QUICK_START.md](QUICK_START.md)** | **Fast checklist to get started** | 5 min |
| **[TESTFLIGHT_SETUP.md](TESTFLIGHT_SETUP.md)** | Complete step-by-step guide | 15 min |
| **[SECRETS_SETUP.md](SECRETS_SETUP.md)** | How to configure GitHub secrets | 10 min |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues and fixes | 5-20 min |
| **[CI_CD_OVERVIEW.md](CI_CD_OVERVIEW.md)** | Technical overview | 5 min |

## 🎯 What This Does

```
You push code to 'main' branch on GitHub
              ↓
GitHub Actions automatically:
  1. Spins up a macOS runner
  2. Builds your iOS app
  3. Signs it with your Apple certificate
  4. Uploads to TestFlight
  5. 5-10 minutes later, testers can download
              ↓
You get results in TestFlight!
```

## ✅ What You Need

- ✅ Paid Apple Developer Account
- ✅ App created in App Store Connect
- ✅ GitHub account with admin access to repo
- ✅ Windows PC (where you are now!)

## 📋 Setup Process Overview

### 1️⃣ Create API Key (5 min)
Go to App Store Connect → Users and Access → Keys → Create new API key for GitHub Actions

### 2️⃣ Add GitHub Secrets (5 min)
Copy API credentials to GitHub → Settings → Secrets

### 3️⃣ Configure iOS Project (5 min)
Copy example files and update your Bundle ID and Team ID

### 4️⃣ Test (5 min)
Push to main or manually trigger workflow

**Total time: ~20 minutes to go from nothing to first TestFlight build!**

## 📂 File Structure

```
CI_CD/
├── QUICK_START.md                    # ⭐ Start here (5-min checklist)
├── CI_CD_OVERVIEW.md                 # Technical overview
├── TESTFLIGHT_SETUP.md               # Detailed guide
├── SECRETS_SETUP.md                  # Secret configuration
├── TROUBLESHOOTING.md                # Fix common issues
├── README.md                         # This file
├── scripts/
│   ├── validate-setup.sh             # Verify setup (bash)
│   ├── validate-setup.ps1            # Verify setup (PowerShell)
│   └── local-build-test.sh           # Test build locally
└── examples/
    ├── ExportOptions.plist           # iOS export config
    └── README.md                     # How to use examples
```

## 🔧 Key Files in Your Project

| File | Purpose |
|------|---------|
| `.github/workflows/ios-testflight.yml` | GitHub Actions workflow (automated build) |
| `vertex_app/ios/ExportOptions.plist` | iOS signing configuration (you need to create) |
| `vertex_app/pubspec.yaml` | Flutter version config |
| GitHub Secrets | API credentials (keep secret!) |

## 🎓 Learning Path

**New to CI/CD?**
1. Read [QUICK_START.md](QUICK_START.md) - Get oriented
2. Read [CI_CD_OVERVIEW.md](CI_CD_OVERVIEW.md) - Understand the process
3. Follow [TESTFLIGHT_SETUP.md](TESTFLIGHT_SETUP.md) - Step by step

**Already know what you're doing?**
1. Jump to [QUICK_START.md](QUICK_START.md)
2. Reference [SECRETS_SETUP.md](SECRETS_SETUP.md) for credentials
3. Use [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if issues arise

## 🚨 Important Security Notes

🔒 **NEVER:**
- ❌ Commit your `.p8` file to Git
- ❌ Share your GitHub secrets
- ❌ Post your API keys online
- ❌ Use production secrets for testing

✅ **DO:**
- ✅ Store `.p8` file securely offline
- ✅ Use GitHub's encrypted secrets storage
- ✅ Rotate keys periodically
- ✅ Review what each secret does

## 📊 Expected Timeline

| Stage | Duration | What Happens |
|-------|----------|--------------|
| Initial Setup | 15-20 min | Create API key, add secrets, configure files |
| First Build | 20-25 min | GitHub builds app and uploads to TestFlight |
| TestFlight Processing | 5-10 min | Apple processes the build |
| Tester Access | Immediate | You can immediately add and invite testers |
| Subsequent Builds | 15-20 min | Push → Build → TestFlight (fully automatic) |

## 💻 Getting Started Steps

### For Windows Users (You!)

1. Open Terminal/PowerShell in your project folder
2. Read [QUICK_START.md](QUICK_START.md)
3. Complete the checklist
4. GitHub Actions handles the rest!

No need for a Mac during setup - you're on Windows pushing code. GitHub Actions runs on their macOS servers.

## 🔄 Typical Workflow After Setup

```
Every time you want to deploy:

1. Make your code changes
2. git push origin main
3. GitHub automatically:
   - Builds iOS app
   - Signs it
   - Uploads to TestFlight
4. Monitor at: GitHub → Actions tab
5. 15-20 minutes later: New build in TestFlight!
6. Invite testers and get feedback
7. Repeat
```

## ✨ Key Benefits

✅ **Automatic** - No manual build process  
✅ **Fast** - 15-20 minutes from push to TestFlight  
✅ **Reliable** - Same build process every time  
✅ **Scalable** - Works for any number of builds  
✅ **Secure** - Credentials stored safely in GitHub  

## 🎯 First Deployment Checklist

Before pushing your first build:

- [ ] Created API key in App Store Connect
- [ ] Added all 5 secrets to GitHub
- [ ] Created `vertex_app/ios/ExportOptions.plist`
- [ ] Updated ExportOptions.plist with your Team ID and Bundle ID
- [ ] Verified version format in `pubspec.yaml` is `X.Y.Z+N`
- [ ] Read at least [QUICK_START.md](QUICK_START.md)

Ready? Push to main and watch it go! 🚀

## 📞 Need Help?

1. **Just starting?** → Read [QUICK_START.md](QUICK_START.md)
2. **Stuck on setup?** → Check [TESTFLIGHT_SETUP.md](TESTFLIGHT_SETUP.md)
3. **Having secrets issues?** → See [SECRETS_SETUP.md](SECRETS_SETUP.md)
4. **Build failed?** → Look at [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
5. **Want to understand it?** → Read [CI_CD_OVERVIEW.md](CI_CD_OVERVIEW.md)

## 🌐 External Resources

- [Apple App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flutter iOS Deployment](https://docs.flutter.dev/deployment/ios)
- [Xcode Build Settings](https://developer.apple.com/documentation/xcode/build-settings-reference)

## 📝 File Reference

### Documentation Files
- `README.md` - This file
- `QUICK_START.md` - Fast 5-minute setup checklist
- `TESTFLIGHT_SETUP.md` - Complete step-by-step guide  
- `SECRETS_SETUP.md` - GitHub secrets configuration
- `TROUBLESHOOTING.md` - Solving common problems
- `CI_CD_OVERVIEW.md` - Technical details

### Script Files
- `scripts/validate-setup.sh` - Verify setup (requires bash)
- `scripts/validate-setup.ps1` - Verify setup (PowerShell)
- `scripts/local-build-test.sh` - Test build locally (bash)

### Example Files
- `examples/ExportOptions.plist` - Template for iOS export config
- `examples/README.md` - How to use the examples

## 🎉 Success!

You're all set! Once you complete the setup:

✅ **New builds upload automatically** when you push to main  
✅ **No Mac required** on your Windows machine  
✅ **TestFlight updated automatically**  
✅ **Testers get access immediately**  
✅ **Full audit trail** in GitHub Actions  

Happy deploying! 🚀

---

**Last Updated:** May 2026  
**Workflow Status:** Active and maintained  
**Framework:** Flutter + GitHub Actions + TestFlight
