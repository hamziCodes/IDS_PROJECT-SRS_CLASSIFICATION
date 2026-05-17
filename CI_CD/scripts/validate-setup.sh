#!/bin/bash

# Validate TestFlight CI/CD Setup
# This script checks if everything is configured correctly before deploying
# Run this from the project root: bash CI_CD/scripts/validate-setup.sh

echo "🔍 Validating TestFlight CI/CD Setup..."
echo ""

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: GitHub workflow file exists
echo "📋 Checking GitHub Actions workflow..."
if [ -f ".github/workflows/ios-testflight.yml" ]; then
    echo -e "${GREEN}✓${NC} Workflow file found"
else
    echo -e "${RED}✗${NC} Workflow file missing at .github/workflows/ios-testflight.yml"
    ((ERRORS++))
fi

# Check 2: Flutter project exists
echo ""
echo "📦 Checking Flutter project..."
if [ -f "vertex_app/pubspec.yaml" ]; then
    echo -e "${GREEN}✓${NC} Flutter project found"
    
    # Check version format
    VERSION=$(grep "^version:" vertex_app/pubspec.yaml | awk '{print $2}')
    if [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+\+[0-9]+$ ]]; then
        echo -e "${GREEN}✓${NC} Version format correct: $VERSION"
    else
        echo -e "${RED}✗${NC} Version format incorrect: $VERSION (should be X.Y.Z+N)"
        ((ERRORS++))
    fi
else
    echo -e "${RED}✗${NC} Flutter project not found at vertex_app/pubspec.yaml"
    ((ERRORS++))
fi

# Check 3: iOS configuration
echo ""
echo "🍎 Checking iOS configuration..."
if [ -f "vertex_app/ios/Runner/Info.plist" ]; then
    echo -e "${GREEN}✓${NC} Info.plist found"
else
    echo -e "${YELLOW}⚠${NC} Info.plist not found (might be okay)"
    ((WARNINGS++))
fi

if [ -f "vertex_app/ios/ExportOptions.plist" ]; then
    echo -e "${GREEN}✓${NC} ExportOptions.plist found"
else
    echo -e "${RED}✗${NC} ExportOptions.plist missing at vertex_app/ios/ExportOptions.plist"
    echo "   Create it from: CI_CD/examples/ExportOptions.plist"
    ((ERRORS++))
fi

# Check 4: CI/CD documentation
echo ""
echo "📚 Checking CI/CD documentation..."
DOCS=("CI_CD/TESTFLIGHT_SETUP.md" "CI_CD/SECRETS_SETUP.md" "CI_CD/TROUBLESHOOTING.md" "CI_CD/CI_CD_OVERVIEW.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo -e "${GREEN}✓${NC} $(basename $doc) found"
    else
        echo -e "${RED}✗${NC} $(basename $doc) missing"
        ((ERRORS++))
    fi
done

# Check 5: .gitignore configuration
echo ""
echo "🔐 Checking security (.gitignore)..."
if grep -q "*.p8" .gitignore 2>/dev/null || grep -q "AuthKey" .gitignore 2>/dev/null; then
    echo -e "${GREEN}✓${NC} .p8 files are ignored"
else
    echo -e "${YELLOW}⚠${NC} Consider adding *.p8 to .gitignore"
    ((WARNINGS++))
fi

# Summary
echo ""
echo "════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Setup looks good!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Read CI_CD/TESTFLIGHT_SETUP.md"
    echo "2. Follow CI_CD/SECRETS_SETUP.md to add GitHub secrets"
    echo "3. Update ExportOptions.plist with your Team ID"
    echo "4. Push to main branch to trigger workflow"
else
    echo -e "${RED}✗ Found $ERRORS errors${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ Found $WARNINGS warnings${NC}"
    fi
    echo ""
    echo "Please fix the errors above before proceeding."
fi

echo "════════════════════════════════════════"

exit $ERRORS
