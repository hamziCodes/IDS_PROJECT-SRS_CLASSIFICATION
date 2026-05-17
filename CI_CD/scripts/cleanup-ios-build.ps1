# Clean Flutter iOS Build Cache
# Run this from vertex_app directory
# Usage: powershell -ExecutionPolicy Bypass -File ..\CI_CD\scripts\cleanup-ios-build.ps1

Write-Host "Cleaning iOS Build Cache..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop any running Flutter processes
Write-Host "Step 1: Stopping Flutter processes..."
Get-Process flutter -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process dart -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "Done"
Write-Host ""

# Step 2: Clean Flutter
Write-Host "Step 2: Running flutter clean..."
flutter clean
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: flutter clean had issues, continuing anyway..." -ForegroundColor Yellow
}
Write-Host "Done"
Write-Host ""

# Step 3: Remove build artifacts
Write-Host "Step 3: Removing build artifacts..."
$toRemove = @("ios/Pods", "ios/Podfile.lock", "build", ".dart_tool", "pubspec.lock")

foreach ($item in $toRemove) {
    if (Test-Path $item) {
        Write-Host "  Removing: $item"
        Remove-Item -Path $item -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Write-Host "Done"
Write-Host ""

# Step 4: Get fresh dependencies
Write-Host "Step 4: Getting fresh dependencies..."
flutter pub get
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: flutter pub get failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Done"
Write-Host ""

# Step 5: Verify files exist
Write-Host "Step 5: Verifying setup..."
Write-Host "  - pubspec.yaml: " -NoNewline
if (Test-Path "pubspec.yaml") { Write-Host "OK" -ForegroundColor Green } else { Write-Host "MISSING" -ForegroundColor Red }

Write-Host "  - ios/ExportOptions.plist: " -NoNewline
if (Test-Path "ios/ExportOptions.plist") { Write-Host "OK" -ForegroundColor Green } else { Write-Host "MISSING" -ForegroundColor Yellow }

Write-Host "  - ios/Podfile: " -NoNewline
if (Test-Path "ios/Podfile") { Write-Host "OK" -ForegroundColor Green } else { Write-Host "Will be generated" -ForegroundColor Yellow }

Write-Host ""
Write-Host "Cleanup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Verify ios/Podfile has: platform :ios, '12.0'"
Write-Host "  2. Run: git add ."
Write-Host "  3. Run: git commit -m 'Clean iOS build cache'"
Write-Host "  4. Run: git push"
Write-Host "  5. Watch GitHub Actions workflow"
Write-Host ""
