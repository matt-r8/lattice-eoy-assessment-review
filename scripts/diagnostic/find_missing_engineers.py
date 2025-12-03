#!/usr/bin/env python3
"""
find_missing_engineers.py - Debug script to find missing Software engineers
Searches all reviewees for partial name matches
"""

import json
import urllib.request
from pathlib import Path

# ─────────────────────────────  Load .env manually  ──────────────────
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

if not TOKEN or not BASE_URL:
    print("❌ Missing LATTICE_API_URL or LATTICE_API_TOKEN in .env")
    exit(1)

# ─────────────────────────────  API Helpers  ──────────────────────────
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
    """Find missing Software engineers in Lattice API."""

    CYCLE_NAME = "2025 EOY Assessment"

    # Target names to search for (flexible matching)
    search_names = [
        "Kyle Smart",
        "Nate Enders",
        "Cason Brinson",
        "Angie Davidson",
        "Gannon Gardner",
        "Kevin Nguyen"
    ]

    print(f"🔍 Searching for review cycle: '{CYCLE_NAME}'")

    # Find cycle
    cycles = get_all_review_cycles()
    cycle = next((c for c in cycles if c["name"] == CYCLE_NAME), None)

    if not cycle:
        print(f"❌ Review cycle '{CYCLE_NAME}' not found.")
        return

    print(f"✅ Found cycle: {cycle['name']}")

    # Get all reviewees
    print(f"🔍 Fetching all reviewees...")
    reviewees = get_reviewees_for_cycle(cycle["id"])
    print(f"✅ Found {len(reviewees)} total reviewees")

    # Build full list of reviewee names
    print(f"\n📋 Fetching reviewee details...")
    reviewee_names = {}

    for i, reviewee in enumerate(reviewees, 1):
        try:
            reviewee_detail = get_reviewee_by_id(reviewee["id"])
            user = get_user_by_id(reviewee_detail["user"]["id"])
            reviewee_names[user["name"]] = reviewee["id"]

            if i % 10 == 0:
                print(f"   Processed {i}/{len(reviewees)} reviewees...")
        except Exception as e:
            print(f"   ⚠️  Error processing reviewee {reviewee['id']}: {e}")
            continue

    print(f"\n✅ Processed {len(reviewee_names)} reviewee names")

    # Search for missing engineers
    print(f"\n{'='*70}")
    print(f"🔍 SEARCHING FOR MISSING ENGINEERS")
    print(f"{'='*70}")

    found_count = 0
    not_found_count = 0

    for search_name in search_names:
        print(f"\n🔎 Searching for: {search_name}")

        # Exact match first
        if search_name in reviewee_names:
            print(f"   ✅ EXACT MATCH FOUND: {search_name}")
            print(f"      Reviewee ID: {reviewee_names[search_name]}")
            found_count += 1
            continue

        # Partial match - check if any part of search name appears in reviewee names
        search_lower = search_name.lower()
        search_parts = search_lower.split()

        matches = []
        for reviewee_name in reviewee_names.keys():
            reviewee_lower = reviewee_name.lower()

            # Check if all parts of search name appear in reviewee name
            if all(part in reviewee_lower for part in search_parts):
                matches.append(reviewee_name)

        if matches:
            print(f"   ✅ PARTIAL MATCH(ES) FOUND:")
            for match in matches:
                print(f"      - {match} (ID: {reviewee_names[match]})")
            found_count += 1
        else:
            print(f"   ❌ NOT FOUND in cycle reviewees")
            not_found_count += 1

    # Summary
    print(f"\n{'='*70}")
    print(f"📊 SEARCH SUMMARY")
    print(f"{'='*70}")
    print(f"   ✅ Found: {found_count}/{len(search_names)}")
    print(f"   ❌ Not Found: {not_found_count}/{len(search_names)}")
    print(f"\n💡 Next steps:")
    print(f"   - For FOUND engineers: Use exact Lattice names to pull assessments")
    print(f"   - For NOT FOUND: They may not be in the '2025 EOY Assessment' cycle")

if __name__ == "__main__":
    main()
