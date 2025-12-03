#!/usr/bin/env python3
"""
fetch_eoy_assessment.py - Pull Matt Pacione's peer assessment from "2025 EOY Assessment"
and save as markdown file locally.
"""

import os
import sys
import re
import html
from pathlib import Path
from collections import defaultdict
import logging

# Add LatticeAPI to path
sys.path.insert(0, str(Path(__file__).parent / "LatticeAPI" / "lattice_api_client"))

import requests
from dotenv import load_dotenv

# ─────────────────────────────  Logging  ──────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ─────────────────────────────  Env & session  ────────────────────────
# Load from LatticeAPI/.env
env_path = Path(__file__).parent / "LatticeAPI" / ".env"
load_dotenv(env_path)

BASE_URL = os.getenv("LATTICE_API_URL")
TOKEN = os.getenv("LATTICE_API_TOKEN")

if not TOKEN or not BASE_URL:
    logger.error("Missing LATTICE_API_URL or LATTICE_API_TOKEN in .env file.")
    sys.exit(1)

SESSION = requests.Session()
SESSION.headers.update({"Authorization": f"Bearer {TOKEN}"})

# ─────────────────────────────  Constants  ────────────────────────────
REVIEW_LIMIT = 100
REVIEWEE_LIMIT = 100
TIMEOUT = (30, 120)

# ─────────────────────────────  API Helpers  ──────────────────────────
def _get(url: str):
    """Make GET request to Lattice API."""
    resp = SESSION.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def get_all_review_cycles():
    """Fetch all review cycles."""
    url = f"{BASE_URL}/reviewCycles?limit=100"
    cycles = []
    while url:
        out = _get(url)
        cycles.extend(out["data"])
        url = (
            f"{BASE_URL}/reviewCycles?limit=100&startingAfter={out['endingCursor']}"
            if out.get("hasMore") else None
        )
    return cycles

def get_reviewees_for_cycle(cycle_id):
    """Fetch all reviewees for a given cycle."""
    url = f"{BASE_URL}/reviewCycle/{cycle_id}/reviewees?limit={REVIEWEE_LIMIT}"
    reviewees = []
    while url:
        out = _get(url)
        reviewees.extend(out["data"])
        url = (
            f"{BASE_URL}/reviewCycle/{cycle_id}/reviewees?limit={REVIEWEE_LIMIT}&startingAfter={out['endingCursor']}"
            if out.get("hasMore") else None
        )
    return reviewees

def get_reviewee_by_id(reviewee_id):
    """Fetch reviewee details."""
    return _get(f"{BASE_URL}/reviewee/{reviewee_id}")

def get_user_by_id(user_id):
    """Fetch user details."""
    return _get(f"{BASE_URL}/user/{user_id}")

def get_reviews_for_reviewee(reviewee_id):
    """Fetch all reviews for a reviewee."""
    url = f"{BASE_URL}/reviewee/{reviewee_id}/reviews?limit={REVIEW_LIMIT}"
    reviews = []
    while url:
        out = _get(url)
        reviews.extend(out["data"])
        url = (
            f"{BASE_URL}/reviewee/{reviewee_id}/reviews?limit={REVIEW_LIMIT}&startingAfter={out['endingCursor']}"
            if out.get("hasMore") else None
        )
    return reviews

def get_question_by_id(question_id):
    """Fetch question details."""
    return _get(f"{BASE_URL}/question/{question_id}")

# ─────────────────────────────  Markdown Generation  ──────────────────
def generate_markdown_summary(reviewee_id: str, cycle_name: str) -> str:
    """Generate markdown summary for a reviewee's assessment."""

    # Get reviewee and user info
    reviewee = get_reviewee_by_id(reviewee_id)
    user_id = reviewee["user"]["id"]
    user = get_user_by_id(user_id)
    user_name = user["name"]

    # Pull all reviews
    reviews = get_reviews_for_reviewee(reviewee_id)

    # Calculate overall scores
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
        if score == 6:  # "Haven't had opportunity to observe" - skip
            continue
        if r.get("reviewType") == "Self":
            self_scores.append(score)
        else:
            peer_scores.append(score)

    def _avg(lst):
        return round(sum(lst) / len(lst), 2) if lst else None

    self_avg = _avg(self_scores)
    peer_avg = _avg(peer_scores)
    delta = round(self_avg - peer_avg, 2) if self_avg and peer_avg else None

    # Start building markdown
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

    # Group reviews by reviewer
    reviews_by_reviewer = defaultdict(list)
    question_cache = {}

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
def main():
    """Fetch Matt Pacione's assessment from '2025 EOY Assessment' and save as markdown."""

    # Configuration
    TARGET_NAME = "Matt Pacione"
    CYCLE_NAME = "2025 EOY Assessment"
    OUTPUT_DIR = Path(__file__).parent / "assessments"
    OUTPUT_DIR.mkdir(exist_ok=True)

    logger.info(f"🔍 Searching for review cycle: '{CYCLE_NAME}'")

    # Find the cycle
    cycles = get_all_review_cycles()
    cycle = next((c for c in cycles if c["name"] == CYCLE_NAME), None)

    if not cycle:
        logger.error(f"❌ Review cycle '{CYCLE_NAME}' not found.")
        logger.info("\n📋 Available cycles:")
        for c in cycles:
            logger.info(f"  - {c['name']}")
        sys.exit(1)

    logger.info(f"✅ Found cycle: {cycle['name']} (ID: {cycle['id']})")

    # Get all reviewees for this cycle
    logger.info(f"🔍 Fetching reviewees for cycle...")
    reviewees = get_reviewees_for_cycle(cycle["id"])
    logger.info(f"✅ Found {len(reviewees)} reviewees")

    # Find Matt Pacione's reviewee record
    logger.info(f"🔍 Searching for '{TARGET_NAME}'...")
    target_reviewee = None

    for reviewee in reviewees:
        reviewee_detail = get_reviewee_by_id(reviewee["id"])
        user = get_user_by_id(reviewee_detail["user"]["id"])
        if user["name"] == TARGET_NAME:
            target_reviewee = reviewee
            logger.info(f"✅ Found {TARGET_NAME} (Reviewee ID: {reviewee['id']})")
            break

    if not target_reviewee:
        logger.error(f"❌ Could not find reviewee record for '{TARGET_NAME}'")
        sys.exit(1)

    # Generate markdown summary
    logger.info(f"📝 Generating markdown summary...")
    markdown_content = generate_markdown_summary(target_reviewee["id"], CYCLE_NAME)

    # Save to file
    output_file = OUTPUT_DIR / f"{TARGET_NAME.replace(' ', '_')}.md"
    output_file.write_text(markdown_content)

    logger.info(f"✅ Assessment saved to: {output_file}")
    logger.info(f"\n📊 Summary:")
    logger.info(f"   - Reviewee: {TARGET_NAME}")
    logger.info(f"   - Cycle: {CYCLE_NAME}")
    logger.info(f"   - Output: {output_file}")
    logger.info("\n🎉 Done!")

if __name__ == "__main__":
    main()
