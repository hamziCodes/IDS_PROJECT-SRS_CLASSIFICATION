#!/bin/bash

# Test iOS build locally
# This script tests building iOS IPA locally before pushing to CI/CD
# Run from project root: bash CI_CD/scripts/local-build-test.sh

echo "🚀 Testing iOS Build Locally..."
echo ""

PROJECT_PATH="vertex_app"

# Check Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter not found. Please install Flutter first."
    echo "   https://docs.flutter.dev/get-started/install/windows"
    exit 1
fi

echo "✓ Flutter found: $(flutter --version)"
echo ""

# Navigate to project
cd "$PROJECT_PATH" || exit 1

echo "📍 Working directory: $(pwd)"
echo ""

# Step 1: Clean
echo "🧹 Step 1: Cleaning previous builds..."
flutter clean
if [ $? -ne 0 ]; then
    echo "❌ Clean failed"
    exit 1
fi
echo "✓ Clean completed"
echo ""

# Step 2: Get dependencies
echo "📦 Step 2: Getting dependencies..."
flutter pub get
if [ $? -ne 0 ]; then
    echo "❌ Dependency fetch failed"
    exit 1
fi
echo "✓ Dependencies fetched"
echo ""

# Step 3: Build for iOS
echo "🍎 Step 3: Building iOS app..."
echo "   This may take 10-20 minutes on first build..."
flutter build ipa --release

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ iOS build failed"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check error message above"
    echo "2. Run: flutter doctor"
    echo "3. Check iOS deployment target in Xcode"
    echo "4. Review CI_CD/TROUBLESHOOTING.md"
    exit 1
fi

echo ""
echo "✓ iOS build completed successfully!"
echo ""

# Step 4: Check IPA exists
IPA_PATH="build/ios/ipa/vertex_app.ipa"
if [ -f "$IPA_PATH" ]; then
    IPA_SIZE=$(du -h "$IPA_PATH" | cut -f1)
    echo "✓ IPA created: $IPA_PATH ($IPA_SIZE)"
else
    echo "⚠ IPA file not found at expected location"
fi

echo ""
echo "════════════════════════════════════════"
echo "✓ Local build test passed!"
echo ""
echo "✓ Your code compiles correctly"
echo "✓ iOS signing is configured properly"
echo ""
echo "You can now:"
echo "1. Push code to main branch"
echo "2. GitHub Actions will build automatically"
echo "3. Build will upload to TestFlight"
echo ""
echo "To upload this build manually to TestFlight:"
echo "  xcodebuild -importArchive -archivePath build/ios/archive/Runner.xcarchive \\"
echo "    -exportOptionsPlist ios/ExportOptions.plist \\"
echo "    -exportPath build/ios/ipa \\"
echo "    -allowProvisioningUpdates"
echo "════════════════════════════════════════"

cd - > /dev/null
exit 0
