#!/usr/bin/env python3
"""
fetch_eoy_simple.py - Pull EOY assessments using only stdlib

Usage:
  python3 fetch_eoy_simple.py                    # Pull Matt Pacione only (default)
  python3 fetch_eoy_simple.py --practice platform # Pull all Platform/Cyber practice
  python3 fetch_eoy_simple.py --all              # Pull all missing reviewees
"""

import json
import urllib.request
import urllib.parse
import re
import argparse
import sys
import time
from pathlib import Path
from collections import defaultdict
import html

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
def api_get(url, retries=3, retry_delay=5):
    """Make GET request to Lattice API with retry logic."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if attempt < retries - 1:
                print(f"   ⚠️  HTTP Error {e.code}, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            print(f"❌ HTTP Error {e.code}: {e.reason}")
            print(f"   URL: {url}")
            raise
        except (urllib.error.URLError, ConnectionError) as e:
            if attempt < retries - 1:
                print(f"   ⚠️  Connection error, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            print(f"❌ Connection error: {e}")
            raise
        except Exception as e:
            if attempt < retries - 1:
                print(f"   ⚠️  Error {e}, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            print(f"❌ Error: {e}")
            raise

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

def get_reviews_for_reviewee(reviewee_id):
    """Fetch all reviews for a reviewee."""
    url = f"{BASE_URL}/reviewee/{reviewee_id}/reviews?limit=100"
    reviews = []
    while url:
        data = api_get(url)
        reviews.extend(data["data"])
        if data.get("hasMore"):
            url = f"{BASE_URL}/reviewee/{reviewee_id}/reviews?limit=100&startingAfter={data['endingCursor']}"
        else:
            url = None
    return reviews

def get_question_by_id(question_id):
    """Fetch question details."""
    return api_get(f"{BASE_URL}/question/{question_id}")

# ─────────────────────────────  Helper Functions  ─────────────────────
def load_platform_roster(roster_path):
    """Load Platform/Cyber practice roster from JSON file."""
    try:
        with open(roster_path) as f:
            roster = json.load(f)
        # Convert "Last, First" to "First Last" format
        names = []
        for name_key in roster.keys():
            if ", " in name_key:
                last, first = name_key.split(", ", 1)
                names.append(f"{first} {last}")
            else:
                names.append(name_key)
        return names
    except FileNotFoundError:
        print(f"❌ Roster file not found: {roster_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in roster file: {e}")
        sys.exit(1)

def load_all_rosters():
    """Load all roster files and return a mapping of name -> folder."""
    base_path = Path(__file__).parent / "LatticeAPI" / "lattice_api_client"

    roster_mapping = {
        "team_map_platform.json": "Platform-Cyber",
        "team_map_software.json": "Software",
        "team_map_design.json": "Design",
        "team_map_product.json": "Product-Management"
    }

    name_to_folder = {}

    for roster_file, folder_name in roster_mapping.items():
        roster_path = base_path / roster_file
        if roster_path.exists():
            try:
                with open(roster_path) as f:
                    roster = json.load(f)
                for name_key in roster.keys():
                    if ", " in name_key:
                        last, first = name_key.split(", ", 1)
                        full_name = f"{first} {last}"
                    else:
                        full_name = name_key
                    name_to_folder[full_name] = folder_name
            except Exception as e:
                print(f"⚠️  Warning: Could not load {roster_file}: {e}")

    return name_to_folder

def get_existing_assessments(base_output_dir):
    """Get list of existing assessment names (without underscores and .md extension)."""
    existing = set()
    for md_file in base_output_dir.rglob("*.md"):
        # Convert filename back to name format: "First_Last.md" -> "First Last"
        name = md_file.stem.replace("_", " ")
        existing.add(name)
    return existing

def find_reviewee_by_name(name, reviewees, cycle_id):
    """Find reviewee by name, return reviewee_id or None."""
    for reviewee in reviewees:
        try:
            reviewee_detail = get_reviewee_by_id(reviewee["id"])
            user = get_user_by_id(reviewee_detail["user"]["id"])
            if user["name"] == name:
                return reviewee["id"]
        except Exception:
            continue
    return None

# ─────────────────────────────  Markdown Generation  ──────────────────
def generate_markdown_summary(reviewee_id, cycle_name, silent=False):
    """Generate markdown summary for a reviewee."""

    # Get basic info
    reviewee = get_reviewee_by_id(reviewee_id)
    user_id = reviewee["user"]["id"]
    user = get_user_by_id(user_id)
    user_name = user["name"]

    if not silent:
        print(f"   📊 Fetching reviews for {user_name}...")
    reviews = get_reviews_for_reviewee(reviewee_id)
    if not silent:
        print(f"   ✅ Found {len(reviews)} reviews")

    # Calculate scores
    self_scores = []
    peer_scores = []
    peer_not_observed = 0  # Track "not observed" responses

    for r in reviews:
        if not r or not r.get("response"):
            continue
        val = r.get("response", {}).get("ratingString")
        try:
            score = float(val)
        except (TypeError, ValueError):
            continue

        if r.get("reviewType") == "Self":
            self_scores.append(score)
        elif score == 6:  # "Haven't had opportunity to observe"
            peer_not_observed += 1
        else:
            peer_scores.append(score)

    def avg(lst):
        return round(sum(lst) / len(lst), 2) if lst else None

    self_avg = avg(self_scores)
    peer_avg = avg(peer_scores)
    delta = round(self_avg - peer_avg, 2) if self_avg and peer_avg else None

    # Build markdown
    md = []
    md.append(f"# {user_name} - {cycle_name}")
    md.append("")
    md.append("## Overall Scores")
    md.append("")
    if peer_avg is not None:
        peer_count = len(peer_scores)
        total_peer_reviews = peer_count + peer_not_observed
        response_rate = int((peer_count / total_peer_reviews * 100)) if total_peer_reviews > 0 else 0

        md.append(f"- **Peers Average**: {peer_avg} (based on {peer_count} ratings)")
        md.append(f"- **Response Rate**: {peer_count}/{total_peer_reviews} peer reviewers ({response_rate}%)")
    if self_avg is not None:
        md.append(f"- **Self Average**: {self_avg}")
    if delta is not None:
        md.append(f"- **Delta (Self - Peers)**: {delta:+.2f}")
    md.append("")
    md.append("---")
    md.append("")

    # Group by reviewer
    reviews_by_reviewer = defaultdict(list)
    question_cache = {}

    if not silent:
        print(f"   📝 Processing {len(reviews)} reviews...")
    for review in reviews:
        if not review or not review.get("question"):
            continue

        reviewer = get_user_by_id(review["reviewer"]["id"])
        q_id = review["question"]["id"]

        if q_id not in question_cache:
            question_cache[q_id] = get_question_by_id(q_id)

        q = question_cache[q_id]
        q_text = html.unescape(q["body"])

        scale = {str(v["value"]): v["descriptor"] for v in q.get("ratingScale") or []}
        resp = review.get("response") or {}

        rating_str = resp.get("ratingString", "N/A")
        rating_desc = scale.get(rating_str, "Unknown")

        comment = resp.get("comment") or ""
        comment = html.unescape(comment)
        comment = re.sub(r"<br\s*/?>", "\n", comment).strip() or None

        r_type = review.get("reviewType", "Peer")
        reviews_by_reviewer[(reviewer["id"], reviewer["name"], r_type)].append(
            (q_text, rating_str, rating_desc, comment)
        )

    # Output by reviewer
    for (rid, name, r_type), resps in reviews_by_reviewer.items():
        md.append(f"## {name} ({r_type})")
        md.append("")

        for i, (q, val, desc, com) in enumerate(resps, 1):
            md.append(f"### Question {i}")
            md.append(f"**{q}**")
            md.append("")
            md.append(f"**Rating**: {val} - {desc}")
            if com:
                md.append("")
                md.append("**Comment**:")
                md.append(f"> {com}")
            md.append("")

    return "\n".join(md)

# ─────────────────────────────  Main  ─────────────────────────────────
def process_single_person(name, cycle, reviewees, output_dir, cycle_name):
    """Process a single person's assessment."""
    print(f"\n🔍 Processing: {name}")

    try:
        # Find reviewee
        reviewee_id = find_reviewee_by_name(name, reviewees, cycle["id"])

        if not reviewee_id:
            print(f"   ⚠️  Skipped (not found in reviewees)")
            return False

        # Generate markdown
        markdown_content = generate_markdown_summary(reviewee_id, cycle_name, silent=True)

        # Save
        filename = name.replace(" ", "_").replace(",", "") + ".md"
        output_file = output_dir / filename
        output_file.write_text(markdown_content)

        print(f"   ✅ Saved {filename}")
        return True
    except KeyboardInterrupt:
        print(f"   ⚠️  Interrupted by user")
        raise
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return False

def main():
    """Fetch assessment(s) and save as markdown."""

    # Parse CLI arguments
    parser = argparse.ArgumentParser(
        description="Pull Rise8 EOY assessments from Lattice API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fetch_eoy_simple.py                    # Pull Matt Pacione only (default)
  python3 fetch_eoy_simple.py --practice platform # Pull all Platform/Cyber practice
  python3 fetch_eoy_simple.py --all              # Pull all missing reviewees
        """
    )
    parser.add_argument(
        "--practice",
        choices=["platform", "software", "design", "product"],
        help="Pull all members of specified practice"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Pull all missing reviewees with automatic categorization"
    )

    args = parser.parse_args()

    # Configuration
    CYCLE_NAME = "2025 EOY Assessment"
    BASE_OUTPUT_DIR = Path(__file__).parent / "assessments"
    BASE_OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"🔍 Searching for review cycle: '{CYCLE_NAME}'")

    # Find cycle
    cycles = get_all_review_cycles()
    cycle = next((c for c in cycles if c["name"] == CYCLE_NAME), None)

    if not cycle:
        print(f"❌ Review cycle '{CYCLE_NAME}' not found.")
        print("\n📋 Available cycles:")
        for c in cycles[:10]:
            print(f"  - {c['name']}")
        sys.exit(1)

    print(f"✅ Found cycle: {cycle['name']}")

    # Get reviewees
    print(f"🔍 Fetching reviewees...")
    reviewees = get_reviewees_for_cycle(cycle["id"])
    print(f"✅ Found {len(reviewees)} reviewees")

    # Determine which names to process and output directory
    if args.all:
        # Get all reviewees and filter out existing ones
        print(f"\n🔍 Loading all rosters for categorization...")
        name_to_folder = load_all_rosters()
        print(f"✅ Loaded {len(name_to_folder)} names from roster files")

        print(f"\n🔍 Checking existing assessments...")
        existing_names = get_existing_assessments(BASE_OUTPUT_DIR)
        print(f"✅ Found {len(existing_names)} existing assessments")

        # Get all names from reviewees
        print(f"\n🔍 Fetching all reviewee names from cycle...")
        all_reviewee_names = []
        for reviewee in reviewees:
            try:
                reviewee_detail = get_reviewee_by_id(reviewee["id"])
                user = get_user_by_id(reviewee_detail["user"]["id"])
                all_reviewee_names.append(user["name"])
            except Exception as e:
                print(f"   ⚠️  Error fetching reviewee: {e}")
                continue

        print(f"✅ Found {len(all_reviewee_names)} total reviewees in cycle")

        # Find missing names
        missing_names = [name for name in all_reviewee_names if name not in existing_names]
        print(f"\n📋 Missing assessments: {len(missing_names)}")

        if len(missing_names) == 0:
            print("✅ All assessments already pulled!")
            sys.exit(0)

        # Process missing names with categorization
        categorized = defaultdict(list)
        for name in missing_names:
            folder = name_to_folder.get(name, "Other")
            categorized[folder].append(name)

        print(f"\n📊 Categorization breakdown:")
        for folder, names in sorted(categorized.items()):
            print(f"   - {folder}: {len(names)} people")

        # Process each category
        success_count = 0
        failed_count = 0
        total_to_process = len(missing_names)

        for folder, names in sorted(categorized.items()):
            OUTPUT_DIR = BASE_OUTPUT_DIR / folder
            OUTPUT_DIR.mkdir(exist_ok=True)

            print(f"\n{'='*60}")
            print(f"📁 Processing {folder} ({len(names)} people)")
            print(f"{'='*60}")

            for i, name in enumerate(names, 1):
                print(f"\n[{success_count + failed_count + 1}/{total_to_process}] {folder}/{name}")
                success = process_single_person(name, cycle, reviewees, OUTPUT_DIR, CYCLE_NAME)
                if success:
                    success_count += 1
                else:
                    failed_count += 1

        # Final summary
        print(f"\n{'='*60}")
        print(f"✅ FINAL SUMMARY:")
        print(f"   - Successfully pulled: {success_count}/{total_to_process} assessments")
        if failed_count > 0:
            print(f"   - Failed/Skipped: {failed_count}")
        print(f"\n📊 Files placed in:")
        for folder, names in sorted(categorized.items()):
            saved = len([n for n in names if n not in failed_count])
            print(f"   - {folder}: {len(names)} assessments")
        print(f"\n🎉 Done!")
        sys.exit(0)

    elif args.practice == "platform":
        # Load Platform/Cyber roster
        roster_path = Path(__file__).parent / "LatticeAPI" / "lattice_api_client" / "team_map_platform.json"
        names_to_process = load_platform_roster(roster_path)
        OUTPUT_DIR = BASE_OUTPUT_DIR / "Platform-Cyber"
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"\n📋 Processing {len(names_to_process)} Platform/Cyber practice members")
    elif args.practice == "software":
        # Load Software roster
        roster_path = Path(__file__).parent / "LatticeAPI" / "lattice_api_client" / "team_map_software.json"
        names_to_process = load_platform_roster(roster_path)
        OUTPUT_DIR = BASE_OUTPUT_DIR / "Software"
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"\n📋 Processing {len(names_to_process)} Software practice members")
    elif args.practice == "design":
        # Load Design roster
        roster_path = Path(__file__).parent / "LatticeAPI" / "lattice_api_client" / "team_map_design.json"
        names_to_process = load_platform_roster(roster_path)
        OUTPUT_DIR = BASE_OUTPUT_DIR / "Design"
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"\n📋 Processing {len(names_to_process)} Design practice members")
    elif args.practice == "product":
        # Load Product roster
        roster_path = Path(__file__).parent / "LatticeAPI" / "lattice_api_client" / "team_map_product.json"
        names_to_process = load_platform_roster(roster_path)
        OUTPUT_DIR = BASE_OUTPUT_DIR / "Product-Management"
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"\n📋 Processing {len(names_to_process)} Product Management practice members")
    else:
        # Default: Matt Pacione only
        names_to_process = ["Matt Pacione"]
        OUTPUT_DIR = BASE_OUTPUT_DIR
        print(f"\n📋 Processing single person (default)")

    # Process each person
    success_count = 0
    failed_count = 0

    for i, name in enumerate(names_to_process, 1):
        if len(names_to_process) > 1:
            print(f"\n[{i}/{len(names_to_process)}]", end=" ")

        success = process_single_person(name, cycle, reviewees, OUTPUT_DIR, CYCLE_NAME)
        if success:
            success_count += 1
        else:
            failed_count += 1

    # Final summary
    print(f"\n{'='*60}")
    print(f"✅ Summary:")
    print(f"   - Successfully pulled: {success_count}/{len(names_to_process)} assessments")
    if failed_count > 0:
        print(f"   - Failed/Skipped: {failed_count}")
    print(f"   - Output directory: {OUTPUT_DIR}")
    print(f"\n🎉 Done!")

if __name__ == "__main__":
    main()
