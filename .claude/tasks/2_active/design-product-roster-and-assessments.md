# Task: Design and Product Management Roster + Assessment Pull

## Objective
Create roster files for Design (16 members) and Product Management (22 members) practices, extend fetch_eoy_simple.py to support these practices, and pull their EOY assessments.

## Context
- Existing rosters: `team_map_platform.json` (44 members), `team_map_software.json` (43 members)
- Existing script supports: `--practice platform` and `--practice software`
- Output directories: `assessments/Platform-Cyber/`, `assessments/Software/`
- Format: JSON with "Last, First": "Team" mapping

## Constraints
- Follow existing roster file format and naming conventions
- Match Lattice API name format: "Last, First"
- Use placeholder team names if unknown (e.g., "Design", "Product Management")
- Script must support `--practice design` and `--practice product` options

## Expected Deliverables

### 1. Design Roster File
- **File**: `LatticeAPI/lattice_api_client/team_map_design.json`
- **Members (16)**:
  - Van Dalen, Jonathan
  - O'Donnell, Matt
  - Mendiola, Nick
  - Yoo, Sally
  - Almond, Jacob
  - Zubia, Anthony
  - Akre, Sagar
  - Brierton, Alexandra
  - McFarland, Drew
  - Gates, Kevin
  - McGraw, Darla
  - Cheng, Hannah
  - Kim, Seehyun
  - Redding, Damon
  - Anastasio, Tom
  - Chang, Erica

### 2. Product Management Roster File
- **File**: `LatticeAPI/lattice_api_client/team_map_product.json`
- **Members (22)**:
  - Pritchett, Joshua
  - James, Becca
  - Van Hove, Jennifer
  - Hernandez, Abel
  - Estoy, Michael
  - Strebel, Luke
  - Croney, David
  - Golan, Ron
  - Mladinov, Evan
  - Liu, Yi
  - Kung, Ann
  - Chapman, David
  - Wilkins, Jesse
  - Pollin, Mary
  - Weiss, Nick
  - Sperry, Ian
  - Patel, Roshni
  - Goel, Shubham
  - Burton, Abbie
  - Berner, Alex
  - Tovar, Art
  - Pain, Clark

### 3. Script Enhancement
- **File**: `fetch_eoy_simple.py`
- **Changes**:
  - Add "design" and "product" to `--practice` choices
  - Add logic to handle design roster → `assessments/Design/` output
  - Add logic to handle product roster → `assessments/Product-Management/` output

### 4. Pull Assessments
- **Design**: `python3 fetch_eoy_simple.py --practice design`
- **Product**: `python3 fetch_eoy_simple.py --practice product`

## Success Criteria
- [ ] `team_map_design.json` created with 16 entries in "Last, First" format
- [ ] `team_map_product.json` created with 22 entries in "Last, First" format
- [ ] Script accepts `--practice design` option
- [ ] Script accepts `--practice product` option
- [ ] Design assessments saved to `assessments/Design/`
- [ ] Product assessments saved to `assessments/Product-Management/`
- [ ] Final report showing: X/16 design pulled, Y/22 product pulled
- [ ] List any missing/skipped people with reasons

## Commands to Run
```bash
# Verify roster files
cat LatticeAPI/lattice_api_client/team_map_design.json
cat LatticeAPI/lattice_api_client/team_map_product.json

# Pull design assessments
python3 fetch_eoy_simple.py --practice design

# Pull product management assessments
python3 fetch_eoy_simple.py --practice product

# Verify outputs
ls -la assessments/Design/
ls -la assessments/Product-Management/
```

## Notes
- Convert "First Last" to "Last, First" format to match Lattice API conventions
- Use placeholder team names since specific team assignments unknown
- Follow existing code patterns from platform/software roster handling
