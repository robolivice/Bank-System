"""
db.py

A thin SQLite persistence layer for the bank system. Kept completely
separate from Account/Bank so the domain classes have no idea a
database exists — Bank just calls save_account()/save_txn() after
each operation, and can rebuild its state from fetch_accounts()/
fetch_txns() on startup.

Two tables:
  accounts     - one row per Account (current snapshot, not history)
  transactions - append-only ledger, one row per Transaction
"""
import sqlite3

class BankDB:
    def __init__(self, db_path="bank.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_number INTEGER PRIMARY KEY,
                owner_name     TEXT NOT NULL,
                account_type   TEXT NOT NULL,
                balance        REAL NOT NULL,
                is_active      INTEGER NOT NULL DEFAULT 1
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number INTEGER NOT NULL,
                tx_type        TEXT NOT NULL,
                amount         REAL NOT NULL,
                balance_after  REAL NOT NULL,
                note           TEXT,
                timestamp      TEXT NOT NULL,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        """)
        self.conn.commit()

    def save_account(self, account):
        """Insert the account, or update it if the account_number already exists."""
        self.conn.execute(
            """
            INSERT INTO accounts (account_number, owner_name, account_type, balance, is_active)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(account_number) DO UPDATE SET
                owner_name = excluded.owner_name,
                balance    = excluded.balance,
                is_active  = excluded.is_active
            """,
            (
                account.account_number,
                account.owner_name,
                account.get_acc_type(),
                account.balance,
                int(account.is_active),
            ),
        )
        self.conn.commit()

    def save_txn(self, account_number, tx):
        self.conn.execute(
            """
            INSERT INTO transactions (account_number, tx_type, amount, balance_after, note, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (account_number, tx.tx_type, tx.amount, tx.balance_after, tx.note, tx.timestamp.isoformat()),
        )
        self.conn.commit()

    def fetch_accounts(self):
        cur = self.conn.execute(
            "SELECT account_number, owner_name, account_type, balance, is_active FROM accounts"
        )
        return cur.fetchall()

    def fetch_txns(self, account_number):
        cur = self.conn.execute(
            """
            SELECT tx_type, amount, balance_after, note, timestamp
            FROM transactions
            WHERE account_number = ?
            ORDER BY id
            """,
            (account_number,),
        )
        return cur.fetchall()

    def close(self):
        self.conn.close()