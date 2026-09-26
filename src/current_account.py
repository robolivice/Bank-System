from src.account import Account
from src.exceptions import OverdraftLimitError, InactiveAccountError


class CurrentAccount(Account):
    OVERDRAFT_LIMIT = 5000.0

    def withdraw(self, amount):
        if not self.is_active:
            raise InactiveAccountError(self.account_number)
        amount = Account.check_amount(amount)
        remaining = self.balance - amount
        if remaining < -CurrentAccount.OVERDRAFT_LIMIT:
            raise OverdraftLimitError(CurrentAccount.OVERDRAFT_LIMIT)
        self._do_withdraw(amount)
        return self.balance

    def calc_interest(self):
        return 0.0

    def get_acc_type(self):
        return "Current"
