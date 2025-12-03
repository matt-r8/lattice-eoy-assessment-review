#!/usr/bin/env python3
"""
Fix manual name mismatches in team_map.json leveling data.
Maps known differences between team_map.json and leveling data.
"""

import json
from pathlib import Path

# Manual mapping of team_map names to leveling data names
MANUAL_MATCHES = {
    # Benjamin vs Ben
    "Adinata, Ben": ("Benjamin Adinata", "Practitioner III"),
    # Abel Hernandez vs Hernandez, Abel A A
    "Hernandez, Abel A A": ("Abel Hernandez", "Senior Practitioner"),
    # Jacob vs Jacobi
    "Ayala, Jacobi": ("Jacob Ayala", "Senior Practitioner"),
    # David Chapman is "David Croney" in leveling - NO MATCH
    # David Chapman is actually David Croney in leveling data
    # Cory vs Corey
    "Hurlbut, Cory": ("Cory Hurlbut", "Practitioner III"),
    # Derek vs Dereck
    "Dombek, Derek": ("Derek Dombek", "Practitioner II"),
    # Dylan vs Dillan
    "Doub, Dylan": ("Dylan Doub", "Practitioner III"),
    # Jake vs Jacob
    "Cook, Jake": ("Jake Cook", "Practitioner III"),
    # Jeremy vs Jeramie
    "Viray, Jeremy": ("Jeremy Viray", "Practitioner II"),
    # Michael vs Micheal
    "Estoy, Michael": ("Michael Estoy", "Practitioner III"),
    # Michael Maye vs Michael
    "Maye, Michael": ("Michael Maye", "Practitioner II"),
    # Mohammed, Hafeez Rahman vs Mohammed, Hafeez Ur Rahman (different first part)
    "Mohammed, Hafeez Rahman": ("Hafeez Ur Rahman Mohammed", "Senior Practitioner"),
    # Roshni Bhanderi vs Roshni Patel confusion
    "Bhanderi, Roshni": ("Roshni Bhanderi", "Senior Practitioner"),
    # Patel, Roshni - need to check if this is a different person
    "Patel, Roshni": ("Roshni Patel", "Senior Practitioner"),
    # Special cases from leveling that might not be in roster
    # Samuel McQueen
    "McQueen, Samuel": ("Samuel McQueen", "Senior Practitioner"),
    # Schuyler
    "Reinken, Schuyler": ("Schuyler Reinken", "Senior Practitioner"),
}

# People in leveling data that don't have exact matches - need investigation
NEEDS_INVESTIGATION = {
    "Almond, Coby": "Jacob Almond in leveling - different first name",
    "Chapman, Dave": "No match - 'David Chapman' in leveling is likely different, 'David Croney' is in team_map as Croney, David",
    "Laugle, Alex": "In leveling but not in team_map",
    "Miles Smith": "In leveling but not in team_map",
    "Nate Enders": "In leveling but not in team_map",
    "Paul Coluccio": "In leveling but not in team_map",
    "Terry Rydz": "In leveling but not in team_map",
    "Vicente Pamparo": "In leveling but not in team_map",
}


def main():
    """Apply manual fixes."""
    team_map_path = Path('/workspaces/lattice-eoy-assessment-review/LatticeAPI/lattice_api_client/team_map.json')

    with open(team_map_path, 'r') as f:
        team_map = json.load(f)

    updated_count = 0

    for team_map_name, (leveling_name, level) in MANUAL_MATCHES.items():
        if team_map_name in team_map:
            if team_map[team_map_name]["level"] is None:
                team_map[team_map_name]["level"] = level
                updated_count += 1
                print(f"✓ Updated {team_map_name} with level {level}")
            else:
                print(f"- Skipped {team_map_name} (already has level)")
        else:
            print(f"✗ {team_map_name} not found in team_map")

    with open(team_map_path, 'w') as f:
        json.dump(team_map, f, indent=4)

    print(f"\nApplied {updated_count} manual fixes")
    print(f"File saved: {team_map_path}")


if __name__ == '__main__':
    main()
