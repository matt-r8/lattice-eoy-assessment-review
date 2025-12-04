# Batch Report Generation Guide

## Overview

The `batch_generate_all_reports.py` script generates synthesized assessment reports for all 146 Rise8 employees in parallel, with production-ready features for unattended operation.

**Current Status:**
- **Total Employees:** 146
- **Already Completed:** 9 reports
- **Pending Generation:** 137 reports
- **Estimated Time:** 5-7 hours (4 workers) or 3-4 hours (8 workers)

## Quick Start

### Basic Usage

```bash
# Generate all pending reports with default settings (4 workers)
python scripts/batch_generate_all_reports.py
```

This will:
- Skip the 9 already-completed reports automatically
- Generate 137 pending reports using 4 parallel workers
- Show real-time progress with time estimates
- Save progress state every 10 reports
- Log failures to `batch_generation_failures.log`
- Complete in approximately 5-7 hours

### Recommended Production Run

```bash
# Use 8 workers for faster execution
python scripts/batch_generate_all_reports.py --parallel 8 --verbose
```

Expected completion: **3-4 hours** for all 137 reports

## Command Reference

### Basic Commands

```bash
# Default execution (4 workers)
python scripts/batch_generate_all_reports.py

# Faster execution (8 workers)
python scripts/batch_generate_all_reports.py --parallel 8

# Check what would be generated
python scripts/batch_generate_all_reports.py --dry-run

# Verbose logging
python scripts/batch_generate_all_reports.py --verbose
```

### Resume After Interruption

If the script is interrupted (Ctrl+C, network issue, system restart):

```bash
# Resume from where it left off
python scripts/batch_generate_all_reports.py --resume
```

The script **always skips completed reports**, so this is safe to run multiple times.

## Features

### 1. Parallel Processing

- **Default:** 4 parallel workers
- **Maximum:** 8 parallel workers
- **Configurable:** `--parallel N` (1-8)

Each worker processes one employee at a time, invoking the `generate_individual_report.py` script as a subprocess.

### 2. Progress Tracking

Real-time progress display:
```
[45/137] (32.8%) | Elapsed: 1h 23m | Est. remaining: 4h 12m | Current: Chris Brodowski
```

Shows:
- Current/total count and percentage
- Elapsed time
- Estimated remaining time (based on average)
- Current employee being processed

### 3. Error Handling

**Automatic Failure Logging:**
- All failures logged to `batch_generation_failures.log`
- Includes timestamp, employee name, and error details
- Processing continues for other employees

**Timeout Protection:**
- 5-minute timeout per employee
- Prevents hung processes from blocking progress

**Progress State:**
- State saved to `batch_generation_progress.json` every 10 reports
- Enables resume capability
- Tracks completed and failed employees

### 4. Resume Capability

The script tracks:
- ✅ Completed reports (synthesized report exists)
- ❌ Failed reports (logged with errors)
- ⏸️ Pending reports (not yet attempted)

Running with `--resume` (or just re-running) automatically skips completed reports.

### 5. Interruption Handling

**Graceful Ctrl+C:**
```
⚠️  Interrupted by user (Ctrl+C)
Progress saved to: batch_generation_progress.json
Run with --resume to continue from where you left off.
```

**Safe to interrupt:**
- In-flight reports will fail gracefully
- Completed reports are already saved
- Progress state is saved
- No data corruption

## Output Files

### Generated Reports

Each employee gets a synthesized report:
```
assessments/[Department]/[Last], [First] - Synthesized Report.md
```

Example:
```
assessments/Platform-Cyber/Pacione, Matt - Synthesized Report.md
```

### Progress Tracking Files

**`batch_generation_progress.json`**
```json
{
  "last_update": "2025-12-04 14:30:22",
  "completed_count": 45,
  "failed_count": 2,
  "completed_employees": ["Matt Pacione", "Adam Gardner", ...],
  "failed_employees": [
    {"name": "John Doe", "error": "timeout", "duration": 300.0}
  ]
}
```

**`batch_generation_failures.log`**
```
[2025-12-04 14:25:10] John Doe: Timeout (>5 minutes)
[2025-12-04 14:30:15] Jane Smith: Exit code 1: Missing assessment file
```

## Performance

### Timing Estimates

| Workers | Time per Report | Total Time (137 reports) |
|---------|----------------|-------------------------|
| 1       | 2-3 min        | 4.5-6.8 hours          |
| 4       | 2-3 min        | 1.1-1.7 hours          |
| 8       | 2-3 min        | 0.6-0.8 hours          |

**Actual times include:**
- Report parsing and calculation
- 3 AI synthesis calls per report (via rise8-assessment-reviewer agent)
- File I/O and progress tracking

**Recommended:** Use 8 workers for production runs (fastest completion).

### System Resources

**CPU:**
- Each worker uses ~10-20% CPU during AI synthesis
- 8 workers ≈ 80-160% total CPU (multi-core recommended)

**Memory:**
- Each worker uses ~50-100 MB
- 8 workers ≈ 400-800 MB total

**Network:**
- AI synthesis calls to API (if external)
- Minimal bandwidth requirements

## Monitoring Progress

### Real-Time Progress

Watch the progress bar during execution:
```
[45/137] (32.8%) | Elapsed: 1h 23m | Est. remaining: 4h 12m | Current: Chris Brodowski
```

### Check Progress State

```bash
# View progress JSON
cat batch_generation_progress.json

# Count completed reports
ls -1 assessments/**/*Synthesized\ Report.md | wc -l

# Check failures
cat batch_generation_failures.log
```

### Verbose Logging

Add `--verbose` flag for detailed logging:
```bash
python scripts/batch_generate_all_reports.py --parallel 8 --verbose
```

Output includes:
- Employee list loading
- Report existence checks
- Per-employee processing details
- Error details

## Final Summary

After completion, you'll see:

```
================================================================================
Batch Generation Complete!
================================================================================
✓ Successfully generated: 135/137 (98.5%)
✗ Failed: 2/137 (1.5%)
⏱  Total time: 3h 47m
📊 Average time per report: 1m 39s

❌ Failed employees (2):
  - John Doe: Timeout (>5 minutes)
  - Jane Smith: Exit code 1: Missing assessment file

Full failure log: batch_generation_failures.log
Progress state saved to: batch_generation_progress.json
================================================================================
```

## Troubleshooting

### Issue: Script fails immediately

**Check:**
```bash
# Verify Python version (3.8+ required)
python3 --version

# Verify generator script exists
ls -la scripts/generate_individual_report.py

# Verify team map exists
ls -la LatticeAPI/lattice_api_client/team_map.json
```

### Issue: Some reports fail

**Check failures log:**
```bash
cat batch_generation_failures.log
```

**Common errors:**
- **Timeout (>5 minutes):** Employee assessment file may be malformed or AI synthesis hanging
- **Missing assessment file:** Employee not in assessments directory
- **Exit code 1:** Generator script error (check with `--verbose`)

**Fix individual failures:**
```bash
# Regenerate specific employee
python scripts/generate_individual_report.py "Employee Name" -v
```

### Issue: Progress seems slow

**Check:**
- AI synthesis calls may be rate-limited
- Network latency to AI API
- System resource constraints

**Optimize:**
- Reduce workers: `--parallel 4` (less contention)
- Check system resources: `top`, `htop`
- Monitor network: AI API response times

### Issue: Need to restart

**Safe to restart anytime:**
```bash
# Kill with Ctrl+C
# Then restart - completed reports are automatically skipped
python scripts/batch_generate_all_reports.py --parallel 8
```

## Production Checklist

Before running the full batch:

- [ ] Verify 9 reports already completed: `ls assessments/**/*Synthesized\ Report.md | wc -l`
- [ ] Run dry-run to see pending list: `python scripts/batch_generate_all_reports.py --dry-run`
- [ ] Test with 1-2 employees first (modify list temporarily if needed)
- [ ] Ensure adequate disk space: `df -h .`
- [ ] Check system resources: `top` or `htop`
- [ ] Plan for 3-4 hours runtime (with 8 workers)
- [ ] Run in screen/tmux for remote sessions: `screen -S batch_reports`

## Running in Background

### Using screen (recommended for remote sessions)

```bash
# Start screen session
screen -S batch_reports

# Run batch generation
python scripts/batch_generate_all_reports.py --parallel 8 --verbose

# Detach: Ctrl+A then D

# Reattach later
screen -r batch_reports
```

### Using tmux

```bash
# Start tmux session
tmux new -s batch_reports

# Run batch generation
python scripts/batch_generate_all_reports.py --parallel 8 --verbose

# Detach: Ctrl+B then D

# Reattach later
tmux attach -t batch_reports
```

### Using nohup

```bash
# Run in background with output logging
nohup python scripts/batch_generate_all_reports.py --parallel 8 --verbose > batch_output.log 2>&1 &

# Check progress
tail -f batch_output.log

# Or check progress file
cat batch_generation_progress.json
```

## Next Steps

After batch generation completes:

1. **Verify completion:**
   ```bash
   ls -1 assessments/**/*Synthesized\ Report.md | wc -l
   # Should show 146 (or 137 new + 9 existing)
   ```

2. **Check failures:**
   ```bash
   cat batch_generation_failures.log
   ```

3. **Regenerate failures individually:**
   ```bash
   python scripts/generate_individual_report.py "Failed Employee Name" -v
   ```

4. **Quality check sample reports:**
   ```bash
   # Check a few reports for completeness
   head -100 assessments/Platform-Cyber/Pacione,\ Matt\ -\ Synthesized\ Report.md
   ```

5. **AI synthesis (if needed):**
   - Reports contain placeholders for AI synthesis
   - Invoke `rise8-assessment-reviewer` agent for qualitative sections
   - See individual report template for synthesis sections

## Support

For issues or questions:
- Check `batch_generation_failures.log` for errors
- Run with `--verbose` for detailed logging
- Test single employee: `python scripts/generate_individual_report.py "Name" -v`
- Review scripts/README.md for troubleshooting guide
