# Scripts Directory

This directory contains Python scripts and shell utilities for the Lattice EOY Assessment Review project.

## Main Scripts

These are the primary scripts for regular operation:

### `fetch_eoy_simple.py`
**Primary fetch script for End-of-Year assessments**

Fetches assessment data from Lattice API with progress tracking and error handling.

Usage:
```bash
python scripts/fetch_eoy_simple.py
```

Features:
- Simplified API interaction
- Progress tracking
- Comprehensive error logging
- Response rate monitoring

### `fetch_eoy_assessment.py`
**Original fetch script (alternative)**

Legacy version of the fetch script with additional features. Use `fetch_eoy_simple.py` as the primary option.

Usage:
```bash
python scripts/fetch_eoy_assessment.py
```

### `analyze_scores.py`
**Score analysis and reporting**

Analyzes assessment scores and generates reports.

Usage:
```bash
python scripts/analyze_scores.py
```

### `regenerate_all.sh`
**Batch regeneration script**

Regenerates all assessment data in batch mode. Useful for full data refreshes.

Usage:
```bash
bash scripts/regenerate_all.sh
```

## Diagnostic Scripts

Located in `scripts/diagnostic/` - Use for troubleshooting, analysis, and validation:

### Data Validation
- **`check_roster_completeness.py`** - Validates roster data completeness
- **`verify_remaining_missing.py`** - Identifies and verifies missing data
- **`verify_response_rates.py`** - Analyzes response rate metrics

### Data Analysis
- **`analyze_scores.py`** - Comprehensive score analysis (also in main scripts)
- **`test_response_rate.py`** - Response rate testing and analysis
- **`find_missing_engineers.py`** - Identifies missing engineer records

### File Management
- **`find_extra_files.py`** - Locates extra/unexpected files
- **`fetch_missing_software.py`** - Fetches missing software assessment data
- **`pull_missing_two.py`** - Pulls specific missing data segments

### Utilities
- **`search_enders.py`** - Searches for data records
- **`test_names.py`** - Name validation and testing

Usage for any diagnostic script:
```bash
python scripts/diagnostic/[script_name].py
```

## Environment Setup

All scripts require `.env` configuration:

```bash
# Copy environment template
cp .env.example .env

# Edit with your Lattice API credentials
# LATTICE_API_KEY=your_key_here
# LATTICE_API_URL=your_url_here
```

## Directory Structure

```
scripts/
├── README.md                     # This file
├── fetch_eoy_simple.py          # Primary fetch script
├── fetch_eoy_assessment.py      # Alternative fetch script
├── analyze_scores.py            # Score analysis
├── regenerate_all.sh            # Batch regeneration
└── diagnostic/                   # Diagnostic utilities
    ├── check_roster_completeness.py
    ├── fetch_missing_software.py
    ├── find_extra_files.py
    ├── find_missing_engineers.py
    ├── pull_missing_two.py
    ├── search_enders.py
    ├── test_names.py
    ├── test_response_rate.py
    ├── verify_remaining_missing.py
    └── verify_response_rates.py
```

## Running Scripts

### From Project Root
```bash
# Run primary fetch
python scripts/fetch_eoy_simple.py

# Run analysis
python scripts/analyze_scores.py

# Run batch regeneration
bash scripts/regenerate_all.sh

# Run diagnostic scripts
python scripts/diagnostic/check_roster_completeness.py
```

### From Scripts Directory
```bash
cd scripts/
python fetch_eoy_simple.py
python diagnostic/check_roster_completeness.py
```

## Session Documentation

Temporary documentation and session notes are stored in `docs/session-notes/`:
- `IMPLEMENTATION_SUMMARY.md` - Implementation progress notes
- `REGENERATION_STATUS.md` - Data regeneration status
- `MISSING_SOFTWARE_MEMBERS_ANALYSIS.md` - Analysis of missing software records

## Troubleshooting

### Scripts not running?
1. Verify Python 3.8+ is installed: `python --version`
2. Check `.env` file exists and is configured
3. Verify API credentials in `.env` are correct
4. Check script permissions: `chmod +x scripts/*.py scripts/diagnostic/*.py`

### API connection issues?
1. Verify `LATTICE_API_KEY` and `LATTICE_API_URL` in `.env`
2. Test connectivity: `curl $LATTICE_API_URL`
3. Check network access and firewall settings

### Missing data?
1. Run: `python scripts/diagnostic/verify_remaining_missing.py`
2. Check: `python scripts/diagnostic/find_missing_engineers.py`
3. Fetch missing data: `python scripts/diagnostic/fetch_missing_software.py`

## Dependencies

All scripts use Python 3.8+ standard library and the following packages:
- `requests` - API communication
- `python-dotenv` - Environment configuration
- `pandas` - Data analysis (for analyze_scores.py)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Adding New Scripts

When adding new scripts:
1. Place in `scripts/` for main scripts
2. Place in `scripts/diagnostic/` for diagnostic/utility scripts
3. Update this README with usage instructions
4. Follow existing code style and documentation patterns
5. Use `.env` for configuration (don't hardcode credentials)
