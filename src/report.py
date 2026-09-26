"""Analytics, kept out of Bank so Bank stays just the domain model."""
import numpy as np
from src.utils import format_money, group_accs_by_type, top_accs


class BankReport:
    def __init__(self, bank):
        self.bank = bank

    def _balances(self):
        return np.array([acc.balance for acc in self.bank], dtype=float)

    def summary_stats(self):
        balances = self._balances()
        if balances.size == 0:
            return {"total": 0.0, "mean": 0.0, "median": 0.0, "std": 0.0, "count": 0}

        total = float(np.sum(balances))
        mean = total / balances.size  # simple average, don't need numpy for this
        return {
            "total": total,
            "mean": mean,
            "median": float(np.median(balances)),
            "std": float(np.std(balances)),
            "count": int(balances.size),
        }

    def total_interest(self):
        return round(sum(acc.calc_interest() for acc in self.bank), 2)

    def gen_report(self, top_n=3):
        stats = self.summary_stats()
        grouped = group_accs_by_type(self.bank.get_all_accs())
        best_accs = top_accs(self.bank.get_all_accs(), top_n)

        lines = []
        lines.append("===== " + self.bank.name + " — Bank Report =====")
        lines.append("Total accounts     : {}".format(stats['count']))
        lines.append("Total deposits     : " + format_money(stats['total']))
        lines.append(f"Average balance    : {format_money(stats['mean'])}")
        lines.append(f"Median balance     : {format_money(stats['median'])}")
        lines.append("Balance std. dev.  : {}".format(format_money(stats['std'])))
        lines.append(f"Total interest owed: {format_money(self.total_interest())}")
        lines.append("")
        lines.append("-- By account type --")
        for acc_type, accs in grouped.items():
            lines.append("  {}: {} account(s)".format(acc_type, len(accs)))

        lines.append("")
        lines.append(f"-- Top {top_n} accounts by balance --")
        for acc in best_accs:
            lines.append("  " + str(acc))

        return "\n".join(lines)
