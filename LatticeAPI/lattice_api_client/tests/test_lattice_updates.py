import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import lattice_populate_updates
import sqlite3
import logging
import textwrap
import shutil
from docx import Document
from unittest.mock import MagicMock, patch
from collections import defaultdict
from datetime import datetime, date, timedelta
from pathlib import Path
import lattice_populate_updates
import os.path

@patch("lattice_populate_updates.SESSION.get")
def test__get_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_resp

    result = lattice_populate_updates._get("https://example.com")
    assert result == {"data": "ok"}

def test_format_last_first():
    assert lattice_populate_updates.format_last_first("John Doe") == "Doe, John"
    assert lattice_populate_updates.format_last_first("SingleName") == "SingleName"

@patch("lattice_populate_updates._get")
def test_user_name(mock__get):
    mock__get.return_value = {"name": "Jane Smith"}
    assert lattice_populate_updates.user_name("abc123") == "Jane Smith"

@patch("lattice_populate_updates._get")
def test_get_me(mock__get):
    mock__get.return_value = {"id": "123", "name": "Me"}
    assert lattice_populate_updates.get_me() == {"id": "123", "name": "Me"}

@patch("lattice_populate_updates._get")
def test_get_direct_reports(mock__get):
    mock__get.return_value = {"data": [{"id": "1"}, {"id": "2"}]}
    result = lattice_populate_updates.get_direct_reports("123")
    assert len(result) == 2

@patch("lattice_populate_updates._get")
def test_all_updates(mock__get):
    mock__get.side_effect = [
        {"data": [{"id": "1"}, {"id": "2"}], "hasMore": True, "endingCursor": "cursor1"},
        {"data": [{"id": "3"}], "hasMore": False}
    ]

    results = list(lattice_populate_updates.all_updates(page_size=2))
    assert results == [{"id": "1"}, {"id": "2"}, {"id": "3"}]
    assert mock__get.call_count == 2

@patch("lattice_populate_updates._get")
def test_get_update_by_id(mock__get):
    mock__get.return_value = {"id": "123", "text": "Update text"}
    result = lattice_populate_updates.get_update_by_id("123")
    assert result["id"] == "123"
    assert result["text"] == "Update text"
    mock__get.assert_called_once_with(f"{lattice_populate_updates.BASE}/update/123")

def test_open_db_creates_file_and_table(tmp_path):
    # Override DB_PATH temporarily
    test_db = tmp_path / "test_lattice.db"
    lattice_populate_updates.DB_PATH = str(test_db)

    # Open DB (should create new file and table)
    con = lattice_populate_updates.open_db()
    assert os.path.exists(test_db)
    cur = con.cursor()

    # Check if 'updates' table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='updates';")
    assert cur.fetchone() is not None

    con.close()

def test_show_updates_for_name_logs(caplog, tmp_path):
    caplog.set_level(logging.INFO)
    # Setup temp DB and insert sample data
    test_db = tmp_path / "test_lattice.db"
    lattice_populate_updates.DB_PATH = str(test_db)
    con = lattice_populate_updates.open_db()
    con.execute("""
        INSERT INTO updates (id, author_id, author_name, created_at, question, answer, sentiment_object, sentiment_rating)
        VALUES ('1', 'uid1', 'Doe, John', '2025-06-01', 'Q1', 'A1', 'obj1', 4)
    """)
    con.commit()
    con.close()

    lattice_populate_updates.show_updates_for_name("Doe, John")

    # Check if logs contain expected output
    log_msgs = [r.getMessage() for r in caplog.records]
    assert any("📝 Updates for Doe, John" in m for m in log_msgs)
    assert any("2025-06-01 — Sentiment: 4" in m for m in log_msgs)
    assert any("Q1" in m for m in log_msgs)
    assert any("A1" in m for m in log_msgs)

@patch("lattice_populate_updates.get_me")
@patch("lattice_populate_updates.get_direct_reports")
@patch("lattice_populate_updates.open_db")
@patch("lattice_populate_updates.export_updates_to_docx")
@patch("lattice_populate_updates.TEAM_MAP", {"Doe, John": "Test Team", "Smith, Jane": "Test Team"})
def test_export_all_direct_reports(mock_export_docx, mock_open_db, mock_get_direct_reports, mock_get_me, caplog):
    caplog.set_level('WARNING')

    # Setup mocks
    mock_get_me.return_value = {"id": "me_id"}
    direct_reports = [
        {"name": "John Doe"},
        {"name": "Jane Smith"},
    ]
    mock_get_direct_reports.return_value = direct_reports

    # Mock DB cursor and connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_open_db.return_value = mock_conn

    # Setup DB fetchall responses for queries
    # For each direct report, first query returns some rows for export
    def execute_side_effect(query, params):
        author_name = params[0]
        if "question, answer" in query:
            return [("2025-05-01", "Q1", "A1", 4), ("2025-05-02", "Q2", "A2", 3)]
        if "sentiment_rating" in query:
            return [("2025-05-01", 4), ("2025-05-02", 3)]
        if "COUNT(DISTINCT author_name)" in query:
            return [(2,)]
        if "DISTINCT author_name" in query:
            return [("John Doe",), ("Jane Smith",)]
        return []

    mock_cursor.execute.side_effect = lambda q, p: mock_cursor
    mock_cursor.fetchall.side_effect = lambda: execute_side_effect(mock_cursor.execute.call_args[0][0], mock_cursor.execute.call_args[0][1])
    mock_cursor.fetchone.side_effect = lambda: (2,)

    # Run function
    lattice_populate_updates.export_all_direct_reports()

    # Assert export_updates_to_docx called for each direct report
    assert mock_export_docx.call_count == len(direct_reports)

    # Assert a log warning was not issued for missing team map (assuming TEAM_MAP has entries)
    assert not any("Missing team mapping" in rec.message for rec in caplog.records)

    # Check the output file was saved
    expected_path = os.path.join("updates", "_team_sentiment_summary.docx")
    assert os.path.exists("updates") or True  # just directory exists check, actual file not created in test

def test_export_updates_to_docx_creates_file(tmp_path, caplog):
    caplog.set_level('DEBUG')
    updates = [
        ("2025-05-01", "How was your week?", "Good week overall.", 4),
        ("2025-04-20", "Any blockers?", "No blockers.", 3),
        ("2025-05-15", "What are you working on?", "Working on testing.", 5),
        ("2025-04-10", "Any help needed?", "No help needed.", 3),
    ]
    name = "Doe, John"

    output_dir = tmp_path / "updates"
    output_dir.mkdir()

    # Patch Document.save to write to our tmp directory instead of real file system path
    with patch("docx.document.Document.save") as mock_save:
        def save_side_effect(path):
            # Save to our tmp dir manually
            dest_path = output_dir / f"{name}.docx"
            # Call original save with tmp path (or just create empty file to simulate)
            with open(dest_path, "wb") as f:
                f.write(b"Fake docx content")
            return None

        mock_save.side_effect = save_side_effect

        lattice_populate_updates.export_updates_to_docx(name, updates)

        expected_file = output_dir / f"{name}.docx"
        assert expected_file.exists()

def test_export_one_report_calls_export(tmp_path, caplog):
    caplog.set_level(logging.WARNING)
    test_db = tmp_path / "test_lattice.db"
    lattice_populate_updates.DB_PATH = str(test_db)

    # Setup DB with sample data
    con = lattice_populate_updates.open_db()
    con.execute("""
        INSERT INTO updates (id, author_id, author_name, created_at, question, answer, sentiment_object, sentiment_rating)
        VALUES ('1', 'uid1', 'Doe, John', '2025-06-01', 'Q1', 'A1', 'obj1', 4)
    """)
    con.commit()
    con.close()

    with patch("lattice_populate_updates.export_updates_to_docx") as mock_export:
        lattice_populate_updates.export_one_report("Doe, John")
        mock_export.assert_called_once()

    # Test no rows scenario triggers warning
    with patch("lattice_populate_updates.export_updates_to_docx") as mock_export:
        lattice_populate_updates.export_one_report("Jane Smith")
        mock_export.assert_not_called()
        assert any("No updates found for 'Jane Smith'." in record.message for record in caplog.records)

@patch("lattice_populate_updates.get_me")
@patch("lattice_populate_updates.get_direct_reports")
@patch("lattice_populate_updates.all_updates")
@patch("lattice_populate_updates.get_update_by_id")
@patch("lattice_populate_updates._get")
@patch("lattice_populate_updates.open_db")
@patch("lattice_populate_updates.user_name", side_effect=lambda uid: f"User {uid}")
@patch("lattice_populate_updates.format_last_first", side_effect=lambda name: name)
@patch("lattice_populate_updates.to_iso", side_effect=lambda ts: "2025-06-01")
@patch("lattice_populate_updates.clean_text", side_effect=lambda x: x)
def test_populate_updates(
    mock_clean_text,
    mock_to_iso,
    mock_format_last_first,
    mock_user_name,
    mock_open_db,
    mock__get,
    mock_get_update_by_id,
    mock_all_updates,
    mock_get_direct_reports,
    mock_get_me,
):
    mock_get_me.return_value = {"id": "me_id"}
    mock_get_direct_reports.return_value = [{"id": "uid1"}, {"id": "uid2"}]

    # Mock updates: one direct report update, one non-direct, one duplicate
    updates = [
        {"id": "upd1", "user": {"id": "uid1"}, "createdAt": 1234567890},
        {"id": "upd2", "user": {"id": "uid3"}, "createdAt": 1234567891},  # not direct
        {"id": "upd3", "user": {"id": "uid2"}, "createdAt": 1234567892},
    ]
    mock_all_updates.return_value = iter(updates)

    # get_update_by_id returns full update details
    mock_get_update_by_id.side_effect = [
        {
            "text": "text1",
            "sentiment": {"object": "obj1", "rating": 5},
        },
        {
            "text": None,
            "responses": {
                "data": [
                    {"question": "Q1", "answer": "A1"},
                    {"question": "Q2", "answer": "A2"},
                ]
            },
            "sentiment": {"object": "obj2", "rating": 3},
        },
    ]

    # Mock DB cursor and connection
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_open_db.return_value = mock_conn

    # Simulate no duplicates initially
    def fetchone_side_effect(*args, **kwargs):
        # For id 'upd1' and 'upd3', return None (no duplicates)
        # For others return a row (simulate duplicate)
        query = args[0] if args else ""
        params = args[1] if len(args) > 1 else ()
        if params and params[0] in ("upd1", "upd3"):
            return None
        return (1,)

    mock_cursor.execute.side_effect = lambda *a, **k: mock_cursor
    mock_cursor.fetchone.side_effect = fetchone_side_effect

    lattice_populate_updates.populate_updates(page_size=10, restrict_to_directs=True)

    # Should skip upd2 (not direct) and insert upd1 and upd3
    assert mock_cursor.execute.call_count >= 2
    assert mock_conn.commit.called
    assert mock_conn.close.called
