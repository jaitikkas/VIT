"""
Database module — handles all SQLite3 operations for the Smart Library system.
Creates tables on first run and exposes CRUD helpers for members, books, and borrows.
"""

import sqlite3
import os
import logging

# ---------------------------------------------------------------------------
# Logger setup (writes to logs/activity.log)
# ---------------------------------------------------------------------------
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "activity.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("library")

# ---------------------------------------------------------------------------
# Database path (stored next to this file)
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")


def get_connection(db_path: str | None = None) -> sqlite3.Connection:
    """Return a new connection to the SQLite database."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # access columns by name
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db(db_path: str | None = None) -> None:
    """Create all required tables if they do not yet exist."""
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                email       TEXT    NOT NULL UNIQUE,
                phone       TEXT    NOT NULL,
                join_date   TEXT    NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                title            TEXT    NOT NULL,
                author           TEXT    NOT NULL,
                isbn             TEXT    NOT NULL UNIQUE,
                total_copies     INTEGER NOT NULL CHECK(total_copies >= 0),
                available_copies INTEGER NOT NULL CHECK(available_copies >= 0)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrows (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id   INTEGER NOT NULL,
                book_id     INTEGER NOT NULL,
                issue_date  TEXT    NOT NULL,
                due_date    TEXT    NOT NULL,
                return_date TEXT,
                FOREIGN KEY (member_id) REFERENCES members(id),
                FOREIGN KEY (book_id)   REFERENCES books(id)
            )
        """)

        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as exc:
        logger.error("Failed to initialize database: %s", exc)
        raise
    finally:
        conn.close()


# ========================== MEMBER OPERATIONS ==============================

def add_member(name: str, email: str, phone: str, join_date: str,
               db_path: str | None = None) -> int:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO members (name, email, phone, join_date) VALUES (?, ?, ?, ?)",
            (name, email, phone, join_date),
        )
        conn.commit()
        member_id = cursor.lastrowid
        logger.info("Added member id=%s name='%s'", member_id, name)
        return member_id
    except sqlite3.Error as exc:
        logger.error("Error adding member '%s': %s", name, exc)
        raise
    finally:
        conn.close()


def get_all_members(db_path: str | None = None) -> list[dict]:
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM members ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as exc:
        logger.error("Error fetching members: %s", exc)
        raise
    finally:
        conn.close()


def get_member_by_id(member_id: int, db_path: str | None = None) -> dict | None:
    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as exc:
        logger.error("Error fetching member id=%s: %s", member_id, exc)
        raise
    finally:
        conn.close()


def update_member(member_id: int, name: str, email: str, phone: str,
                  db_path: str | None = None) -> bool:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE members SET name = ?, email = ?, phone = ? WHERE id = ?",
            (name, email, phone, member_id),
        )
        conn.commit()
        updated = cursor.rowcount > 0
        if updated:
            logger.info("Updated member id=%s", member_id)
        return updated
    except sqlite3.Error as exc:
        logger.error("Error updating member id=%s: %s", member_id, exc)
        raise
    finally:
        conn.close()


def delete_member(member_id: int, db_path: str | None = None) -> bool:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info("Deleted member id=%s", member_id)
        return deleted
    except sqlite3.Error as exc:
        logger.error("Error deleting member id=%s: %s", member_id, exc)
        raise
    finally:
        conn.close()


# =========================== BOOK OPERATIONS ===============================

def add_book(title: str, author: str, isbn: str, total_copies: int,
             db_path: str | None = None) -> int:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, isbn, total_copies, available_copies) "
            "VALUES (?, ?, ?, ?, ?)",
            (title, author, isbn, total_copies, total_copies),
        )
        conn.commit()
        book_id = cursor.lastrowid
        logger.info("Added book id=%s title='%s'", book_id, title)
        return book_id
    except sqlite3.Error as exc:
        logger.error("Error adding book '%s': %s", title, exc)
        raise
    finally:
        conn.close()


def get_all_books(db_path: str | None = None) -> list[dict]:
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM books ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as exc:
        logger.error("Error fetching books: %s", exc)
        raise
    finally:
        conn.close()


def get_book_by_id(book_id: int, db_path: str | None = None) -> dict | None:
    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as exc:
        logger.error("Error fetching book id=%s: %s", book_id, exc)
        raise
    finally:
        conn.close()


def update_book(book_id: int, title: str, author: str, isbn: str,
                total_copies: int, db_path: str | None = None) -> bool:
    conn = get_connection(db_path)
    try:
        # Recalculate available_copies based on how many are currently borrowed
        cur_book = conn.execute("SELECT total_copies, available_copies FROM books WHERE id = ?",
                                (book_id,)).fetchone()
        if not cur_book:
            return False
        borrowed = cur_book["total_copies"] - cur_book["available_copies"]
        new_available = max(total_copies - borrowed, 0)

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET title = ?, author = ?, isbn = ?, "
            "total_copies = ?, available_copies = ? WHERE id = ?",
            (title, author, isbn, total_copies, new_available, book_id),
        )
        conn.commit()
        updated = cursor.rowcount > 0
        if updated:
            logger.info("Updated book id=%s", book_id)
        return updated
    except sqlite3.Error as exc:
        logger.error("Error updating book id=%s: %s", book_id, exc)
        raise
    finally:
        conn.close()


def delete_book(book_id: int, db_path: str | None = None) -> bool:
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info("Deleted book id=%s", book_id)
        return deleted
    except sqlite3.Error as exc:
        logger.error("Error deleting book id=%s: %s", book_id, exc)
        raise
    finally:
        conn.close()


# ========================= BORROW / RETURN =================================

def issue_book(member_id: int, book_id: int, issue_date: str, due_date: str,
               db_path: str | None = None) -> int:
    """Issue a book: inserts a borrow record and decrements available_copies."""
    conn = get_connection(db_path)
    try:
        book = conn.execute("SELECT available_copies FROM books WHERE id = ?",
                            (book_id,)).fetchone()
        if not book:
            raise ValueError(f"Book id={book_id} not found.")
        if book["available_copies"] <= 0:
            raise ValueError(f"Book id={book_id} has no available copies.")

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO borrows (member_id, book_id, issue_date, due_date) "
            "VALUES (?, ?, ?, ?)",
            (member_id, book_id, issue_date, due_date),
        )
        cursor.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?",
            (book_id,),
        )
        conn.commit()
        borrow_id = cursor.lastrowid
        logger.info("Issued book id=%s to member id=%s (borrow id=%s, due=%s)",
                     book_id, member_id, borrow_id, due_date)
        return borrow_id
    except sqlite3.Error as exc:
        conn.rollback()
        logger.error("Error issuing book id=%s to member id=%s: %s",
                      book_id, member_id, exc)
        raise
    except ValueError:
        conn.rollback()
        raise
    finally:
        conn.close()


def return_book(borrow_id: int, return_date: str,
                db_path: str | None = None) -> dict:
    """
    Process a return: sets return_date, increments available_copies.
    Returns a dict with 'overdue' (bool) and 'days_overdue' (int).
    """
    conn = get_connection(db_path)
    try:
        borrow = conn.execute("SELECT * FROM borrows WHERE id = ?",
                              (borrow_id,)).fetchone()
        if not borrow:
            raise ValueError(f"Borrow record id={borrow_id} not found.")
        if borrow["return_date"] is not None:
            raise ValueError(f"Borrow id={borrow_id} has already been returned.")

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE borrows SET return_date = ? WHERE id = ?",
            (return_date, borrow_id),
        )
        cursor.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?",
            (borrow["book_id"],),
        )
        conn.commit()

        from datetime import datetime
        due = datetime.strptime(borrow["due_date"], "%Y-%m-%d")
        ret = datetime.strptime(return_date, "%Y-%m-%d")
        overdue = ret > due
        days_overdue = (ret - due).days if overdue else 0

        status = "OVERDUE" if overdue else "on-time"
        logger.info("Returned borrow id=%s (%s, %d days late)",
                     borrow_id, status, days_overdue)

        return {"overdue": overdue, "days_overdue": days_overdue}
    except sqlite3.Error as exc:
        conn.rollback()
        logger.error("Error returning borrow id=%s: %s", borrow_id, exc)
        raise
    except ValueError:
        conn.rollback()
        raise
    finally:
        conn.close()


# ============================ REPORTS ======================================

def get_overdue_books(today: str, db_path: str | None = None) -> list[dict]:
    """Return all borrows that are past due_date and not yet returned."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT b.id AS borrow_id, m.name AS member_name, bk.title AS book_title, "
            "       b.issue_date, b.due_date "
            "FROM borrows b "
            "JOIN members m  ON b.member_id = m.id "
            "JOIN books   bk ON b.book_id   = bk.id "
            "WHERE b.return_date IS NULL AND b.due_date < ? "
            "ORDER BY b.due_date",
            (today,),
        ).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as exc:
        logger.error("Error fetching overdue books: %s", exc)
        raise
    finally:
        conn.close()


def get_most_borrowed_books(db_path: str | None = None) -> list[dict]:
    """Return books ranked by total number of times they've been borrowed."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT bk.id, bk.title, bk.author, COUNT(b.id) AS borrow_count "
            "FROM borrows b "
            "JOIN books bk ON b.book_id = bk.id "
            "GROUP BY bk.id "
            "ORDER BY borrow_count DESC",
        ).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.Error as exc:
        logger.error("Error fetching most-borrowed books: %s", exc)
        raise
    finally:
        conn.close()
