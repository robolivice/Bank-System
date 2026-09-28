"""
test_accounts.py

Run with: python -m unittest discover -s tests -v
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import Bank, SavingsAccount, CurrentAccount, BankReport
from src.exceptions import (
    MinimumBalanceError,
    OverdraftLimitError,
    InvalidAmountError,
    AccountNotFoundError,
    InactiveAccountError,
)


class TestSavingsAccount(unittest.TestCase):
    def setUp(self):
        self.acc = SavingsAccount("Alice Johnson", 1000)

    def test_initial_balance_respects_minimum(self):
        low = SavingsAccount("Bob Lee", 100)
        self.assertEqual(low.balance, SavingsAccount.min_balance)

    def test_deposit_increases_balance(self):
        self.acc.deposit(500)
        self.assertEqual(self.acc.balance, 1500)

    def test_withdraw_below_minimum_raises(self):
        with self.assertRaises(MinimumBalanceError):
            self.acc.withdraw(600)  # would leave 400, below the 500 minimum

    def test_valid_withdraw_succeeds(self):
        new_balance = self.acc.withdraw(400)
        self.assertEqual(new_balance, 600)

    def test_negative_deposit_raises(self):
        with self.assertRaises(InvalidAmountError):
            self.acc.deposit(-50)

    def test_interest_calculation(self):
        expected = round(1000 * SavingsAccount.INTEREST_RATE, 2)
        self.assertEqual(self.acc.calc_interest(), expected)

    def test_account_type_label(self):
        self.assertEqual(self.acc.get_acc_type(), "Savings")


class TestCurrentAccount(unittest.TestCase):
    def setUp(self):
        self.acc = CurrentAccount("Chris Diaz", 1000)

    def test_overdraft_allowed_within_limit(self):
        new_balance = self.acc.withdraw(5500)  # -4500, still within the -5000 limit
        self.assertEqual(new_balance, -4500)

    def test_overdraft_beyond_limit_raises(self):
        with self.assertRaises(OverdraftLimitError):
            self.acc.withdraw(6001)

    def test_no_interest(self):
        self.assertEqual(self.acc.calc_interest(), 0.0)


class TestAccountOperators(unittest.TestCase):
    def test_equality_by_account_number(self):
        a = SavingsAccount("A", 1000)
        b = SavingsAccount("B", 1000)
        self.assertNotEqual(a, b)
        self.assertEqual(a, a)

    def test_comparison_by_balance(self):
        rich = SavingsAccount("Rich", 5000)
        poor = SavingsAccount("Poor", 500)
        self.assertTrue(rich > poor)
        self.assertTrue(poor < rich)


class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank("Test Bank")
        self.acc1 = self.bank.create_account("Dana White", "savings", 1000)
        self.acc2 = self.bank.create_account("Evan Wright", "current", 2000)

    def test_bank_len_and_contains(self):
        self.assertEqual(len(self.bank), 2)
        self.assertIn(self.acc1.account_number, self.bank)

    def test_get_unknown_account_raises(self):
        with self.assertRaises(AccountNotFoundError):
            self.bank.get_acc(999999)

    def test_transfer_between_accounts(self):
        src_bal, dst_bal = self.bank.transfer(
            self.acc1.account_number, self.acc2.account_number, 300
        )
        self.assertEqual(src_bal, 700)
        self.assertEqual(dst_bal, 2300)

    def test_transfer_insufficient_funds_rolls_back(self):
        with self.assertRaises(MinimumBalanceError):
            self.bank.transfer(self.acc1.account_number, self.acc2.account_number, 10000)
        # should be unchanged since the transfer got rolled back
        self.assertEqual(self.acc1.balance, 1000)
        self.assertEqual(self.acc2.balance, 2000)

    def test_closed_account_rejects_deposit(self):
        self.bank.close_acc(self.acc1.account_number)
        with self.assertRaises(InactiveAccountError):
            self.bank.deposit(self.acc1.account_number, 100)

    def test_invalid_account_type_raises(self):
        with self.assertRaises(ValueError):
            self.bank.create_account("Frank", "crypto", 100)


class TestBankReport(unittest.TestCase):
    def test_report_generates_without_error(self):
        bank = Bank("Report Bank")
        bank.create_account("Gina Park", "savings", 1000)
        bank.create_account("Hank Kim", "current", 2000)
        report = BankReport(bank)
        text = report.gen_report()
        self.assertIn("Report Bank", text)
        self.assertIn("Total accounts", text)


if __name__ == "__main__":
    unittest.main()
