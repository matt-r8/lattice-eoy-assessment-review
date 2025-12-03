#!/usr/bin/env python3
"""Test which names exist in the reviewee list"""

import json
import urllib.request
import sys
from pathlib import Path

# Load .env
def load_env(env_path):
    env = {}
    if not env_path.exists():
        return env
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env

env_path = Path(__file__).parent / "LatticeAPI" / ".env"
env = load_env(env_path)

BASE_URL = env.get("LATTICE_API_URL")
TOKEN = env.get("LATTICE_API_TOKEN")

if not TOKEN or not BASE_URL:
    print("❌ Missing credentials")
    exit(1)

def api_get(url):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode())

# Get cycles
cycles = api_get(f"{BASE_URL}/reviewCycles?limit=100")["data"]
cycle = next((c for c in cycles if c["name"] == "2025 EOY Assessment"), None)

if not cycle:
    print("❌ Cycle not found")
    exit(1)

print(f"✅ Found cycle: {cycle['name']}")

# Get all reviewees
url = f"{BASE_URL}/reviewCycle/{cycle['id']}/reviewees?limit=100"
all_reviewees = []
while url:
    data = api_get(url)
    all_reviewees.extend(data["data"])
    if data.get("hasMore"):
        url = f"{BASE_URL}/reviewCycle/{cycle['id']}/reviewees?limit=100&startingAfter={data['endingCursor']}"
    else:
        url = None

print(f"✅ Found {len(all_reviewees)} total reviewees")

# Get all names
print("\n🔍 Fetching all names...")
all_names = []
for reviewee in all_reviewees:
    try:
        reviewee_detail = api_get(f"{BASE_URL}/reviewee/{reviewee['id']}")
        user = api_get(f"{BASE_URL}/user/{reviewee_detail['user']['id']}")
        all_names.append(user["name"])
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        continue

print(f"✅ Got {len(all_names)} names\n")

# Check for our target names
TARGET_NAMES = [
    "Angie Davidson",
    "Nate Enders",
    "Gannon Gardner",
    "Kevin Nguyen",
    "Dustin Tran"
]

print("="*60)
print("CHECKING TARGET NAMES:")
print("="*60)

for target in TARGET_NAMES:
    if target in all_names:
        print(f"✅ FOUND: {target}")
    else:
        # Try variations
        print(f"❌ NOT FOUND: {target}")
        # Check for similar names
        similar = [n for n in all_names if target.split()[1].lower() in n.lower()]
        if similar:
            print(f"   Similar names found: {similar}")

print("\n" + "="*60)
print("ALL NAMES IN SYSTEM (Software-related):")
print("="*60)

# Load Software roster to filter
roster_path = Path(__file__).parent / "LatticeAPI" / "lattice_api_client" / "team_map_software.json"
with open(roster_path) as f:
    roster = json.load(f)

software_names = []
for name_key in roster.keys():
    if ", " in name_key:
        last, first = name_key.split(", ", 1)
        software_names.append(f"{first} {last}")
    else:
        software_names.append(name_key)

# Filter to only show Software practice names
software_in_cycle = [n for n in all_names if n in software_names]
for name in sorted(software_in_cycle):
    print(f"  - {name}")

print(f"\nTotal Software practice members in cycle: {len(software_in_cycle)}")
