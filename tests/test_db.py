"""
test_db.py

Tests the SQLite persistence path specifically: create accounts in
one Bank instance, throw that instance away, then check a brand new
Bank pointed at the same db file sees the same data.

Run with: python -m unittest discover -s tests -v
"""
import sys
import os
import unittest
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import Bank


class TestPersistence(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.remove(self.db_path)  # let BankDB create it fresh

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_account_survives_reload(self):
        bank = Bank("Test Bank", db_path=self.db_path)
        acc = bank.create_account("Alice Johnson", "savings", 1000)
        bank.deposit(acc.account_number, 250)
        bank.close_db()

        reloaded = Bank("Test Bank", db_path=self.db_path)
        self.assertEqual(len(reloaded), 1)
        loaded_acc = reloaded.get_acc(acc.account_number)
        self.assertEqual(loaded_acc.owner_name, "Alice Johnson")
        self.assertEqual(loaded_acc.balance, 1250)
        self.assertEqual(loaded_acc.get_acc_type(), "Savings")
        reloaded.close_db()

    def test_transaction_history_survives_reload(self):
        bank = Bank("Test Bank", db_path=self.db_path)
        acc = bank.create_account("Bob Lee", "current", 1000)
        bank.deposit(acc.account_number, 100)
        bank.withdraw(acc.account_number, 50)
        bank.close_db()

        reloaded = Bank("Test Bank", db_path=self.db_path)
        loaded_acc = reloaded.get_acc(acc.account_number)
        tx_types = [tx.tx_type for tx in loaded_acc.transactions]
        self.assertEqual(tx_types, ["DEPOSIT", "DEPOSIT", "WITHDRAW"])
        reloaded.close_db()

    def test_new_accounts_after_reload_dont_collide(self):
        bank = Bank("Test Bank", db_path=self.db_path)
        first = bank.create_account("Chris Diaz", "savings", 1000)
        bank.close_db()

        reloaded = Bank("Test Bank", db_path=self.db_path)
        second = reloaded.create_account("Dana White", "savings", 1000)
        self.assertNotEqual(first.account_number, second.account_number)
        self.assertGreater(second.account_number, first.account_number)
        reloaded.close_db()

    def test_closed_account_status_persists(self):
        bank = Bank("Test Bank", db_path=self.db_path)
        acc = bank.create_account("Evan Wright", "current", 1000)
        bank.close_acc(acc.account_number)
        bank.close_db()

        reloaded = Bank("Test Bank", db_path=self.db_path)
        loaded_acc = reloaded.get_acc(acc.account_number)
        self.assertFalse(loaded_acc.is_active)
        reloaded.close_db()


if __name__ == "__main__":
    unittest.main()
