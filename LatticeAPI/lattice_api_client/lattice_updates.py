#!/usr/bin/env python3
"""
lattice_updates.py
List the most-recent Lattice **Updates** written only by your direct reports.

Environment
-----------
LATTICE_API_URL   e.g. https://api.latticehq.com/v1
LATTICE_API_TOKEN your bearer token (Admin → Settings → API)

Usage
-----
python lattice_updates.py --rows 10        # first 10 updates from directs
python lattice_updates.py --page 50        # bigger API page-size, unlimited rows
"""
from __future__ import annotations
import os, sys, argparse, datetime, logging, re
from functools import lru_cache
from typing    import Iterator, Any, Dict

import requests
from dotenv import load_dotenv               # pip install python-dotenv

# ─── logging ───────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ─── env / session ─────────────────────────────────────────────────────
load_dotenv()
BASE_URL = os.getenv("LATTICE_API_URL")
TOKEN    = os.getenv("LATTICE_API_TOKEN")
TIMEOUT  = 15

if not BASE_URL or not TOKEN:
    logger.error("Missing LATTICE_API_URL or LATTICE_API_TOKEN.")
    sys.exit(1)

SESSION = requests.Session()
SESSION.headers.update({"Authorization": f"Bearer {TOKEN}"})

# ─── thin wrappers ─────────────────────────────────────────────────────
def _get(url: str) -> Dict[str, Any]:
    r = SESSION.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

@lru_cache(maxsize=1024)
def get_user_by_id(uid: str) -> Dict[str, Any]:
    return _get(f"{BASE_URL}/user/{uid}")

def get_me() -> Dict[str, Any]:
    return _get(f"{BASE_URL}/me")

def get_direct_reports(uid: str) -> list[Dict[str, Any]]:
    return _get(f"{BASE_URL}/user/{uid}/directReports")["data"]

def ts_to_iso(ts: int) -> str:
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date().isoformat()

# ─── pagination over updates ───────────────────────────────────────────
def fetch_updates(page_size: int = 100) -> Iterator[Dict[str, Any]]:
    url: str | None = f"{BASE_URL}/updates?limit={page_size}"
    while url:
        block = _get(url)
        yield from block["data"]
        url = (f"{BASE_URL}/updates?limit={page_size}&startingAfter={block['endingCursor']}"
               if block.get("hasMore") else None)

# ─── main ──────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="List Lattice updates from your direct reports.")
    ap.add_argument("--page", type=int, default=100,
                    help="API page-size (default 100)")
    ap.add_argument("--rows", type=int, default=None,
                    help="Maximum rows to print (None = unlimited)")
    args = ap.parse_args()

    # ── gather direct-report IDs ──────────────────────────────────────
    me        = get_me()
    reports   = get_direct_reports(me["id"])
    report_ids = {u["id"] for u in reports}

    logger.info(f"Manager       : {me['name']}")
    logger.info(f"Direct reports: {len(report_ids)}")
    logger.info("Fetching updates …\n")

    shown = 0
    for upd in fetch_updates(page_size=args.page):
        uid = (
            (upd.get("user")    or {}).get("id")
            or (upd.get("author")  or {}).get("id")
            or (upd.get("creator") or {}).get("id")
        )
        if uid not in report_ids:
            continue                      # skip non-directs
        # guard: some empty placeholders
        if upd is None or upd.get("createdAt") is None:
            continue

        when   = ts_to_iso(upd["createdAt"])
        author = get_user_by_id(uid)["name"] if uid else "Unknown"
        body   = (upd.get("text") or "").strip()
        body   = re.sub(r"\s+", " ", body)     # collapse whitespace
        snippet = (body[:117] + "…") if len(body) > 120 else body

        logger.info(f"{when}  {author:<25}  {snippet}")
        shown += 1
        if args.rows and shown >= args.rows:
            break

if __name__ == "__main__":
    main()
