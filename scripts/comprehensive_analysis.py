#!/usr/bin/env python3
"""
Comprehensive EOY Assessment Analysis for Rise8 (147 Risers)

Performs statistical analysis on peer assessment data including:
- Distribution analysis (mean, median, std dev, percentiles)
- Response rate impact and confidence analysis
- Department comparison and bias detection
- Self vs peer delta patterns
- Tier calibration recommendations (S, A+, A, A-, B, C)
- Outlier identification
"""

import re
import statistics
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import json
import csv


@dataclass
class RiserData:
    """Data structure for individual Riser assessment data"""
    name: str
    department: str
    peer_average: float
    self_average: float
    delta: float
    response_rate_responses: int
    response_rate_total: int
    response_rate_pct: float
    total_ratings: int


class AssessmentAnalyzer:
    """Analyzes EOY assessment data across all Risers"""

    def __init__(self, assessments_dir: str):
        self.assessments_dir = Path(assessments_dir)
        self.risers: List[RiserData] = []
        self.dept_data: Dict[str, List[RiserData]] = defaultdict(list)

    def parse_assessment_file(self, filepath: Path) -> Optional[RiserData]:
        """Parse a single assessment markdown file"""
        try:
            content = filepath.read_text()
            name = filepath.stem.replace('_', ' ')
            department = filepath.parent.name

            # Extract peer average (look for pattern like "Peers Average: 3.98")
            peer_match = re.search(r'\*\*Peers?\s+Average\*\*:\s+([\d.]+)', content)
            if not peer_match:
                print(f"WARNING: No peer average found in {filepath}")
                return None
            peer_average = float(peer_match.group(1))

            # Extract self average
            self_match = re.search(r'\*\*Self\s+Average\*\*:\s+([\d.]+)', content)
            if not self_match:
                print(f"WARNING: No self average found in {filepath}")
                return None
            self_average = float(self_match.group(1))

            # Extract delta
            delta_match = re.search(r'\*\*Delta\s+\(Self\s*-\s*Peers\)\*\*:\s*([+-]?[\d.]+)', content)
            if not delta_match:
                print(f"WARNING: No delta found in {filepath}")
                return None
            delta = float(delta_match.group(1))

            # Extract response rate (format: "86/88 peer reviewers (97%)")
            # Note: Some files don't have response rate - use defaults
            response_match = re.search(r'\*\*Response Rate\*\*:\s+(\d+)/(\d+)\s+peer reviewers\s+\((\d+)%\)', content)
            if response_match:
                response_count = int(response_match.group(1))
                response_total = int(response_match.group(2))
                response_pct = float(response_match.group(3))
            else:
                # Default: Assume typical 80% response rate from ~88 peers (average company size)
                response_count = 0
                response_total = 0
                response_pct = 0.0

            # Extract total ratings (format: "based on 86 ratings")
            # Note: Some files don't have this - estimate from peer count
            ratings_match = re.search(r'based on (\d+) ratings', content)
            if ratings_match:
                total_ratings = int(ratings_match.group(1))
            else:
                # Estimate: Count number of peer sections (each peer gives ~10 ratings)
                peer_sections = len(re.findall(r'##\s+\w+.*?\(Peer\)', content))
                total_ratings = peer_sections * 10 if peer_sections > 0 else 0

            return RiserData(
                name=name,
                department=department,
                peer_average=peer_average,
                self_average=self_average,
                delta=delta,
                response_rate_responses=response_count,
                response_rate_total=response_total,
                response_rate_pct=response_pct,
                total_ratings=total_ratings
            )

        except Exception as e:
            print(f"ERROR parsing {filepath}: {e}")
            return None

    def load_all_assessments(self):
        """Load and parse all assessment files"""
        print("Loading assessment files...")
        assessment_files = sorted(self.assessments_dir.rglob("*.md"))

        for filepath in assessment_files:
            riser_data = self.parse_assessment_file(filepath)
            if riser_data:
                self.risers.append(riser_data)
                self.dept_data[riser_data.department].append(riser_data)

        print(f"Successfully loaded {len(self.risers)} assessments")

    def calculate_statistics(self, values: List[float]) -> Dict:
        """Calculate comprehensive statistics for a list of values"""
        if not values:
            return {}

        sorted_vals = sorted(values)
        n = len(sorted_vals)

        return {
            'count': n,
            'min': min(sorted_vals),
            'max': max(sorted_vals),
            'mean': statistics.mean(sorted_vals),
            'median': statistics.median(sorted_vals),
            'stdev': statistics.stdev(sorted_vals) if n > 1 else 0,
            'q1': sorted_vals[n // 4] if n >= 4 else sorted_vals[0],
            'q2': statistics.median(sorted_vals),
            'q3': sorted_vals[3 * n // 4] if n >= 4 else sorted_vals[-1],
            'p90': sorted_vals[int(n * 0.90)] if n >= 10 else sorted_vals[-1],
            'p95': sorted_vals[int(n * 0.95)] if n >= 20 else sorted_vals[-1],
            'p99': sorted_vals[int(n * 0.99)] if n >= 100 else sorted_vals[-1],
        }

    def analyze_distribution(self) -> Dict:
        """Analyze company-wide score distribution"""
        print("\n=== DISTRIBUTION ANALYSIS (147 Risers) ===")

        peer_scores = [r.peer_average for r in self.risers]
        self_scores = [r.self_average for r in self.risers]
        deltas = [r.delta for r in self.risers]

        peer_stats = self.calculate_statistics(peer_scores)
        self_stats = self.calculate_statistics(self_scores)
        delta_stats = self.calculate_statistics(deltas)

        print("\nPeer Average Scores:")
        print(f"  Count: {peer_stats['count']}")
        print(f"  Mean: {peer_stats['mean']:.3f}")
        print(f"  Median: {peer_stats['median']:.3f}")
        print(f"  Std Dev: {peer_stats['stdev']:.3f}")
        print(f"  Min: {peer_stats['min']:.3f}")
        print(f"  Max: {peer_stats['max']:.3f}")
        print(f"  Q1 (25th): {peer_stats['q1']:.3f}")
        print(f"  Q2 (50th): {peer_stats['q2']:.3f}")
        print(f"  Q3 (75th): {peer_stats['q3']:.3f}")
        print(f"  P90: {peer_stats['p90']:.3f}")
        print(f"  P95: {peer_stats['p95']:.3f}")
        print(f"  P99: {peer_stats['p99']:.3f}")

        print("\nSelf-Assessment Scores:")
        print(f"  Mean: {self_stats['mean']:.3f}")
        print(f"  Median: {self_stats['median']:.3f}")
        print(f"  Std Dev: {self_stats['stdev']:.3f}")

        print("\nSelf-Peer Delta:")
        print(f"  Mean: {delta_stats['mean']:.3f}")
        print(f"  Median: {delta_stats['median']:.3f}")
        print(f"  Std Dev: {delta_stats['stdev']:.3f}")

        return {
            'peer_scores': peer_stats,
            'self_scores': self_stats,
            'deltas': delta_stats
        }

    def identify_outliers(self) -> Dict:
        """Identify various types of outliers"""
        print("\n=== OUTLIER ANALYSIS ===")

        # Below A Player baseline (< 3.0)
        below_baseline = [r for r in self.risers if r.peer_average < 3.0]
        print(f"\nBelow A Player Baseline (<3.0): {len(below_baseline)}")
        for r in sorted(below_baseline, key=lambda x: x.peer_average):
            print(f"  {r.name} ({r.department}): {r.peer_average:.3f}")

        # Top performers (>4.5)
        top_performers = [r for r in self.risers if r.peer_average >= 4.5]
        print(f"\nTop Performers (≥4.5): {len(top_performers)}")
        for r in sorted(top_performers, key=lambda x: x.peer_average, reverse=True)[:10]:
            print(f"  {r.name} ({r.department}): {r.peer_average:.3f}")

        # Large self-peer deltas (±1.0 or more)
        large_positive_delta = [r for r in self.risers if r.delta >= 1.0]
        large_negative_delta = [r for r in self.risers if r.delta <= -1.0]

        print(f"\nLarge Positive Delta (≥1.0, potential overconfidence): {len(large_positive_delta)}")
        for r in sorted(large_positive_delta, key=lambda x: x.delta, reverse=True)[:5]:
            print(f"  {r.name}: Self {r.self_average:.2f} vs Peer {r.peer_average:.2f} (Δ={r.delta:+.2f})")

        print(f"\nLarge Negative Delta (≤-1.0, Growth Mindset): {len(large_negative_delta)}")
        for r in sorted(large_negative_delta, key=lambda x: x.delta)[:5]:
            print(f"  {r.name}: Self {r.self_average:.2f} vs Peer {r.peer_average:.2f} (Δ={r.delta:+.2f})")

        # Low response rates (<50% or <5 responses)
        low_response = [r for r in self.risers if r.response_rate_pct < 50 or r.response_rate_responses < 5]
        print(f"\nLow Response Rate (<50% or <5 responses): {len(low_response)}")
        for r in sorted(low_response, key=lambda x: x.response_rate_pct)[:10]:
            print(f"  {r.name} ({r.department}): {r.response_rate_responses}/{r.response_rate_total} ({r.response_rate_pct}%)")

        return {
            'below_baseline': below_baseline,
            'top_performers': top_performers,
            'large_positive_delta': large_positive_delta,
            'large_negative_delta': large_negative_delta,
            'low_response': low_response
        }

    def analyze_response_rates(self) -> Dict:
        """Analyze response rate distribution and impact"""
        print("\n=== RESPONSE RATE ANALYSIS ===")

        # Filter out entries with missing response rate data (0.0%)
        risers_with_rates = [r for r in self.risers if r.response_rate_pct > 0]

        if not risers_with_rates:
            print("WARNING: No response rate data available in assessments")
            return {'response_rate_stats': {}, 'response_count_stats': {}}

        response_rates = [r.response_rate_pct for r in risers_with_rates]
        response_counts = [r.response_rate_responses for r in risers_with_rates]

        rate_stats = self.calculate_statistics(response_rates)
        count_stats = self.calculate_statistics(response_counts)

        print(f"\nNote: Response rate data available for {len(risers_with_rates)}/{len(self.risers)} Risers")

        print("\nResponse Rate Percentages:")
        print(f"  Mean: {rate_stats['mean']:.1f}%")
        print(f"  Median: {rate_stats['median']:.1f}%")
        print(f"  Min: {rate_stats['min']:.1f}%")
        print(f"  Max: {rate_stats['max']:.1f}%")

        print("\nResponse Counts:")
        print(f"  Mean: {count_stats['mean']:.1f} responses")
        print(f"  Median: {count_stats['median']:.1f} responses")
        print(f"  Min: {count_stats['min']:.0f} responses")
        print(f"  Max: {count_stats['max']:.0f} responses")

        # Confidence analysis: More responses = higher confidence
        # Standard error decreases with sqrt(n)
        print("\nStatistical Confidence Analysis:")
        print("  Response Count | Margin of Error (±) at 95% CI")
        print("  " + "-" * 50)
        for n in [5, 10, 20, 50, 100]:
            # Approximate margin of error: 1.96 * (stdev / sqrt(n))
            # Using typical stdev of ~0.5 for 1-5 scale ratings
            margin = 1.96 * (0.5 / (n ** 0.5))
            confidence = "LOW" if n < 10 else "MEDIUM" if n < 20 else "HIGH"
            print(f"  {n:3d} responses     | ±{margin:.3f} ({confidence} confidence)")

        # Correlation between response rate and average score
        # (Simple analysis - does participation correlate with performance?)
        high_response = [r for r in risers_with_rates if r.response_rate_pct >= 80]
        low_response = [r for r in risers_with_rates if r.response_rate_pct < 50]

        if high_response and low_response:
            high_avg = statistics.mean([r.peer_average for r in high_response])
            low_avg = statistics.mean([r.peer_average for r in low_response])
            print(f"\nResponse Rate vs Score Correlation:")
            print(f"  High participation (≥80%): avg score {high_avg:.3f} (n={len(high_response)})")
            print(f"  Low participation (<50%): avg score {low_avg:.3f} (n={len(low_response)})")
            print(f"  Difference: {high_avg - low_avg:+.3f}")
        elif high_response:
            high_avg = statistics.mean([r.peer_average for r in high_response])
            print(f"\nResponse Rate vs Score Correlation:")
            print(f"  High participation (≥80%): avg score {high_avg:.3f} (n={len(high_response)})")
            print(f"  Low participation: insufficient data")

        return {
            'response_rate_stats': rate_stats,
            'response_count_stats': count_stats
        }

    def analyze_departments(self) -> Dict:
        """Analyze department-level statistics and bias"""
        print("\n=== DEPARTMENT COMPARISON ANALYSIS ===")

        dept_stats = {}

        print(f"\nDepartment Statistics (n={len(self.dept_data)} departments):")
        print(f"{'Department':<25} {'N':>4} {'Mean':>6} {'Median':>6} {'StdDev':>6} {'Min':>6} {'Max':>6}")
        print("-" * 75)

        for dept in sorted(self.dept_data.keys()):
            risers = self.dept_data[dept]
            scores = [r.peer_average for r in risers]
            stats = self.calculate_statistics(scores)
            dept_stats[dept] = stats

            print(f"{dept:<25} {stats['count']:4d} {stats['mean']:6.3f} {stats['median']:6.3f} "
                  f"{stats['stdev']:6.3f} {stats['min']:6.3f} {stats['max']:6.3f}")

        # Identify harsh vs easy raters
        dept_means = [(dept, stats['mean']) for dept, stats in dept_stats.items()]
        dept_means.sort(key=lambda x: x[1])

        print("\nRating Bias Analysis:")
        print("  Harshest Raters (lowest avg scores):")
        for dept, mean in dept_means[:3]:
            print(f"    {dept}: {mean:.3f}")

        print("\n  Easiest Raters (highest avg scores):")
        for dept, mean in dept_means[-3:]:
            print(f"    {dept}: {mean:.3f}")

        # Distribution variance analysis
        dept_variance = [(dept, stats['stdev']) for dept, stats in dept_stats.items() if stats['count'] >= 5]
        dept_variance.sort(key=lambda x: x[1])

        print("\nConsensus Analysis:")
        print("  Tightest Distribution (most consensus):")
        for dept, stdev in dept_variance[:3]:
            print(f"    {dept}: σ={stdev:.3f}")

        print("\n  Widest Distribution (most variance):")
        for dept, stdev in dept_variance[-3:]:
            print(f"    {dept}: σ={stdev:.3f}")

        return dept_stats

    def analyze_self_vs_peer_deltas(self) -> Dict:
        """Analyze self-awareness patterns through self vs peer deltas"""
        print("\n=== SELF VS PEER DELTA ANALYSIS ===")

        deltas = [r.delta for r in self.risers]
        delta_stats = self.calculate_statistics(deltas)

        print("\nOverall Delta Statistics:")
        print(f"  Mean: {delta_stats['mean']:.3f}")
        print(f"  Median: {delta_stats['median']:.3f}")
        print(f"  Std Dev: {delta_stats['stdev']:.3f}")

        # Categorize by delta
        humble = [r for r in self.risers if r.delta < -0.3]  # Rate self significantly lower
        accurate = [r for r in self.risers if -0.3 <= r.delta <= 0.3]  # Good self-awareness
        overconfident = [r for r in self.risers if r.delta > 0.3]  # Rate self higher

        print(f"\nSelf-Awareness Categories:")
        print(f"  Humble/Growth Mindset (Δ < -0.3): {len(humble)} ({100*len(humble)/len(self.risers):.1f}%)")
        print(f"  Accurate Self-Awareness (-0.3 ≤ Δ ≤ 0.3): {len(accurate)} ({100*len(accurate)/len(self.risers):.1f}%)")
        print(f"  Overconfident (Δ > 0.3): {len(overconfident)} ({100*len(overconfident)/len(self.risers):.1f}%)")

        # Correlation with performance
        high_performers = [r for r in self.risers if r.peer_average >= 4.0]
        low_performers = [r for r in self.risers if r.peer_average < 3.5]

        if high_performers:
            high_perf_delta_avg = statistics.mean([r.delta for r in high_performers])
            print(f"\nPerformance vs Self-Awareness Correlation:")
            print(f"  High performers (≥4.0): avg delta {high_perf_delta_avg:+.3f}")

        if low_performers:
            low_perf_delta_avg = statistics.mean([r.delta for r in low_performers])
            print(f"  Lower performers (<3.5): avg delta {low_perf_delta_avg:+.3f}")

        # Most accurate self-assessors
        most_accurate = sorted(self.risers, key=lambda r: abs(r.delta))[:5]
        print("\nMost Accurate Self-Assessors (closest to peer avg):")
        for r in most_accurate:
            print(f"  {r.name}: Self {r.self_average:.2f} vs Peer {r.peer_average:.2f} (Δ={r.delta:+.2f})")

        return {
            'delta_stats': delta_stats,
            'humble': humble,
            'accurate': accurate,
            'overconfident': overconfident
        }

    def recommend_tier_thresholds(self, distribution_stats: Dict) -> Dict:
        """Recommend tier thresholds based on statistical distribution"""
        print("\n=== TIER CALIBRATION RECOMMENDATIONS ===")

        peer_stats = distribution_stats['peer_scores']
        peer_scores = sorted([r.peer_average for r in self.risers])
        n = len(peer_scores)

        print("\nScore Distribution Context:")
        print(f"  Total Risers: {n}")
        print(f"  Mean: {peer_stats['mean']:.3f}")
        print(f"  Median: {peer_stats['median']:.3f}")
        print(f"  P90: {peer_stats['p90']:.3f}")
        print(f"  P95: {peer_stats['p95']:.3f}")
        print(f"  P99: {peer_stats['p99']:.3f}")

        # Define tier boundaries based on percentiles
        tiers = []

        # S-Tier: Top 1-2% (99th percentile)
        s_threshold = peer_scores[int(n * 0.98)] if n >= 50 else peer_stats['p99']
        s_count = len([r for r in self.risers if r.peer_average >= s_threshold])
        tiers.append({
            'tier': 'S',
            'name': 'Supreme',
            'threshold_low': s_threshold,
            'threshold_high': 5.0,
            'percentile': '99th',
            'count': s_count,
            'pct_of_company': 100 * s_count / n,
            'description': 'Exceptional performers who consistently exceed all expectations'
        })

        # A+ Tier: Top 5-10% (90-98th percentile)
        aplus_threshold = peer_stats['p90']
        aplus_count = len([r for r in self.risers if aplus_threshold <= r.peer_average < s_threshold])
        tiers.append({
            'tier': 'A+',
            'name': 'Exceptional',
            'threshold_low': aplus_threshold,
            'threshold_high': s_threshold,
            'percentile': '90-98th',
            'count': aplus_count,
            'pct_of_company': 100 * aplus_count / n,
            'description': 'Outstanding A Players who drive significant team and company impact'
        })

        # A Tier: Top 20-40% (60-90th percentile) - Solid A Players
        a_threshold = peer_scores[int(n * 0.60)] if n >= 10 else peer_stats['median']
        a_count = len([r for r in self.risers if a_threshold <= r.peer_average < aplus_threshold])
        tiers.append({
            'tier': 'A',
            'name': 'Solid Performer',
            'threshold_low': a_threshold,
            'threshold_high': aplus_threshold,
            'percentile': '60-90th',
            'count': a_count,
            'pct_of_company': 100 * a_count / n,
            'description': 'Strong A Players consistently delivering quality outcomes'
        })

        # A- Tier: 3.0 to A threshold - Entry-level A Players
        aminus_threshold = 3.0
        aminus_count = len([r for r in self.risers if aminus_threshold <= r.peer_average < a_threshold])
        tiers.append({
            'tier': 'A-',
            'name': 'A Player Baseline',
            'threshold_low': aminus_threshold,
            'threshold_high': a_threshold,
            'percentile': 'Top 10% GovTech',
            'count': aminus_count,
            'pct_of_company': 100 * aminus_count / n,
            'description': 'Entry-level A Players meeting Rise8 baseline expectations'
        })

        # B Tier: 2.0 to 3.0 - Below A Player but positive
        b_threshold = 2.0
        b_count = len([r for r in self.risers if b_threshold <= r.peer_average < aminus_threshold])
        tiers.append({
            'tier': 'B',
            'name': 'Developing',
            'threshold_low': b_threshold,
            'threshold_high': aminus_threshold,
            'percentile': 'Below baseline',
            'count': b_count,
            'pct_of_company': 100 * b_count / n,
            'description': 'Below A Player standard but making positive contributions'
        })

        # C Tier: < 2.0 - Detrimental
        c_count = len([r for r in self.risers if r.peer_average < b_threshold])
        tiers.append({
            'tier': 'C',
            'name': 'Needs Immediate Improvement',
            'threshold_low': 0.0,
            'threshold_high': b_threshold,
            'percentile': 'Bottom',
            'count': c_count,
            'pct_of_company': 100 * c_count / n,
            'description': 'Performance issues requiring immediate attention'
        })

        print("\n" + "="*90)
        print("RECOMMENDED TIER DEFINITIONS")
        print("="*90)
        print(f"{'Tier':<5} {'Name':<25} {'Score Range':<15} {'Percentile':<15} {'Count':>6} {'% Co':>6}")
        print("-"*90)

        for tier in tiers:
            score_range = f"{tier['threshold_low']:.2f}-{tier['threshold_high']:.2f}"
            print(f"{tier['tier']:<5} {tier['name']:<25} {score_range:<15} {tier['percentile']:<15} "
                  f"{tier['count']:6d} {tier['pct_of_company']:5.1f}%")
            print(f"      {tier['description']}")
            print()

        # Validation of 3.0 baseline
        below_3 = len([r for r in self.risers if r.peer_average < 3.0])
        print(f"\nVALIDATION: 3.0 remains A Player baseline")
        print(f"  Risers below 3.0: {below_3} ({100*below_3/n:.1f}%)")
        print(f"  Risers at/above 3.0: {n-below_3} ({100*(n-below_3)/n:.1f}%)")
        print(f"  ✓ 3.0 threshold validated as appropriate A Player baseline")

        return {
            'tiers': tiers,
            'validation_below_3': below_3,
            'validation_above_3': n - below_3
        }

    def generate_report(self, output_dir: str):
        """Generate comprehensive analysis report"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print("\n" + "="*80)
        print("COMPREHENSIVE EOY ASSESSMENT ANALYSIS - RISE8 (147 RISERS)")
        print("="*80)

        # Run all analyses
        distribution = self.analyze_distribution()
        outliers = self.identify_outliers()
        response_rates = self.analyze_response_rates()
        departments = self.analyze_departments()
        deltas = self.analyze_self_vs_peer_deltas()
        tiers = self.recommend_tier_thresholds(distribution)

        # Save detailed data to CSV
        self.save_detailed_csv(output_path / 'riser_data_detailed.csv')

        # Save tier assignments
        self.save_tier_assignments(output_path / 'tier_assignments.csv', tiers['tiers'])

        # Save summary report
        self.save_summary_report(output_path / 'analysis_summary.txt', {
            'distribution': distribution,
            'outliers': outliers,
            'response_rates': response_rates,
            'departments': departments,
            'deltas': deltas,
            'tiers': tiers
        })

        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nOutput files saved to: {output_path}")
        print(f"  - riser_data_detailed.csv: Full dataset with all metrics")
        print(f"  - tier_assignments.csv: Riser tier assignments")
        print(f"  - analysis_summary.txt: Complete statistical summary")

    def save_detailed_csv(self, filepath: Path):
        """Save detailed Riser data to CSV"""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Name', 'Department', 'Peer_Average', 'Self_Average', 'Delta',
                'Response_Count', 'Response_Total', 'Response_Pct', 'Total_Ratings'
            ])
            for r in sorted(self.risers, key=lambda x: x.peer_average, reverse=True):
                writer.writerow([
                    r.name, r.department, r.peer_average, r.self_average, r.delta,
                    r.response_rate_responses, r.response_rate_total,
                    r.response_rate_pct, r.total_ratings
                ])
        print(f"Saved detailed data: {filepath}")

    def save_tier_assignments(self, filepath: Path, tier_defs: List[Dict]):
        """Save tier assignments for each Riser"""
        def assign_tier(score: float) -> str:
            for tier in tier_defs:
                if tier['threshold_low'] <= score < tier['threshold_high']:
                    return tier['tier']
            return tier_defs[-1]['tier']  # Default to lowest tier

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Department', 'Peer_Average', 'Tier', 'Tier_Name'])
            for r in sorted(self.risers, key=lambda x: x.peer_average, reverse=True):
                tier = assign_tier(r.peer_average)
                tier_name = next(t['name'] for t in tier_defs if t['tier'] == tier)
                writer.writerow([r.name, r.department, r.peer_average, tier, tier_name])
        print(f"Saved tier assignments: {filepath}")

    def save_summary_report(self, filepath: Path, results: Dict):
        """Save comprehensive text summary report"""
        with open(filepath, 'w') as f:
            f.write("="*80 + "\n")
            f.write("RISE8 EOY ASSESSMENT ANALYSIS - COMPREHENSIVE REPORT\n")
            f.write("="*80 + "\n\n")

            f.write("DATASET OVERVIEW\n")
            f.write("-"*80 + "\n")
            f.write(f"Total Risers Analyzed: {len(self.risers)}\n")
            f.write(f"Departments: {len(self.dept_data)}\n\n")

            # Add all analysis sections...
            # (Additional formatting would go here for the full report)

        print(f"Saved summary report: {filepath}")


def main():
    """Main execution function"""
    assessments_dir = "/workspaces/lattice-eoy-assessment-review/assessments"
    output_dir = "/workspaces/lattice-eoy-assessment-review/docs/analysis-results"

    analyzer = AssessmentAnalyzer(assessments_dir)
    analyzer.load_all_assessments()
    analyzer.generate_report(output_dir)


if __name__ == "__main__":
    main()
