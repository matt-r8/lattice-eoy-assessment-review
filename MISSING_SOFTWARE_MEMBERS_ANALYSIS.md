# Missing Software Practice Members Analysis

## Summary

Created `fetch_missing_software.py` script to fetch 5 specific missing Software practice members from the roster. However, **these 5 members do not exist in the Lattice "2025 EOY Assessment" cycle**.

## Script Created

- **File**: `/workspaces/lattice-eoy-assessment-review/fetch_missing_software.py`
- **Purpose**: Fetch EOY assessments for 5 specific missing Software practice members
- **Features**:
  - Uses same API patterns from `fetch_eoy_simple.py`
  - 2-second delays between requests for rate limit protection
  - Retry logic for HTTP 429 errors (5s retry delay)
  - Progress reporting for each member
  - Saves to `assessments/Software/` directory

## Requested Missing Members

The following 5 members were identified as missing from the Software practice assessments:

1. **Angie Davidson** - R&D
2. **Nate Enders** - Tracer
3. **Gannon Gardner** - MOSS
4. **Kevin Nguyen** - EM&C App Team 2
5. **Dustin Tran** (dustintktran) - Star Fox

## Investigation Results

### Lattice System Check

Verified that these 5 members **do NOT exist** in the Lattice "2025 EOY Assessment" reviewee list:

```
❌ NOT FOUND: Angie Davidson
❌ NOT FOUND: Nate Enders
❌ NOT FOUND: Gannon Gardner
❌ NOT FOUND: Kevin Nguyen
❌ NOT FOUND: Dustin Tran
```

### Similar Names Found

The Lattice system contains similar names that may cause confusion:

- **Alden Davidson** (not Angie Davidson) - exists in cycle
- **Adam Gardner** (not Gannon Gardner) - exists in cycle

### Current Status

| Roster Name | Team | Status in Lattice | Fetched |
|------------|------|------------------|---------|
| Angie Davidson | R&D | ❌ Not in cycle | No |
| Nate Enders | Tracer | ❌ Not in cycle | No |
| Gannon Gardner | MOSS | ❌ Not in cycle | No |
| Kevin Nguyen | EM&C App Team 2 | ❌ Not in cycle | No |
| dustintktran Tran | Star Fox | ❌ Not in cycle | No |

### Additional Missing Member

There is 1 additional missing member from the roster not included in the original 5:

- **Cory** - Beach (❌ Not in cycle)

## Roster vs. Assessment Comparison

- **Total in Software roster**: 41 members
- **Total assessments fetched**: 36 members
- **Missing from assessments**: 6 members (including "Cory")

## Possible Explanations

1. **Not part of EOY assessment cycle**: These 5 members may not be participating in the 2025 EOY Assessment
2. **Name mismatches**: Their Lattice profiles may use different names than the roster
3. **Joined after cycle creation**: They may have joined Rise8 after the assessment cycle was created
4. **Left before assessment**: They may have left Rise8 before completing the assessment

## Recommendations

1. **Verify with HR/Manager**: Confirm whether these 5 people should be in the 2025 EOY Assessment
2. **Check Lattice Admin**: Review the Lattice admin panel to see if these users exist but weren't added to the cycle
3. **Name verification**: Verify the exact names these users have in Lattice (may differ from roster)
4. **Manual investigation**: Check if they have assessments under different names or in different cycles

## How to Run the Script

Even though these members don't exist in the cycle, the script is ready to use if they are added later:

```bash
python3 fetch_missing_software.py
```

The script will:
- Search for each of the 5 members
- Report "not found" for members not in the cycle
- Fetch and save assessments for any members that are found
- Include 2-second delays between requests to avoid rate limiting
- Retry on HTTP 429 errors with 5-second delay

## Testing Performed

1. ✅ Script created with proper API integration
2. ✅ Rate limiting protection implemented (2s delays)
3. ✅ Retry logic for HTTP 429 errors implemented
4. ✅ Verified names don't exist in Lattice cycle
5. ✅ Identified similar names that do exist
6. ✅ Confirmed total missing count (6 members)

## Conclusion

The `fetch_missing_software.py` script has been successfully created and is ready to use. However, the 5 requested members do not exist in the Lattice "2025 EOY Assessment" cycle, so no assessments can be fetched for them at this time.

Further investigation with HR or Lattice administrators is needed to determine why these roster members are not in the assessment cycle.
