"""
Book inventory - handles user interaction for adding, viewing,
updating, and deleting books in the library catalogue.
"""

from db import database as db
from utils import validators


def _prompt(label, validator, *args):
    """Keep asking until the validator passes. Returns cleaned value."""
    while True:
        value = input(f"  {label}: ").strip()
        ok, msg = validator(value, *args) if args else validator(value)
        if ok:
            return value
        print(f"  Error: {msg}")


def add_book():
    print("\n-- Add New Book --")
    title = _prompt("Title", validators.validate_non_empty, "Title")
    author = _prompt("Author", validators.validate_name)
    isbn = _prompt("ISBN", validators.validate_isbn)
    copies = _prompt("Total copies", validators.validate_positive_int, "Total copies")

    try:
        bid = db.add_book(title, author, isbn, int(copies))
        print(f"  Book added (ID: {bid})")
    except Exception as exc:
        print(f"  Could not add book - {exc}")


def view_books():
    print("\n-- All Books --")
    try:
        books = db.get_all_books()
        if not books:
            print("  No books found.")
            return
        print(f"  {'ID':<5} {'Title':<30} {'Author':<22} {'ISBN':<16} "
              f"{'Total':<7} {'Avail'}")
        print(f"  {'-'*5} {'-'*30} {'-'*22} {'-'*16} {'-'*7} {'-'*5}")
        for b in books:
            print(f"  {b['id']:<5} {b['title']:<30} {b['author']:<22} "
                  f"{b['isbn']:<16} {b['total_copies']:<7} {b['available_copies']}")
    except Exception as exc:
        print(f"  Error - {exc}")


def update_book():
    print("\n-- Update Book --")
    raw_id = input("  Book ID to update: ").strip()
    ok, msg = validators.validate_positive_int(raw_id, "Book ID")
    if not ok:
        print(f"  Error: {msg}")
        return

    book = db.get_book_by_id(int(raw_id))
    if not book:
        print(f"  No book with ID {raw_id}.")
        return

    print(f"  Current: {book['title']} | {book['author']} | {book['isbn']} "
          f"| copies: {book['total_copies']}")
    title = _prompt("New title", validators.validate_non_empty, "Title")
    author = _prompt("New author", validators.validate_name)
    isbn = _prompt("New ISBN", validators.validate_isbn)
    copies = _prompt("New total copies", validators.validate_positive_int, "Total copies")

    try:
        if db.update_book(int(raw_id), title, author, isbn, int(copies)):
            print("  Book updated.")
        else:
            print("  Update failed (book may have been deleted).")
    except Exception as exc:
        print(f"  Error - {exc}")


def delete_book():
    print("\n-- Delete Book --")
    raw_id = input("  Book ID to delete: ").strip()
    ok, msg = validators.validate_positive_int(raw_id, "Book ID")
    if not ok:
        print(f"  Error: {msg}")
        return

    book = db.get_book_by_id(int(raw_id))
    if not book:
        print(f"  No book with ID {raw_id}.")
        return

    confirm = input(f"  Delete '{book['title']}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    try:
        if db.delete_book(int(raw_id)):
            print("  Book deleted.")
        else:
            print("  Deletion failed.")
    except Exception as exc:
        print(f"  Error - {exc}")
