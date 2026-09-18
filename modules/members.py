"""
Member management - handles user interaction for adding, viewing,
updating, and deleting library members.
"""

from datetime import date

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


def add_member():
    print("\n-- Add New Member --")
    name = _prompt("Full name", validators.validate_name)
    email = _prompt("Email", validators.validate_email)
    phone = _prompt("Phone", validators.validate_phone)
    join_date = date.today().isoformat()

    try:
        mid = db.add_member(name, email, phone, join_date)
        print(f"  Member added (ID: {mid})")
    except Exception as exc:
        print(f"  Could not add member - {exc}")


def view_members():
    print("\n-- All Members --")
    try:
        members = db.get_all_members()
        if not members:
            print("  No members found.")
            return
        print(f"  {'ID':<5} {'Name':<25} {'Email':<30} {'Phone':<16} {'Joined'}")
        print(f"  {'-'*5} {'-'*25} {'-'*30} {'-'*16} {'-'*10}")
        for m in members:
            print(f"  {m['id']:<5} {m['name']:<25} {m['email']:<30} "
                  f"{m['phone']:<16} {m['join_date']}")
    except Exception as exc:
        print(f"  Error - {exc}")


def update_member():
    print("\n-- Update Member --")
    raw_id = input("  Member ID to update: ").strip()
    ok, msg = validators.validate_positive_int(raw_id, "Member ID")
    if not ok:
        print(f"  Error: {msg}")
        return

    member = db.get_member_by_id(int(raw_id))
    if not member:
        print(f"  No member with ID {raw_id}.")
        return

    print(f"  Current: {member['name']} | {member['email']} | {member['phone']}")
    name = _prompt("New name", validators.validate_name)
    email = _prompt("New email", validators.validate_email)
    phone = _prompt("New phone", validators.validate_phone)

    try:
        if db.update_member(int(raw_id), name, email, phone):
            print("  Member updated.")
        else:
            print("  Update failed (member may have been deleted).")
    except Exception as exc:
        print(f"  Error - {exc}")


def delete_member():
    print("\n-- Delete Member --")
    raw_id = input("  Member ID to delete: ").strip()
    ok, msg = validators.validate_positive_int(raw_id, "Member ID")
    if not ok:
        print(f"  Error: {msg}")
        return

    member = db.get_member_by_id(int(raw_id))
    if not member:
        print(f"  No member with ID {raw_id}.")
        return

    confirm = input(f"  Delete '{member['name']}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    try:
        if db.delete_member(int(raw_id)):
            print("  Member deleted.")
        else:
            print("  Deletion failed.")
    except Exception as exc:
        print(f"  Error - {exc}")
