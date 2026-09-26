"""
Abstract base for every account type. Handles the stuff that's the
same regardless of account type (balance, deposits, txn log) and
leaves the type-specific rules to the subclasses.
"""
from abc import ABC, abstractmethod
from src.exceptions import InvalidAmountError, InactiveAccountError
from src.transaction import Transaction


class Account(ABC):

    _acc_counter = 1000  # shared across every account ever created

    def __init__(self, owner_name: str, initial_balance: float = 0.0):
        self._acc_no = Account._next_acc_no()
        self._owner_name = owner_name
        self.__balance = Account.check_amount(initial_balance, allow_zero=True)
        self._is_active = True
        self._transactions = []

        if initial_balance > 0:
            self._record_txn("DEPOSIT", initial_balance, "Initial deposit")

    @classmethod
    def _next_acc_no(cls):
        cls._acc_counter += 1
        return cls._acc_counter

    @classmethod
    def _load(cls, acc_no, owner_name, balance, is_active):
        """
        Rebuild an account from a saved DB row, bypassing __init__ (and
        therefore any subclass rules like SavingsAccount's minimum-balance
        bump) since this is a restore, not a new account being opened.
        """
        obj = cls.__new__(cls)
        obj._acc_no = acc_no
        obj._owner_name = owner_name
        obj.__balance = balance
        obj._is_active = is_active
        obj._transactions = []
        return obj

    @staticmethod
    def check_amount(amount, allow_zero=False):
        """Basic sanity check on any amount before it touches a balance."""
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise InvalidAmountError(amount)
        if amount < 0 or (amount == 0 and not allow_zero):
            raise InvalidAmountError(amount)
        return float(amount)

    @property
    def balance(self):
        return self.__balance

    @property
    def account_number(self):
        return self._acc_no

    @property
    def owner_name(self):
        return self._owner_name

    @property
    def is_active(self):
        return self._is_active

    @property
    def transactions(self):
        return list(self._transactions)

    def deposit(self, amount):
        if not self._is_active:
            raise InactiveAccountError(self._acc_no)
        amount = Account.check_amount(amount)
        self.__balance += amount
        self._record_txn("DEPOSIT", amount)
        return self.__balance

    def close_acc(self):
        self._is_active = False

    def _do_withdraw(self, amount):
        # subclasses call this once they've checked their own rules
        self.__balance -= amount
        self._record_txn("WITHDRAW", amount)

    def _record_txn(self, tx_type, amount, note=""):
        self._transactions.append(Transaction(tx_type, amount, self.__balance, note))

    @abstractmethod
    def withdraw(self, amount):
        raise NotImplementedError

    @abstractmethod
    def calc_interest(self):
        raise NotImplementedError

    @abstractmethod
    def get_acc_type(self):
        raise NotImplementedError

    def __str__(self):
        status = "ACTIVE" if self._is_active else "CLOSED"
        return f"[{self.get_acc_type()}] #{self._acc_no} - {self._owner_name} - Balance: {self.__balance:.2f} ({status})"

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self._acc_no == other._acc_no

    def __lt__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self.__balance < other.balance

    def __gt__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self.__balance > other.balance

    def __add__(self, other):
        # combined balance for a quick net-worth query - doesn't merge accounts
        if not isinstance(other, Account):
            return NotImplemented
        return self.__balance + other.balance
