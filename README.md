# Smart Library Management System

> A beginner-friendly, terminal-based library management application built with **Python 3** and **SQLite3**.

---

##  Overview

Smart Library is a CLI application that lets you manage a small library's members, book inventory, and borrowing activity — all from the terminal. No external database server or GUI is required.

---

##  Features

| Area | Capabilities |
|------|-------------|
| **Member Management** | Add, view, update, and delete library members |
| **Book Inventory** | Add, view, update, and delete books (tracks total & available copies) |
| **Borrow / Return** | Issue a book to a member (14-day due date), process returns with overdue detection |
| **Reports** | List overdue books · Rank most-borrowed books |
| **Validation** | Email format, non-empty names, phone format, ISBN (10/13), non-negative quantities |
| **Logging** | Every add/issue/return/error is timestamped in `logs/activity.log` |
| **Tests** | 5 unit tests covering the borrow/return logic |

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Database | SQLite3 (built-in, no install needed) |
| Testing | `unittest` (standard library) |
| Logging | `logging` (standard library) |

> **Zero external dependencies.** Everything runs with a standard Python installation.

---

##  Project Structure

```
smart_library/
├── main.py                 # Entry point — menu-driven CLI loop
├── README.md
├── statement.md
│
├── db/
│   ├── __init__.py
│   └── database.py         # All SQLite3 operations (CRUD + reports)
│
├── modules/
│   ├── __init__.py
│   ├── members.py           # Member management (business logic)
│   ├── books.py             # Book inventory   (business logic)
│   └── borrow.py            # Issue / Return / Reports (business logic)
│
├── utils/
│   ├── __init__.py
│   └── validators.py        # Input validation helpers
│
├── tests/
│   ├── __init__.py
│   └── test_borrow.py       # Unit tests for borrow / return
│
└── logs/
    └── activity.log          # Created automatically at runtime
```

---

##  Setup & Run

### Prerequisites

- **Python 3.10 or later** — [Download Python](https://www.python.org/downloads/)

Verify your installation:

```bash
python --version
# Expected output: Python 3.10.x  (or higher)
```

### Clone / Download

```bash
git clone https://github.com/jaitikkas/VIT.git
cd smart_library
```

Or simply download and extract the project folder.

### Run the Application

```bash
python main.py
```

You'll see the main menu:

```
╔══════════════════════════════════════════════════════════════╗
║              Smart Library Management System                 ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────┐
│            MAIN  MENU                │
├──────────────────────────────────────┤
│  1 │ Member Management              │
│  2 │ Book Inventory                 │
│  3 │ Issue a Book                   │
│  4 │ Return a Book                  │
│  5 │ Reports                        │
│  0 │ Exit                           │
└──────────────────────────────────────┘
```

Navigate by typing the menu number and pressing **Enter**.

### Run the Tests

```bash
python -m unittest discover -s tests -v
```

Expected output:

```
test_double_return_raises (test_borrow.BorrowReturnTestCase) ... ok
test_issue_fails_when_no_copies (test_borrow.BorrowReturnTestCase) ... ok
test_issue_reduces_available_copies (test_borrow.BorrowReturnTestCase) ... ok
test_on_time_return_not_overdue (test_borrow.BorrowReturnTestCase) ... ok
test_return_restores_copies_and_detects_overdue (test_borrow.BorrowReturnTestCase) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.XXXs

OK
```

---
