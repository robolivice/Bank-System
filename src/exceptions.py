# Custom exceptions so we're not just raising bare Value Errors everywhere.

class BankError(Exception):
    pass


class InvalidAmountError(BankError):
    def __init__(self, amount):
        msg = "Invalid amount: {}. Amount must be a positive number.".format(amount)
        super().__init__(msg)
        self.amount = amount


class InsufficientFundsError(BankError):
    def __init__(self, balance, requested):
        msg = "Insufficient funds: balance is %.2f, but %.2f was requested." % (balance, requested)
        super().__init__(msg)
        self.balance = balance
        self.requested = requested


class AccountNotFoundError(BankError):
    def __init__(self, acc_no):
        super().__init__("Account number " + str(acc_no) + " was not found.")
        self.acc_no = acc_no


class InactiveAccountError(BankError):
    def __init__(self, acc_no):
        super().__init__(f"Account {acc_no} is inactive/closed.")
        self.acc_no = acc_no


class MinimumBalanceError(BankError):
    def __init__(self, min_balance):
        super().__init__("Withdrawal would breach minimum balance of %.2f." % min_balance)
        self.min_balance = min_balance


class OverdraftLimitError(BankError):
    def __init__(self, overdraft_limit):
        super().__init__(f"Withdrawal would exceed overdraft limit of {overdraft_limit:.2f}.")
        self.overdraft_limit = overdraft_limit
