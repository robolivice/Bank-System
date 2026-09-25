"""Little helper functions that don't belong on any one class."""
import itertools


def format_money(amount, symbol="$"):
    return symbol + "{:,.2f}".format(amount)
def group_accs_by_type(accounts):
    # groupby only groups consecutive matches, so sort by the key first
    sorted_accs = sorted(accounts, key=lambda a: a.get_acc_type())
    grouped = {}
    for acc_type, group in itertools.groupby(sorted_accs, key=lambda a: a.get_acc_type()):
        grouped[acc_type] = list(group)
    return grouped

def top_accs(accounts, n=3):
    ranked = sorted(accounts, key=lambda a: a.balance, reverse=True)
    return ranked[:n]

def is_valid_name(name):
    return isinstance(name, str) and len(name.strip()) >= 2 and name.replace(" ", "").isalpha()
