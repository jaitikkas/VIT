# Smart Library Management System — Statement

---

## Problem Statement

Small libraries and reading clubs often rely on paper registers or ad-hoc spreadsheets to track their book inventory, member records, and borrowing activity. This leads to:

- **Lost records** — paper logs get misplaced or damaged.
- **No overdue tracking** — late returns go unnoticed, reducing availability for other readers.
- **Duplication** — the same book or member can be entered multiple times with no safeguard.
- **No analytics** — it's hard to know which books are most popular or how active the library is.

The **Smart Library Management System** solves these problems with a lightweight, terminal-based application that stores all data in a local SQLite database, validates every input, and logs every transaction.

---

## Scope

| In Scope | Out of Scope |
|----------|-------------|
| CRUD for members (name, email, phone) | Multi-user / networked access |
| CRUD for books (title, author, ISBN, copies) | GUI / web interface |
| Issue / return workflow with 14-day due dates | Payment / fine calculation |
| Overdue books report | Email / SMS notifications |
| Most-borrowed books report | Advanced search / filtering |
| Input validation (email, phone, ISBN, quantities) | Barcode / QR scanning |
| Activity logging to file | Cloud deployment |

---

## Target Users

- **Beginner Python learners** looking for a real-world project to study CRUD, SQLite, and modular design.
- **Small community libraries** or **book clubs** that need a zero-setup inventory tracker.
- **Educators** who want a clean reference project demonstrating separation of concerns, input validation, logging, and unit testing.

---

## High-Level Features

1. **Member Management**
   - Register new members with validated contact information.
   - View, edit, or remove member records.

2. **Book Inventory**
   - Add books with title, author, ISBN, and copy count.
   - Track total vs. available copies automatically.
   - Update or remove books from the catalogue.

3. **Borrow & Return System**
   - Issue a book to a member — the system sets a 14-day due date and decrements available copies.
   - Process a return — the system restores the copy count and flags overdue returns.

4. **Reports**
   - **Overdue Books** — lists all books that are past their due date and not yet returned.
   - **Most-Borrowed Books** — ranks books by total number of times they have been borrowed.

5. **Data Integrity**
   - Input validation for names, emails, phone numbers, ISBNs, and numeric fields.
   - Foreign-key constraints in the database.
   - All database operations wrapped in `try/except` with error logging.

6. **Audit Trail**
   - Every significant action (add, issue, return, error) is written to `logs/activity.log` with a timestamp via Python's `logging` module.

7. **Automated Tests**
   - Unit tests verify borrow/return correctness: copy count changes, overdue detection, edge cases (no copies, double return).
