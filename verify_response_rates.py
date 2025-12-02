#!/usr/bin/env python3
"""
Verify response rate appears in all assessment files.
Report any files with low response rates (<50%).
"""

from pathlib import Path
import re
import sys


def check_assessment_file(file_path):
    """Check if an assessment file has response rate information."""
    try:
        content = file_path.read_text()

        # Look for response rate line
        response_rate_match = re.search(
            r'- \*\*Response Rate\*\*: (\d+)/(\d+) peer reviewers \((\d+)%\)',
            content
        )

        if not response_rate_match:
            return {
                'has_response_rate': False,
                'file': str(file_path),
                'peer_count': None,
                'total_reviews': None,
                'response_rate': None
            }

        peer_count = int(response_rate_match.group(1))
        total_reviews = int(response_rate_match.group(2))
        response_rate = int(response_rate_match.group(3))

        return {
            'has_response_rate': True,
            'file': str(file_path),
            'peer_count': peer_count,
            'total_reviews': total_reviews,
            'response_rate': response_rate
        }

    except Exception as e:
        return {
            'has_response_rate': False,
            'file': str(file_path),
            'error': str(e)
        }


def main():
    """Verify all assessment files have response rate information."""
    base_dir = Path(__file__).parent / "assessments"

    if not base_dir.exists():
        print(f"❌ Assessments directory not found: {base_dir}")
        sys.exit(1)

    # Find all markdown files
    md_files = list(base_dir.rglob("*.md"))

    if not md_files:
        print(f"❌ No assessment files found in {base_dir}")
        sys.exit(1)

    print(f"🔍 Checking {len(md_files)} assessment files...\n")

    # Check each file
    files_with_response_rate = 0
    files_without_response_rate = []
    low_response_rate_files = []

    for md_file in sorted(md_files):
        result = check_assessment_file(md_file)

        if result['has_response_rate']:
            files_with_response_rate += 1

            # Flag low response rates (<50%)
            if result['response_rate'] < 50:
                low_response_rate_files.append(result)
        else:
            files_without_response_rate.append(result)

    # Report results
    print(f"✅ Files with response rate: {files_with_response_rate}/{len(md_files)}")

    if files_without_response_rate:
        print(f"\n⚠️  Files MISSING response rate: {len(files_without_response_rate)}")
        for result in files_without_response_rate[:10]:  # Show first 10
            print(f"   - {result['file']}")
            if 'error' in result:
                print(f"     Error: {result['error']}")
        if len(files_without_response_rate) > 10:
            print(f"   ... and {len(files_without_response_rate) - 10} more")

    if low_response_rate_files:
        print(f"\n⚠️  Files with LOW response rate (<50%): {len(low_response_rate_files)}")
        for result in sorted(low_response_rate_files, key=lambda x: x['response_rate']):
            rel_path = result['file'].replace(str(base_dir) + "/", "")
            print(f"   - {rel_path}")
            print(f"     Response Rate: {result['peer_count']}/{result['total_reviews']} ({result['response_rate']}%)")

    # Summary
    print(f"\n{'='*60}")
    if files_without_response_rate:
        print("❌ VERIFICATION FAILED: Not all files have response rates")
        sys.exit(1)
    elif low_response_rate_files:
        print("⚠️  VERIFICATION PASSED: All files have response rates")
        print(f"   However, {len(low_response_rate_files)} files have <50% response rate")
    else:
        print("✅ VERIFICATION PASSED: All files have response rates")
        print("   No files with low response rates found")


if __name__ == "__main__":
    main()
