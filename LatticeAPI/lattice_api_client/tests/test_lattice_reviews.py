# tests/test_lattice_api.py
import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lattice_reviews import get_user_by_id

@patch("lattice_reviews._get")
def test_get_user_by_id(mock_get):
    mock_get.return_value = {"id": "abc123", "name": "Test User"}
    user = get_user_by_id("abc123")
    assert user["id"] == "abc123"
    assert user["name"] == "Test User"

@patch("lattice_reviews._get")
def test_get_question_by_id(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"id": "q1", "body": "Sample question"}
    
    from lattice_reviews import get_question_by_id
    result = get_question_by_id("q1")

    assert result["id"] == "q1"
    assert result["body"] == "Sample question"

@patch("lattice_reviews._get")
def test_get_reviews_for_reviewee(mock_get):
    mock_response_page1 = {
        "data": [{"id": "r1"}],
        "hasMore": True,
        "endingCursor": "cursor1"
    }
    mock_response_page2 = {
        "data": [{"id": "r2"}],
        "hasMore": False
    }
    mock_get.side_effect = [mock_response_page1, mock_response_page2]

    from lattice_reviews import get_reviews_for_reviewee
    reviews = get_reviews_for_reviewee("user123")

    assert len(reviews) == 2
    assert reviews[0]["id"] == "r1"
    assert reviews[1]["id"] == "r2"


@patch("lattice_reviews._get")
def test_get_reviewee_by_id(mock_get):
    mock_response = {"id": "reviewee123", "user": {"id": "user456"}}
    mock_get.return_value = mock_response  # Correct mock response

    from lattice_reviews import get_reviewee_by_id
    result = get_reviewee_by_id("reviewee123")

    assert result["id"] == "reviewee123"
    assert result["user"]["id"] == "user456"


@patch("lattice_reviews._get")
def test_get_question_by_id(mock_get):
    mock_get.return_value = {"id": "q123", "body": "How do you embody our values?"}
    
    from lattice_reviews import get_question_by_id
    result = get_question_by_id("q123")

    assert result["id"] == "q123"


@patch("lattice_reviews._get")
def test_get_reviewees_for_cycle(mock_get):
    mock_response_page1 = {
        "data": [{"id": "rev1"}, {"id": "rev2"}],
        "hasMore": True,
        "endingCursor": "cursor1"
    }
    mock_response_page2 = {
        "data": [{"id": "rev3"}],
        "hasMore": False
    }
    # Provide side_effect as simple dicts, enough calls to cover pagination
    mock_get.side_effect = [
        mock_response_page1,
        mock_response_page2,
    ]

    from lattice_reviews import get_reviewees_for_cycle
    result = get_reviewees_for_cycle("cycle123")

    assert len(result) == 3
    assert result[0]["id"] == "rev1"
    assert result[2]["id"] == "rev3"

from lattice_reviews import get_fuzzy_key

@pytest.mark.parametrize("input_text, expected_key", [
    ("Shows a growth mindset", "growth"),
    ("Demonstrates feedback loops", "feedback"),
    ("Communicates effectively", "communication"),
    ("Would rehire this person", "rehire"),
    ("Unmatched text", "other"),
])
def test_get_fuzzy_key(input_text, expected_key):
    assert get_fuzzy_key(input_text) == expected_key

from lattice_reviews import find_user_by_name

def test_find_user_by_name():
    users = [
        {"name": "Alice Smith"},
        {"name": "Bob Jones"},
    ]
    result = find_user_by_name("alice smith", users)
    assert result["name"] == "Alice Smith"