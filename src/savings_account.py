# Savings account - has a minimum balance you can't dip below, earns interest.
from src.account import Account
from src.exceptions import MinimumBalanceError, InactiveAccountError


class SavingsAccount(Account):
    min_balance = 500.0
    INTEREST_RATE = 0.04  # 4% flat, applied whenever calc_interest() is called

    def __init__(self, owner_name, initial_balance=0.0):
        if initial_balance < SavingsAccount.min_balance:
            initial_balance = max(initial_balance, SavingsAccount.min_balance)
        super().__init__(owner_name, initial_balance)

    def withdraw(self, amount):
        if not self.is_active:
            raise InactiveAccountError(self.account_number)
        amount = Account.check_amount(amount)
        remaining = self.balance - amount
        if remaining < SavingsAccount.min_balance:
            raise MinimumBalanceError(SavingsAccount.min_balance)
        self._do_withdraw(amount)
        return self.balance

    def calc_interest(self):
        return round(self.balance * SavingsAccount.INTEREST_RATE, 2)

    def get_acc_type(self):
        return "Savings"
