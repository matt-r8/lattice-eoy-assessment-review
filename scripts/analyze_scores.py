#!/usr/bin/env python3
"""
Analyze Platform/Cyber Assessment Score Distribution

Extracts peer average scores from markdown assessment files and calculates
comprehensive statistical distribution metrics.
"""

import argparse
import re
from pathlib import Path
from statistics import mean, median, stdev
from typing import List, Tuple


def extract_peer_scores(assessments_dir: Path) -> List[float]:
    """
    Extract peer average scores from all markdown files in the assessments directory.

    Args:
        assessments_dir: Path to directory containing assessment markdown files

    Returns:
        List of peer average scores (floats)
    """
    pattern = re.compile(r'- \*\*Peers Average\*\*: ([\d.]+)')
    scores = []

    # Find all markdown files
    md_files = sorted(assessments_dir.glob('*.md'))

    for file_path in md_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            match = pattern.search(content)
            if match:
                score = float(match.group(1))
                scores.append(score)
            else:
                print(f"Warning: No peer average found in {file_path.name}", flush=True)
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}", flush=True)

    return scores


def calculate_percentile(sorted_scores: List[float], percentile: int) -> float:
    """
    Calculate the specified percentile from sorted scores.

    Args:
        sorted_scores: List of scores sorted in ascending order
        percentile: Percentile to calculate (1-99)

    Returns:
        Score at the specified percentile
    """
    n = len(sorted_scores)
    if n == 0:
        return 0.0

    # Use nearest rank method
    rank = (percentile / 100.0) * n
    index = int(rank) - 1

    # Handle edge cases
    if index < 0:
        index = 0
    elif index >= n:
        index = n - 1

    return sorted_scores[index]


def count_distribution(scores: List[float]) -> List[Tuple[str, int, float]]:
    """
    Count scores in distribution buckets.

    Args:
        scores: List of all scores

    Returns:
        List of tuples: (bucket_label, count, percentage)
    """
    total = len(scores)
    if total == 0:
        return []

    buckets = [
        ("4.50-5.00", 4.50, 5.00),
        ("4.00-4.49", 4.00, 4.49),
        ("3.00-3.99", 3.00, 3.99),
        ("2.00-2.99", 2.00, 2.99),
        ("<2.00", 0.00, 1.99),
    ]

    results = []
    for label, min_score, max_score in buckets:
        count = sum(1 for s in scores if min_score <= s <= max_score)
        percentage = (count / total) * 100
        results.append((label, count, percentage))

    return results


def format_report(scores: List[float]) -> str:
    """
    Generate formatted report of score distribution analysis.

    Args:
        scores: List of all extracted scores

    Returns:
        Formatted report string
    """
    if not scores:
        return "ERROR: No scores found to analyze"

    # Sort scores for percentile calculations
    sorted_scores = sorted(scores)

    # Calculate basic statistics
    min_score = min(scores)
    max_score = max(scores)
    mean_score = mean(scores)
    median_score = median(scores)
    std_dev = stdev(scores) if len(scores) > 1 else 0.0

    # Calculate percentiles
    percentiles = {
        1: calculate_percentile(sorted_scores, 1),
        5: calculate_percentile(sorted_scores, 5),
        10: calculate_percentile(sorted_scores, 10),
        25: calculate_percentile(sorted_scores, 25),
        50: calculate_percentile(sorted_scores, 50),
        75: calculate_percentile(sorted_scores, 75),
        90: calculate_percentile(sorted_scores, 90),
        95: calculate_percentile(sorted_scores, 95),
        99: calculate_percentile(sorted_scores, 99),
    }

    # Calculate distribution
    distribution = count_distribution(scores)

    # Build report
    report = []
    report.append("=" * 60)
    report.append("PLATFORM/CYBER SCORE DISTRIBUTION ANALYSIS")
    report.append("=" * 60)
    report.append(f"Sample Size: {len(scores)}")
    report.append("")

    report.append("SCORE STATISTICS")
    report.append("-" * 60)
    report.append(f"  Min:    {min_score:.2f}")
    report.append(f"  Max:    {max_score:.2f}")
    report.append(f"  Mean:   {mean_score:.2f}")
    report.append(f"  Median: {median_score:.2f}")
    report.append(f"  StdDev: {std_dev:.2f}")
    report.append("")

    report.append("PERCENTILES")
    report.append("-" * 60)
    report.append(f"   1st: {percentiles[1]:.2f}  (Top 1%)")
    report.append(f"   5th: {percentiles[5]:.2f}  (Top 5%)")
    report.append(f"  10th: {percentiles[10]:.2f}  (Top 10%)")
    report.append(f"  25th: {percentiles[25]:.2f}  (Top 25%)")
    report.append(f"  50th: {percentiles[50]:.2f}  (Median)")
    report.append(f"  75th: {percentiles[75]:.2f}")
    report.append(f"  90th: {percentiles[90]:.2f}")
    report.append(f"  95th: {percentiles[95]:.2f}")
    report.append(f"  99th: {percentiles[99]:.2f}")
    report.append("")

    report.append("DISTRIBUTION BY SCORE RANGE")
    report.append("-" * 60)
    for bucket_label, count, percentage in distribution:
        # Format with right-aligned numbers for clean appearance
        report.append(f"  {bucket_label:>10}:  {count:>2} ({percentage:>5.1f}%)")
    report.append("")

    report.append("=" * 60)

    return "\n".join(report)


def main():
    """Main execution function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Analyze peer score distribution from assessment markdown files'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='assessments',
        help='Directory containing assessment markdown files (default: assessments)'
    )
    args = parser.parse_args()

    # Determine assessments directory path
    assessments_dir = Path(args.directory)

    # Handle relative paths from script location
    if not assessments_dir.is_absolute():
        script_dir = Path(__file__).parent
        assessments_dir = script_dir / assessments_dir

    # Verify directory exists
    if not assessments_dir.exists():
        print(f"ERROR: Assessments directory not found: {assessments_dir}")
        return 1

    if not assessments_dir.is_dir():
        print(f"ERROR: Path is not a directory: {assessments_dir}")
        return 1

    # Extract scores
    scores = extract_peer_scores(assessments_dir)

    # Generate and print report
    report = format_report(scores)
    print(report)

    return 0


if __name__ == '__main__':
    exit(main())
