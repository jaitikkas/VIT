"""
Borrow / Return module - handles issuing books to members,
processing returns, and printing reports.
"""

from datetime import date, timedelta

from db import database as db
from utils import validators


def issue_book():
    print("\n-- Issue a Book --")

    raw_member = input("  Member ID: ").strip()
    ok, msg = validators.validate_positive_int(raw_member, "Member ID")
    if not ok:
        print(f"  Error: {msg}")
        return

    member = db.get_member_by_id(int(raw_member))
    if not member:
        print(f"  No member with ID {raw_member}.")
        return

    raw_book = input("  Book ID: ").strip()
    ok, msg = validators.validate_positive_int(raw_book, "Book ID")
    if not ok:
        print(f"  Error: {msg}")
        return

    book = db.get_book_by_id(int(raw_book))
    if not book:
        print(f"  No book with ID {raw_book}.")
        return

    if book["available_copies"] <= 0:
        print(f"  '{book['title']}' has no available copies right now.")
        return

    issue_date = date.today().isoformat()
    due_date = (date.today() + timedelta(days=14)).isoformat()

    try:
        borrow_id = db.issue_book(int(raw_member), int(raw_book),
                                  issue_date, due_date)
        print(f"  Book issued. Borrow ID: {borrow_id}")
        print(f"  Due date: {due_date}")
    except Exception as exc:
        print(f"  Could not issue book - {exc}")


def return_book():
    print("\n-- Return a Book --")

    raw_id = input("  Borrow ID: ").strip()
    ok, msg = validators.validate_positive_int(raw_id, "Borrow ID")
    if not ok:
        print(f"  Error: {msg}")
        return

    return_date = date.today().isoformat()

    try:
        result = db.return_book(int(raw_id), return_date)
        if result["overdue"]:
            print(f"  Returned OVERDUE by {result['days_overdue']} day(s).")
        else:
            print("  Book returned on time.")
    except Exception as exc:
        print(f"  Could not process return - {exc}")


def overdue_report():
    print("\n-- Overdue Books Report --")
    today = date.today().isoformat()
    try:
        records = db.get_overdue_books(today)
        if not records:
            print("  No overdue books at the moment.")
            return
        print(f"  {'Borrow':<8} {'Member':<22} {'Book':<28} "
              f"{'Issued':<12} {'Due':<12}")
        print(f"  {'-'*8} {'-'*22} {'-'*28} {'-'*12} {'-'*12}")
        for r in records:
            print(f"  {r['borrow_id']:<8} {r['member_name']:<22} "
                  f"{r['book_title']:<28} {r['issue_date']:<12} {r['due_date']:<12}")
    except Exception as exc:
        print(f"  Error - {exc}")


def most_borrowed_report():
    print("\n-- Most-Borrowed Books --")
    try:
        records = db.get_most_borrowed_books()
        if not records:
            print("  No borrow records yet.")
            return
        print(f"  {'Rank':<6} {'Title':<30} {'Author':<22} {'Times Borrowed'}")
        print(f"  {'-'*6} {'-'*30} {'-'*22} {'-'*14}")
        for i, r in enumerate(records, 1):
            print(f"  {i:<6} {r['title']:<30} {r['author']:<22} "
                  f"{r['borrow_count']}")
    except Exception as exc:
        print(f"  Error - {exc}")
