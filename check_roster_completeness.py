#!/usr/bin/env python3
"""
Check which Software roster members are missing from assessments directory
"""

import json
from pathlib import Path

def main():
    # Load roster
    roster_path = Path("LatticeAPI/lattice_api_client/team_map_software.json")
    with open(roster_path) as f:
        roster = json.load(f)

    # Get assessment directory files
    assessments_dir = Path("assessments/Software")
    existing_files = set(f.name for f in assessments_dir.glob("*.md"))

    print(f"📋 Software Roster Check")
    print(f"{'='*70}\n")
    print(f"Total roster entries: {len(roster)}")
    print(f"Total assessment files: {len(existing_files)}\n")

    missing = []
    found = []

    for name_key in roster.keys():
        # Convert roster name format to filename format
        if ", " in name_key:
            last, first = name_key.split(", ", 1)
            expected_filename = f"{first}_{last}.md"
        else:
            # Handle special cases like "Cory" with no last name
            expected_filename = name_key.replace(" ", "_") + ".md"

        if expected_filename in existing_files:
            found.append((name_key, expected_filename))
        else:
            missing.append((name_key, expected_filename))

    if missing:
        print(f"❌ MISSING ({len(missing)}):")
        for name, filename in sorted(missing):
            print(f"   - {name:30s} → {filename}")
        print()

    print(f"✅ FOUND ({len(found)}):")
    print(f"   All {len(found)} assessments present in directory\n")

    print(f"{'='*70}")
    print(f"Summary:")
    print(f"   - Roster entries: {len(roster)}")
    print(f"   - Found: {len(found)}")
    print(f"   - Missing: {len(missing)}")
    print(f"   - Files in directory: {len(existing_files)}")

if __name__ == "__main__":
    main()
