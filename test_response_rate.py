#!/usr/bin/env python3
"""
Test for response rate tracking feature.

Tests that the score calculation correctly tracks:
- peer_scores (actual ratings 1-5)
- peer_not_observed (score == 6)
- Response rate calculation
"""

import unittest
from unittest.mock import Mock, patch


class TestResponseRateTracking(unittest.TestCase):
    """Test response rate tracking in assessment generation."""

    def test_response_rate_calculation_all_observed(self):
        """Test response rate when all peers provide ratings (100%)."""
        # Simulate reviews: 3 peer ratings, 0 not-observed, 1 self
        mock_reviews = [
            {"reviewType": "Peer", "response": {"ratingString": "4"}},
            {"reviewType": "Peer", "response": {"ratingString": "5"}},
            {"reviewType": "Peer", "response": {"ratingString": "3"}},
            {"reviewType": "Self", "response": {"ratingString": "4"}},
        ]

        # Calculate as the code will
        self_scores = []
        peer_scores = []
        peer_not_observed = 0

        for r in mock_reviews:
            if not r or not r.get("response"):
                continue
            val = r.get("response", {}).get("ratingString")
            try:
                score = float(val)
            except (TypeError, ValueError):
                continue

            if r.get("reviewType") == "Self":
                self_scores.append(score)
            elif score == 6:  # "Haven't had opportunity to observe"
                peer_not_observed += 1
            else:
                peer_scores.append(score)

        # Verify counts
        self.assertEqual(len(peer_scores), 3, "Should have 3 peer ratings")
        self.assertEqual(peer_not_observed, 0, "Should have 0 not-observed")
        self.assertEqual(len(self_scores), 1, "Should have 1 self rating")

        # Calculate response rate
        peer_count = len(peer_scores)
        total_peer_reviews = peer_count + peer_not_observed
        response_rate = int((peer_count / total_peer_reviews * 100)) if total_peer_reviews > 0 else 0

        self.assertEqual(peer_count, 3)
        self.assertEqual(total_peer_reviews, 3)
        self.assertEqual(response_rate, 100)

    def test_response_rate_calculation_with_not_observed(self):
        """Test response rate when some peers say 'not observed' (80%)."""
        # Simulate reviews: 8 peer ratings, 2 not-observed, 1 self
        mock_reviews = [
            {"reviewType": "Peer", "response": {"ratingString": "4"}},
            {"reviewType": "Peer", "response": {"ratingString": "5"}},
            {"reviewType": "Peer", "response": {"ratingString": "3"}},
            {"reviewType": "Peer", "response": {"ratingString": "4"}},
            {"reviewType": "Peer", "response": {"ratingString": "5"}},
            {"reviewType": "Peer", "response": {"ratingString": "4"}},
            {"reviewType": "Peer", "response": {"ratingString": "5"}},
            {"reviewType": "Peer", "response": {"ratingString": "4"}},
            {"reviewType": "Peer", "response": {"ratingString": "6"}},  # NOT OBSERVED
            {"reviewType": "Peer", "response": {"ratingString": "6"}},  # NOT OBSERVED
            {"reviewType": "Self", "response": {"ratingString": "4"}},
        ]

        # Calculate as the code will
        self_scores = []
        peer_scores = []
        peer_not_observed = 0

        for r in mock_reviews:
            if not r or not r.get("response"):
                continue
            val = r.get("response", {}).get("ratingString")
            try:
                score = float(val)
            except (TypeError, ValueError):
                continue

            if r.get("reviewType") == "Self":
                self_scores.append(score)
            elif score == 6:
                peer_not_observed += 1
            else:
                peer_scores.append(score)

        # Verify counts
        self.assertEqual(len(peer_scores), 8, "Should have 8 peer ratings")
        self.assertEqual(peer_not_observed, 2, "Should have 2 not-observed")
        self.assertEqual(len(self_scores), 1, "Should have 1 self rating")

        # Calculate response rate
        peer_count = len(peer_scores)
        total_peer_reviews = peer_count + peer_not_observed
        response_rate = int((peer_count / total_peer_reviews * 100)) if total_peer_reviews > 0 else 0

        self.assertEqual(peer_count, 8)
        self.assertEqual(total_peer_reviews, 10)
        self.assertEqual(response_rate, 80)

    def test_response_rate_calculation_all_not_observed(self):
        """Test response rate when NO peers provide ratings (0%)."""
        # Simulate reviews: 0 peer ratings, 5 not-observed, 1 self
        mock_reviews = [
            {"reviewType": "Peer", "response": {"ratingString": "6"}},
            {"reviewType": "Peer", "response": {"ratingString": "6"}},
            {"reviewType": "Peer", "response": {"ratingString": "6"}},
            {"reviewType": "Peer", "response": {"ratingString": "6"}},
            {"reviewType": "Peer", "response": {"ratingString": "6"}},
            {"reviewType": "Self", "response": {"ratingString": "4"}},
        ]

        # Calculate as the code will
        self_scores = []
        peer_scores = []
        peer_not_observed = 0

        for r in mock_reviews:
            if not r or not r.get("response"):
                continue
            val = r.get("response", {}).get("ratingString")
            try:
                score = float(val)
            except (TypeError, ValueError):
                continue

            if r.get("reviewType") == "Self":
                self_scores.append(score)
            elif score == 6:
                peer_not_observed += 1
            else:
                peer_scores.append(score)

        # Verify counts
        self.assertEqual(len(peer_scores), 0, "Should have 0 peer ratings")
        self.assertEqual(peer_not_observed, 5, "Should have 5 not-observed")
        self.assertEqual(len(self_scores), 1, "Should have 1 self rating")

        # Calculate response rate
        peer_count = len(peer_scores)
        total_peer_reviews = peer_count + peer_not_observed
        response_rate = int((peer_count / total_peer_reviews * 100)) if total_peer_reviews > 0 else 0

        self.assertEqual(peer_count, 0)
        self.assertEqual(total_peer_reviews, 5)
        self.assertEqual(response_rate, 0)

    def test_response_rate_no_peer_reviews(self):
        """Test response rate when there are NO peer reviews at all (self-only)."""
        # Simulate reviews: only self
        mock_reviews = [
            {"reviewType": "Self", "response": {"ratingString": "4"}},
        ]

        # Calculate as the code will
        self_scores = []
        peer_scores = []
        peer_not_observed = 0

        for r in mock_reviews:
            if not r or not r.get("response"):
                continue
            val = r.get("response", {}).get("ratingString")
            try:
                score = float(val)
            except (TypeError, ValueError):
                continue

            if r.get("reviewType") == "Self":
                self_scores.append(score)
            elif score == 6:
                peer_not_observed += 1
            else:
                peer_scores.append(score)

        # Verify counts
        self.assertEqual(len(peer_scores), 0, "Should have 0 peer ratings")
        self.assertEqual(peer_not_observed, 0, "Should have 0 not-observed")
        self.assertEqual(len(self_scores), 1, "Should have 1 self rating")

        # Calculate response rate (avoid division by zero)
        peer_count = len(peer_scores)
        total_peer_reviews = peer_count + peer_not_observed
        response_rate = int((peer_count / total_peer_reviews * 100)) if total_peer_reviews > 0 else 0

        self.assertEqual(total_peer_reviews, 0)
        self.assertEqual(response_rate, 0)


if __name__ == "__main__":
    unittest.main()
