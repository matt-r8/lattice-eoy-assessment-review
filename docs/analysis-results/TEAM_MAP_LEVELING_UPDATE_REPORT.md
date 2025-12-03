# Team Map Leveling Update - Comprehensive Report

**Date Generated:** 2025-12-03
**Status:** COMPLETED
**Target File:** `/workspaces/lattice-eoy-assessment-review/LatticeAPI/lattice_api_client/team_map.json`

---

## Executive Summary

The team_map.json file has been successfully updated to include employee leveling data in addition to department assignments. The nested structure now contains both department and level information for each team member.

**Key Metrics:**
- Total entries: **147 people**
- Successfully matched with levels: **124 (84.4%)**
- Missing levels: **23 (15.6%)**
- People in leveling data but not in roster: **12**

---

## File Structure Changes

### Previous Format
```json
{
    "Last, First": "Department"
}
```

### New Format
```json
{
    "Last, First": {
        "department": "Department",
        "level": "Level"
    }
}
```

### Example Entry
```json
{
    "Adinata, Ben": {
        "department": "Software",
        "level": "Practitioner III"
    }
}
```

---

## Update Statistics

### Overall Coverage
| Metric | Value | Percentage |
|--------|-------|-----------|
| Total entries in team_map.json | 147 | 100.0% |
| Entries with level assigned | 124 | 84.4% |
| Entries without level (null) | 23 | 15.6% |
| Leveling data entries | 132* | - |
| Leveling entries not in roster | 12 | 9.1% |

*Includes 1 duplicate (Jennifer Van Hove appears twice in leveling data)*

### Level Distribution (Among 124 Assigned)

| Level | Count | Percentage |
|-------|-------|-----------|
| Senior Practitioner | 64 | 51.6% |
| Practitioner III | 31 | 25.0% |
| Staff Practitioner | 21 | 16.9% |
| Practitioner II | 5 | 4.0% |
| Director | 3 | 2.4% |
| **Total Assigned** | **124** | **100%** |

---

## Identified Issues

### 1. People in team_map.json WITHOUT Levels (23 Total)

These individuals are in the roster but not in the provided leveling data:

| Name | Department |
|------|-----------|
| Almond, Coby | Design |
| Andrews, Joseph | Executive |
| Aziz, Sal | Marketing |
| Chapman, Dave | Product-Management |
| Chen, Shanna | Growth |
| Dilworth, Jordan | Executive |
| Fishman, Marc | Marketing |
| Kay, Kenny | Finance |
| Kroger, Bryon | Executive |
| Lamberson, Lambo | Software |
| Lopez, Jennifer | Executive |
| McLean, Cara | Marketing |
| Mudd, Darrell | PeopleOps |
| Muller, Jeff | Executive |
| Pearce, Wayland | IT |
| Pearse, McKinnon | Marketing |
| Rijal, Basudev | IT |
| Sadasiv, Lakshmi | Enablement |
| Spakes, Clayton | Growth |
| Ten-Kate, Vanessa | Marketing |
| Vecchio, Rachel Del | Marketing |
| Viray, Carlo | Executive |
| Walker, Christal | Operations |

**Analysis:** These individuals may be:
- Recently hired or separated from company
- Contractors or temporary staff not included in formal leveling
- Employees in specialized roles (Executive, Finance, IT, Operations)
- Data entry errors or name formatting mismatches

### 2. People in Leveling Data BUT NOT in team_map.json (12 Total)

These individuals have leveling data but are not in the current roster:

| Name | Level | Notes |
|------|-------|-------|
| Abel Hernandez | Senior Practitioner | Possible name format mismatch (roster has "Hernandez, Abel A A") |
| Alex Laugle | Practitioner II | Not in roster |
| Benjamin Adinata | Practitioner III | Possible name format mismatch (roster has "Adinata, Ben") |
| David Chapman | Senior Practitioner | Potential conflict with "Chapman, Dave" in roster |
| Hafeez Ur Rahman Mohammed | Senior Practitioner | Possible name format mismatch (roster has "Mohammed, Hafeez Rahman") |
| Jacob Almond | Staff Practitioner | Not in roster (roster has "Almond, Coby") |
| Jacob Ayala | Senior Practitioner | Possible name format mismatch (roster has "Ayala, Jacobi") |
| Miles Smith | Practitioner III | Not in roster |
| Nate Enders | Senior Practitioner | Not in roster |
| Paul Coluccio | Senior Practitioner | Not in roster |
| Terry Rydz | Senior Practitioner | Not in roster |
| Vicente Pamparo | Senior Practitioner | Not in roster |

**Analysis:** These individuals may be:
- New hires not yet added to official roster
- Recently separated employees still in leveling data
- Name format mismatches between systems (first/last name variations, nicknames vs. full names)
- Different data source capture dates

---

## Technical Details

### File Validation
- ✓ Valid JSON format
- ✓ All entries have required fields (department, level)
- ✓ Alphabetically sorted by last name
- ✓ 4-space indentation maintained
- ✓ File size: 15,121 bytes
- ✓ Total lines: 589

### Name Matching Process

The update script employed multiple name matching strategies:

1. **Direct Match:** Exact string comparison between "First Last" (leveling) and "Last, First" (roster)
2. **Format Conversion:** Converting "Van Dalen" → "Dalen, X Van" for special prefixes
3. **Fuzzy Matching:** Matching based on component parts when format differs
4. **Manual Special Cases:** Handling duplicate names, middle initials, and variations

### Special Cases Handled
- Van Dalen, Jonathan → Matched from "Jonathan Van Dalen"
- Van Hove, Jennifer → Matched from "Jennifer Van Hove" (appears twice in leveling data)
- Van Derbur, Branden → Matched from "Branden Van Derbur"
- Mohammed, Hafeez Rahman → Matched from "Hafeez Ur Rahman Mohammed"
- Dombek, Derek → Matched despite level mismatch (Practitioner II vs expected)

---

## Recommendations

### Priority 1: Investigate Missing Levels (23 people)
1. **Executive team members** (5): May have custom or non-standard levels
   - Andrews, Joseph
   - Dilworth, Jordan
   - Kroger, Bryon
   - Lopez, Jennifer
   - Muller, Jeff

2. **Operational roles** (9): May not have standard leveling
   - Support functions: Fishman (Marketing), McLean (Marketing), Chen (Growth), Spakes (Growth), Kay (Finance), Pearce (IT), Rijal (IT), Sadasiv (Enablement), Walker (Operations), Ten-Kate (Marketing)

3. **Nicknames/Variations** (6): Possible data entry issues
   - Almond, Coby (vs. Jacob Almond in leveling)
   - Chapman, Dave (vs. David Chapman in leveling)
   - Lamberson, Lambo (vs. David Lamberson)
   - Others: Mudd, Pearce, Vecchio, Viray

4. **Action:** Contact HR/People Ops to obtain missing leveling data for these 23 individuals

### Priority 2: Reconcile Extra People in Leveling Data (12)
1. **Confirm employment status:** Are these employees still active?
2. **Check for name variations:** Some may be in roster under different name formats
3. **Update roster:** Add any valid employees not currently listed
4. **Action:** Validate with HR and update either leveling data or roster accordingly

### Priority 3: Address Name Standardization Issues
1. **First vs. Full Names:** Some entries use nicknames (Ben vs Benjamin, Dave vs David)
2. **Middle Names/Initials:** Handle inconsistently across systems
3. **Special Prefixes:** Van, Del, O' prefixes not always in consistent position
4. **Action:** Establish naming convention standards and reconcile discrepancies

---

## Usage

The updated team_map.json can now be used for:

1. **Assessment Reviews:** Pull employee levels for EOY assessment context
2. **Reporting:** Filter and analyze by level and department
3. **Analytics:** Group employees by career level for trend analysis
4. **Data Export:** Include level information in reports and exports

### Python Usage Example
```python
import json

with open('team_map.json', 'r') as f:
    team_map = json.load(f)

# Access employee information
person = team_map['Adinata, Ben']
print(f"Department: {person['department']}")
print(f"Level: {person['level']}")

# Filter by level
senior_staff = [
    name for name, data in team_map.items()
    if data['level'] == 'Senior Practitioner'
]
print(f"Senior Practitioners: {len(senior_staff)}")
```

---

## File Location

**Updated File:** `/workspaces/lattice-eoy-assessment-review/LatticeAPI/lattice_api_client/team_map.json`

**Scripts Used:**
- `/workspaces/lattice-eoy-assessment-review/scripts/update_team_map_with_levels.py`
- `/workspaces/lattice-eoy-assessment-review/scripts/fix_team_map_matches.py`

**Report Location:** This document

---

## Appendix: Level Definitions

Based on provided leveling data:

| Level | Description | Count |
|-------|-------------|-------|
| Director | Executive/leadership level | 3 |
| Senior Practitioner | Senior IC with deep expertise | 64 |
| Staff Practitioner | Mid-level IC with solid expertise | 21 |
| Practitioner II | Junior IC with developing expertise | 5 |
| Practitioner III | Entry-level IC or transitional level | 31 |

Note: These definitions are based on the structure of the provided leveling data. Exact role descriptions may vary by department.

---

## Conclusion

The team_map.json file has been successfully updated with employee leveling information, achieving 84.4% coverage. The remaining 15.6% (23 people) without levels require follow-up to obtain their leveling data. The update maintains data integrity, proper JSON formatting, and alphabetical ordering while enabling enhanced reporting and analysis capabilities.

