#!/usr/bin/env python3
"""
Process team/project data and update team_map.json with team and project fields.
"""
import json
import re
from collections import defaultdict

# Parse the provided data
data_text = """SLD45 Nebula - Landing Zone (Dark Wolf)	Nebula	Justin Joseph
VA Lighthouse - SecRel & LHDI (Technatomy)	SecRel	Luke Strebel
VA Lighthouse - SecRel & LHDI (Technatomy)	SecRel	Sally Yoo
VA Lighthouse - SecRel & LHDI (Technatomy)	SecRel	Scott Carlson
VA Lighthouse - SecRel & LHDI (Technatomy)	SecRel	John Zubiri
VA Lighthouse - SecRel & LHDI (Technatomy)	SecRel	Derek Dombek
VA Lighthouse - SecRel & LHDI (Technatomy)	SecRel	Dylan Doub
VA Lighthouse - SecRel & LHDI (Technatomy)	SecRel	Branden Van Derbur
VA Lighthouse - SecRel & LHDI (Technatomy)	Platform	Hafeez Ur Rahman Mohammed
VA Lighthouse - SecRel & LHDI (Technatomy)	Platform	Kyle Dozier
KM - Section 31 & Platform (Tecolote)	Portfolio	Alex Berner
KM - Section 31 & Platform (Tecolote)	Malibu	Abbie Burton
KM - Section 31 & Platform (Tecolote)	Starfox	Darius DeSpain
KM - Section 31 & Platform (Tecolote)	Malibu	Damon Redding
KM - Section 31 & Platform (Tecolote)	Malibu	Tom Anastasio
Overhead	TRACER	Justin Reynolds
Overhead	TRACER	Paul Nieto
Customer Success	SPOC	Riya Patel
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	Portfolio	Becca James
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	Portfolio	Shawn Kilroy
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	Portfolio	David Lamberson
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Yi Liu
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Anthony Zubia
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Danny Benson
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Mases Krikorian
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT/POSNEG	Evan Mladinov
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT/POSNEG	Sagar Akre
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Roshni Bhanderi
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Dan Bitter
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Kyle Smart
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Cory Hurlbut
SPOC/S35F - Combat Enhancement Teams (AP IDIQ)	OSIT	Nate Enders
VA OCTO - Watchtower (SBIR)	WatchTower	Art Tovar
VA OCTO - Watchtower (SBIR)	WatchTower	Sridhar Vennela
VA OCTO - Watchtower (SBIR)	WatchTower	Kevin Nash
Customer Success	FORGE	Terry Rydz
SSC/SNGF FORGE (AP IDIQ)	Portfolio	Joshua Pritchett
SSC/SNGF FORGE (AP IDIQ)	Platform	Kevin Gates
SSC/SNGF FORGE (AP IDIQ)	Platform	Nick Weiss
SSC/SNGF FORGE (AP IDIQ)	Platform	Steven Bair
SSC/SNGF FORGE (AP IDIQ)	Platform	Brandon Shouse
SSC/SNGF FORGE (AP IDIQ)	Platform	Dylan Bossie
SSC/SNGF FORGE (AP IDIQ)	Platform	Eric Whitman
SSC/SNGF FORGE (AP IDIQ)	Platform	Asare Nkansah
SSC/SNGF FORGE (AP IDIQ)	Platform	Nick Luckey
SSC/SNGF FORGE (AP IDIQ)	Platform	Ethan Reid
SSC/SNGF FORGE (AP IDIQ)	Platform	Jerod Culpepper
SSC/SNGF FORGE (AP IDIQ)	SecRel	Mary Pollin
SSC/SNGF FORGE (AP IDIQ)	SecRel	Ashley Pearce
SSC/SNGF FORGE (AP IDIQ)	SecRel	Pedro Torres
SSC/SNGF FORGE (AP IDIQ)	SecRel	Chris Brodowski
SSC/SNGF FORGE (AP IDIQ)	SecRel	Schuyler Reinken
SSC/SNGF FORGE (AP IDIQ)	SecRel	Andrew Knife
SSC/SNGF FORGE (AP IDIQ)	SecRel	Sean Herbert
SSC/SNGF FORGE (AP IDIQ)	Cyber	Octavia Leon
SSC/SNGF FORGE (AP IDIQ)	Cyber	Samuel McQueen
SSC/SNGF FORGE (AP IDIQ)	Cyber	Benjamin Alvarez
SSC/SNGF FORGE (AP IDIQ)	Cyber	Jeremy Steinbeck
SSC/SNGF FORGE (AP IDIQ)	Enablement	Jesse Wilkins
SSC/SNGF FORGE (AP IDIQ)	Enablement	Drew McFarland
SSC/SNGF FORGE (AP IDIQ)	Enablement	Pooja Jhaveri
SSC/SNGF FORGE (AP IDIQ)	Enablement	David Alvarado
SSC/SNGF FORGE (AP IDIQ)	Enablement	Oddball - FORGE
SSC/SNGF FORGE (AP IDIQ)	Enablement	Jacob Ayala
SSC/SNGF FORGE (AP IDIQ)	IT Services	Ann Kung
SSC/SNGF FORGE (AP IDIQ)	IT Services	Dave Blotter
SSC/SNGF FORGE (AP IDIQ)	IT Services	Chase Cast
SSC/SNGF FORGE (AP IDIQ)	Onboarding	David Chapman
SSC/SNGF FORGE (AP IDIQ)	Onboarding	Alexandra Brierton
SSC/SNGF FORGE (AP IDIQ)	Onboarding	Michael Silverman
SSC/SNGF FORGE (AP IDIQ)	Onboarding	Alden Davidson
SSC/SNGF FORGE (AP IDIQ)	Framework Services	Adam Gardner
SSC/SNGF FORGE (AP IDIQ)	Framework Services	Jake Cook
SSC/SNGF FORGE (AP IDIQ)	Framework Services	Miles Smith
SSC/CGTM EM&C SATCOM (AP IDIQ)	Blitzar	Ian Sperry
SSC/CGTM EM&C SATCOM (AP IDIQ)	Blitzar	Darla McGraw
SSC/CGTM EM&C SATCOM (AP IDIQ)	Blitzar	Peter Duong
SSC/CGTM EM&C SATCOM (AP IDIQ)	Blitzar	Vin Foregard
SSC/CGTM EM&C SATCOM (AP IDIQ)	Blitzar	Nick Eissler
SSC/CGTM EM&C SATCOM (AP IDIQ)	Blitzar	Cason Brinson
SSC/CGTM EM&C SATCOM (AP IDIQ)	Nebula	Roshni Patel
SSC/CGTM EM&C SATCOM (AP IDIQ)	Nebula	Hannah Cheng
SSC/CGTM EM&C SATCOM (AP IDIQ)	Nebula	Edwin Karaya
SSC/CGTM EM&C SATCOM (AP IDIQ)	Nebula	Yechiel Kalmenson
SSC/CGTM EM&C SATCOM (AP IDIQ)	Nebula	Wilcore - Jordan Flyod
SSC/CGTM EM&C SATCOM (AP IDIQ)	Nebula	Minh Nguyen
SSC/CGTM EM&C SATCOM (AP IDIQ)	Polaris	Shubham Goel
SSC/CGTM EM&C SATCOM (AP IDIQ)	Polaris	Seehyun Kim
SSC/CGTM EM&C SATCOM (AP IDIQ)	Polaris	Chris Wang
SSC/CGTM EM&C SATCOM (AP IDIQ)	Polaris	Norman Sharpe
SSC/CGTM EM&C SATCOM (AP IDIQ)	Polaris	Drew Fugate
SSC/CGTM EM&C SATCOM (AP IDIQ)	Polaris	Benjamin Adinata
Customer Success	Bifrost	Riya Patel
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	App	Clark Pain
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	App	Steven Souto
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	Platform/Cyber	Chris Johns
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	Platform/Cyber	Dan Sanker
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	Cyber	Kenny Slater
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	App	Vicente Pamparo
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	App	Erica Chang
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	App	Delaney Coveno
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	App	Bryce Nguonly
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	App	Jeremy Viray
SSC/BCCB Apollo Path to Prod - Bifrost (STRATFI SBIR)	Platform/Cyber	Tiyyiba Zahid
SDA - PWSA AppFactory Transition Study (SciTec)	SciTec	David Croney
SDA - PWSA AppFactory Transition Study (SciTec)	SciTec	Jon Brooks
VA OCTO - Accelerate Cybersecurity Excellence (SPRUCE)	ACE	Ron Golan
VA OCTO - Accelerate Cybersecurity Excellence (SPRUCE)	ACE	Jacob Almond
VA OCTO - Accelerate Cybersecurity Excellence (SPRUCE)	ACE	Jeremy Arzuaga
VA OCTO - Accelerate Cybersecurity Excellence (SPRUCE)	ACE	Alex Laugle
VA OCTO - Accelerate Cybersecurity Excellence (SPRUCE)	ACE	Jason Elting
VA OCTO - Accelerate Cybersecurity Excellence (SPRUCE)	ACE	Ryan Tuck
Customer Success	VA	Sharon Hamilton
VA PTEMS Lighthouse (Deloitte)	DevEn	David Croney
VA PTEMS Lighthouse (Deloitte)	DevEn	Coty Allen
VA PTEMS Lighthouse (Deloitte)	Crew Lead	Brent Baumann
VA PTEMS Lighthouse (Deloitte)	DevEn	Andrew Lazarek
VA PTEMS Lighthouse (Deloitte)	SecRel	Paul Coluccio"""

def convert_name_to_last_first(first_last):
    """Convert 'First Last' or 'First Middle Last' to 'Last, First' format."""
    # Skip non-riser entries
    if first_last in ["Oddball - FORGE", "Wilcore - Jordan Flyod"]:
        return None

    parts = first_last.strip().split()
    if len(parts) < 2:
        return None

    # Handle 'Van', 'Del', 'De', etc. as part of last name
    special_prefixes = {'Van', 'Del', 'De', 'O\'', "O'"}

    # Check if second-to-last part is a special prefix
    if len(parts) >= 3:
        if parts[-2] in special_prefixes:
            # e.g., "Branden Van Derbur" -> "Derbur, Branden Van"
            last_name = ' '.join(parts[-2:])  # "Van Derbur"
            first_name = ' '.join(parts[:-2])  # "Branden"
            return f"{parts[-1]}, {first_name} {parts[-2]}"

    # Standard case: last element is last name
    last_name = parts[-1]
    first_name = ' '.join(parts[:-1])
    return f"{last_name}, {first_name}"

# Parse the data
data_mappings = defaultdict(list)
non_risers = []

for line in data_text.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) == 3:
        project, team, riser = parts

        # Check if this is a non-riser entry
        if riser in ["Oddball - FORGE", "Wilcore - Jordan Flyod"]:
            non_risers.append((project, team, riser))
            continue

        # Convert name
        last_first = convert_name_to_last_first(riser)
        if last_first:
            data_mappings[last_first].append({
                'project': project,
                'team': team,
                'original_name': riser
            })

# Load the current team_map.json
with open('/workspaces/lattice-eoy-assessment-review/LatticeAPI/lattice_api_client/team_map.json', 'r') as f:
    team_map = json.load(f)

# Track statistics
matched_count = 0
unmatched_in_data = []
duplicate_risers = []

# Update team_map with team and project info
for name, entries in data_mappings.items():
    if name in team_map:
        matched_count += 1
        if len(entries) > 1:
            # Handle duplicates
            duplicate_risers.append({
                'name': name,
                'entries': entries
            })
            # Use the first entry for now
            team_map[name]['team'] = entries[0]['team']
            team_map[name]['project'] = entries[0]['project']
        else:
            team_map[name]['team'] = entries[0]['team']
            team_map[name]['project'] = entries[0]['project']
    else:
        unmatched_in_data.append({
            'original_name': entries[0]['original_name'],
            'converted_name': name,
            'team': entries[0]['team'],
            'project': entries[0]['project']
        })

# Add null team/project to entries not in the provided data
unmatched_in_map = 0
for name in team_map:
    if 'team' not in team_map[name]:
        team_map[name]['team'] = None
        team_map[name]['project'] = None
        unmatched_in_map += 1

# Sort the team_map by key to maintain alphabetical order
team_map = dict(sorted(team_map.items()))

# Save the updated team_map.json
with open('/workspaces/lattice-eoy-assessment-review/LatticeAPI/lattice_api_client/team_map.json', 'w') as f:
    json.dump(team_map, f, indent=4)

# Print report
print("=" * 80)
print("TEAM MAP UPDATE REPORT")
print("=" * 80)
print(f"\nMatched Risers: {matched_count}")
print(f"Unmatched in team_map.json (set to null): {unmatched_in_map}")
print(f"Non-Risers (skipped): {len(non_risers)}")
print(f"\n{'=' * 80}")

if unmatched_in_data:
    print(f"\nUNMATCHED NAMES IN PROVIDED DATA: {len(unmatched_in_data)}")
    print("(These names not found in team_map.json)")
    for item in unmatched_in_data:
        original = item.get('original_name', item.get('converted_name', 'Unknown'))
        converted = item.get('converted_name', 'Unknown')
        team = item.get('team', 'Unknown')
        project = item.get('project', 'Unknown')
        print(f"  - {original:25s} (converted: {converted:30s}) | Team: {team:15s} | Project: {project}")

if non_risers:
    print(f"\nNON-RISERS SKIPPED: {len(non_risers)}")
    for project, team, riser in non_risers:
        print(f"  - {riser:25s} | Team: {team:15s} | Project: {project}")

if duplicate_risers:
    print(f"\nDUPLICATE RISERS IN PROVIDED DATA: {len(duplicate_risers)}")
    for item in duplicate_risers:
        print(f"  - {item['name']}")
        for entry in item['entries']:
            print(f"    - Team: {entry['team']:20s} | Project: {entry['project']}")

print(f"\n{'=' * 80}")
print(f"Total entries in team_map.json: {len(team_map)}")
print(f"Entries with team/project assigned: {matched_count}")
print(f"Entries with null team/project: {unmatched_in_map}")
print(f"{'=' * 80}\n")

# Save a detailed report
report = {
    'summary': {
        'total_entries': len(team_map),
        'matched': matched_count,
        'unmatched_in_map': unmatched_in_map,
        'unmatched_in_data': len(unmatched_in_data),
        'non_risers_skipped': len(non_risers),
        'duplicates': len(duplicate_risers)
    },
    'unmatched_in_data': unmatched_in_data,
    'non_risers': non_risers,
    'duplicates': duplicate_risers
}

with open('/workspaces/lattice-eoy-assessment-review/team_map_update_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("Report saved to: team_map_update_report.json")
