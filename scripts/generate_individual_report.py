#!/usr/bin/env python3
"""
Generate Individual Assessment Report for Rise8 EOY Reviews

This script generates comprehensive individual assessment reports including:
- Overall scores with multiple comparison deltas (peers, level, team, department, project)
- Per-question breakdowns (Questions 1-11)
- Reviewer quality analysis (firewall 5s, low-effort, high-quality detection)
- Placeholders for AI synthesis of qualitative feedback

Usage:
    python scripts/generate_individual_report.py "Matt Pacione"
    python scripts/generate_individual_report.py "Matt Pacione" -v  # verbose mode
    python scripts/generate_individual_report.py "Matt Pacione" --output-dir reports/individual

Author: Rise8 Data Science Team
Version: 1.0.0
"""

import re
import json
import csv
import argparse
import statistics
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class EmployeeMetadata:
    """Employee metadata from team mapping"""
    name: str
    department: str
    level: str
    team: str
    project: str


@dataclass
class TierInfo:
    """Tier assignment information"""
    tier: str
    tier_name: str
    peer_average: float


@dataclass
class ReviewerData:
    """Reviewer's scores and comments for an employee"""
    name: str
    scores: Dict[int, float]  # question_num -> score (1-11)
    comments: Dict[int, str]  # question_num -> comment text (11, 12)


@dataclass
class QuestionStats:
    """Statistics for a single question"""
    question_num: int
    peer_avg: float
    response_count: int
    response_pct: float
    self_score: float
    delta_self_peers: float
    delta_self_level: float
    delta_self_team: float
    delta_self_dept: float
    delta_self_project: float
    # New statistical fields
    median: float
    stdev: float
    min_score: float
    max_score: float
    score_range: float
    percentile: float
    agreement_level: str
    vs_team: str
    vs_project: str
    vs_department: str
    vs_company: str
    interpretation: str


class IndividualReportGenerator:
    """Generate comprehensive individual assessment reports"""

    SCRIPT_VERSION = "1.0.0"

    QUESTION_NAMES = {
        1: "Be Bold",
        2: "Do The Right Thing",
        3: "Do What Works",
        4: "Do What is Required",
        5: "Always Be Kind",
        6: "Keep it Real",
        7: "Outcomes in Production",
        8: "Grit",
        9: "Growth Mindset",
        10: "No Unnecessary Rules",
        11: "eNPS (Employee Net Promoter Score)"
    }

    SCORE_MAP = {
        "1 - Does Not Meet Expectations": 1.0,
        "2 - Needs Improvement": 2.0,
        "3 - Solid Performer": 3.0,
        "4 - Team Leader": 4.0,
        "5 - Best in Grade": 5.0,
        "5 - Best in Class": 5.0,  # Alternative text for same rating
        "1 - Strongly Disagree": 1.0,
        "2 - Disagree": 2.0,
        "3 - Neutral": 3.0,
        "4 - Agree": 4.0,
        "5 - Strongly Agree": 5.0,
        "6 - Haven't had the opportunity to observe": 6.0,  # Exclude from calculations
    }

    def __init__(self, base_dir: str, verbose: bool = False):
        self.base_dir = Path(base_dir)
        self.verbose = verbose
        self.assessments_dir = self.base_dir / "assessments"
        self.team_map_file = self.base_dir / "LatticeAPI" / "lattice_api_client" / "team_map.json"
        self.comprehensive_data_file = self.base_dir / "docs" / "analysis-results" / "riser_data_detailed.csv"
        self.tier_assignments_file = self.base_dir / "docs" / "analysis-results" / "tier_assignments.csv"
        self.template_file = self.base_dir / ".claude" / "templates" / "individual-assessment-report-template.md"

        # Cache for parsed data
        self.team_map: Dict[str, EmployeeMetadata] = {}
        self.comprehensive_data: Dict[str, dict] = {}
        self.tier_assignments: Dict[str, TierInfo] = {}
        self.all_assessment_data: Dict[str, dict] = {}  # Cache for per-question comparisons

    def log(self, message: str):
        """Log message if verbose mode enabled"""
        if self.verbose:
            print(f"[INFO] {message}")

    def load_team_mapping(self):
        """Load team mapping JSON"""
        self.log(f"Loading team mapping from {self.team_map_file}")
        with open(self.team_map_file, 'r') as f:
            data = json.load(f)

        for name, info in data.items():
            # Normalize name format from "Last, First" to "First Last"
            if ", " in name:
                parts = name.split(", ")
                normalized_name = f"{parts[1]} {parts[0]}"
            else:
                normalized_name = name

            self.team_map[normalized_name] = EmployeeMetadata(
                name=normalized_name,
                department=info["department"],
                level=info["level"],
                team=info["team"],
                project=info["project"]
            )

        self.log(f"Loaded {len(self.team_map)} employee records")

    def load_comprehensive_data(self):
        """Load comprehensive analysis CSV"""
        self.log(f"Loading comprehensive data from {self.comprehensive_data_file}")
        with open(self.comprehensive_data_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.comprehensive_data[row['Name']] = {
                    'department': row['Department'],
                    'peer_average': float(row['Peer_Average']),
                    'self_average': float(row['Self_Average']),
                    'delta': float(row['Delta']),
                    'response_count': int(row['Response_Count']),
                    'response_total': int(row['Response_Total']),
                    'response_pct': float(row['Response_Pct']),
                    'total_ratings': int(row['Total_Ratings'])
                }

        self.log(f"Loaded data for {len(self.comprehensive_data)} employees")

    def load_tier_assignments(self):
        """Load tier assignments CSV"""
        self.log(f"Loading tier assignments from {self.tier_assignments_file}")
        with open(self.tier_assignments_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tier_assignments[row['Name']] = TierInfo(
                    tier=row['Tier'],
                    tier_name=row['Tier_Name'],
                    peer_average=float(row['Peer_Average'])
                )

        self.log(f"Loaded tier assignments for {len(self.tier_assignments)} employees")

    def parse_score(self, rating_text: str) -> Optional[float]:
        """Parse rating text to numeric score"""
        for pattern, score in self.SCORE_MAP.items():
            if pattern in rating_text:
                return score
        return None

    def parse_assessment_file(self, employee_name: str) -> Tuple[Dict, List[ReviewerData], Path]:
        """Parse individual assessment file to extract scores and comments"""
        # Find assessment file
        name_file = employee_name.replace(" ", "_")
        assessment_file = None

        for dept_dir in self.assessments_dir.iterdir():
            if dept_dir.is_dir():
                potential_file = dept_dir / "Raw" / f"{name_file}.md"
                if potential_file.exists():
                    assessment_file = potential_file
                    break

        if not assessment_file:
            raise FileNotFoundError(f"Assessment file not found for {employee_name}")

        self.log(f"Parsing assessment file: {assessment_file}")
        content = assessment_file.read_text()

        # Extract overall scores from header
        overall_data = {}
        peer_avg_match = re.search(r'\*\*Peers?\s+Average\*\*:\s+([\d.]+)', content)
        if peer_avg_match:
            overall_data['peer_average'] = float(peer_avg_match.group(1))

        response_match = re.search(r'\*\*Response Rate\*\*:\s+(\d+)/(\d+)\s+peer reviewers\s+\((\d+)%\)', content)
        if response_match:
            overall_data['response_count'] = int(response_match.group(1))
            overall_data['response_total'] = int(response_match.group(2))
            overall_data['response_pct'] = float(response_match.group(3))

        self_avg_match = re.search(r'\*\*Self\s+Average\*\*:\s+([\d.]+)', content)
        if self_avg_match:
            overall_data['self_average'] = float(self_avg_match.group(1))

        ratings_match = re.search(r'based on (\d+) ratings', content)
        if ratings_match:
            overall_data['total_ratings'] = int(ratings_match.group(1))

        # Parse self-assessment scores
        self_scores = {}
        self_section_match = re.search(rf'##\s+{re.escape(employee_name)}\s+\(Self\)(.*?)(?=\n##\s|\Z)', content, re.DOTALL)
        if self_section_match:
            self_section = self_section_match.group(1)
            for q_num in range(1, 12):  # Questions 1-11
                q_pattern = rf'### Question {q_num}\s+.*?\*\*Rating\*\*:\s+([^\n]+)'
                q_match = re.search(q_pattern, self_section, re.DOTALL)
                if q_match:
                    score = self.parse_score(q_match.group(1))
                    if score and score != 6.0:  # Exclude "haven't observed"
                        self_scores[q_num] = score

        overall_data['self_scores'] = self_scores

        # Extract accomplishments text (Question 13)
        accomplishments_match = re.search(
            r'### Question 13\s+.*?\*\*Comment\*\*:\s*\n\s*>\s*(.*?)(?=###|\#\#|\Z)',
            content, re.DOTALL
        )
        if accomplishments_match:
            overall_data['accomplishments'] = accomplishments_match.group(1).strip()

        # Parse peer reviews
        peer_reviewers = []
        # Match "## Name (Peer)" where Name is on the same line (not spanning multiple lines)
        peer_sections = re.finditer(r'##\s+([^\n]+?)\s+\(Peer\)(.*?)(?=\n##\s|\Z)', content, re.DOTALL)

        for peer_match in peer_sections:
            reviewer_name = peer_match.group(1).strip()
            peer_content = peer_match.group(2)

            scores = {}
            comments = {}

            # Extract scores for Questions 1-11
            for q_num in range(1, 12):
                q_pattern = rf'### Question {q_num}\s+.*?\*\*Rating\*\*:\s+([^\n]+)'
                q_match = re.search(q_pattern, peer_content, re.DOTALL)
                if q_match:
                    score = self.parse_score(q_match.group(1))
                    if score and score != 6.0:  # Exclude "haven't observed"
                        scores[q_num] = score

            # Extract comments for Question 11 (eNPS)
            q11_comment_match = re.search(
                r'### Question 11\s+.*?\*\*Comment\*\*:\s*\n\s*>\s*(.*?)(?=###|\Z)',
                peer_content, re.DOTALL
            )
            if q11_comment_match:
                comments[11] = q11_comment_match.group(1).strip()

            # Extract comments for Question 12 (Start/Stop/Keep)
            q12_comment_match = re.search(
                r'### Question 12\s+.*?\*\*Comment\*\*:\s*\n\s*>\s*(.*?)(?=###|\Z)',
                peer_content, re.DOTALL
            )
            if q12_comment_match:
                comments[12] = q12_comment_match.group(1).strip()

            if scores:  # Only add if reviewer provided scores
                peer_reviewers.append(ReviewerData(
                    name=reviewer_name,
                    scores=scores,
                    comments=comments
                ))

        self.log(f"Parsed {len(peer_reviewers)} peer reviews")
        return overall_data, peer_reviewers, assessment_file

    def calculate_question_statistics(self, peer_scores: List[float]) -> Optional[Dict]:
        """
        Calculate comprehensive statistics for a single question.

        Args:
            peer_scores: List of peer scores for this question

        Returns:
            dict with: mean, median, stdev, min, max, range
        """
        if not peer_scores:
            return None

        return {
            'mean': statistics.mean(peer_scores),
            'median': statistics.median(peer_scores),
            'stdev': statistics.pstdev(peer_scores),
            'min': min(peer_scores),
            'max': max(peer_scores),
            'range': max(peer_scores) - min(peer_scores),
            'count': len(peer_scores)
        }

    def calculate_percentile_rank(self, score: float, all_scores: List[float]) -> Optional[float]:
        """
        Calculate percentile rank of a score among all scores.

        Args:
            score: The score to rank
            all_scores: List of all scores to compare against

        Returns:
            Percentile rank (0-100)
        """
        if not all_scores or score is None:
            return None

        # Count how many scores are below this score
        below = sum(1 for s in all_scores if s < score)
        equal = sum(1 for s in all_scores if s == score)

        # Percentile = (# below + 0.5 * # equal) / total * 100
        percentile = ((below + 0.5 * equal) / len(all_scores)) * 100

        return round(percentile, 1)

    def interpret_stdev(self, stdev: Optional[float]) -> str:
        """
        Interpret standard deviation for agreement level.

        Args:
            stdev: Standard deviation value

        Returns:
            String interpretation
        """
        if stdev is None:
            return "Unknown"
        elif stdev < 0.30:
            return "High consensus"
        elif stdev < 0.60:
            return "Moderate agreement"
        else:
            return "Mixed opinions"

    def format_comparison(self, peer_avg: float, group_avg: float, group_name: str) -> str:
        """
        Format comparison of peer average vs group average.

        Args:
            peer_avg: Employee's peer average for this question
            group_avg: Group's average for this question
            group_name: Name of the group (Team/Project/Department/Company)

        Returns:
            Formatted string
        """
        if peer_avg is None or group_avg is None or group_avg == 0.0:
            return f"- **vs {group_name} Average**: N/A"

        delta = peer_avg - group_avg

        if abs(delta) < 0.05:
            position = "At"
        elif delta > 0:
            position = "Above"
        else:
            position = "Below"

        return f"- **vs {group_name} Average**: {delta:+.2f} ({group_name} avg: {group_avg:.2f}) - {position} {group_name.lower()}"

    def format_delta_with_emoji(self, delta: float) -> str:
        """
        Format delta score with emoji indicator for self-awareness calibration.

        Args:
            delta: Delta score (self - comparison)

        Returns:
            Formatted string with emoji and interpretation
        """
        if delta <= -0.10:
            return f"{delta:+.2f} 🟢 (Humble)"
        elif delta >= 0.10:
            return f"{delta:+.2f} 🔴 (Overconfident)"
        else:
            return f"{delta:+.2f} 🟡 (Well-calibrated)"

    def generate_interpretation_with_data_check(
        self,
        question_name: str,
        peer_avg: float,
        percentile: Optional[float],
        stdev: Optional[float],
        score_range: Tuple[float, float],
        peer_vs_groups: Dict[str, float],
        num_responses: int
    ) -> str:
        """
        Generate auto-interpretation text with proper insufficient data handling.

        Args:
            question_name: Name of the question
            peer_avg: Employee's peer average
            percentile: Percentile rank
            stdev: Standard deviation
            score_range: Tuple of (min, max)
            peer_vs_groups: Dict with deltas vs team/project/dept/company
            num_responses: Number of peer responses for this question

        Returns:
            Formatted interpretation string
        """
        # Check for truly insufficient data (< 3 responses)
        if num_responses < 3:
            return "*Insufficient data for interpretation (minimum 3 responses needed)*"

        # Check for perfect consensus
        if stdev == 0.0:
            return "*Perfect consensus - all reviewers gave identical scores*"

        # Proceed with normal interpretation
        return self.generate_interpretation(
            question_name, peer_avg, percentile, stdev, score_range, peer_vs_groups
        )

    def generate_interpretation(
        self,
        question_name: str,
        peer_avg: float,
        percentile: Optional[float],
        stdev: Optional[float],
        score_range: Tuple[float, float],
        peer_vs_groups: Dict[str, float]
    ) -> str:
        """
        Generate auto-interpretation text for a question.

        Args:
            question_name: Name of the question
            peer_avg: Employee's peer average
            percentile: Percentile rank
            stdev: Standard deviation
            score_range: Tuple of (min, max)
            peer_vs_groups: Dict with deltas vs team/project/dept/company

        Returns:
            Formatted interpretation string
        """
        if not all([peer_avg is not None, percentile is not None, stdev is not None, score_range]):
            return "*Insufficient data for interpretation*"

        min_score, max_score = score_range
        spread = max_score - min_score

        # Percentile text
        if percentile >= 10:
            percentile_text = f"**{int(percentile)}th percentile**"
            top_pct = 100 - percentile
        else:
            percentile_text = f"**bottom {100-int(percentile)}%**"
            top_pct = percentile

        # Agreement text
        agreement = self.interpret_stdev(stdev)

        # Spread interpretation
        if spread < 0.5:
            spread_text = "very tight clustering"
        elif spread < 1.5:
            spread_text = "reasonable consistency"
        else:
            spread_text = "notable variability"

        # Find best comparison (highest positive or lowest negative delta)
        comparisons = []
        for group_name, delta in peer_vs_groups.items():
            if delta != 0.0:
                comparisons.append((group_name, delta))

        if comparisons:
            # Sort by absolute value, take highest
            comparisons.sort(key=lambda x: abs(x[1]), reverse=True)
            best_group, best_delta = comparisons[0]
            if abs(best_delta) < 0.05:
                comp_text = f"is approximately **at {best_group} average** ({peer_avg:.2f})"
            elif best_delta > 0:
                comp_text = f"is **{best_delta:+.2f} above {best_group} average**"
            else:
                comp_text = f"is **{best_delta:.2f} below {best_group} average**"
        else:
            comp_text = "is at group averages"

        interpretation = f"""**Interpretation:**
- Scores in the {percentile_text} on {question_name} company-wide (top {top_pct:.0f}%)
- Peer average ({peer_avg:.2f}) {comp_text}
- **{agreement}** among reviewers (SD: {stdev:.2f})
- Score range ({min_score:.1f}-{max_score:.1f}) shows {spread_text} in reviewer perceptions"""

        return interpretation

    def calculate_group_averages(self, metadata: EmployeeMetadata) -> Dict[str, float]:
        """Calculate average peer scores for various groups"""
        self.log("Calculating group averages")

        # Group employees by category
        level_scores = []
        team_scores = []
        dept_scores = []
        project_scores = []

        for emp_name, emp_meta in self.team_map.items():
            if emp_name not in self.comprehensive_data:
                continue

            peer_avg = self.comprehensive_data[emp_name]['peer_average']

            if emp_meta.level == metadata.level:
                level_scores.append(peer_avg)
            if emp_meta.team == metadata.team:
                team_scores.append(peer_avg)
            if emp_meta.department == metadata.department:
                dept_scores.append(peer_avg)
            if emp_meta.project == metadata.project:
                project_scores.append(peer_avg)

        return {
            'level': statistics.mean(level_scores) if level_scores else 0.0,
            'team': statistics.mean(team_scores) if team_scores else 0.0,
            'department': statistics.mean(dept_scores) if dept_scores else 0.0,
            'project': statistics.mean(project_scores) if project_scores else 0.0,
        }

    def calculate_question_group_averages(
        self,
        question_num: int,
        metadata: EmployeeMetadata
    ) -> Tuple[Dict[str, float], List[float]]:
        """
        Calculate average scores for a specific question by group.

        Returns:
            Tuple of (group_averages_dict, all_company_scores_list)
        """
        # Build cache of all assessment data if not already done
        if not self.all_assessment_data:
            self.log("Building question-level cache for all employees")
            for dept_dir in self.assessments_dir.iterdir():
                if not dept_dir.is_dir():
                    continue
                raw_dir = dept_dir / "Raw"
                if not raw_dir.exists():
                    continue
                for assess_file in raw_dir.glob("*.md"):
                    emp_name = assess_file.stem.replace("_", " ")
                    try:
                        overall_data, peer_reviewers, _ = self.parse_assessment_file(emp_name)
                        self.all_assessment_data[emp_name] = {
                            'peer_reviewers': peer_reviewers,
                            'self_scores': overall_data.get('self_scores', {})
                        }
                    except Exception as e:
                        self.log(f"Warning: Could not parse {emp_name}: {e}")

        # Calculate averages for this question
        level_scores = []
        team_scores = []
        dept_scores = []
        project_scores = []
        company_scores = []  # All scores company-wide for percentile calculation

        for emp_name, emp_meta in self.team_map.items():
            if emp_name not in self.all_assessment_data:
                continue

            # Calculate peer average for this question
            peer_scores = []
            for reviewer in self.all_assessment_data[emp_name]['peer_reviewers']:
                if question_num in reviewer.scores:
                    peer_scores.append(reviewer.scores[question_num])

            if not peer_scores:
                continue

            peer_avg = statistics.mean(peer_scores)
            company_scores.append(peer_avg)  # Add to company-wide list

            if emp_meta.level == metadata.level:
                level_scores.append(peer_avg)
            if emp_meta.team == metadata.team:
                team_scores.append(peer_avg)
            if emp_meta.department == metadata.department:
                dept_scores.append(peer_avg)
            if emp_meta.project == metadata.project:
                project_scores.append(peer_avg)

        group_avgs = {
            'level': statistics.mean(level_scores) if level_scores else 0.0,
            'team': statistics.mean(team_scores) if team_scores else 0.0,
            'department': statistics.mean(dept_scores) if dept_scores else 0.0,
            'project': statistics.mean(project_scores) if project_scores else 0.0,
            'company': statistics.mean(company_scores) if company_scores else 0.0,
        }

        return group_avgs, company_scores

    def calculate_question_stats(
        self,
        question_num: int,
        peer_reviewers: List[ReviewerData],
        self_scores: Dict[int, float],
        metadata: EmployeeMetadata,
        response_total: int
    ) -> QuestionStats:
        """Calculate comprehensive statistics for a specific question"""
        # Extract peer scores for this question
        peer_scores = [r.scores[question_num] for r in peer_reviewers if question_num in r.scores]

        if not peer_scores:
            # Return empty stats if no peer scores
            return QuestionStats(
                question_num=question_num,
                peer_avg=0.0,
                response_count=0,
                response_pct=0.0,
                self_score=self_scores.get(question_num, 0.0),
                delta_self_peers=0.0,
                delta_self_level=0.0,
                delta_self_team=0.0,
                delta_self_dept=0.0,
                delta_self_project=0.0,
                median=0.0,
                stdev=0.0,
                min_score=0.0,
                max_score=0.0,
                score_range=0.0,
                percentile=0.0,
                agreement_level="N/A",
                vs_team="N/A",
                vs_project="N/A",
                vs_department="N/A",
                vs_company="N/A",
                interpretation="*Insufficient data for interpretation*"
            )

        # Basic statistics
        peer_avg = statistics.mean(peer_scores)
        response_count = len(peer_scores)
        response_pct = (response_count / response_total * 100) if response_total > 0 else 0.0
        self_score = self_scores.get(question_num, 0.0)

        # Calculate group averages for this question
        group_avgs, company_scores = self.calculate_question_group_averages(question_num, metadata)

        # Calculate self-awareness deltas
        delta_self_peers = self_score - peer_avg
        delta_self_level = self_score - group_avgs['level']
        delta_self_team = self_score - group_avgs['team']
        delta_self_dept = self_score - group_avgs['department']
        delta_self_project = self_score - group_avgs['project']

        # Calculate comprehensive statistics
        stats = self.calculate_question_statistics(peer_scores)
        if stats:
            median = stats['median']
            stdev = stats['stdev']
            min_score = stats['min']
            max_score = stats['max']
            score_range = stats['range']
        else:
            median = peer_avg
            stdev = 0.0
            min_score = peer_avg
            max_score = peer_avg
            score_range = 0.0

        # Calculate percentile rank
        percentile = self.calculate_percentile_rank(peer_avg, company_scores)
        if percentile is None:
            percentile = 0.0

        # Agreement level
        agreement_level = self.interpret_stdev(stdev)

        # Format group comparisons (peer avg vs group averages)
        vs_team = self.format_comparison(peer_avg, group_avgs['team'], "Team")
        vs_project = self.format_comparison(peer_avg, group_avgs['project'], "Project")
        vs_department = self.format_comparison(peer_avg, group_avgs['department'], "Department")
        vs_company = self.format_comparison(peer_avg, group_avgs['company'], "Company")

        # Calculate peer vs group deltas for interpretation
        peer_vs_groups = {
            'team': peer_avg - group_avgs['team'] if group_avgs['team'] > 0 else 0.0,
            'project': peer_avg - group_avgs['project'] if group_avgs['project'] > 0 else 0.0,
            'department': peer_avg - group_avgs['department'] if group_avgs['department'] > 0 else 0.0,
            'company': peer_avg - group_avgs['company'] if group_avgs['company'] > 0 else 0.0,
        }

        # Generate interpretation with data check
        question_name = self.QUESTION_NAMES.get(question_num, f"Question {question_num}")
        interpretation = self.generate_interpretation_with_data_check(
            question_name,
            peer_avg,
            percentile,
            stdev,
            (min_score, max_score),
            peer_vs_groups,
            response_count  # Number of responses for this question
        )

        return QuestionStats(
            question_num=question_num,
            peer_avg=peer_avg,
            response_count=response_count,
            response_pct=response_pct,
            self_score=self_score,
            delta_self_peers=delta_self_peers,
            delta_self_level=delta_self_level,
            delta_self_team=delta_self_team,
            delta_self_dept=delta_self_dept,
            delta_self_project=delta_self_project,
            median=median,
            stdev=stdev,
            min_score=min_score,
            max_score=max_score,
            score_range=score_range,
            percentile=percentile,
            agreement_level=agreement_level,
            vs_team=vs_team,
            vs_project=vs_project,
            vs_department=vs_department,
            vs_company=vs_company,
            interpretation=interpretation
        )

    def detect_firewall_5s(self, peer_reviewers: List[ReviewerData]) -> List[Dict]:
        """Detect reviewers who gave automatic 5s without differentiation"""
        self.log("Detecting firewall 5s reviewers")
        firewall_reviewers = []

        for reviewer in peer_reviewers:
            # Get scores for questions 1-10 only (exclude eNPS Q11)
            scores = [reviewer.scores[q] for q in range(1, 11) if q in reviewer.scores]

            if len(scores) < 5:  # Need at least 5 scores to evaluate
                continue

            # Calculate variance and count 5s
            if len(scores) > 1:
                variance = statistics.pvariance(scores)
            else:
                variance = 0.0

            count_5s = sum(1 for s in scores if s == 5.0)

            # Classify
            classification = None
            if variance < 0.10 and count_5s >= 9:
                classification = "Definite Firewall 5"
            elif variance < 0.25 and count_5s >= 8:
                classification = "Likely Firewall 5"

            if classification:
                firewall_reviewers.append({
                    'name': reviewer.name,
                    'variance': variance,
                    'count_5s': count_5s,
                    'total_scores': len(scores),
                    'classification': classification
                })

        return sorted(firewall_reviewers, key=lambda x: x['variance'])

    def detect_low_effort(self, peer_reviewers: List[ReviewerData]) -> List[Dict]:
        """Detect reviewers with minimal text responses or low variance"""
        self.log("Detecting low-effort reviewers")
        low_effort_reviewers = []

        for reviewer in peer_reviewers:
            # Calculate average word count from comments
            word_counts = []
            for comment in reviewer.comments.values():
                if comment:
                    word_counts.append(len(comment.split()))

            avg_words = statistics.mean(word_counts) if word_counts else 0

            # Calculate score variance (Q1-10)
            scores = [reviewer.scores[q] for q in range(1, 11) if q in reviewer.scores]
            if len(scores) > 1:
                variance = statistics.pvariance(scores)
            else:
                variance = 0.0

            # Classify as low effort
            if avg_words < 20 and variance < 0.50 and len(scores) >= 5:
                low_effort_reviewers.append({
                    'name': reviewer.name,
                    'avg_words': avg_words,
                    'variance': variance,
                    'total_scores': len(scores)
                })

        return sorted(low_effort_reviewers, key=lambda x: x['avg_words'])

    def detect_high_quality(self, peer_reviewers: List[ReviewerData]) -> List[Dict]:
        """Detect reviewers with thoughtful, differentiated feedback"""
        self.log("Detecting high-quality reviewers")
        high_quality_reviewers = []

        for reviewer in peer_reviewers:
            # Calculate average word count
            word_counts = []
            for comment in reviewer.comments.values():
                if comment:
                    word_counts.append(len(comment.split()))

            avg_words = statistics.mean(word_counts) if word_counts else 0

            # Calculate score variance (Q1-10)
            scores = [reviewer.scores[q] for q in range(1, 11) if q in reviewer.scores]
            if len(scores) > 1:
                variance = statistics.pvariance(scores)
            else:
                variance = 0.0

            # Classify as high quality
            if variance > 0.60 and avg_words > 50 and len(scores) >= 5:
                high_quality_reviewers.append({
                    'name': reviewer.name,
                    'variance': variance,
                    'avg_words': avg_words,
                    'total_scores': len(scores)
                })

        return sorted(high_quality_reviewers, key=lambda x: -x['variance'])

    def extract_qualitative_feedback(
        self,
        peer_reviewers: List[ReviewerData]
    ) -> Dict[str, str]:
        """Extract raw qualitative feedback text for agent synthesis"""
        # Extract eNPS comments (Q11)
        enps_comments = []
        for reviewer in peer_reviewers:
            if 11 in reviewer.comments and reviewer.comments[11]:
                enps_comments.append(f"**{reviewer.name}:**\n{reviewer.comments[11]}\n")

        # Extract Start/Stop/Keep comments (Q12)
        start_stop_keep = []
        for reviewer in peer_reviewers:
            if 12 in reviewer.comments and reviewer.comments[12]:
                start_stop_keep.append(f"**{reviewer.name}:**\n{reviewer.comments[12]}\n")

        return {
            'enps_comments': '\n'.join(enps_comments) if enps_comments else '[No eNPS comments provided]',
            'start_stop_keep': '\n'.join(start_stop_keep) if start_stop_keep else '[No Start/Stop/Keep feedback provided]'
        }

    def generate_report(self, employee_name: str, output_dir: str) -> str:
        """Generate complete individual assessment report"""
        self.log(f"Generating report for {employee_name}")

        # Load all data sources
        self.load_team_mapping()
        self.load_comprehensive_data()
        self.load_tier_assignments()

        # Get employee metadata
        if employee_name not in self.team_map:
            raise ValueError(f"Employee '{employee_name}' not found in team mapping")

        metadata = self.team_map[employee_name]

        # Get comprehensive data
        if employee_name not in self.comprehensive_data:
            raise ValueError(f"Employee '{employee_name}' not found in comprehensive data")

        comp_data = self.comprehensive_data[employee_name]

        # Get tier assignment
        tier_info = self.tier_assignments.get(employee_name, TierInfo("Unknown", "Unknown", 0.0))

        # Parse assessment file and get source file path
        overall_data, peer_reviewers, assessment_file = self.parse_assessment_file(employee_name)

        # Extract qualitative feedback for synthesis
        qualitative_data = self.extract_qualitative_feedback(peer_reviewers)

        # Calculate group averages
        group_avgs = self.calculate_group_averages(metadata)

        # Calculate per-question statistics
        # Use actual count of peer reviewers, not total ratings from CSV
        total_peer_reviewers = len(peer_reviewers)
        question_stats = []
        for q_num in range(1, 12):  # Questions 1-11
            stats = self.calculate_question_stats(
                q_num,
                peer_reviewers,
                overall_data['self_scores'],
                metadata,
                total_peer_reviewers  # Pass count of unique reviewers
            )
            question_stats.append(stats)

        # Reviewer quality analysis - REMOVED from individual reports
        # (Firewall 5s detection should be global reviewer analysis, not per-person)
        # firewall_5s = self.detect_firewall_5s(peer_reviewers)
        # low_effort = self.detect_low_effort(peer_reviewers)
        # high_quality = self.detect_high_quality(peer_reviewers)

        # Load template
        template = self.template_file.read_text()

        # Populate template
        report = template

        # Employee information
        report = report.replace("{{EMPLOYEE_NAME}}", employee_name)
        report = report.replace("{{EMPLOYEE_NAME_FILE}}", employee_name.replace(" ", "_"))
        report = report.replace("{{DEPARTMENT}}", metadata.department)
        report = report.replace("{{LEVEL}}", metadata.level)
        report = report.replace("{{TEAM}}", metadata.team)
        report = report.replace("{{PROJECT}}", metadata.project)
        report = report.replace("{{TIER}}", tier_info.tier)
        report = report.replace("{{TIER_NAME}}", tier_info.tier_name)

        # Overall scores
        report = report.replace("{{PEER_AVERAGE}}", f"{comp_data['peer_average']:.2f}")
        report = report.replace("{{TOTAL_RATINGS}}", str(comp_data['total_ratings']))

        # Response rate: Use actual count of peer reviewers (not ratings from CSV)
        report = report.replace("{{RESPONSE_COUNT}}", str(total_peer_reviewers))
        report = report.replace("{{RESPONSE_TOTAL}}", str(total_peer_reviewers))
        report = report.replace("{{RESPONSE_PCT}}", "100")
        report = report.replace("{{SELF_AVERAGE}}", f"{comp_data['self_average']:.2f}")

        # Overall delta scores with emoji indicators
        report = report.replace("{{DELTA_SELF_PEERS}}",
            self.format_delta_with_emoji(comp_data['delta']))
        report = report.replace("{{DELTA_SELF_LEVEL}}",
            self.format_delta_with_emoji(comp_data['self_average'] - group_avgs['level']))
        report = report.replace("{{LEVEL_AVERAGE}}", f"{group_avgs['level']:.2f}")
        report = report.replace("{{DELTA_SELF_TEAM}}",
            self.format_delta_with_emoji(comp_data['self_average'] - group_avgs['team']))
        report = report.replace("{{TEAM_AVERAGE}}", f"{group_avgs['team']:.2f}")
        report = report.replace("{{DELTA_SELF_DEPT}}",
            self.format_delta_with_emoji(comp_data['self_average'] - group_avgs['department']))
        report = report.replace("{{DEPT_AVERAGE}}", f"{group_avgs['department']:.2f}")
        report = report.replace("{{DELTA_SELF_PROJECT}}",
            self.format_delta_with_emoji(comp_data['self_average'] - group_avgs['project']))
        report = report.replace("{{PROJECT_AVERAGE}}", f"{group_avgs['project']:.2f}")

        # Accomplishments (raw text saved for later synthesis)
        accomplishments_text = overall_data.get('accomplishments', '[No accomplishments text found]')
        report = report.replace("{{ACCOMPLISHMENTS_RAW}}", accomplishments_text)

        # eNPS comments (raw text saved for later synthesis)
        report = report.replace("{{ENPS_COMMENTS_RAW}}", qualitative_data['enps_comments'])

        # Start/Stop/Keep (raw text saved for later synthesis)
        report = report.replace("{{START_STOP_KEEP_RAW}}", qualitative_data['start_stop_keep'])

        # Save synthesis data to JSON file for agent processing (in same folder as assessment)
        synthesis_data = {
            'employee_name': employee_name,
            'accomplishments': accomplishments_text,
            'enps_comments': qualitative_data['enps_comments'],
            'start_stop_keep': qualitative_data['start_stop_keep'],
            'generation_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Determine output location (practice folder, not Raw/ subdirectory)
        # assessment_file is in assessments/Practice/Raw/Name.md
        # We want to save synthesis file in assessments/Practice/
        practice_dir = assessment_file.parent.parent
        synthesis_file = practice_dir / f"{employee_name.replace(' ', '_')}_synthesis_data.json"
        synthesis_file.parent.mkdir(parents=True, exist_ok=True)
        with open(synthesis_file, 'w') as f:
            json.dump(synthesis_data, f, indent=2)

        self.log(f"Synthesis data saved to {synthesis_file}")

        # Per-question stats
        for stats in question_stats:
            q_prefix = f"Q{stats.question_num}"

            # Basic scores
            report = report.replace(f"{{{{{q_prefix}_PEER_AVG}}}}", f"{stats.peer_avg:.2f}")
            report = report.replace(f"{{{{{q_prefix}_RESPONSE_COUNT}}}}", str(stats.response_count))
            report = report.replace(f"{{{{{q_prefix}_RESPONSE_PCT}}}}", f"{stats.response_pct:.0f}")
            report = report.replace(f"{{{{{q_prefix}_SELF}}}}", f"{stats.self_score:.1f}")
            report = report.replace(f"{{{{{q_prefix}_MEDIAN}}}}", f"{stats.median:.2f}")

            # Self-awareness deltas with emoji indicators
            report = report.replace(f"{{{{{q_prefix}_DELTA_SELF_PEERS}}}}",
                self.format_delta_with_emoji(stats.delta_self_peers))
            report = report.replace(f"{{{{{q_prefix}_DELTA_SELF_LEVEL}}}}",
                self.format_delta_with_emoji(stats.delta_self_level))
            report = report.replace(f"{{{{{q_prefix}_DELTA_SELF_TEAM}}}}",
                self.format_delta_with_emoji(stats.delta_self_team))
            report = report.replace(f"{{{{{q_prefix}_DELTA_SELF_DEPT}}}}",
                self.format_delta_with_emoji(stats.delta_self_dept))
            report = report.replace(f"{{{{{q_prefix}_DELTA_SELF_PROJECT}}}}",
                self.format_delta_with_emoji(stats.delta_self_project))

            # Performance comparisons (pre-formatted strings)
            report = report.replace(f"{{{{{q_prefix}_VS_TEAM}}}}", stats.vs_team)
            report = report.replace(f"{{{{{q_prefix}_VS_PROJECT}}}}", stats.vs_project)
            report = report.replace(f"{{{{{q_prefix}_VS_DEPARTMENT}}}}", stats.vs_department)
            report = report.replace(f"{{{{{q_prefix}_VS_COMPANY}}}}", stats.vs_company)

            # Statistical analysis
            report = report.replace(f"{{{{{q_prefix}_STDEV}}}}", f"{stats.stdev:.2f}")
            report = report.replace(f"{{{{{q_prefix}_AGREEMENT}}}}", stats.agreement_level)
            report = report.replace(f"{{{{{q_prefix}_PERCENTILE}}}}", f"{stats.percentile:.1f}")
            report = report.replace(f"{{{{{q_prefix}_MIN}}}}", f"{stats.min_score:.1f}")
            report = report.replace(f"{{{{{q_prefix}_MAX}}}}", f"{stats.max_score:.1f}")
            report = report.replace(f"{{{{{q_prefix}_RANGE}}}}", f"{stats.score_range:.1f}")

            # Interpretation
            report = report.replace(f"{{{{{q_prefix}_INTERPRETATION}}}}", stats.interpretation)

        # Qualitative synthesis placeholders (to be filled by rise8-assessment-reviewer agent)
        report = report.replace("{{ACCOMPLISHMENTS_SYNTHESIS}}",
            "*[AI synthesis needed - invoke rise8-assessment-reviewer agent with accomplishments text]*")
        report = report.replace("{{ENPS_COMMENTS_SYNTHESIS}}",
            "*[AI synthesis needed - invoke rise8-assessment-reviewer agent with eNPS comments]*")
        report = report.replace("{{START_SYNTHESIS}}",
            "*[AI synthesis needed - invoke rise8-assessment-reviewer agent with START feedback]*")
        report = report.replace("{{STOP_SYNTHESIS}}",
            "*[AI synthesis needed - invoke rise8-assessment-reviewer agent with STOP feedback]*")
        report = report.replace("{{KEEP_SYNTHESIS}}",
            "*[AI synthesis needed - invoke rise8-assessment-reviewer agent with KEEP feedback]*")

        # Reviewer quality analysis - REMOVED from individual reports
        # (Template section already removed, no need to populate)

        # Metadata
        report = report.replace("{{GENERATION_TIMESTAMP}}",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        report = report.replace("{{SCRIPT_VERSION}}", self.SCRIPT_VERSION)

        # Save report - use "Last, First - Synthesized Report.md" format in source assessment folder
        name_parts = employee_name.split()
        if len(name_parts) >= 2:
            first_name = " ".join(name_parts[:-1])
            last_name = name_parts[-1]
        else:
            first_name = employee_name
            last_name = ""

        # Get directory of practice folder (parent of Raw/)
        # assessment_file is in assessments/Practice/Raw/Name.md
        # We want to save report in assessments/Practice/
        practice_dir = assessment_file.parent.parent
        output_filename = f"{last_name}, {first_name} - Synthesized Report.md"
        output_path = practice_dir / output_filename

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)

        self.log(f"Report saved to {output_path}")
        return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate individual assessment report for Rise8 EOY reviews"
    )
    parser.add_argument(
        "employee_name",
        help="Full name of employee (e.g., 'Matt Pacione')"
    )
    parser.add_argument(
        "--output-dir",
        default="reports/individual",
        help="Output directory for report (default: reports/individual)"
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

    try:
        generator = IndividualReportGenerator(args.base_dir, verbose=args.verbose)
        output_file = generator.generate_report(args.employee_name, args.output_dir)
        print(f"✓ Report generated successfully: {output_file}")
        return 0
    except Exception as e:
        print(f"✗ Error generating report: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
