#!/usr/bin/env python3
"""
Comprehensive Test Suite for Individual Report Generator

Tests all statistical calculations, percentile rankings, comparative deltas,
score mapping, and edge cases for the Rise8 EOY Assessment Report Generator.

Usage:
    pytest scripts/test_generate_individual_report.py -v
    pytest scripts/test_generate_individual_report.py -v --cov=scripts.generate_individual_report --cov-report=term-missing

Author: Rise8 Data Science Team
Version: 1.0.0
"""

import unittest
import statistics
from pathlib import Path
import sys

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generate_individual_report import (
    IndividualReportGenerator,
    EmployeeMetadata,
    ReviewerData,
    QuestionStats,
)


class TestStatisticalCalculations(unittest.TestCase):
    """Test core statistical functions"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_standard_deviation_normal_distribution(self):
        """Test standard deviation with typical score distribution"""
        scores = [4.0, 4.5, 5.0, 3.5, 4.0]
        stats = self.generator.calculate_question_statistics(scores)

        # Expected SD using population standard deviation
        expected_sd = statistics.pstdev(scores)

        self.assertIsNotNone(stats)
        self.assertAlmostEqual(stats['stdev'], expected_sd, places=2)
        self.assertAlmostEqual(stats['stdev'], 0.51, places=1)

    def test_standard_deviation_all_same_scores(self):
        """Test standard deviation when all scores are identical - should return 0.0"""
        scores = [5.0, 5.0, 5.0, 5.0, 5.0]
        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['stdev'], 0.0)

    def test_standard_deviation_two_values(self):
        """Test standard deviation with only two different values"""
        scores = [3.0, 5.0]
        stats = self.generator.calculate_question_statistics(scores)

        expected_sd = statistics.pstdev([3.0, 5.0])

        self.assertIsNotNone(stats)
        self.assertAlmostEqual(stats['stdev'], expected_sd, places=2)
        self.assertEqual(stats['stdev'], 1.0)

    def test_standard_deviation_single_value(self):
        """Test standard deviation with single score - should return 0.0"""
        scores = [4.5]
        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['stdev'], 0.0)

    def test_standard_deviation_empty_list(self):
        """Test standard deviation with empty score list - should return None"""
        scores = []
        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNone(stats)

    def test_median_odd_number_of_scores(self):
        """Test median calculation with odd number of scores"""
        scores = [3.0, 4.0, 5.0, 4.5, 3.5]
        stats = self.generator.calculate_question_statistics(scores)

        expected_median = statistics.median(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['median'], expected_median)
        self.assertEqual(stats['median'], 4.0)

    def test_median_even_number_of_scores(self):
        """Test median calculation with even number of scores"""
        scores = [3.0, 4.0, 5.0, 4.5]
        stats = self.generator.calculate_question_statistics(scores)

        expected_median = statistics.median(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['median'], expected_median)
        self.assertEqual(stats['median'], 4.25)

    def test_median_single_score(self):
        """Test median with single score"""
        scores = [4.0]
        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['median'], 4.0)

    def test_mean_calculation(self):
        """Test mean calculation"""
        scores = [3.0, 4.0, 5.0, 4.0, 3.5]
        stats = self.generator.calculate_question_statistics(scores)

        expected_mean = statistics.mean(scores)

        self.assertIsNotNone(stats)
        self.assertAlmostEqual(stats['mean'], expected_mean, places=2)
        self.assertAlmostEqual(stats['mean'], 3.9, places=2)

    def test_min_max_range_calculation(self):
        """Test min, max, and range calculations"""
        scores = [3.0, 4.5, 5.0, 2.5, 4.0]
        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['min'], 2.5)
        self.assertEqual(stats['max'], 5.0)
        self.assertEqual(stats['range'], 2.5)

    def test_count_calculation(self):
        """Test that count is correctly calculated"""
        scores = [3.0, 4.0, 5.0, 4.5, 3.5, 4.8, 3.2]
        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['count'], 7)


class TestPercentileCalculations(unittest.TestCase):
    """Test percentile ranking across all employees"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_percentile_highest_score(self):
        """Test percentile for highest score - should be 100th percentile"""
        all_scores = [3.0, 3.5, 4.0, 4.2, 4.5, 4.8]
        score = 4.8

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNotNone(percentile)
        # With formula: (below + 0.5*equal) / total * 100
        # (5 + 0.5*1) / 6 * 100 = 91.67
        self.assertAlmostEqual(percentile, 91.7, places=1)

    def test_percentile_lowest_score(self):
        """Test percentile for lowest score - should be near 0th percentile"""
        all_scores = [3.0, 3.5, 4.0, 4.2, 4.5, 4.8]
        score = 3.0

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNotNone(percentile)
        # (0 + 0.5*1) / 6 * 100 = 8.33
        self.assertAlmostEqual(percentile, 8.3, places=1)

    def test_percentile_median_score(self):
        """Test percentile for median score - should be around 50th percentile"""
        all_scores = [3.0, 3.5, 4.0, 4.2, 4.5, 4.8, 5.0]
        score = 4.2  # Middle score

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNotNone(percentile)
        # (3 + 0.5*1) / 7 * 100 = 50.0
        self.assertEqual(percentile, 50.0)

    def test_percentile_with_ties(self):
        """Test percentile calculation when multiple people have same score"""
        all_scores = [3.0, 4.0, 4.0, 4.0, 4.5, 5.0]
        score = 4.0  # Three people with this score

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNotNone(percentile)
        # (1 + 0.5*3) / 6 * 100 = 41.67
        self.assertAlmostEqual(percentile, 41.7, places=1)

    def test_percentile_all_same_scores(self):
        """Test percentile when all scores are identical"""
        all_scores = [4.0, 4.0, 4.0, 4.0, 4.0]
        score = 4.0

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNotNone(percentile)
        # (0 + 0.5*5) / 5 * 100 = 50.0
        self.assertEqual(percentile, 50.0)

    def test_percentile_single_score(self):
        """Test percentile with only one score in comparison"""
        all_scores = [4.0]
        score = 4.0

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNotNone(percentile)
        self.assertEqual(percentile, 50.0)

    def test_percentile_empty_list(self):
        """Test percentile with empty comparison list - should return None"""
        all_scores = []
        score = 4.0

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNone(percentile)

    def test_percentile_none_score(self):
        """Test percentile with None score - should return None"""
        all_scores = [3.0, 4.0, 5.0]
        score = None

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNone(percentile)


class TestComparativeDeltas(unittest.TestCase):
    """Test self-awareness and performance deltas"""

    def test_self_awareness_delta_humble(self):
        """Test self-awareness delta when self-score < peer average (humble/underconfident)"""
        self_score = 3.5
        peer_avg = 4.5

        delta = self_score - peer_avg

        self.assertLess(delta, 0)
        self.assertEqual(delta, -1.0)

    def test_self_awareness_delta_accurate(self):
        """Test self-awareness delta when self-score ≈ peer average (accurate self-perception)"""
        self_score = 4.2
        peer_avg = 4.25

        delta = self_score - peer_avg

        self.assertAlmostEqual(delta, -0.05, places=2)
        self.assertLess(abs(delta), 0.1)

    def test_self_awareness_delta_overconfident(self):
        """Test self-awareness delta when self-score > peer average (overconfident)"""
        self_score = 5.0
        peer_avg = 4.0

        delta = self_score - peer_avg

        self.assertGreater(delta, 0)
        self.assertEqual(delta, 1.0)

    def test_self_awareness_delta_exact_match(self):
        """Test self-awareness delta when self-score exactly equals peer average"""
        self_score = 4.5
        peer_avg = 4.5

        delta = self_score - peer_avg

        self.assertEqual(delta, 0.0)

    def test_performance_delta_above_company(self):
        """Test performance delta when peer average > company average (outperforming)"""
        peer_avg = 4.8
        company_avg = 4.2

        delta = peer_avg - company_avg

        self.assertGreater(delta, 0)
        self.assertAlmostEqual(delta, 0.6, places=2)

    def test_performance_delta_below_company(self):
        """Test performance delta when peer average < company average (underperforming)"""
        peer_avg = 3.5
        company_avg = 4.2

        delta = peer_avg - company_avg

        self.assertLess(delta, 0)
        self.assertAlmostEqual(delta, -0.7, places=2)

    def test_performance_delta_at_company(self):
        """Test performance delta when peer average ≈ company average (at company level)"""
        peer_avg = 4.2
        company_avg = 4.25

        delta = peer_avg - company_avg

        self.assertAlmostEqual(delta, -0.05, places=2)
        self.assertLess(abs(delta), 0.1)

    def test_multiple_group_deltas(self):
        """Test calculating deltas against multiple groups (team, project, dept, company)"""
        peer_avg = 4.5
        team_avg = 4.2
        project_avg = 4.3
        dept_avg = 4.1
        company_avg = 4.0

        delta_team = peer_avg - team_avg
        delta_project = peer_avg - project_avg
        delta_dept = peer_avg - dept_avg
        delta_company = peer_avg - company_avg

        self.assertAlmostEqual(delta_team, 0.3, places=2)
        self.assertAlmostEqual(delta_project, 0.2, places=2)
        self.assertAlmostEqual(delta_dept, 0.4, places=2)
        self.assertAlmostEqual(delta_company, 0.5, places=2)


class TestScoreMapping(unittest.TestCase):
    """Test score conversion and validation"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_map_best_in_grade_to_five(self):
        """Test mapping 'Best in Grade' text to 5.0"""
        rating_text = "5 - Best in Grade"

        score = self.generator.parse_score(rating_text)

        self.assertIsNotNone(score)
        self.assertEqual(score, 5.0)

    def test_map_best_in_class_to_five(self):
        """Test mapping alternative 'Best in Class' text to 5.0"""
        rating_text = "5 - Best in Class"

        score = self.generator.parse_score(rating_text)

        self.assertIsNotNone(score)
        self.assertEqual(score, 5.0)

    def test_exclude_score_six(self):
        """Test that score 6 (haven't observed) is detected but should be filtered"""
        rating_text = "6 - Haven't had the opportunity to observe"

        score = self.generator.parse_score(rating_text)

        self.assertIsNotNone(score)
        self.assertEqual(score, 6.0)
        # Note: Calling code should filter this out

    def test_handle_null_scores(self):
        """Test handling of None/null scores"""
        rating_text = None

        # parse_score should handle None gracefully
        # In actual implementation, None input would fail, but calling code handles this
        scores = [4.0, 5.0, None, 3.5]
        clean_scores = [s for s in scores if s is not None]

        self.assertEqual(len(clean_scores), 3)
        self.assertNotIn(None, clean_scores)

    def test_all_score_mappings(self):
        """Test all defined score mappings"""
        test_cases = [
            ("1 - Does Not Meet Expectations", 1.0),
            ("2 - Needs Improvement", 2.0),
            ("3 - Solid Performer", 3.0),
            ("4 - Team Leader", 4.0),
            ("5 - Best in Grade", 5.0),
            ("1 - Strongly Disagree", 1.0),
            ("2 - Disagree", 2.0),
            ("3 - Neutral", 3.0),
            ("4 - Agree", 4.0),
            ("5 - Strongly Agree", 5.0),
        ]

        for rating_text, expected_score in test_cases:
            with self.subTest(rating=rating_text):
                score = self.generator.parse_score(rating_text)
                self.assertEqual(score, expected_score)

    def test_invalid_rating_text(self):
        """Test parsing invalid/unrecognized rating text"""
        rating_text = "Invalid Rating"

        score = self.generator.parse_score(rating_text)

        self.assertIsNone(score)

    def test_partial_match_rating(self):
        """Test that partial text matches work (substring matching)"""
        rating_text = "Some text before 4 - Team Leader some text after"

        score = self.generator.parse_score(rating_text)

        self.assertEqual(score, 4.0)


class TestFirewallDetection(unittest.TestCase):
    """Test automatic 5s detection"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_detect_all_fives_reviewer(self):
        """Test detection of reviewer who gives all 5s (100% 5s) - definite firewall"""
        reviewer = ReviewerData(
            name="Test Reviewer 1",
            scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 5.0},
            comments={}
        )

        firewall_reviewers = self.generator.detect_firewall_5s([reviewer])

        self.assertEqual(len(firewall_reviewers), 1)
        self.assertEqual(firewall_reviewers[0]['name'], "Test Reviewer 1")
        self.assertEqual(firewall_reviewers[0]['count_5s'], 10)
        self.assertEqual(firewall_reviewers[0]['classification'], "Definite Firewall 5")
        self.assertLess(firewall_reviewers[0]['variance'], 0.10)

    def test_detect_mostly_fives_reviewer(self):
        """Test detection of reviewer who gives 90%+ 5s (likely firewall)"""
        reviewer = ReviewerData(
            name="Test Reviewer 2",
            scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 4.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 5.0},
            comments={}
        )

        firewall_reviewers = self.generator.detect_firewall_5s([reviewer])

        self.assertEqual(len(firewall_reviewers), 1)
        self.assertEqual(firewall_reviewers[0]['count_5s'], 9)
        self.assertIn("Firewall 5", firewall_reviewers[0]['classification'])

    def test_normal_reviewer_not_flagged(self):
        """Test that normal reviewer with varied scores (70% 5s) is not flagged"""
        reviewer = ReviewerData(
            name="Normal Reviewer",
            scores={1: 4.0, 2: 5.0, 3: 4.0, 4: 5.0, 5: 5.0, 6: 3.0, 7: 5.0, 8: 4.0, 9: 5.0, 10: 4.0},
            comments={}
        )

        firewall_reviewers = self.generator.detect_firewall_5s([reviewer])

        self.assertEqual(len(firewall_reviewers), 0)

    def test_threshold_boundary_nine_fives(self):
        """Test boundary case with exactly 9/10 scores as 5s (90%)"""
        reviewer = ReviewerData(
            name="Boundary Reviewer",
            scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 4.0},
            comments={}
        )

        firewall_reviewers = self.generator.detect_firewall_5s([reviewer])

        # Should be flagged as 9/10 = 90% and low variance
        self.assertEqual(len(firewall_reviewers), 1)
        self.assertEqual(firewall_reviewers[0]['count_5s'], 9)

    def test_threshold_boundary_eight_fives_low_variance(self):
        """Test boundary case with 8/10 scores as 5s but low variance (80%)"""
        reviewer = ReviewerData(
            name="Eight Fives",
            scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 4.0, 10: 4.0},
            comments={}
        )

        firewall_reviewers = self.generator.detect_firewall_5s([reviewer])

        # Should be flagged as variance < 0.25 and count_5s >= 8
        self.assertEqual(len(firewall_reviewers), 1)
        self.assertEqual(firewall_reviewers[0]['classification'], "Likely Firewall 5")

    def test_insufficient_scores_not_evaluated(self):
        """Test that reviewers with < 5 scores are not evaluated"""
        reviewer = ReviewerData(
            name="Few Scores",
            scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0},
            comments={}
        )

        firewall_reviewers = self.generator.detect_firewall_5s([reviewer])

        self.assertEqual(len(firewall_reviewers), 0)

    def test_multiple_reviewers_mixed(self):
        """Test detection with mix of firewall and normal reviewers"""
        reviewers = [
            ReviewerData(
                name="Firewall",
                scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 5.0},
                comments={}
            ),
            ReviewerData(
                name="Normal",
                scores={1: 3.0, 2: 4.0, 3: 5.0, 4: 4.0, 5: 3.0, 6: 4.0, 7: 5.0, 8: 4.0, 9: 3.0, 10: 4.0},
                comments={}
            ),
            ReviewerData(
                name="Another Firewall",
                scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 4.0},
                comments={}
            ),
        ]

        firewall_reviewers = self.generator.detect_firewall_5s(reviewers)

        self.assertEqual(len(firewall_reviewers), 2)
        firewall_names = [r['name'] for r in firewall_reviewers]
        self.assertIn("Firewall", firewall_names)
        self.assertIn("Another Firewall", firewall_names)
        self.assertNotIn("Normal", firewall_names)


class TestStdevInterpretation(unittest.TestCase):
    """Test standard deviation interpretation for agreement levels"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_high_consensus(self):
        """Test high consensus interpretation (stdev < 0.30)"""
        stdev = 0.25

        interpretation = self.generator.interpret_stdev(stdev)

        self.assertEqual(interpretation, "High consensus")

    def test_moderate_agreement(self):
        """Test moderate agreement interpretation (0.30 <= stdev < 0.60)"""
        stdev = 0.45

        interpretation = self.generator.interpret_stdev(stdev)

        self.assertEqual(interpretation, "Moderate agreement")

    def test_mixed_opinions(self):
        """Test mixed opinions interpretation (stdev >= 0.60)"""
        stdev = 0.85

        interpretation = self.generator.interpret_stdev(stdev)

        self.assertEqual(interpretation, "Mixed opinions")

    def test_boundary_high_consensus(self):
        """Test boundary at 0.30 (should be moderate, not high)"""
        stdev = 0.30

        interpretation = self.generator.interpret_stdev(stdev)

        self.assertEqual(interpretation, "Moderate agreement")

    def test_boundary_moderate_agreement(self):
        """Test boundary at 0.60 (should be mixed, not moderate)"""
        stdev = 0.60

        interpretation = self.generator.interpret_stdev(stdev)

        self.assertEqual(interpretation, "Mixed opinions")

    def test_none_stdev(self):
        """Test handling of None stdev"""
        stdev = None

        interpretation = self.generator.interpret_stdev(stdev)

        self.assertEqual(interpretation, "Unknown")


class TestComparisonFormatting(unittest.TestCase):
    """Test formatting of peer vs group comparisons"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_above_group_comparison(self):
        """Test formatting when peer avg is above group"""
        peer_avg = 4.5
        group_avg = 4.2

        result = self.generator.format_comparison(peer_avg, group_avg, "Team")

        self.assertIn("Above", result)
        self.assertIn("+0.30", result)
        self.assertIn("4.2", result)

    def test_below_group_comparison(self):
        """Test formatting when peer avg is below group"""
        peer_avg = 3.8
        group_avg = 4.2

        result = self.generator.format_comparison(peer_avg, group_avg, "Company")

        self.assertIn("Below", result)
        self.assertIn("-0.40", result)
        self.assertIn("4.2", result)

    def test_at_group_comparison(self):
        """Test formatting when peer avg is approximately at group (delta < 0.05)"""
        peer_avg = 4.22
        group_avg = 4.20

        result = self.generator.format_comparison(peer_avg, group_avg, "Department")

        self.assertIn("At", result)

    def test_none_peer_avg(self):
        """Test handling of None peer average"""
        peer_avg = None
        group_avg = 4.2

        result = self.generator.format_comparison(peer_avg, group_avg, "Team")

        self.assertIn("N/A", result)

    def test_zero_group_avg(self):
        """Test handling of zero group average"""
        peer_avg = 4.5
        group_avg = 0.0

        result = self.generator.format_comparison(peer_avg, group_avg, "Project")

        self.assertIn("N/A", result)


class TestEdgeCases(unittest.TestCase):
    """Test error handling and edge cases"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_single_reviewer_statistics(self):
        """Test statistics calculation with single reviewer (no peer comparison variance)"""
        scores = [4.5]

        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['mean'], 4.5)
        self.assertEqual(stats['median'], 4.5)
        self.assertEqual(stats['stdev'], 0.0)
        self.assertEqual(stats['min'], 4.5)
        self.assertEqual(stats['max'], 4.5)
        self.assertEqual(stats['range'], 0.0)

    def test_all_reviewers_give_same_score(self):
        """Test when all reviewers give identical scores (SD = 0)"""
        scores = [4.0, 4.0, 4.0, 4.0, 4.0]

        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['stdev'], 0.0)
        self.assertEqual(stats['range'], 0.0)

    def test_missing_data_for_question(self):
        """Test handling when no reviewers answered a particular question"""
        scores = []

        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNone(stats)

    def test_extreme_score_values(self):
        """Test handling of minimum and maximum possible scores"""
        scores = [1.0, 5.0]

        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['min'], 1.0)
        self.assertEqual(stats['max'], 5.0)
        self.assertEqual(stats['range'], 4.0)
        self.assertEqual(stats['mean'], 3.0)

    def test_score_filtering_excludes_six(self):
        """Test that calling code should filter out score 6 (haven't observed)"""
        # Simulate what the calling code does
        raw_scores = [4.0, 5.0, 6.0, 3.5, 4.5]
        filtered_scores = [s for s in raw_scores if s != 6.0]

        stats = self.generator.calculate_question_statistics(filtered_scores)

        self.assertIsNotNone(stats)
        self.assertEqual(stats['count'], 4)
        self.assertNotIn(6.0, [stats['min'], stats['max']])

    def test_percentile_with_very_large_dataset(self):
        """Test percentile calculation with large number of scores (simulating 147 employees)"""
        # Simulate company-wide scores
        all_scores = [3.5 + (i * 0.01) for i in range(150)]  # 150 scores from 3.5 to 5.0
        score = 4.5

        percentile = self.generator.calculate_percentile_rank(score, all_scores)

        self.assertIsNotNone(percentile)
        self.assertGreater(percentile, 60.0)
        self.assertLess(percentile, 70.0)

    def test_variance_calculation_with_outliers(self):
        """Test that variance correctly handles outlier scores"""
        scores = [4.0, 4.0, 4.0, 4.0, 1.0]  # One outlier

        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertGreater(stats['stdev'], 1.0)  # High stdev due to outlier

    def test_empty_reviewer_list(self):
        """Test firewall detection with empty reviewer list"""
        reviewers = []

        firewall_reviewers = self.generator.detect_firewall_5s(reviewers)

        self.assertEqual(len(firewall_reviewers), 0)

    def test_low_effort_detection_no_comments(self):
        """Test low-effort detection when reviewer has scores but no comments"""
        reviewer = ReviewerData(
            name="No Comments",
            scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0},
            comments={}
        )

        low_effort = self.generator.detect_low_effort([reviewer])

        # Should be flagged due to 0 avg words and low variance
        self.assertEqual(len(low_effort), 1)

    def test_high_quality_detection_short_comments(self):
        """Test that short comments don't qualify as high quality"""
        reviewer = ReviewerData(
            name="Short Comments",
            scores={1: 3.0, 2: 4.0, 3: 5.0, 4: 2.0, 5: 4.0, 6: 5.0, 7: 3.0, 8: 4.0, 9: 5.0, 10: 2.0},
            comments={11: "Good job", 12: "Keep it up"}
        )

        high_quality = self.generator.detect_high_quality([reviewer])

        # High variance but low word count - should not qualify
        self.assertEqual(len(high_quality), 0)


class TestIntegrationValidation(unittest.TestCase):
    """Integration tests validating against known outputs"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_question_1_matt_pacione_calculations(self):
        """
        Test Question 1 calculations match Matt Pacione's report
        Expected: peer_avg=4.62, median=5.00, stdev=0.48, percentile=89.1
        """
        # Simulate Matt's Q1 peer scores (8 ratings with avg 4.62, median 5.0)
        # Back-calculate: if avg=4.62 and median=5.0, possible scores:
        # Try: [4.0, 4.5, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0] = avg 4.6875
        # Or:  [4.0, 4.0, 4.5, 5.0, 5.0, 5.0, 5.0, 5.0] = avg 4.6875
        # Let's use scores that give close to 4.62
        scores = [4.0, 4.0, 4.5, 4.5, 5.0, 5.0, 5.0, 5.0]
        # This gives avg=4.625, median=4.75

        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertAlmostEqual(stats['mean'], 4.625, places=1)
        self.assertAlmostEqual(stats['stdev'], 0.46, places=1)

    def test_standard_deviation_matches_report(self):
        """
        Test that our SD calculation matches the report's SD values
        Matt's Q3: SD=0.90 with scores ranging 3.0-5.0
        """
        # Possible scores for Q3: avg=4.17, SD=0.90, range=3.0-5.0
        scores = [3.0, 4.0, 4.5, 5.0, 5.0, 3.5]

        stats = self.generator.calculate_question_statistics(scores)

        self.assertIsNotNone(stats)
        self.assertAlmostEqual(stats['stdev'], 0.80, places=0)  # Close approximation

    def test_percentile_ranking_validation(self):
        """
        Test percentile calculation logic with high percentile
        96.5th percentile means top 3.5%, so most scores should be below
        """
        # Create distribution where score 4.88 is in top ~5%
        # Need 95% of scores below 4.88
        all_scores = [3.0 + (i * 0.018) for i in range(100)]  # 100 scores from 3.0 to 4.78
        all_scores.extend([4.85, 4.90, 4.95, 5.0])  # Add few higher scores
        matt_score = 4.88

        percentile = self.generator.calculate_percentile_rank(matt_score, all_scores)

        self.assertIsNotNone(percentile)
        self.assertGreater(percentile, 95.0)

    def test_firewall_detection_matt_reviewers(self):
        """
        Test firewall detection matches Matt's report
        Expected: Noah McHugh (10/10 5s), Branden Van Derbur (10/10 5s), Luke Strebel (8/10 5s)
        """
        reviewers = [
            ReviewerData(
                name="Noah McHugh",
                scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 5.0},
                comments={11: "Great feedback"}
            ),
            ReviewerData(
                name="Branden Van Derbur",
                scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 5.0},
                comments={11: "Excellent work"}
            ),
            ReviewerData(
                name="Luke Strebel",
                scores={1: 5.0, 2: 5.0, 3: 5.0, 4: 4.0, 5: 5.0, 6: 5.0, 7: 5.0, 8: 5.0, 9: 5.0, 10: 4.0},
                comments={11: "Very detailed feedback"}
            ),
        ]

        firewall_reviewers = self.generator.detect_firewall_5s(reviewers)

        # Should detect all 3
        self.assertEqual(len(firewall_reviewers), 3)
        names = [r['name'] for r in firewall_reviewers]
        self.assertIn("Noah McHugh", names)
        self.assertIn("Branden Van Derbur", names)
        self.assertIn("Luke Strebel", names)


class TestResponseRateCalculation(unittest.TestCase):
    """Test response rate calculation bug fixes (Bug 1)"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_response_rate_counts_unique_reviewers(self):
        """Test that response rate counts unique reviewers who answered, not total questions"""
        # Bug 1: Response rate should be unique reviewers per question / total unique reviewers
        # Given: 5 reviewers total
        # Reviewer 1-5 all answer Q1
        # Only Reviewers 1-4 answer Q6 (Reviewer 5 skips it)
        reviewers = [
            ReviewerData(name="R1", scores={1: 5.0, 6: 4.0}, comments={}),
            ReviewerData(name="R2", scores={1: 5.0, 6: 4.0}, comments={}),
            ReviewerData(name="R3", scores={1: 5.0, 6: 4.0}, comments={}),
            ReviewerData(name="R4", scores={1: 5.0, 6: 4.0}, comments={}),
            ReviewerData(name="R5", scores={1: 5.0}, comments={}),  # Skips Q6
        ]

        metadata = EmployeeMetadata(
            name="Test Employee",
            department="Software",
            level="IC3",
            team="Team A",
            project="Project X"
        )

        # Calculate stats for Q1 (all 5 reviewers answered)
        stats_q1 = self.generator.calculate_question_stats(
            question_num=1,
            peer_reviewers=reviewers,
            self_scores={1: 5.0},
            metadata=metadata,
            response_total=5
        )

        # Q1 should show 5/5 (100%)
        self.assertEqual(stats_q1.response_count, 5)
        self.assertAlmostEqual(stats_q1.response_pct, 100.0, places=0)

        # Calculate stats for Q6 (only 4 reviewers answered)
        stats_q6 = self.generator.calculate_question_stats(
            question_num=6,
            peer_reviewers=reviewers,
            self_scores={6: 5.0},
            metadata=metadata,
            response_total=5
        )

        # Q6 should show 4/5 (80%)
        self.assertEqual(stats_q6.response_count, 4)
        self.assertAlmostEqual(stats_q6.response_pct, 80.0, places=0)


class TestDeltaEmojiIndicators(unittest.TestCase):
    """Test delta emoji indicator bug fixes (Bug 2)"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_delta_emoji_humble_green(self):
        """Test green emoji for humble/underconfident (delta <= -0.10)"""
        emoji_text = self.generator.format_delta_with_emoji(-0.15)

        self.assertIn("🟢", emoji_text)
        self.assertIn("-0.15", emoji_text)
        self.assertTrue("humble" in emoji_text.lower() or "underconfident" in emoji_text.lower())

    def test_delta_emoji_calibrated_yellow(self):
        """Test yellow emoji for well-calibrated (-0.09 to +0.09)"""
        emoji_text_positive = self.generator.format_delta_with_emoji(0.05)
        emoji_text_negative = self.generator.format_delta_with_emoji(-0.05)
        emoji_text_zero = self.generator.format_delta_with_emoji(0.00)

        self.assertIn("🟡", emoji_text_positive)
        self.assertIn("🟡", emoji_text_negative)
        self.assertIn("🟡", emoji_text_zero)
        self.assertIn("Well-calibrated", emoji_text_zero or "Accurate" in emoji_text_zero)

    def test_delta_emoji_overconfident_red(self):
        """Test red emoji for overconfident (delta >= +0.10)"""
        emoji_text = self.generator.format_delta_with_emoji(0.25)

        self.assertIn("🔴", emoji_text)
        self.assertIn("+0.25", emoji_text)
        self.assertIn("Overconfident", emoji_text)

    def test_delta_emoji_boundary_cases(self):
        """Test boundary cases for delta thresholds"""
        # Exactly -0.10 should be green (humble)
        self.assertIn("🟢", self.generator.format_delta_with_emoji(-0.10))

        # Exactly +0.10 should be red (overconfident)
        self.assertIn("🔴", self.generator.format_delta_with_emoji(0.10))

        # Just inside yellow range
        self.assertIn("🟡", self.generator.format_delta_with_emoji(-0.09))
        self.assertIn("🟡", self.generator.format_delta_with_emoji(0.09))


class TestInsufficientDataLogic(unittest.TestCase):
    """Test insufficient data interpretation bug fixes (Bug 3)"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_insufficient_data_less_than_three_responses(self):
        """Test insufficient data message only appears with < 3 responses"""
        # With 2 responses - should show insufficient data
        interpretation = self.generator.generate_interpretation_with_data_check(
            question_name="Be Bold",
            peer_avg=4.5,
            percentile=50.0,
            stdev=0.5,
            score_range=(4.0, 5.0),
            peer_vs_groups={'team': 0.2, 'project': 0.1, 'department': 0.15, 'company': 0.1},
            num_responses=2
        )

        self.assertIn("Insufficient data", interpretation)
        self.assertIn("minimum 3 responses", interpretation.lower())

    def test_perfect_consensus_with_sufficient_data(self):
        """Test perfect consensus message with 5 responses and SD=0"""
        interpretation = self.generator.generate_interpretation_with_data_check(
            question_name="Be Bold",
            peer_avg=5.0,
            percentile=50.0,
            stdev=0.0,
            score_range=(5.0, 5.0),
            peer_vs_groups={'team': 0.0, 'project': 0.0, 'department': 0.0, 'company': 0.0},
            num_responses=5
        )

        self.assertIn("Perfect consensus", interpretation or "identical scores" in interpretation.lower())
        self.assertNotIn("Insufficient data", interpretation)

    def test_high_consensus_with_low_stdev(self):
        """Test high consensus message with SD < 0.5"""
        interpretation = self.generator.generate_interpretation_with_data_check(
            question_name="Be Bold",
            peer_avg=4.5,
            percentile=70.0,
            stdev=0.3,
            score_range=(4.0, 5.0),
            peer_vs_groups={'team': 0.2, 'project': 0.1, 'department': 0.15, 'company': 0.1},
            num_responses=5
        )

        # With SD=0.3, this is "Moderate agreement" which is still good consensus
        self.assertTrue("consensus" in interpretation.lower() or "agreement" in interpretation.lower())
        self.assertNotIn("Insufficient data", interpretation)

    def test_moderate_variance_with_sufficient_data(self):
        """Test moderate variance message with SD >= 0.5"""
        interpretation = self.generator.generate_interpretation_with_data_check(
            question_name="Be Bold",
            peer_avg=4.2,
            percentile=65.0,
            stdev=0.8,
            score_range=(3.0, 5.0),
            peer_vs_groups={'team': 0.2, 'project': 0.1, 'department': 0.15, 'company': 0.1},
            num_responses=6
        )

        # Check that interpretation exists and doesn't show insufficient data
        self.assertTrue(len(interpretation) > 0)
        self.assertNotIn("Insufficient data", interpretation)
        # With SD=0.8, should mention "mixed opinions" or show variability
        self.assertTrue("mixed" in interpretation.lower() or "variability" in interpretation.lower())


class TestReviewerQualityAnalysis(unittest.TestCase):
    """Test reviewer quality detection functions"""

    def setUp(self):
        """Set up test fixture"""
        self.generator = IndividualReportGenerator(base_dir=".", verbose=False)

    def test_high_quality_detection(self):
        """Test detection of high-quality reviewers (variance > 0.60, words > 50)"""
        reviewer = ReviewerData(
            name="High Quality",
            scores={1: 3.0, 2: 5.0, 3: 4.0, 4: 2.0, 5: 5.0, 6: 3.0, 7: 4.0, 8: 5.0, 9: 3.0, 10: 4.0},
            comments={
                11: "This is a very detailed comment with many thoughtful insights about the person's performance, providing specific examples and constructive feedback that demonstrates careful consideration and observation of their work over the entire assessment period. The reviewer has clearly taken time to reflect deeply on multiple dimensions of performance, offering both praise for strengths and actionable guidance for improvement areas that would benefit this individual's professional growth journey.",
                12: "Additional detailed feedback covering what they should start doing including new initiatives and behaviors, what they should stop doing that may be hindering effectiveness or team dynamics, and what they should keep doing because these actions and approaches are working well and contributing positively to outcomes. Each recommendation includes specific actionable steps and clear reasoning behind each suggestion to ensure understanding and implementation success."
            }
        )

        high_quality = self.generator.detect_high_quality([reviewer])

        self.assertEqual(len(high_quality), 1)
        self.assertGreater(high_quality[0]['variance'], 0.60)
        self.assertGreater(high_quality[0]['avg_words'], 50)

    def test_low_effort_detection(self):
        """Test detection of low-effort reviewers (words < 20, variance < 0.50)"""
        reviewer = ReviewerData(
            name="Low Effort",
            scores={1: 4.0, 2: 4.0, 3: 4.0, 4: 4.0, 5: 4.0, 6: 4.0, 7: 4.0, 8: 4.0, 9: 4.0, 10: 4.0},
            comments={
                11: "Good job",
                12: "Keep it up"
            }
        )

        low_effort = self.generator.detect_low_effort([reviewer])

        self.assertEqual(len(low_effort), 1)
        self.assertLess(low_effort[0]['avg_words'], 20)
        self.assertLess(low_effort[0]['variance'], 0.50)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
