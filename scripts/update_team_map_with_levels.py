#!/usr/bin/env python3
"""
Update team_map.json to include employee levels from provided leveling data.
Handles name format conversion and identifies missing matches.
"""

import json
import re
from pathlib import Path
from typing import Dict, Tuple, List

# Leveling data provided by user
LEVELING_DATA_RAW = """Abbie Burton    Senior Practitioner
Abel Hernandez    Senior Practitioner
Adam Furtado    Director
Adam Gardner    Staff Practitioner
Ainsilie Hibbard    Practitioner III
Alden Davidson    Practitioner III
Alex Berner    Senior Practitioner
Alex Laugle    Practitioner II
Alexandra Brierton    Senior Practitioner
Andrew Knife    Practitioner III
Ann Kung    Practitioner II
Anthony Zubia    Senior Practitioner
Art Tovar    Senior Practitioner
Asare Nkansah    Senior Practitioner
Ashley Pearce    Senior Practitioner
Becca James    Staff Practitioner
Benjamin Adinata    Practitioner III
Benjamin Alvarez    Senior Practitioner
Branden Van Derbur    Practitioner III
Brandon Shouse    Senior Practitioner
Brent Baumann    Senior Practitioner
Brian Jennings    Staff Practitioner
Bryce Nguonly    Practitioner III
Cason Brinson    Practitioner III
Chase Cast    Practitioner III
Chris Brodowski    Senior Practitioner
Chris Johns    Senior Practitioner
Chris Wang    Senior Practitioner
Clark Pain    Staff Practitioner
Cory Hurlbut    Practitioner III
Coty Allen    Senior Practitioner
Damon Redding    Practitioner III
Dan Bitter    Senior Practitioner
Dan Sanker    Senior Practitioner
Danny Benson    Senior Practitioner
Darius DeSpain    Practitioner III
Darla McGraw    Senior Practitioner
Dave Blotter    Senior Practitioner
David Alvarado    Senior Practitioner
David Chapman    Senior Practitioner
David Croney    Staff Practitioner
David Lamberson    Staff Practitioner
Delaney Coveno    Senior Practitioner
Derek Dombek    Practitioner II
Drew Fugate    Practitioner III
Drew McFarland    Senior Practitioner
Dylan Bossie    Senior Practitioner
Dylan Doub    Practitioner III
Edwin Karaya    Senior Practitioner
Eric Whitman    Senior Practitioner
Erica Chang    Practitioner III
Evan Mladinov    Senior Practitioner
Hafeez Ur Rahman Mohammed    Senior Practitioner
Hannah Cheng    Senior Practitioner
Ian Sperry    Senior Practitioner
Jacob Almond    Staff Practitioner
Jacob Ayala    Senior Practitioner
Jake Cook    Practitioner III
Jeff Rodanski    Staff Practitioner
Jeff Wills    Staff Practitioner
Jennifer Van Hove    Staff Practitioner
Jennifer Van Hove    Staff Practitioner
Jeremy Arzuaga    Senior Practitioner
Jeremy Steinbeck    Senior Practitioner
Jeremy Viray    Practitioner II
Jerod Culpepper    Practitioner III
Jesse Wilkins    Senior Practitioner
Jodie Nkansah    Practitioner III
John Zubiri    Senior Practitioner
Jonathan Van Dalen    Senior Practitioner
Joshua Pritchett    Staff Practitioner
Justin Joseph    Staff Practitioner
Justin Reynolds    Practitioner II
Kenny Slater    Staff Practitioner
Kevan Mordan    Staff Practitioner
Kevin Gates    Staff Practitioner
Kevin Nash    Senior Practitioner
Kristin Pearson    Director
Kyle Dozier    Practitioner III
Kyle Smart    Practitioner III
Luke Strebel    Staff Practitioner
Mary Pollin    Practitioner III
Mases Krikorian    Senior Practitioner
Matt O'Donnell    Senior Practitioner
Matt Pacione    Staff Practitioner
Max Reele    Director
Michael Estoy    Practitioner III
Michael Maye    Practitioner II
Michael Silverman    Senior Practitioner
Mike Gehard    Staff Practitioner
Miles Smith    Practitioner III
Minh Nguyen    Practitioner III
Nate Enders    Senior Practitioner
Nick Eissler    Practitioner III
Nick Luckey    Practitioner III
Nick Mendiola    Practitioner III
Nick Weiss    Staff Practitioner
Noah McHugh    Staff Practitioner
Norman Sharpe    Senior Practitioner
Octavia Leon    Practitioner III
Paul Coluccio    Senior Practitioner
Paul Fretz    Senior Practitioner
Paul Nieto    Senior Practitioner
Pedro Torres    Practitioner III
Peter Duong    Senior Practitioner
Pooja Jhaveri    Senior Practitioner
Riya Patel    Senior Practitioner
Rob Monroe    Staff Practitioner
Ron Golan    Senior Practitioner
Roshni Bhanderi    Senior Practitioner
Roshni Patel    Senior Practitioner
Ryan Tuck    Senior Practitioner
Sagar Akre    Senior Practitioner
Sally Yoo    Senior Practitioner
Samuel McQueen    Senior Practitioner
Schuyler Reinken    Senior Practitioner
Scott Carlson    Senior Practitioner
Sean Herbert    Practitioner III
Seehyun Kim    Senior Practitioner
Sharon Hamilton    Senior Practitioner
Shawn Kilroy    Senior Practitioner
Shubham Goel    Senior Practitioner
Sridhar Vennela    Senior Practitioner
Steven Bair    Staff Practitioner
Steven Souto    Senior Practitioner
Terry Rydz    Senior Practitioner
Thomas Reynolds    Practitioner III
Tiyyiba Zahid    Practitioner III
Tom Anastasio    Senior Practitioner
Vicente Pamparo    Senior Practitioner
Vin Foregard    Practitioner III
Yechiel Kalmenson    Senior Practitioner
Yi Liu    Senior Practitioner"""


def parse_leveling_data(raw_data: str) -> Dict[str, str]:
    """
    Parse raw leveling data into {full_name: level} dictionary.
    Handles duplicate entries (e.g., Jennifer Van Hove appears twice).
    """
    leveling_map = {}
    for line in raw_data.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split()
        # Last element is the level (could be multiple words)
        if 'Practitioner' in line or 'Director' in line or 'Staff' in line:
            # Find where level starts
            if 'Practitioner III' in line:
                level = 'Practitioner III'
                name = line.replace('Practitioner III', '').strip()
            elif 'Practitioner II' in line:
                level = 'Practitioner II'
                name = line.replace('Practitioner II', '').strip()
            elif 'Staff Practitioner' in line:
                level = 'Staff Practitioner'
                name = line.replace('Staff Practitioner', '').strip()
            elif 'Senior Practitioner' in line:
                level = 'Senior Practitioner'
                name = line.replace('Senior Practitioner', '').strip()
            elif 'Director' in line:
                level = 'Director'
                name = line.replace('Director', '').strip()
            else:
                continue

            leveling_map[name.strip()] = level

    return leveling_map


def convert_name_format(first_last_name: str) -> str:
    """
    Convert "First Last" format to "Last, First" format.
    Handles special cases like "Van Dalen", "Van Hove", "Del", "O'Donnell", etc.
    """
    name = first_last_name.strip()
    parts = name.split()

    if len(parts) < 2:
        return name

    # Handle special prefixes that are part of last name
    if len(parts) >= 3:
        # Check for "Van", "Del", "O'" prefixes
        if parts[0] == 'Van':
            # "Van Dalen, Jonathan" -> keep as is in reverse order
            # "Jonathan Van Dalen" -> "Dalen, Jonathan Van"
            first_name = ' '.join(parts[2:])
            last_part = ' '.join(parts[:2])
            return f"{parts[1]}, {first_name} {parts[0]}"
        elif parts[0] == 'Del':
            # "Del Vecchio, Rachel" -> "Vecchio, Rachel Del"
            first_name = ' '.join(parts[2:])
            return f"{parts[1]}, {first_name} {parts[0]}"
        elif parts[0].startswith("O'"):
            # Handle O'Donnell etc
            last_name = parts[0]
            first_name = ' '.join(parts[1:])
            return f"{last_name}, {first_name}"
        # Check if middle part is "Ur" (Hafeez Ur Rahman Mohammed case)
        elif parts[0] == 'Hafeez' and len(parts) >= 4 and parts[1] == 'Ur':
            # "Hafeez Ur Rahman Mohammed" -> "Mohammed, Hafeez Ur Rahman"
            return f"{parts[-1]}, {' '.join(parts[:-1])}"

    # Standard case: last element is last name
    last_name = parts[-1]
    first_names = ' '.join(parts[:-1])
    return f"{last_name}, {first_names}"


def find_best_match(first_last_name: str, team_map_keys: List[str]) -> Tuple[str, float]:
    """
    Find best matching key in team_map for a given first/last name format.
    Returns (matched_key, confidence_score).
    """
    # Try direct match first
    for key in team_map_keys:
        if key.lower() == first_last_name.lower():
            return key, 1.0

    # Try name parts matching
    name_parts = first_last_name.lower().split()

    best_match = None
    best_score = 0.0

    for key in team_map_keys:
        key_lower = key.lower()
        key_parts = key_lower.split(', ')  # "Last, First Middle"

        # Check if parts match
        matching_parts = 0
        total_parts = len(name_parts)

        for part in name_parts:
            for key_part in key_parts:
                if part in key_part or key_part in part:
                    matching_parts += 1
                    break

        score = matching_parts / total_parts if total_parts > 0 else 0

        if score > best_score:
            best_score = score
            best_match = key

    return best_match, best_score if best_match else (None, 0.0)


def main():
    """Main execution."""
    # Parse leveling data
    leveling_map = parse_leveling_data(LEVELING_DATA_RAW)
    print(f"Parsed {len(leveling_map)} leveling entries")

    # Load current team_map.json
    team_map_path = Path('/workspaces/lattice-eoy-assessment-review/LatticeAPI/lattice_api_client/team_map.json')
    with open(team_map_path, 'r') as f:
        team_map = json.load(f)

    print(f"Loaded {len(team_map)} entries from team_map.json")

    # Create new structure with levels
    updated_map = {}
    matched_count = 0
    missing_levels = []

    # Convert leveling data to Last, First format
    leveling_lastfirst = {}
    for name, level in leveling_map.items():
        converted = convert_name_format(name)
        leveling_lastfirst[converted] = level

    # Process each person in team_map
    for person_name, department in sorted(team_map.items()):
        # Try to find level
        level = None

        # Direct match
        if person_name in leveling_lastfirst:
            level = leveling_lastfirst[person_name]
            matched_count += 1
        else:
            # Try fuzzy match
            best_match, confidence = find_best_match(person_name, list(leveling_lastfirst.keys()))
            if best_match and confidence >= 0.7:
                level = leveling_lastfirst[best_match]
                matched_count += 1
            else:
                missing_levels.append(person_name)

        # Create new entry
        updated_map[person_name] = {
            "department": department,
            "level": level
        }

    # Identify people in leveling data but not in team_map
    not_in_roster = []
    for converted_name, level in leveling_lastfirst.items():
        if converted_name not in updated_map:
            not_in_roster.append((converted_name, level))

    # Write updated team_map.json
    with open(team_map_path, 'w') as f:
        json.dump(updated_map, f, indent=4)

    # Generate report
    print("\n" + "="*70)
    print("TEAM MAP UPDATE REPORT")
    print("="*70)
    print(f"\nTotal entries in team_map.json: {len(team_map)}")
    print(f"Successfully matched with levels: {matched_count}")
    print(f"Missing levels: {len(missing_levels)}")
    print(f"In leveling data but NOT in roster: {len(not_in_roster)}")

    if missing_levels:
        print(f"\nPeople in team_map.json WITHOUT matching levels ({len(missing_levels)}):")
        for person in sorted(missing_levels):
            print(f"  - {person}")

    if not_in_roster:
        print(f"\nPeople in leveling data but NOT in team_map.json ({len(not_in_roster)}):")
        for person, level in sorted(not_in_roster):
            print(f"  - {person} ({level})")

    print(f"\nUpdated file: {team_map_path}")
    print("="*70)


if __name__ == '__main__':
    main()
