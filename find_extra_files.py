#!/usr/bin/env python3
"""
Find files in assessments/Software that don't match roster entries
"""

import json
from pathlib import Path

def main():
    # Load roster
    roster_path = Path("LatticeAPI/lattice_api_client/team_map_software.json")
    with open(roster_path) as f:
        roster = json.load(f)

    # Build expected filenames from roster
    expected_files = set()
    for name_key in roster.keys():
        if ", " in name_key:
            last, first = name_key.split(", ", 1)
            expected_files.add(f"{first}_{last}.md")
        else:
            expected_files.add(name_key.replace(" ", "_") + ".md")

    # Get actual assessment directory files
    assessments_dir = Path("assessments/Software")
    actual_files = set(f.name for f in assessments_dir.glob("*.md"))

    # Find files not in roster
    extra_files = actual_files - expected_files

    print(f"📋 Finding Extra Files (not in roster)")
    print(f"{'='*70}\n")

    if extra_files:
        print(f"❓ EXTRA FILES ({len(extra_files)}):")
        print(f"   These files exist but aren't in team_map_software.json:\n")
        for filename in sorted(extra_files):
            print(f"   - {filename}")
    else:
        print(f"✅ No extra files - all files match roster")

    print(f"\n{'='*70}")
    print(f"Summary:")
    print(f"   - Expected files (from roster): {len(expected_files)}")
    print(f"   - Actual files (in directory): {len(actual_files)}")
    print(f"   - Extra files: {len(extra_files)}")

if __name__ == "__main__":
    main()
