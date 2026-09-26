"""
Bank Account Management System — core package.

Exposes the main public classes so callers can do:
    from src import Bank, SavingsAccount, CurrentAccount
instead of reaching into individual modules.
"""
from src.account import Account
from src.savings_account import SavingsAccount
from src.current_account import CurrentAccount
from src.bank import Bank
from src.report import BankReport
from src.transaction import Transaction
from src import exceptions

__all__ = [
    "Account",
    "SavingsAccount",
    "CurrentAccount",
    "Bank",
    "BankReport",
    "Transaction",
    "exceptions",
]
