#!/usr/bin/env python3
"""
Verify if the remaining 5 missing engineers are in Lattice or not
(excluding Basudev who we already removed)
"""

import json
import urllib.request
from pathlib import Path

def load_env(env_path):
    """Simple .env parser using only stdlib."""
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

def api_get(url):
    """Make GET request to Lattice API."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode())

def get_all_review_cycles():
    """Fetch all review cycles."""
    url = f"{BASE_URL}/reviewCycles?limit=100"
    cycles = []
    while url:
        data = api_get(url)
        cycles.extend(data["data"])
        if data.get("hasMore"):
            url = f"{BASE_URL}/reviewCycles?limit=100&startingAfter={data['endingCursor']}"
        else:
            url = None
    return cycles

def get_reviewees_for_cycle(cycle_id):
    """Fetch all reviewees for a cycle."""
    url = f"{BASE_URL}/reviewCycle/{cycle_id}/reviewees?limit=100"
    reviewees = []
    while url:
        data = api_get(url)
        reviewees.extend(data["data"])
        if data.get("hasMore"):
            url = f"{BASE_URL}/reviewCycle/{cycle_id}/reviewees?limit=100&startingAfter={data['endingCursor']}"
        else:
            url = None
    return reviewees

def get_reviewee_by_id(reviewee_id):
    """Fetch reviewee details."""
    return api_get(f"{BASE_URL}/reviewee/{reviewee_id}")

def get_user_by_id(user_id):
    """Fetch user details."""
    return api_get(f"{BASE_URL}/user/{user_id}")

def main():
    CYCLE_NAME = "2025 EOY Assessment"

    # Missing engineers (excluding Basudev who was already removed)
    search_names = [
        "Angie Davidson",
        "Nate Enders",
        "Gannon Gardner",
        "Kevin Nguyen",
        "dustintktran",  # special case - unusual name format
    ]

    print(f"🔍 Verifying remaining 5 missing engineers in Lattice")
    print(f"{'='*70}\n")

    cycles = get_all_review_cycles()
    cycle = next((c for c in cycles if c["name"] == CYCLE_NAME), None)

    if not cycle:
        print(f"❌ Cycle not found")
        return

    reviewees = get_reviewees_for_cycle(cycle["id"])
    print(f"✅ Searching through {len(reviewees)} reviewees...\n")

    # Build reviewee names
    reviewee_names = {}
    for reviewee in reviewees:
        try:
            reviewee_detail = get_reviewee_by_id(reviewee["id"])
            user = get_user_by_id(reviewee_detail["user"]["id"])
            reviewee_names[user["name"].lower()] = (user["name"], reviewee["id"])
        except:
            continue

    # Search for each missing engineer
    for search_name in search_names:
        print(f"🔎 Searching for: {search_name}")
        search_lower = search_name.lower()
        search_parts = search_lower.split()

        # Exact match
        if search_lower in reviewee_names:
            exact_name, rid = reviewee_names[search_lower]
            print(f"   ✅ EXACT MATCH: {exact_name}")
            print(f"      Reviewee ID: {rid}")
            continue

        # Partial match
        matches = []
        for name_lower, (name, rid) in reviewee_names.items():
            if all(part in name_lower for part in search_parts):
                matches.append((name, rid))

        if matches:
            print(f"   ✅ PARTIAL MATCH(ES):")
            for name, rid in matches:
                print(f"      - {name} (ID: {rid})")
        else:
            print(f"   ❌ NOT FOUND in 2025 EOY Assessment cycle")

        print()

if __name__ == "__main__":
    main()
