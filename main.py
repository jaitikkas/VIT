#!/usr/bin/env python3
"""
Smart Library Management System - main entry point.
Run with:  python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import database as db
from modules import members, books, borrow

MAIN_MENU = """
=== SMART LIBRARY MANAGEMENT SYSTEM ===

  1. Member Management
  2. Book Inventory
  3. Issue a Book
  4. Return a Book
  5. Reports
  0. Exit
"""

MEMBER_MENU = """
--- Member Management ---

  1. Add Member
  2. View All Members
  3. Update Member
  4. Delete Member
  0. Back
"""

BOOK_MENU = """
--- Book Inventory ---

  1. Add Book
  2. View All Books
  3. Update Book
  4. Delete Book
  0. Back
"""

REPORT_MENU = """
--- Reports ---

  1. Overdue Books
  2. Most-Borrowed Books
  0. Back
"""


def member_menu_loop():
    while True:
        print(MEMBER_MENU)
        choice = input("  Select option: ").strip()
        if choice == "1":
            members.add_member()
        elif choice == "2":
            members.view_members()
        elif choice == "3":
            members.update_member()
        elif choice == "4":
            members.delete_member()
        elif choice == "0":
            break
        else:
            print("  Invalid choice, try again.")


def book_menu_loop():
    while True:
        print(BOOK_MENU)
        choice = input("  Select option: ").strip()
        if choice == "1":
            books.add_book()
        elif choice == "2":
            books.view_books()
        elif choice == "3":
            books.update_book()
        elif choice == "4":
            books.delete_book()
        elif choice == "0":
            break
        else:
            print("  Invalid choice, try again.")


def report_menu_loop():
    while True:
        print(REPORT_MENU)
        choice = input("  Select option: ").strip()
        if choice == "1":
            borrow.overdue_report()
        elif choice == "2":
            borrow.most_borrowed_report()
        elif choice == "0":
            break
        else:
            print("  Invalid choice, try again.")


def main():
    db.initialize_db()

    while True:
        print(MAIN_MENU)
        choice = input("  Select option: ").strip()

        if choice == "1":
            member_menu_loop()
        elif choice == "2":
            book_menu_loop()
        elif choice == "3":
            borrow.issue_book()
        elif choice == "4":
            borrow.return_book()
        elif choice == "5":
            report_menu_loop()
        elif choice == "0":
            print("\n  Goodbye.\n")
            sys.exit(0)
        else:
            print("  Invalid choice, try again.")


if __name__ == "__main__":
    main()
