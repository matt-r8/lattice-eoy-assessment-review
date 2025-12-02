# 🏎️ Quck Run
1. Delete individual updates in Google Drive folder, `./updates`
2. Run these commands in the repo's folder, for example:
```
cd ~/git/lattice/lattice_api_client
source ./.venv/bin/activate
python lattice_populate_updates.py --directs
python lattice_populate_updates.py --export-docx
```

# 📦 Setup Instructions (macOS)

## 1. Clone the Repository

```bash
# Project Repo: https://github.com/rise8-us/LatticeAPI
git clone https://github.com/rise8-us/LatticeAPI.git
cd lattice_api_client
```

## 2. Generate Lattice API Token
Generate a Lattice API token

- Log in to Lattice with an Admin account.
- Navigate to Admin → Settings → API.
- Click Generate Token (or copy the existing one).
- Copy the token to your .env.

## 3. Environment Variables

Create a `.env` file in the root of the project:

```env
LATTICE_API_URL=https://api.latticehq.com/v1
LATTICE_API_TOKEN=your_api_token_here
TEAM=platform #platform, software, product, design
```

---

## 4. Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

# Lattice Update Export Script

This Python script fetches Lattice updates (optionally scoped to your direct reports), stores them in a local SQLite database, and can export each direct report's updates to individual `.docx` files. It also generates a team sentiment summary with participation and sentiment trends by month.

---

## Populate Practice JSON
Create a team_map_{PRACTICE_NAME}.json file with your team breakdowns. Here's `team_map_platform.json` for example:
```json
{
    "Allen, Coty": "VA LH SRE",
    "Alvarez, Benjamin": "FORGE Cyber",
    "Arzuaga, Jeremy": "VA LH SecRel",
    "Bair, Steven": "FORGE Portfolio",
    ...
}
```
Commit this to the repo when finished.

## ✅ Usage

### Fetch & Store Updates in Local SQLite DB

```bash
python lattice_populate_updates.py --directs
```

### Export Updates to `.docx` for All Direct Reports

```bash
python lattice_populate_updates.py --export-docx
```

### Export Updates for a Specific Person

```bash
python lattice_populate_updates.py --export-docx "Last, First"
```

### View Updates in Terminal

```bash
python lattice_populate_updates.py --report-name "Last, First"
```

# Lattice Reviews Export Script

This Python script fetches and summarizes Lattice review-cycle feedback for your direct reports.  
It generates per-report `.docx` summaries and a team stack-rank table.

Export all to the `./summaries` folder as `.docx` files.
```bash
python lattice_reviews.py --group-by question
```
## ✅ Usage

Basic usage:
```bash
python lattice_reviews.py --name "Full Name"
```
Filter by question topic:
```bash
python lattice_reviews.py --name "Full Name" --filter "growth"
```
Group by question instead of reviewer:
```bash
python lattice_reviews.py --name "Full Name" --group-by question
```
See all available filters:
```bash
python lattice_reviews.py --help-questions
```
Set a custom review cycle name:
```bash
python lattice_reviews.py --name "Full Name" --cycle "2025 Formal Mid-Year Feedback"
```