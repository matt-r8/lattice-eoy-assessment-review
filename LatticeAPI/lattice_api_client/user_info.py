import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

BASE = os.getenv("LATTICE_API_URL", "https://api.latticehq.com/v1")
TOKEN = os.getenv("LATTICE_API_TOKEN")

assert TOKEN, "Missing LATTICE_API_TOKEN"

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {TOKEN}"})

resp = session.get(f"{BASE}/users?limit=5")
resp.raise_for_status()

for user in resp.json()["data"]:
    print(json.dumps(user, indent=2))
