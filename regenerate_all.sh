#!/bin/bash
#
# Regenerate all 149 assessments with response rate tracking
# This script regenerates each practice sequentially to avoid API rate limit conflicts
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "🔄 Regenerating All Assessments"
echo "   with Response Rate Tracking"
echo "========================================"
echo ""

# Backup existing assessments first
echo "📦 Creating backup of existing assessments..."
if [ -d "assessments_backup" ]; then
    rm -rf assessments_backup
fi
cp -r assessments assessments_backup
echo "✅ Backup created at: assessments_backup/"
echo ""

# Function to regenerate a practice
regenerate_practice() {
    local practice_name=$1
    local practice_arg=$2
    local expected_count=$3

    echo "========================================"
    echo "📁 Practice: $practice_name"
    echo "   Expected: $expected_count assessments"
    echo "========================================"
    echo ""

    # Remove existing files for this practice
    echo "🗑️  Removing old files from assessments/$practice_name/..."
    rm -rf "assessments/$practice_name/"*.md 2>/dev/null || true

    # Regenerate
    echo "🔄 Regenerating $practice_name assessments..."
    python3 fetch_eoy_simple.py --practice "$practice_arg"

    # Count result
    actual_count=$(find "assessments/$practice_name" -name "*.md" 2>/dev/null | wc -l)
    echo ""
    echo "✅ Complete: $actual_count/$expected_count files regenerated"
    echo ""
}

# Regenerate each practice
regenerate_practice "Platform-Cyber" "platform" 42
regenerate_practice "Software" "software" 37
regenerate_practice "Design" "design" 15
regenerate_practice "Product-Management" "product" 20

# Regenerate "Other" folder
echo "========================================"
echo "📁 Practice: Other"
echo "   Expected: 35 assessments"
echo "========================================"
echo ""
echo "🗑️  Removing old files from assessments/Other/..."
rm -rf assessments/Other/*.md 2>/dev/null || true

echo "🔄 Regenerating Other assessments..."
python3 fetch_eoy_simple.py --all

echo ""
echo "========================================"
echo "✅ REGENERATION COMPLETE"
echo "========================================"
echo ""

# Final count
total_count=$(find assessments -name "*.md" | wc -l)
echo "📊 Total assessments: $total_count"
echo ""

# Run verification
echo "🔍 Running verification..."
python3 verify_response_rates.py
