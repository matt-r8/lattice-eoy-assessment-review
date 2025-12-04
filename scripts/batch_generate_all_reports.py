#!/usr/bin/env python3
"""
Batch Generate All EOY Assessment Reports with Parallel Processing

This script generates synthesized assessment reports for all 147 employees with:
- Parallel processing (configurable workers)
- Progress tracking with time estimates
- Error handling and resume capability
- Comprehensive logging and reporting

Usage:
    python scripts/batch_generate_all_reports.py                    # 4 parallel workers (default)
    python scripts/batch_generate_all_reports.py --parallel 8       # 8 parallel workers
    python scripts/batch_generate_all_reports.py --resume           # Skip completed reports
    python scripts/batch_generate_all_reports.py --dry-run          # Show what would be generated
    python scripts/batch_generate_all_reports.py --verbose          # Verbose output

Author: Rise8 Data Science Team
Version: 1.0.0
"""

import json
import subprocess
import sys
import time
import argparse
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


class BatchReportGenerator:
    """Batch generate all EOY assessment reports with parallel processing"""

    VERSION = "1.0.0"
    MAX_WORKERS = 8

    def __init__(
        self,
        base_dir: str,
        parallel: int = 4,
        resume: bool = False,
        dry_run: bool = False,
        verbose: bool = False
    ):
        self.base_dir = Path(base_dir)
        self.parallel = min(parallel, self.MAX_WORKERS)
        self.resume = resume
        self.dry_run = dry_run
        self.verbose = verbose

        # File paths
        self.team_map_file = self.base_dir / "LatticeAPI" / "lattice_api_client" / "team_map.json"
        self.assessments_dir = self.base_dir / "assessments"
        self.progress_file = self.base_dir / "batch_generation_progress.json"
        self.failures_log = self.base_dir / "batch_generation_failures.log"
        self.generator_script = self.base_dir / "scripts" / "generate_individual_report.py"

        # State tracking
        self.start_time = None
        self.completed_count = 0
        self.failed_count = 0
        self.total_count = 0

    def log(self, message: str):
        """Log message if verbose mode enabled"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {message}")

    def load_employee_list(self) -> List[str]:
        """
        Load employee names from team_map.json.
        Returns list of "First Last" format names.
        """
        self.log(f"Loading employee list from {self.team_map_file}")

        with open(self.team_map_file, 'r') as f:
            team_map = json.load(f)

        employees = []
        for name_key in team_map.keys():
            # Normalize from "Last, First" to "First Last"
            if ", " in name_key:
                parts = name_key.split(", ", 1)
                normalized_name = f"{parts[1]} {parts[0]}"
            else:
                normalized_name = name_key
            employees.append(normalized_name)

        self.log(f"Loaded {len(employees)} employees")
        return sorted(employees)

    def check_report_exists(self, name: str) -> bool:
        """
        Check if synthesized report already exists for this employee.
        Expected format: assessments/[Department]/[Last], [First] - Synthesized Report.md
        """
        # Convert "First Last" to "Last, First" format
        name_parts = name.split()
        if len(name_parts) >= 2:
            first_name = " ".join(name_parts[:-1])
            last_name = name_parts[-1]
            report_filename = f"{last_name}, {first_name} - Synthesized Report.md"
        else:
            report_filename = f"{name} - Synthesized Report.md"

        # Search in all department directories
        for dept_dir in self.assessments_dir.iterdir():
            if dept_dir.is_dir():
                report_path = dept_dir / report_filename
                if report_path.exists():
                    return True

        return False

    def filter_employees(self, employees: List[str]) -> Tuple[List[str], List[str]]:
        """
        Filter employee list to find pending and completed reports.
        Returns: (pending_employees, completed_employees)
        """
        self.log("Filtering employee list for completed reports")

        pending = []
        completed = []

        for name in employees:
            if self.check_report_exists(name):
                completed.append(name)
            else:
                pending.append(name)

        self.log(f"Found {len(completed)} completed, {len(pending)} pending")
        return pending, completed

    def generate_single_report(self, name: str) -> Dict:
        """
        Generate report for a single employee by invoking generate_individual_report.py.
        Returns dict with success status, timing, and error info.
        """
        start_time = time.time()
        result = {
            'name': name,
            'success': False,
            'duration': 0.0,
            'error': None
        }

        try:
            # Invoke the existing generator script
            cmd = [
                sys.executable,  # Use same Python interpreter
                str(self.generator_script),
                name
            ]

            # Run subprocess with timeout (5 minutes max per employee)
            process = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            result['duration'] = time.time() - start_time

            if process.returncode == 0:
                result['success'] = True
            else:
                result['error'] = f"Exit code {process.returncode}: {process.stderr[:200]}"

        except subprocess.TimeoutExpired:
            result['duration'] = time.time() - start_time
            result['error'] = "Timeout (>5 minutes)"
        except Exception as e:
            result['duration'] = time.time() - start_time
            result['error'] = str(e)[:200]

        return result

    def save_progress(self, completed: List[str], failed: List[Dict]):
        """Save progress state to JSON file"""
        progress_data = {
            'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'completed_count': len(completed),
            'failed_count': len(failed),
            'completed_employees': completed,
            'failed_employees': failed
        }

        with open(self.progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)

    def log_failure(self, name: str, error: str):
        """Log failure to failures log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.failures_log, 'a') as f:
            f.write(f"[{timestamp}] {name}: {error}\n")

    def format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human-readable format"""
        td = timedelta(seconds=int(seconds))
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return f"{int(seconds)}s"

    def estimate_remaining_time(self, completed: int, total: int, elapsed: float) -> str:
        """Estimate remaining time based on current progress"""
        if completed == 0:
            return "calculating..."

        avg_time_per_report = elapsed / completed
        remaining_reports = total - completed
        estimated_seconds = avg_time_per_report * remaining_reports

        return self.format_duration(estimated_seconds)

    def print_progress(self, current: int, total: int, name: str, elapsed: float):
        """Print progress update"""
        pct = (current / total * 100) if total > 0 else 0
        remaining = self.estimate_remaining_time(current, total, elapsed)
        elapsed_str = self.format_duration(elapsed)

        print(f"\r[{current}/{total}] ({pct:.1f}%) | Elapsed: {elapsed_str} | Est. remaining: {remaining} | Current: {name[:40]:<40}", end='', flush=True)

    def run_batch(self, employees: List[str]) -> Tuple[List[str], List[Dict]]:
        """
        Run batch generation with parallel processing.
        Returns: (completed_employees, failed_employees)
        """
        self.total_count = len(employees)
        self.start_time = time.time()

        completed = []
        failed = []

        print(f"\nStarting batch generation:")
        print(f"  Total employees: {self.total_count}")
        print(f"  Parallel workers: {self.parallel}")
        print(f"  Dry run: {self.dry_run}")
        print()

        if self.dry_run:
            print("DRY RUN MODE - No reports will be generated\n")
            for i, name in enumerate(employees, 1):
                print(f"  [{i}/{len(employees)}] Would generate: {name}")
            return [], []

        # Submit all jobs to executor
        with ProcessPoolExecutor(max_workers=self.parallel) as executor:
            # Submit all jobs
            future_to_name = {
                executor.submit(self.generate_single_report, name): name
                for name in employees
            }

            # Process results as they complete
            for future in as_completed(future_to_name):
                name = future_to_name[future]

                try:
                    result = future.result()
                    elapsed = time.time() - self.start_time

                    if result['success']:
                        completed.append(name)
                        self.completed_count += 1
                    else:
                        failed.append({
                            'name': name,
                            'error': result['error'],
                            'duration': result['duration']
                        })
                        self.failed_count += 1
                        self.log_failure(name, result['error'])

                    # Print progress
                    current = len(completed) + len(failed)
                    self.print_progress(current, self.total_count, name, elapsed)

                    # Save progress every 10 reports
                    if current % 10 == 0:
                        self.save_progress(completed, failed)

                except Exception as e:
                    self.log(f"Unexpected error processing {name}: {e}")
                    failed.append({
                        'name': name,
                        'error': f"Unexpected error: {str(e)[:200]}",
                        'duration': 0
                    })
                    self.failed_count += 1

        print()  # New line after progress bar

        # Save final progress
        self.save_progress(completed, failed)

        return completed, failed

    def print_summary(self, pending: List[str], completed: List[str], failed: List[Dict]):
        """Print final summary report"""
        total_time = time.time() - self.start_time if self.start_time else 0
        total_attempted = len(completed) + len(failed)

        print("\n" + "=" * 80)
        print("Batch Generation Complete!")
        print("=" * 80)

        if total_attempted > 0:
            success_pct = len(completed) / total_attempted * 100
            failed_pct = len(failed) / total_attempted * 100
            print(f"✓ Successfully generated: {len(completed)}/{total_attempted} ({success_pct:.1f}%)")
            print(f"✗ Failed: {len(failed)}/{total_attempted} ({failed_pct:.1f}%)")
        else:
            print(f"✓ Successfully generated: {len(completed)}/{total_attempted}")
            print(f"✗ Failed: {len(failed)}/{total_attempted}")

        print(f"⏱  Total time: {self.format_duration(total_time)}")

        if total_attempted > 0:
            avg_time = total_time / total_attempted
            print(f"📊 Average time per report: {self.format_duration(avg_time)}")

        if failed:
            print(f"\n❌ Failed employees ({len(failed)}):")
            for failure in failed[:20]:  # Show first 20
                error_short = failure['error'][:60] if failure['error'] else "Unknown error"
                print(f"  - {failure['name']}: {error_short}")

            if len(failed) > 20:
                print(f"  ... and {len(failed) - 20} more (see {self.failures_log})")

            print(f"\nFull failure log: {self.failures_log}")

        print(f"\nProgress state saved to: {self.progress_file}")
        print("=" * 80 + "\n")

    def run(self):
        """Main execution flow"""
        try:
            # Load employee list
            all_employees = self.load_employee_list()

            # Filter for pending/completed
            pending, already_completed = self.filter_employees(all_employees)

            print("\n" + "=" * 80)
            print(f"Batch Report Generation - v{self.VERSION}")
            print("=" * 80)
            print(f"Total employees: {len(all_employees)}")
            print(f"Already completed: {len(already_completed)}")
            print(f"Pending generation: {len(pending)}")
            print("=" * 80)

            if not pending:
                print("\n✓ All reports already generated! Nothing to do.\n")
                return 0

            # Determine which employees to process
            if self.resume:
                employees_to_process = pending
                print(f"\n▶ Resume mode: Processing {len(pending)} pending reports")
            else:
                employees_to_process = pending
                print(f"\n▶ Processing {len(pending)} pending reports")

            # Run batch generation
            completed, failed = self.run_batch(employees_to_process)

            # Print summary
            self.print_summary(pending, completed, failed)

            # Return exit code
            return 0 if len(failed) == 0 else 1

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user (Ctrl+C)")
            print(f"Progress saved to: {self.progress_file}")
            print("Run with --resume to continue from where you left off.\n")
            return 130
        except Exception as e:
            print(f"\n✗ Fatal error: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate all EOY assessment reports with parallel processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Generate all pending reports (4 workers)
  %(prog)s --parallel 8        # Use 8 parallel workers
  %(prog)s --resume            # Resume after interruption
  %(prog)s --dry-run           # Show what would be generated
  %(prog)s --verbose           # Verbose output
        """
    )

    parser.add_argument(
        "--parallel",
        type=int,
        default=4,
        metavar="N",
        help=f"Number of parallel workers (default: 4, max: {BatchReportGenerator.MAX_WORKERS})"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip already-completed reports (always enabled by default)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without actually generating"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Base directory of project (default: current directory)"
    )

    args = parser.parse_args()

    # Validate parallel workers
    if args.parallel < 1 or args.parallel > BatchReportGenerator.MAX_WORKERS:
        print(f"Error: --parallel must be between 1 and {BatchReportGenerator.MAX_WORKERS}")
        return 1

    # Create generator and run
    generator = BatchReportGenerator(
        base_dir=args.base_dir,
        parallel=args.parallel,
        resume=True,  # Always resume by default (skip completed reports)
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    return generator.run()


if __name__ == "__main__":
    sys.exit(main())
