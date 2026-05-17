# Example Files

This directory contains example/template files for the TestFlight CI/CD setup.

## ExportOptions.plist

**Purpose:** Tells Xcode how to export and sign your iOS app for distribution to TestFlight.

**Where to use it:**
1. Copy this file to `vertex_app/ios/ExportOptions.plist`
2. Open it in a text editor
3. Update the values:

### Required Changes:

**1. Update Bundle ID:**
Find:
```xml
<key>com.example.vertexApp</key>
```
Change to your actual Bundle ID from App Store Connect:
```xml
<key>YOUR_BUNDLE_ID_HERE</key>
```

**2. Update Team ID:**
Find:
```xml
<key>teamID</key>
<string>YOUR_TEAM_ID_HERE</string>
```
Change to your Apple Team ID (10 character code):
```xml
<key>teamID</key>
<string>ABCDEF1234</string>
```

How to find your Team ID:
- Apple Developer Account → Membership
- Look for "Team ID" on the page
- Or go to App Store Connect → Account Settings → Team ID

### Optional Customizations:

You can customize other settings in this file:

- `stripSwiftSymbols`: Set to `false` if you need debug symbols
- `uploadBitcode`: Set to `false` for faster uploads (new format)
- `thinning`: Can be set to `<automatic>` for auto-thinning

### File Structure Explained:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- XML declaration - required -->

<plist version="1.0">
<dict>
    <!-- Key-value pairs for export configuration -->
    
    <key>compileBitcode</key>
    <false/>
    <!-- Whether to compile bitcode (false for modern apps) -->
    
    <key>destination</key>
    <string>upload</string>
    <!-- Where to send: "upload" for TestFlight/App Store -->
    
    <key>method</key>
    <string>app-store</string>
    <!-- Distribution method: "app-store" for TestFlight -->
    
    <key>signingStyle</key>
    <string>automatic</string>
    <!-- Automatic signing through Xcode managed profiles -->
    
    <key>teamID</key>
    <string>YOUR_TEAM_ID_HERE</string>
    <!-- Your Apple Developer Team ID -->
    
</dict>
</plist>
```

## Usage Steps

1. **Copy the template:**
   ```bash
   cp CI_CD/examples/ExportOptions.plist vertex_app/ios/ExportOptions.plist
   ```

2. **Edit the file:**
   - Open in your text editor or Xcode
   - Replace `YOUR_TEAM_ID_HERE` with your actual Team ID
   - Replace `com.example.vertexApp` with your actual Bundle ID

3. **Validate the file:**
   ```bash
   # On macOS:
   plutil -lint vertex_app/ios/ExportOptions.plist
   
   # Or just try building:
   cd vertex_app
   flutter build ipa --release
   ```

4. **Commit the file:**
   ```bash
   git add vertex_app/ios/ExportOptions.plist
   git commit -m "Add ExportOptions.plist for TestFlight deployment"
   ```

## Verification

After creating the file, ensure:
- ✓ File is named exactly `ExportOptions.plist`
- ✓ Located at `vertex_app/ios/ExportOptions.plist`
- ✓ Bundle ID matches your App Store Connect app
- ✓ Team ID is your 10-character Apple Team ID
- ✓ File is valid XML (use `plutil -lint` to check)

## Common Issues

**"Invalid export options" error:**
- Check XML syntax with `plutil -lint`
- Verify all `<key>` tags have matching value tags
- Ensure no special characters in strings

**"Team ID not found" error:**
- Get correct Team ID from Apple Developer account
- It's 10 characters (e.g., `ABCDEF1234`)
- Not your personal Developer ID

**"Provisioning profile not found" error:**
- Verify Bundle ID matches exactly (case-sensitive)
- Check App Store Connect has the app registered
- Ensure you're using correct Team ID

## More Information

- [Apple ExportOptions Documentation](https://developer.apple.com/documentation/xcode/export-options-reference)
- [Xcode Export Guide](https://developer.apple.com/documentation/xcode/exporting-an-archive-to-app-store-connect)
- [Flutter iOS Build Settings](https://docs.flutter.dev/deployment/ios)

---

Ready? Copy this file to `vertex_app/ios/ExportOptions.plist` and update the values!
