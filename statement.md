# Problem Statement

## Problem Statement
Traditional bank ledger-keeping requires strict rules that differ by account
type (minimum balance for savings, overdraft limits for current accounts),
consistent interest calculation, accurate transaction history, and safe
handling of invalid operations (e.g. withdrawing more than is available).
Manually enforcing these rules is error-prone. This project builds a
console-based Bank Account Management System that encodes these rules in
software, ensuring every operation is validated and logged consistently.

## Scope of the Project
- Create and manage two account types: Savings and Current.
- Deposit, withdraw, and transfer funds between accounts with full
  validation and rollback on failure.
- Track a per-account transaction history.
- Generate bank-wide analytics (totals, averages, top accounts) using NumPy.
- Provide a menu-driven CLI (`main.py`) as the user-facing entry point.
- Out of scope: persistent storage (database), authentication, and a web/GUI
  front end — the system runs in-memory for a single session.

## Target Users
- Students/instructors evaluating the project for a Python programming
  course (VITyarthi flipped-course submission).
- Anyone wanting a lightweight, extensible reference implementation of
  OOP principles (abstraction, encapsulation, inheritance, polymorphism,
  operator overloading) applied to a realistic domain.

## High-Level Features
1. **Account Management** — create, close, and look up Savings/Current
   accounts, each with its own business rules (`SavingsAccount`,
   `CurrentAccount`, both extending an abstract `Account` base class).
2. **Transactions** — deposit, withdraw, and transfer, each fully validated
   and logged as a `Transaction` object.
3. **Reporting & Analytics** — `BankReport` computes mean/median/std/total
   balances (via NumPy) and lists top accounts and interest liability.
4. **Error Handling** — a dedicated exception hierarchy
   (`InsufficientFundsError`, `MinimumBalanceError`, `OverdraftLimitError`,
   `InvalidAmountError`, `AccountNotFoundError`, `InactiveAccountError`)
   ensures every invalid operation fails safely and predictably.
