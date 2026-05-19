# GitHub Secrets Configuration Guide

This document provides step-by-step instructions for setting up all required secrets for the iOS TestFlight CI/CD workflow.

## Overview of Required Secrets

| Secret | Type | Purpose |
|--------|------|---------|
| `APPSTORE_ISSUER_ID` | UUID | Identify your Apple Developer account |
| `APPSTORE_API_KEY_ID` | String | Identify your API key |
| `APPSTORE_API_PRIVATE_KEY` | RSA Private Key | Authenticate API requests (raw `.p8` content) |
| `APPSTORE_API_KEY_P8_BASE64` | Base64 String | Encoded version for code signing |
| `KEYCHAIN_PASSWORD` | String | Unlock macOS keychain during build |
| `SLACK_WEBHOOK` | URL | (Optional) Send notifications on build failure |

---

## Detailed Setup Instructions

### 1. Create App Store Connect API Key

**Location:** https://appstoreconnect.apple.com/

**Steps:**
1. Sign in to App Store Connect
2. Click your **profile icon** (top right) → **Users and Access**
3. Go to the **Keys** tab (under "App Store Connect API")
4. Click the **+** button to create a new key
5. Enter **Name:** `GitHub Actions`
6. Set **Access:** `Admin` (or `App Manager` for limited access)
7. Click **Generate**
8. **IMPORTANT:** Download the `.p8` file immediately and save it somewhere safe
   - You can only download it once!
   - Store it in a secure location

**After generation, note down:**
- **Key ID:** 8-character alphanumeric code (e.g., `A1B2C3D4`)
- **Issuer ID:** Long UUID (e.g., `12345678-1234-1234-1234-123456789012`)
- The `.p8` file path

---

### 2. Encode the `.p8` File to Base64

You need to create a Base64-encoded version of your `.p8` file.

#### Option A: Windows PowerShell

```powershell
# Set the path to your .p8 file
$p8FilePath = "C:\Users\hamza\Downloads\jtsTCm.p8"

# Read and encode
$bytes = [System.IO.File]::ReadAllBytes($p8FilePath)
$base64 = [System.Convert]::ToBase64String($bytes)

# Copy to clipboard
$base64 | Set-Clipboard

Write-Host "Base64 encoded key copied to clipboard!"
```

Then paste it into the `APPSTORE_API_KEY_P8_BASE64` secret.

#### Option B: macOS/Linux Terminal

```bash
# Navigate to where you downloaded the .p8 file
cd ~/Downloads

# Encode and copy to clipboard
base64 -i AuthKey_A1B2C3D4.p8 | pbcopy

echo "Base64 encoded key copied to clipboard!"
```

#### Option C: Online Tool (use with caution!)

If you don't have access to terminal/PowerShell:
1. Go to [base64encode.org](https://www.base64encode.org/)
2. Click "Choose File" and select your `.p8` file
3. Click "Encode"
4. Copy the result

⚠️ **Security Note:** Using online tools exposes your private key. Only use if necessary and delete your `.p8` file afterward.

---

### 3. Add Secrets to GitHub

**Location:** Your GitHub repository → Settings → Secrets and variables → Actions

**Steps:**

1. Go to your GitHub repository on github.com
2. Click **Settings** (top menu)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **New repository secret** (green button)

#### Add Each Secret:

**Secret #1: APPSTORE_ISSUER_ID**
- **Name:** `APPSTORE_ISSUER_ID`
- **Value:** Your Issuer ID from Step 1 (the UUID)
- **Example:** `12345678-1234-1234-1234-123456789012`
- Click **Add secret**

**Secret #2: APPSTORE_API_KEY_ID**
- **Name:** `APPSTORE_API_KEY_ID`
- **Value:** Your Key ID from Step 1 (8 characters)
- **Example:** `A1B2C3D4`
- Click **Add secret**

**Secret #3: APPSTORE_API_PRIVATE_KEY**
- **Name:** `APPSTORE_API_PRIVATE_KEY`
- **Value:** The raw content of your `.p8` file (starts with `-----BEGIN PRIVATE KEY-----`)
- Open your `.p8` file in a text editor and copy the entire content
- Click **Add secret**

**Secret #4: APPSTORE_API_KEY_P8_BASE64**
- **Name:** `APPSTORE_API_KEY_P8_BASE64`
- **Value:** The Base64-encoded string from Step 2
- This is the long string you copied to clipboard
- Click **Add secret**

**Secret #5: KEYCHAIN_PASSWORD**
- **Name:** `KEYCHAIN_PASSWORD`
- **Value:** Create a strong password (e.g., `SecurePass123!@#`)
- This password is used to unlock the macOS keychain during the build
- Click **Add secret**

#### Optional - Add Slack Webhook:

**Secret #6: SLACK_WEBHOOK** (Optional)
- **Name:** `SLACK_WEBHOOK`
- **Value:** Your Slack incoming webhook URL
- How to get it:
  1. Go to [Slack App Directory](https://api.slack.com/apps)
  2. Create a new app or select existing
  3. Activate "Incoming Webhooks"
  4. Copy your webhook URL
- Click **Add secret**

---

## Verification Checklist

After adding all secrets, verify:

- [ ] All 5 required secrets are present in GitHub
- [ ] Each secret contains non-empty value
- [ ] Secrets are in the correct repository (not organization-level)
- [ ] `.p8` file is stored safely offline
- [ ] You have access to your Apple Developer account
- [ ] Your iOS app is registered in App Store Connect

---

## Secret Values Reference

Keep this table somewhere safe for future reference:

| Secret Name | Value |
|------------|-------|
| `APPSTORE_ISSUER_ID` | _________________ |
| `APPSTORE_API_KEY_ID` | _________________ |
| `KEYCHAIN_PASSWORD` | _________________ |
| `.p8` file location | _________________ |
| Slack Webhook (optional) | _________________ |

---

## Troubleshooting

### "Secret not found" error in workflow
- Verify secret name exactly matches the workflow file (case-sensitive)
- Example: `APPSTORE_ISSUER_ID` not `appstore_issuer_id`
- Secrets must be in the repository, not organization or environment

### "Invalid API key" error
- Ensure your Key ID and Issuer ID are correct
- Verify the `.p8` file wasn't corrupted when downloading
- Check that you're using the correct Base64 encoding

### "Keychain locked" error
- The KEYCHAIN_PASSWORD secret must be present
- Try regenerating your API key in App Store Connect

### "Invalid provisioning profile"
- Verify your Bundle ID matches exactly in:
  - App Store Connect
  - Xcode project settings
  - Flutter pubspec.yaml (if applicable)

---

## Security Best Practices

🔒 **IMPORTANT:**

1. **Never commit your `.p8` file:**
   ```bash
   # Add to .gitignore
   *.p8
   AuthKey_*.p8
   ```

2. **Rotate API keys periodically:**
   - Create new key every 6-12 months
   - Delete old keys from App Store Connect
   - Update GitHub secrets with new key

3. **Limit API key permissions:**
   - Use `App Manager` role instead of `Admin` if possible
   - Only grant the minimum required permissions

4. **Review workflow logs carefully:**
   - GitHub Actions logs can contain sensitive info
   - Set logs to "private" if needed
   - Be careful when sharing logs for debugging

5. **Use branch protection:**
   - Require reviews before merging to `main`
   - Prevents accidental workflow triggers

6. **Monitor API key usage:**
   - Periodically check App Store Connect for suspicious activity
   - Review GitHub Actions workflow runs

---

## Reference

- [App Store Connect API Documentation](https://developer.apple.com/documentation/appstoreconnectapi)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Apple Security Guidelines](https://developer.apple.com/security/)
