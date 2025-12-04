#!/usr/bin/env python3
"""
Reviewer Quality Analysis Script

Analyzes reviewer patterns across all EOY assessments to identify:
- Firewall 5s (reviewers giving 90%+ scores as 5.0)
- Low-effort reviewers (minimal feedback, low variance)
- High-quality reviewers (detailed feedback, good differentiation)
- Score distribution patterns

Author: Data Science Agent
Date: 2025-12-04
"""

import os
import re
import statistics
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple


@dataclass
class ReviewerProfile:
    """Profile of a reviewer's patterns across all their reviews"""
    name: str
    reviews_written: int = 0
    scores_given: List[float] = field(default_factory=list)
    text_feedback: List[str] = field(default_factory=list)
    reviewees: List[str] = field(default_factory=list)

    @property
    def firewall_5_percentage(self) -> float:
        """Calculate percentage of 5.0 scores given"""
        if not self.scores_given:
            return 0.0
        return (sum(1 for s in self.scores_given if s == 5.0) / len(self.scores_given)) * 100

    @property
    def avg_words_per_review(self) -> float:
        """Calculate average words per review (Q11 + Q12 combined text feedback)"""
        if not self.text_feedback:
            return 0.0
        word_counts = [len(text.split()) for text in self.text_feedback]
        return statistics.mean(word_counts)

    @property
    def score_std_dev(self) -> float:
        """Calculate standard deviation of scores"""
        if len(self.scores_given) < 2:
            return 0.0
        return statistics.stdev(self.scores_given)

    @property
    def score_mean(self) -> float:
        """Calculate mean of scores given"""
        if not self.scores_given:
            return 0.0
        return statistics.mean(self.scores_given)

    @property
    def quality_score(self) -> float:
        """Calculate composite quality score (0-100)"""
        # Factors:
        # - High words per review (30 points)
        # - Good score differentiation (30 points)
        # - Review volume (20 points)
        # - Not firewall 5 (20 points)

        score = 0.0

        # Words per review score (0-30): 150+ words per review = full points
        word_score = min(30, (self.avg_words_per_review / 150) * 30)
        score += word_score

        # Score differentiation (0-30): std dev > 1.0 = full points
        diff_score = min(30, (self.score_std_dev / 1.0) * 30)
        score += diff_score

        # Review volume (0-20): 8+ reviews = full points
        volume_score = min(20, (self.reviews_written / 8) * 20)
        score += volume_score

        # Not firewall 5 (0-20): < 90% = full points
        if self.firewall_5_percentage < 90:
            score += 20
        else:
            score += 20 * (1 - (self.firewall_5_percentage - 90) / 10)

        return score

    def score_distribution(self) -> Dict[float, int]:
        """Get distribution of scores given"""
        dist = defaultdict(int)
        for score in self.scores_given:
            dist[score] += 1
        return dict(sorted(dist.items()))


def extract_reviewer_name(header: str) -> str:
    """Extract reviewer name from peer review header"""
    # Pattern: ## Name (Peer) or ## First Last (Peer)
    match = re.search(r'^##\s+(.+?)\s+\(Peer\)', header.strip())
    if match:
        return match.group(1).strip()
    return ""


def extract_score(line: str) -> float:
    """Extract numeric score from rating line"""
    # Look for patterns like "Rating**: 4 - Team Leader" or "Rating**: 5.0"
    # Also handle "6 - Haven't had the opportunity to observe"

    match = re.search(r'\*\*Rating\*\*:\s+(\d+(?:\.\d+)?)', line)
    if match:
        score = float(match.group(1))
        # Filter out 6 (Haven't had opportunity to observe)
        if score == 6.0:
            return None
        return score
    return None


def extract_text_feedback(text: str) -> str:
    """Extract text from comment blocks"""
    # Remove markdown formatting and get clean text
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)  # Remove quote markers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'###+\s*', '', text)  # Remove headers
    text = re.sub(r'\n\s*\n', '\n', text)  # Collapse multiple newlines
    return text.strip()


def parse_assessment_file(file_path: Path) -> Dict[str, List[Tuple[float, List[str]]]]:
    """
    Parse an assessment file and extract peer reviews

    Returns:
        Dict mapping reviewer_name -> [(scores_list, text_feedback_list)]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract reviewee name from filename or header
    reviewee_match = re.search(r'^#\s+(.+?)\s+-\s+2025 EOY', content, re.MULTILINE)
    reviewee_name = reviewee_match.group(1).strip() if reviewee_match else file_path.stem

    peer_reviews = {}

    # Split by peer review sections
    sections = re.split(r'^## (.+?) \(Peer\)\s*$', content, flags=re.MULTILINE)

    # sections[0] is content before first peer review (self-assessment)
    # sections[1:] alternate between reviewer name and review content

    for i in range(1, len(sections), 2):
        if i + 1 >= len(sections):
            break

        reviewer_name = sections[i].strip()
        review_content = sections[i + 1]

        # Extract all scores from questions 1-11
        scores = []
        score_pattern = r'\*\*Rating\*\*:\s+(\d+(?:\.\d+)?)'

        for match in re.finditer(score_pattern, review_content):
            score = float(match.group(1))
            # Filter out 6 (Haven't had opportunity to observe)
            if score != 6.0:
                scores.append(score)

        # Extract text feedback from questions 11 and 12
        text_feedback = []

        # Question 11 comment (rehire question)
        # Fixed: Capture all text from Comment: until next Question or Peer section
        # Use \n## (with space) to match peer review headers like "## Name (Peer)"
        q11_match = re.search(
            r'### Question 11.*?\*\*Comment\*\*:\s*\n(.*?)(?=\n### Question|\n## )',
            review_content,
            re.DOTALL | re.MULTILINE
        )
        if q11_match:
            text_feedback.append(extract_text_feedback(q11_match.group(1)))

        # Question 12 comment (START/STOP/KEEP)
        # Fixed: Capture all text from Comment: until next Peer section or end of string
        # Q12 is last question, so use \n## or end-of-string (\Z) as boundary
        q12_match = re.search(
            r'### Question 12.*?\*\*Comment\*\*:\s*\n(.*?)(?=\n## |\Z)',
            review_content,
            re.DOTALL | re.MULTILINE
        )
        if q12_match:
            text_feedback.append(extract_text_feedback(q12_match.group(1)))

        if reviewer_name and scores:  # Only add if we have valid data
            peer_reviews[reviewer_name] = (scores, text_feedback, reviewee_name)

    return peer_reviews


def build_reviewer_profiles(assessments_dir: Path) -> Dict[str, ReviewerProfile]:
    """Build profiles for all reviewers across all assessments"""
    profiles = {}

    # Find all assessment markdown files (exclude synthesized reports)
    assessment_files = [
        f for f in assessments_dir.rglob("*.md")
        if "Synthesized Report" not in f.name
    ]

    print(f"Analyzing {len(assessment_files)} assessment files...")

    for file_path in assessment_files:
        peer_reviews = parse_assessment_file(file_path)

        for reviewer_name, (scores, text_feedback, reviewee_name) in peer_reviews.items():
            if reviewer_name not in profiles:
                profiles[reviewer_name] = ReviewerProfile(name=reviewer_name)

            profile = profiles[reviewer_name]
            profile.reviews_written += 1
            profile.scores_given.extend(scores)
            profile.text_feedback.extend(text_feedback)
            profile.reviewees.append(reviewee_name)

    return profiles


def generate_report(profiles: Dict[str, ReviewerProfile], output_path: Path):
    """Generate markdown report with analysis findings"""

    # Calculate company average
    all_scores = []
    for profile in profiles.values():
        all_scores.extend(profile.scores_given)
    company_avg = statistics.mean(all_scores) if all_scores else 0.0

    # Identify categories
    firewall_5s = [p for p in profiles.values() if p.firewall_5_percentage >= 90]
    low_effort = [
        p for p in profiles.values()
        if p.avg_words_per_review < 50 and p.score_std_dev < 0.5 and p.reviews_written >= 3
    ]
    high_quality = sorted(
        profiles.values(),
        key=lambda p: p.quality_score,
        reverse=True
    )[:25]

    # Sort lists
    firewall_5s.sort(key=lambda p: p.firewall_5_percentage, reverse=True)
    low_effort.sort(key=lambda p: (p.avg_words_per_review, p.score_std_dev))

    # Generate report
    report = []
    report.append("# Global Reviewer Quality Analysis - 2025 EOY")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    report.append(f"- **Total reviewers analyzed**: {len(profiles)}")
    report.append(f"- **Total reviews written**: {sum(p.reviews_written for p in profiles.values())}")
    report.append(f"- **Total scores given**: {len(all_scores)}")
    report.append(f"- **Company average score**: {company_avg:.2f}")
    report.append(f"- **Firewall 5s identified**: {len(firewall_5s)} ({len(firewall_5s)/len(profiles)*100:.1f}%)")
    report.append(f"- **Low-effort reviewers**: {len(low_effort)} ({len(low_effort)/len(profiles)*100:.1f}%)")
    report.append(f"- **High-quality reviewers** (top 25): {len(high_quality)}")
    report.append("")

    # Firewall 5s section
    report.append("## Firewall 5s Reviewers")
    report.append("")
    report.append("Reviewers who gave 90%+ of their scores as 5.0 across ALL reviewees.")
    report.append("")
    report.append("| Reviewer | % of 5.0s | Reviews Written | Total Scores | Mean Score | Std Dev | Flag |")
    report.append("|----------|-----------|-----------------|--------------|------------|---------|------|")

    for profile in firewall_5s:
        flag = "🚨" if profile.firewall_5_percentage >= 95 else "⚠️"
        report.append(
            f"| {profile.name} | {profile.firewall_5_percentage:.1f}% | "
            f"{profile.reviews_written} | {len(profile.scores_given)} | "
            f"{profile.score_mean:.2f} | {profile.score_std_dev:.2f} | {flag} |"
        )

    report.append("")

    # Low-effort section
    report.append("## Low-Effort Reviewers")
    report.append("")
    report.append("Reviewers with minimal text feedback (< 50 words per review) AND low score variance (< 0.5).")
    report.append("")
    report.append("| Reviewer | Words per Review | Score Std Dev | Reviews Written | Mean Score | Flags |")
    report.append("|----------|------------------|---------------|-----------------|------------|-------|")

    for profile in low_effort:
        flags = []
        if profile.avg_words_per_review < 30:
            flags.append("📝 Very Low Text")
        if profile.score_std_dev < 0.3:
            flags.append("📊 No Variance")
        flag_str = ", ".join(flags) if flags else "⚠️"

        report.append(
            f"| {profile.name} | {profile.avg_words_per_review:.1f} | "
            f"{profile.score_std_dev:.2f} | {profile.reviews_written} | "
            f"{profile.score_mean:.2f} | {flag_str} |"
        )

    report.append("")

    # High-quality section
    report.append("## High-Quality Reviewers (Top 25)")
    report.append("")
    report.append("Reviewers demonstrating thoughtful engagement and differentiation.")
    report.append("")
    report.append("| Rank | Reviewer | Quality Score | Words per Review | Score Std Dev | Reviews Written | Mean Score |")
    report.append("|------|----------|---------------|------------------|---------------|-----------------|------------|")

    for rank, profile in enumerate(high_quality, 1):
        report.append(
            f"| {rank} | {profile.name} | {profile.quality_score:.1f} | "
            f"{profile.avg_words_per_review:.1f} | {profile.score_std_dev:.2f} | "
            f"{profile.reviews_written} | {profile.score_mean:.2f} |"
        )

    report.append("")

    # Score distribution analysis
    report.append("## Score Distribution Analysis")
    report.append("")
    report.append(f"**Company Average Score**: {company_avg:.2f}")
    report.append("")

    # Overall distribution
    overall_dist = defaultdict(int)
    for score in all_scores:
        overall_dist[score] += 1

    report.append("### Overall Score Distribution")
    report.append("")
    report.append("| Score | Count | Percentage |")
    report.append("|-------|-------|------------|")

    for score in sorted(overall_dist.keys()):
        count = overall_dist[score]
        pct = (count / len(all_scores)) * 100
        report.append(f"| {score:.1f} | {count} | {pct:.1f}% |")

    report.append("")

    # Reviewer score distribution patterns
    report.append("### Reviewer Score Pattern Categories")
    report.append("")

    # Categorize reviewers by their scoring patterns
    harsh_reviewers = [p for p in profiles.values() if p.score_mean < company_avg - 0.5]
    generous_reviewers = [p for p in profiles.values() if p.score_mean > company_avg + 0.5]
    calibrated_reviewers = [
        p for p in profiles.values()
        if abs(p.score_mean - company_avg) <= 0.5
    ]

    report.append(f"- **Harsh reviewers** (mean < {company_avg - 0.5:.2f}): {len(harsh_reviewers)} ({len(harsh_reviewers)/len(profiles)*100:.1f}%)")
    report.append(f"- **Generous reviewers** (mean > {company_avg + 0.5:.2f}): {len(generous_reviewers)} ({len(generous_reviewers)/len(profiles)*100:.1f}%)")
    report.append(f"- **Calibrated reviewers** (within ±0.5 of average): {len(calibrated_reviewers)} ({len(calibrated_reviewers)/len(profiles)*100:.1f}%)")
    report.append("")

    # Insights & Recommendations
    report.append("## Insights & Recommendations")
    report.append("")

    report.append("### Key Findings")
    report.append("")
    report.append(f"1. **Firewall 5s Impact**: {len(firewall_5s)} reviewers ({len(firewall_5s)/len(profiles)*100:.1f}%) are giving 90%+ of scores as 5.0, which reduces the signal-to-noise ratio in performance differentiation.")
    report.append("")
    report.append(f"2. **Low-Effort Reviews**: {len(low_effort)} reviewers ({len(low_effort)/len(profiles)*100:.1f}%) are providing minimal text feedback (< 50 words per review) with little score variance (< 0.5 std dev), suggesting checkbox completion rather than thoughtful assessment.")
    report.append("")
    report.append(f"3. **Score Distribution**: The company average of {company_avg:.2f} suggests a generally positive review culture, with {overall_dist.get(5.0, 0)} scores of 5.0 ({overall_dist.get(5.0, 0)/len(all_scores)*100:.1f}% of all scores).")
    report.append("")
    report.append(f"4. **High-Quality Reviewers**: The top 25 reviewers (17% of total) demonstrate significantly higher engagement with 150+ words per review on average and good score differentiation.")
    report.append("")

    report.append("### Recommendations for Calibration")
    report.append("")
    report.append("1. **Address Firewall 5s**: Consider providing calibration training to reviewers who consistently give 90%+ scores as 5.0. They may:")
    report.append("   - Not understand the rating scale")
    report.append("   - Be conflict-averse")
    report.append("   - Lack context to differentiate performance")
    report.append("")
    report.append("2. **Improve Low-Effort Reviews**: Encourage reviewers with minimal feedback to:")
    report.append("   - Provide specific examples")
    report.append("   - Focus on actionable feedback")
    report.append("   - Use the full rating scale appropriately")
    report.append("")
    report.append("3. **Recognize High-Quality Reviewers**: The top 25 reviewers provide valuable, thoughtful feedback. Consider:")
    report.append("   - Sharing examples of high-quality reviews (anonymized)")
    report.append("   - Using them as calibration references")
    report.append("   - Acknowledging their effort")
    report.append("")
    report.append("4. **Rating Scale Calibration**: With a company average of {:.2f}, consider whether:".format(company_avg))
    report.append("   - The scale is being used as intended")
    report.append("   - There's grade inflation")
    report.append("   - Calibration sessions would help reviewers differentiate performance levels")
    report.append("")

    report.append("### Data Quality Notes")
    report.append("")
    report.append("- Scores of 6.0 ('Haven't had opportunity to observe') were excluded from analysis")
    report.append("- Text feedback analyzed includes Question 11 (rehire comment) and Question 12 (START/STOP/KEEP) combined")
    report.append("- 'Words per review' represents the average combined word count from Q11 + Q12 text feedback")
    report.append("- Reviewers with < 3 reviews were not flagged as low-effort (insufficient sample size)")
    report.append("- Quality score is a composite metric (0-100) based on words per review, score differentiation, review volume, and calibration")
    report.append("")

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f"\n✅ Report generated: {output_path}")


def main():
    """Main execution function"""
    # Set up paths
    project_root = Path(__file__).parent.parent
    assessments_dir = project_root / "assessments"
    output_path = project_root / "docs" / "reviewer-quality-analysis.md"

    print("=" * 80)
    print("REVIEWER QUALITY ANALYSIS")
    print("=" * 80)
    print()

    # Build reviewer profiles
    profiles = build_reviewer_profiles(assessments_dir)

    print(f"\n✅ Analyzed {len(profiles)} unique reviewers")
    print(f"✅ Total reviews: {sum(p.reviews_written for p in profiles.values())}")
    print(f"✅ Total scores: {sum(len(p.scores_given) for p in profiles.values())}")

    # Generate report
    generate_report(profiles, output_path)

    # Print summary
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print(f"📊 Total reviewers: {len(profiles)}")
    print(f"🔥 Firewall 5s: {len([p for p in profiles.values() if p.firewall_5_percentage >= 90])}")
    print(f"📝 Low-effort: {len([p for p in profiles.values() if p.avg_words_per_review < 50 and p.score_std_dev < 0.5 and p.reviews_written >= 3])}")
    print(f"⭐ High-quality (top 25): 25")
    print()
    print(f"📄 Full report: {output_path}")
    print()


if __name__ == "__main__":
    main()
