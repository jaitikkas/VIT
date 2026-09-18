"""
Unit tests for the borrow / return logic.
Uses a temporary on-disk SQLite database so each test suite gets a fresh, isolated DB.
"""

import os
import sys
import tempfile
import unittest
from datetime import date, timedelta

# Ensure project root is on sys.path so imports resolve correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import database as db  # noqa: E402


class BorrowReturnTestCase(unittest.TestCase):
    """Base class that sets up a fresh temp DB with sample data."""

    def setUp(self):
        """Create a temp DB file, init tables, and insert one member + one book."""
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        db.initialize_db(self.db_path)
        self.member_id = db.add_member(
            "Alice Smith", "alice@example.com", "1234567890",
            date.today().isoformat(), db_path=self.db_path,
        )
        self.book_id = db.add_book(
            "Clean Code", "Robert C. Martin", "9780132350884", 3,
            db_path=self.db_path,
        )

    def tearDown(self):
        """Remove the temp DB file."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    # ------------------------------------------------------------------ #
    # Test 1 — Successful issue reduces available_copies
    # ------------------------------------------------------------------ #
    def test_issue_reduces_available_copies(self):
        issue_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=14)).isoformat()

        borrow_id = db.issue_book(
            self.member_id, self.book_id, issue_date, due_date,
            db_path=self.db_path,
        )
        self.assertIsNotNone(borrow_id)

        book = db.get_book_by_id(self.book_id, db_path=self.db_path)
        self.assertEqual(book["available_copies"], 2,
                         "Available copies should decrease by 1 after issuing.")

    # ------------------------------------------------------------------ #
    # Test 2 — Return restores available_copies & detects overdue
    # ------------------------------------------------------------------ #
    def test_return_restores_copies_and_detects_overdue(self):
        issue_date = (date.today() - timedelta(days=20)).isoformat()
        due_date = (date.today() - timedelta(days=6)).isoformat()   # already past

        borrow_id = db.issue_book(
            self.member_id, self.book_id, issue_date, due_date,
            db_path=self.db_path,
        )

        return_date = date.today().isoformat()
        result = db.return_book(borrow_id, return_date, db_path=self.db_path)

        self.assertTrue(result["overdue"],
                        "Book returned after due date should be flagged overdue.")
        self.assertGreater(result["days_overdue"], 0)

        book = db.get_book_by_id(self.book_id, db_path=self.db_path)
        self.assertEqual(book["available_copies"], 3,
                         "Available copies should restore after return.")

    # ------------------------------------------------------------------ #
    # Test 3 — Cannot issue when no copies are available
    # ------------------------------------------------------------------ #
    def test_issue_fails_when_no_copies(self):
        # Issue all 3 copies
        for _ in range(3):
            db.issue_book(
                self.member_id, self.book_id,
                date.today().isoformat(),
                (date.today() + timedelta(days=14)).isoformat(),
                db_path=self.db_path,
            )

        with self.assertRaises(ValueError):
            db.issue_book(
                self.member_id, self.book_id,
                date.today().isoformat(),
                (date.today() + timedelta(days=14)).isoformat(),
                db_path=self.db_path,
            )

    # ------------------------------------------------------------------ #
    # Test 4 — On-time return is not flagged overdue
    # ------------------------------------------------------------------ #
    def test_on_time_return_not_overdue(self):
        issue_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=14)).isoformat()

        borrow_id = db.issue_book(
            self.member_id, self.book_id, issue_date, due_date,
            db_path=self.db_path,
        )

        # Return on the due date itself
        result = db.return_book(borrow_id, due_date, db_path=self.db_path)
        self.assertFalse(result["overdue"],
                         "Return on due date should NOT be overdue.")
        self.assertEqual(result["days_overdue"], 0)

    # ------------------------------------------------------------------ #
    # Test 5 — Double-return raises ValueError
    # ------------------------------------------------------------------ #
    def test_double_return_raises(self):
        borrow_id = db.issue_book(
            self.member_id, self.book_id,
            date.today().isoformat(),
            (date.today() + timedelta(days=14)).isoformat(),
            db_path=self.db_path,
        )
        db.return_book(borrow_id, date.today().isoformat(), db_path=self.db_path)

        with self.assertRaises(ValueError):
            db.return_book(borrow_id, date.today().isoformat(), db_path=self.db_path)


if __name__ == "__main__":
    unittest.main()
