"""
Bank owns the accounts and exposes create/deposit/withdraw/transfer/close.
Doesn't care whether an account is Savings or Current - withdraw() and
calc_interest() just work because of polymorphism.

Persistence is optional: pass db_path to __init__ and every mutating
operation gets mirrored into SQLite via BankDB. Without db_path the
bank behaves exactly like before (in-memory only).
"""
from src.savings_account import SavingsAccount
from src.current_account import CurrentAccount
from src.account import Account
from src.transaction import Transaction
from src.exceptions import AccountNotFoundError
from src.utils import is_valid_name
from src.db import BankDB


class Bank:
    ACCOUNT_TYPES = {
        "savings": SavingsAccount,
        "current": CurrentAccount,
    }

    def __init__(self, name, db_path=None):
        self.name = name
        self._accounts = {}  # account_number -> Account
        self._synced = {}    # account_number -> how many of its txns are already saved
        self.db = BankDB(db_path) if db_path else None
        if self.db:
            self._load_from_db()

    def _load_from_db(self):
        for acc_no, owner_name, acc_type, balance, is_active in self.db.fetch_accounts():
            acc_cls = Bank.ACCOUNT_TYPES[acc_type.lower()]
            account = acc_cls._load(acc_no, owner_name, balance, bool(is_active))
            account._transactions = [Transaction._from_row(row) for row in self.db.fetch_txns(acc_no)]
            self._accounts[acc_no] = account
            self._synced[acc_no] = len(account._transactions)
            if acc_no > Account._acc_counter:
                Account._acc_counter = acc_no

    def _sync(self, account):
        """Push an account's current state + any new transactions to the DB."""
        if not self.db:
            return
        self.db.save_account(account)
        done = self._synced.get(account.account_number, 0)
        for tx in account.transactions[done:]:
            self.db.save_txn(account.account_number, tx)
        self._synced[account.account_number] = len(account.transactions)

    def create_account(self, owner_name, account_type, initial_deposit=0.0):
        if not is_valid_name(owner_name):
            raise ValueError(f"Invalid owner name: {owner_name!r}")

        account_type = account_type.strip().lower()
        if account_type not in Bank.ACCOUNT_TYPES:
            raise ValueError("Unknown account type '%s'. Choose from %s." % (
                account_type, list(Bank.ACCOUNT_TYPES)
            ))

        acc_cls = Bank.ACCOUNT_TYPES[account_type]
        account = acc_cls(owner_name, initial_deposit)
        self._accounts[account.account_number] = account
        self._sync(account)
        return account

    def get_acc(self, account_number):
        try:
            return self._accounts[account_number]
        except KeyError:
            raise AccountNotFoundError(account_number)

    def close_acc(self, account_number):
        acc = self.get_acc(account_number)
        acc.close_acc()
        self._sync(acc)
        return acc

    def get_all_accs(self):
        return list(self._accounts.values())

    def deposit(self, account_number, amount):
        acc = self.get_acc(account_number)
        result = acc.deposit(amount)
        self._sync(acc)
        return result

    def withdraw(self, account_number, amount):
        acc = self.get_acc(account_number)
        result = acc.withdraw(amount)
        self._sync(acc)
        return result

    def transfer(self, from_acc_no, to_acc_no, amount):
        """Move money between two accounts. Rolls back if the deposit side fails."""
        source = self.get_acc(from_acc_no)
        target = self.get_acc(to_acc_no)

        source.withdraw(amount)  # raises if the rules don't allow it
        try:
            target.deposit(amount)
        except Exception:
            source.deposit(amount)  # undo the withdrawal
            self._sync(source)
            raise
        source._record_txn("TRANSFER_OUT", 0, "to #%s" % to_acc_no)
        target._record_txn("TRANSFER_IN", 0, "from #%s" % from_acc_no)
        self._sync(source)
        self._sync(target)
        return source.balance, target.balance

    def close_db(self):
        if self.db:
            self.db.close()

    def __len__(self):
        return len(self._accounts)

    def __iter__(self):
        return iter(self._accounts.values())

    def __contains__(self, account_number):
        return account_number in self._accounts

    def __str__(self):
        return "Bank(name={!r}, accounts={})".format(self.name, len(self))
