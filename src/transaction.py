"""
Transaction module - one ledger entry per deposit/withdraw/transfer.
Kept separate from Account so the ledger format can change on its own.
"""
from datetime import datetime

class Transaction:
    def __init__(self, tx_type, amount, balance_after, note=""):
        self.timestamp = datetime.now()
        self.tx_type = tx_type
        self.amount = amount
        self.balance_after = balance_after
        self.note = note

    def __str__(self):
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return "[{}] {:<13} amount={:>10.2f}  balance_after={:>10.2f}  {}".format(
            ts, self.tx_type, self.amount, self.balance_after, self.note)

    @classmethod
    def _from_row(cls, row):
        """Rebuild a Transaction from a DB row (see BankDB.fetch_txns)."""
        tx_type, amount, balance_after, note, timestamp = row
        obj = cls.__new__(cls)
        obj.tx_type = tx_type
        obj.amount = amount
        obj.balance_after = balance_after
        obj.note = note
        obj.timestamp = datetime.fromisoformat(timestamp)
        return obj

    def as_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "type": self.tx_type,
            "amount": self.amount,
            "balance_after": self.balance_after,
            "note": self.note,
        }