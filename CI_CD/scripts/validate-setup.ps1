# Validate TestFlight CI/CD Setup
# PowerShell version for Windows
# Run from project root: .\CI_CD\scripts\validate-setup.ps1

Write-Host "🔍 Validating TestFlight CI/CD Setup..." -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Check 1: GitHub workflow file exists
Write-Host "📋 Checking GitHub Actions workflow..." -ForegroundColor Blue
if (Test-Path ".github/workflows/ios-testflight.yml") {
    Write-Host "✓ Workflow file found" -ForegroundColor Green
}
else {
    Write-Host "✗ Workflow file missing at .github/workflows/ios-testflight.yml" -ForegroundColor Red
    $errors++
}

# Check 2: Flutter project exists
Write-Host ""
Write-Host "📦 Checking Flutter project..." -ForegroundColor Blue
if (Test-Path "vertex_app/pubspec.yaml") {
    Write-Host "✓ Flutter project found" -ForegroundColor Green
    
    # Check version format
    $pubspec = Get-Content "vertex_app/pubspec.yaml" | Select-String "^version:"
    if ($pubspec -match '\d+\.\d+\.\d+\+\d+') {
        Write-Host "✓ Version format correct: $($matches[0])" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Version format incorrect (should be X.Y.Z+N)" -ForegroundColor Red
        $errors++
    }
}
else {
    Write-Host "✗ Flutter project not found at vertex_app/pubspec.yaml" -ForegroundColor Red
    $errors++
}

# Check 3: iOS configuration
Write-Host ""
Write-Host "🍎 Checking iOS configuration..." -ForegroundColor Blue
if (Test-Path "vertex_app/ios/Runner/Info.plist") {
    Write-Host "✓ Info.plist found" -ForegroundColor Green
}
else {
    Write-Host "⚠ Info.plist not found (might be okay)" -ForegroundColor Yellow
    $warnings++
}

if (Test-Path "vertex_app/ios/ExportOptions.plist") {
    Write-Host "✓ ExportOptions.plist found" -ForegroundColor Green
}
else {
    Write-Host "✗ ExportOptions.plist missing at vertex_app/ios/ExportOptions.plist" -ForegroundColor Red
    Write-Host "   Create it from: CI_CD/examples/ExportOptions.plist" -ForegroundColor Yellow
    $errors++
}

# Check 4: CI/CD documentation
Write-Host ""
Write-Host "📚 Checking CI/CD documentation..." -ForegroundColor Blue
$docs = @(
    "CI_CD/TESTFLIGHT_SETUP.md",
    "CI_CD/SECRETS_SETUP.md",
    "CI_CD/TROUBLESHOOTING.md",
    "CI_CD/CI_CD_OVERVIEW.md"
)

foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "✓ $(Split-Path $doc -Leaf) found" -ForegroundColor Green
    }
    else {
        Write-Host "✗ $(Split-Path $doc -Leaf) missing" -ForegroundColor Red
        $errors++
    }
}

# Check 5: .gitignore configuration
Write-Host ""
Write-Host "🔐 Checking security (.gitignore)..." -ForegroundColor Blue
if (Test-Path ".gitignore") {
    $gitignore = Get-Content ".gitignore" -Raw
    if ($gitignore -match "\.p8|AuthKey") {
        Write-Host "✓ .p8 files are ignored" -ForegroundColor Green
    }
    else {
        Write-Host "⚠ Consider adding *.p8 to .gitignore" -ForegroundColor Yellow
        $warnings++
    }
}

# Summary
Write-Host ""
Write-Host "════════════════════════════════════════"
if ($errors -eq 0) {
    Write-Host "✓ Setup looks good!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Read CI_CD/TESTFLIGHT_SETUP.md"
    Write-Host "2. Follow CI_CD/SECRETS_SETUP.md to add GitHub secrets"
    Write-Host "3. Update ExportOptions.plist with your Team ID"
    Write-Host "4. Push to main branch to trigger workflow"
}
else {
    Write-Host "✗ Found $errors errors" -ForegroundColor Red
    if ($warnings -gt 0) {
        Write-Host "⚠ Found $warnings warnings" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please fix the errors above before proceeding."
}

Write-Host "════════════════════════════════════════"

exit $errors
