#!/usr/bin/env python3
"""
Pull assessments for Kyle Smart and Cason Brinson
"""

import json
import urllib.request
from pathlib import Path
from collections import defaultdict
import html
import re

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

def generate_markdown_summary(reviewee_id, cycle_name):
    """Generate markdown summary for a reviewee."""

    # Get basic info
    reviewee = get_reviewee_by_id(reviewee_id)
    user_id = reviewee["user"]["id"]
    user = get_user_by_id(user_id)
    user_name = user["name"]

    print(f"   📊 Fetching reviews for {user_name}...")
    reviews = get_reviews_for_reviewee(reviewee_id)
    print(f"   ✅ Found {len(reviews)} reviews")

    # Calculate scores
    self_scores = []
    peer_scores = []

    for r in reviews:
        if not r or not r.get("response"):
            continue
        val = r.get("response", {}).get("ratingString")
        try:
            score = float(val)
        except (TypeError, ValueError):
            continue
        if score == 6:  # Skip "Haven't had opportunity to observe"
            continue
        if r.get("reviewType") == "Self":
            self_scores.append(score)
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
        md.append(f"- **Peers Average**: {peer_avg}")
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

def main():
    """Pull assessments for Kyle Smart and Cason Brinson"""

    CYCLE_NAME = "2025 EOY Assessment"
    OUTPUT_DIR = Path(__file__).parent / "assessments" / "Software"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Target reviewees (found from previous search)
    targets = [
        ("Kyle Smart", "reviewee-2bb6f3ce-b34c-11f0-b023-2fa8ecb68ae7"),
        ("Cason Brinson", "reviewee-2ba79b2c-b34c-11f0-b023-7bb5f69e7f1e")
    ]

    print(f"🔍 Pulling assessments for 2 missing Software engineers\n")

    success_count = 0
    for name, reviewee_id in targets:
        print(f"📥 Processing: {name}")

        try:
            # Generate markdown
            markdown_content = generate_markdown_summary(reviewee_id, CYCLE_NAME)

            # Save
            filename = name.replace(" ", "_").replace(",", "") + ".md"
            output_file = OUTPUT_DIR / filename
            output_file.write_text(markdown_content)

            print(f"   ✅ Saved {filename}\n")
            success_count += 1
        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")

    print(f"{'='*60}")
    print(f"✅ Summary:")
    print(f"   - Successfully pulled: {success_count}/{len(targets)} assessments")
    print(f"   - Output directory: {OUTPUT_DIR}")
    print(f"\n🎉 Done!")

if __name__ == "__main__":
    main()
