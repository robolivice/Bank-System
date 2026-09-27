# Bank Account Management System

A console-based Python application for managing Savings and Current bank
accounts — built to demonstrate core Python and OOP concepts (abstraction,
encapsulation, inheritance, polymorphism, operator overloading, static/class
methods, custom exceptions, and NumPy-based analytics).

## Overview
The system lets a bank create accounts, process deposits/withdrawals/
transfers under type-specific rules, and generate analytics reports —
all through a simple menu-driven CLI.

## Features
- **Two account types** with different rules, sharing one interface:
  - `SavingsAccount` — enforces a minimum balance ($500) and earns interest.
  - `CurrentAccount` — allows overdraft up to a limit ($5,000), earns no interest.
- **Core operations**: create account, deposit, withdraw, transfer (with
  automatic rollback on failure), close account.
- **Transaction history** per account (timestamped ledger entries).
- **SQLite persistence** (optional): pass a `db_path` and every account/
  transaction is saved automatically — restart the app and everything's
  still there.
- **Bank-wide analytics** via NumPy: total deposits, mean/median/std
  balance, total interest liability, top-N accounts by balance.
- **Custom exception hierarchy** for clean, predictable error handling.
- **Operator overloading**: compare accounts by balance (`<`, `>`), check
  equality by account number (`==`), combine balances (`+`), readable
  string output (`str()`).
- **Unit tests** covering validation, polymorphic behaviour, rollback, and
  persistence (data survives across separate Bank instances/db reloads).

## Technologies / Tools Used
- Python 3.x
- SQLite (`sqlite3`, built-in) for persistence
- NumPy (for statistical reporting)
- `unittest` (built-in) for testing
- `abc`, `itertools`, `datetime` (standard library)

## Diagrams
See the `diagrams/` folder for the design artefacts referenced in the report:
- `architecture.svg` — layered system architecture
- `class_diagram.svg` — class relationships (inheritance, aggregation, composition)
- `use_case_diagram.svg` — customer-facing use cases
- `sequence_transfer.svg` — sequence diagram for the transfer operation
- `workflow_diagram.svg` — CLI menu process flow
- `er_conceptual_diagram.svg` — conceptual entity relationships (in-memory, no DB yet)

## Project Structure
```
bank_system/
├── README.md
├── statement.md
├── requirements.txt
├── main.py                  # CLI entry point
├── diagrams/                # design diagrams (see above)
├── src/
│   ├── __init__.py          # package exports
│   ├── exceptions.py        # custom exception hierarchy
│   ├── transaction.py       # Transaction ledger entry
│   ├── account.py           # abstract Account base class
│   ├── savings_account.py   # SavingsAccount (inherits Account)
│   ├── current_account.py   # CurrentAccount (inherits Account)
│   ├── bank.py               # Bank: manages accounts, transfers, CRUD
│   ├── db.py                  # SQLite persistence layer
│   ├── utils.py               # formatting + itertools-based helpers
│   └── report.py              # NumPy-based analytics/reporting
└── tests/
    ├── test_accounts.py     # unit tests for accounts/bank/report
    └── test_db.py            # persistence tests (survives reload)
```

## Persistence (SQLite)
By default `Bank("Some Name")` runs purely in memory. Pass a `db_path`
to turn on persistence:
```python
bank = Bank("VITyarthi National Bank", db_path="bank.db")
```
Every `create_account`, `deposit`, `withdraw`, `transfer`, and `close_acc`
call is automatically mirrored into the SQLite file — the account's
current balance/status plus every new transaction. On the next run,
passing the same `db_path` reloads all accounts and their full
transaction history before you do anything else. `main.py` already
does this (`db_path="bank.db"`), so running the CLI twice in a row
picks up right where you left off. Call `bank.close_db()` when you're
done (the CLI does this on exit).

## Steps to Install & Run
1. Clone the repository and enter the project folder:
   ```bash
   git clone https://github.com/robolivice/Bank-System
   cd bank_system
   ```
2. (Recommended) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Follow the on-screen menu to create accounts, deposit/withdraw,
   transfer funds, and view reports.

## Instructions for Testing
Run the full unit test suite from the project root:
```bash
python -m unittest discover -s tests -v
```
All 23 tests should pass, covering:
- Savings minimum-balance enforcement
- Current-account overdraft limits
- Deposit/withdraw validation (negative amounts, closed accounts)
- Operator overloading (`==`, `<`, `>`)
- Bank-level operations (transfer with rollback, account lookup errors)
- Report generation
- SQLite persistence (balances, transaction history, and open account
  numbers all survive being reloaded from disk in a fresh `Bank` instance)

## Sample Report Output
```
===== VITyarthi National Bank — Bank Report =====
Total accounts     : 3
Total deposits     : $6,000.00
Average balance    : $2,000.00
Median balance     : $2,000.00
Balance std. dev.  : $816.50
Total interest owed: $160.00

-- By account type --
  Current: 1 account(s)
  Savings: 2 account(s)

-- Top 3 accounts by balance --
  [Savings] #1003 - Chris Diaz - Balance: 3000.00 (ACTIVE)
  [Current] #1002 - Bob Lee - Balance: 2000.00 (ACTIVE)
  [Savings] #1001 - Alice Johnson - Balance: 1000.00 (ACTIVE)
```

## Future Enhancements
- Support joint accounts and scheduled/recurring transactions.
- Move the schema to something with real concurrent-write support (Postgres) if this ever needs multiple users at once.
- Add a REST API or web UI on top of the same `src/` core.