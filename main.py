"""
main.py

CLI for the bank system. Run with: python main.py
"""
from src import Bank, BankReport
from src.exceptions import BankError

MENU = """
{bank_name}
1. Create account
2. Deposit
3. Withdraw
4. Transfer between accounts
5. View account details
6. List all accounts
7. View bank report
8. Close account
0. Exit
"""


def prompt_float(label):
    while True:
        raw = input(label)
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a valid number.")


def prompt_int(label):
    while True:
        raw = input(label)
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a valid account number.")


def run():
    bank = Bank("VITyarthi National Bank", db_path="bank.db")

    while True:
        print(MENU.format(bank_name=bank.name))
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Owner name: ").strip()
                acc_type = input("Account type (savings/current): ").strip()
                deposit = prompt_float("Initial deposit: ")
                account = bank.create_account(name, acc_type, deposit)
                print("  Created: " + str(account))

            elif choice == "2":
                acc_no = prompt_int("Account number: ")
                amount = prompt_float("Deposit amount: ")
                new_balance = bank.deposit(acc_no, amount)
                print("  New balance: %.2f" % new_balance)

            elif choice == "3":
                acc_no = prompt_int("Account number: ")
                amount = prompt_float("Withdraw amount: ")
                new_balance = bank.withdraw(acc_no, amount)
                print(f"  New balance: {new_balance:.2f}")

            elif choice == "4":
                src_no = prompt_int("From account number: ")
                dst_no = prompt_int("To account number: ")
                amount = prompt_float("Transfer amount: ")
                src_bal, dst_bal = bank.transfer(src_no, dst_no, amount)
                print("  Source balance: {:.2f} | Target balance: {:.2f}".format(src_bal, dst_bal))

            elif choice == "5":
                acc_no = prompt_int("Account number: ")
                account = bank.get_acc(acc_no)
                print("  " + str(account))
                print(f"  Interest (if paid today): {account.calc_interest():.2f}")
                print("  Recent transactions:")
                for tx in account.transactions[-5:]:
                    print("    " + str(tx))

            elif choice == "6":
                if len(bank) == 0:
                    print("  No accounts yet.")
                for account in sorted(bank, reverse=True):
                    print("  " + str(account))

            elif choice == "7":
                report = BankReport(bank)
                print(report.gen_report())

            elif choice == "8":
                acc_no = prompt_int("Account number to close: ")
                bank.close_acc(acc_no)
                print("  Account %s closed." % acc_no)

            elif choice == "0":
                print("Goodbye!")
                bank.close_db()
                break

            else:
                print("  Invalid option, try again.")

        except BankError as e:
            print(f"  [Error] {e}")
        except ValueError as e:
            print("  [Error] " + str(e))


if __name__ == "__main__":
    run()
