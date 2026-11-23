from abc import ABC, abstractmethod


# ==========================================
# ABSTRACT CLASS
# ==========================================
class Account(ABC):

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def check_balance(self):
        pass


# ==========================================
# PARENT CLASS
# ==========================================
class BankAccount(Account):

    bank_name = "ABC Bank"

    def __init__(self, account_number, holder_name, balance):
        self.account_number = account_number
        self.holder_name = holder_name
        self.__balance = balance
        self.transactions = []

    # Getter
    def get_balance(self):
        return self.__balance

    # Internal balance update methods
    def _add_balance(self, amount):
        self.__balance += amount

    def _subtract_balance(self, amount):
        self.__balance -= amount

    def deposit(self, amount):
        if amount > 0:
            self._add_balance(amount)
            self.transactions.append(f"Deposited: {amount}")
            print("Deposit successful!")
            return True
        else:
            print("Invalid deposit amount.")
            return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self._subtract_balance(amount)
            self.transactions.append(f"Withdrawn: {amount}")
            print("Withdrawal successful!")
            return True
        else:
            print("Insufficient balance or invalid amount.")
            return False

    def check_balance(self):
        print("Account Balance:", self.__balance)

    def display_details(self):
        print("\n----- ACCOUNT DETAILS -----")
        print("Bank Name      :", self.bank_name)
        print("Account Number  :", self.account_number)
        print("Account Holder  :", self.holder_name)
        print("Account Type    :", self.get_account_type())
        print("Balance        :", self.get_balance())

    def get_account_type(self):
        return "General Account"


# ==========================================
# CHILD CLASS - SAVINGS ACCOUNT
# ==========================================
class SavingsAccount(BankAccount):

    MINIMUM_BALANCE = 1000

    def get_account_type(self):
        return "Savings Account"

    # Method overriding (Polymorphism)
    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return False

        if self.get_balance() - amount >= self.MINIMUM_BALANCE:
            self._subtract_balance(amount)
            self.transactions.append(f"Withdrawn: {amount}")
            print("Savings withdrawal successful!")
            return True
        else:
            print("Minimum balance of 1000 must be maintained.")
            return False


# ==========================================
# CHILD CLASS - CURRENT ACCOUNT
# ==========================================
class CurrentAccount(BankAccount):

    OVERDRAFT_LIMIT = 5000

    def get_account_type(self):
        return "Current Account"

    # Method overriding (Polymorphism)
    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return False

        available_balance = self.get_balance() + self.OVERDRAFT_LIMIT

        if amount <= available_balance:
            self._subtract_balance(amount)
            self.transactions.append(f"Withdrawn: {amount}")
            print("Current account withdrawal successful!")
            return True
        else:
            print("Overdraft limit exceeded.")
            return False


# ==========================================
# BANK MANAGEMENT CLASS
# ==========================================
class Bank:

    def __init__(self):
        self.accounts = {}

    def create_account(self):
        account_number = input("Enter account number: ").strip()

        if not account_number:
            print("Account number cannot be empty.")
            return

        if account_number in self.accounts:
            print("Account number already exists.")
            return

        holder_name = input("Enter account holder name: ").strip()

        if not holder_name:
            print("Name cannot be empty.")
            return

        print("\n1. Savings Account")
        print("2. Current Account")

        account_type = input("Select account type: ").strip()

        try:
            balance = float(input("Enter initial balance: "))

            if balance < 0:
                print("Balance cannot be negative.")
                return

            if account_type == "1":
                if balance < SavingsAccount.MINIMUM_BALANCE:
                    print("Savings account requires minimum balance of 1000.")
                    return

                account = SavingsAccount(
                    account_number, holder_name, balance
                )

            elif account_type == "2":
                account = CurrentAccount(
                    account_number, holder_name, balance
                )

            else:
                print("Invalid account type.")
                return

            self.accounts[account_number] = account
            print("Account created successfully!")

        except ValueError:
            print("Please enter a valid balance.")

    def get_account(self):
        account_number = input("Enter account number: ").strip()

        account = self.accounts.get(account_number)

        if account is None:
            print("Account not found.")

        return account

    def view_account(self):
        account = self.get_account()

        if account:
            account.display_details()

    def view_all_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return

        print("\n===== ALL BANK ACCOUNTS =====")

        for account in self.accounts.values():
            account.display_details()

    def deposit_money(self):
        account = self.get_account()

        if account:
            try:
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)
            except ValueError:
                print("Please enter a valid amount.")

    def withdraw_money(self):
        account = self.get_account()

        if account:
            try:
                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)
            except ValueError:
                print("Please enter a valid amount.")

    def transfer_money(self):
        print("\n===== MONEY TRANSFER =====")

        sender_number = input("Enter sender account number: ").strip()
        receiver_number = input("Enter receiver account number: ").strip()

        if sender_number == receiver_number:
            print("Cannot transfer to the same account.")
            return

        sender = self.accounts.get(sender_number)
        receiver = self.accounts.get(receiver_number)

        if sender is None:
            print("Sender account not found.")
            return

        if receiver is None:
            print("Receiver account not found.")
            return

        try:
            amount = float(input("Enter transfer amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            # Withdraw from sender
            if sender.withdraw(amount):

                # Deposit into receiver
                receiver.deposit(amount)

                # Update transaction history
                sender.transactions.append(
                    f"Transfer sent to {receiver_number}: {amount}"
                )

                receiver.transactions.append(
                    f"Transfer received from {sender_number}: {amount}"
                )

                print("Transfer completed successfully!")

        except ValueError:
            print("Invalid amount.")

    def transaction_history(self):
        account = self.get_account()

        if account:
            print("\n===== TRANSACTION HISTORY =====")

            if not account.transactions:
                print("No transactions available.")
                return

            for transaction in account.transactions:
                print(transaction)

    def menu(self):
        while True:
            print("\n===== ABC BANK MANAGEMENT SYSTEM =====")
            print("1. Create Account")
            print("2. View Account Details")
            print("3. View All Accounts")
            print("4. Deposit Money")
            print("5. Withdraw Money")
            print("6. Transfer Money")
            print("7. Transaction History")
            print("8. Check Balance")
            print("9. Exit")

            try:
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    self.create_account()

                elif choice == 2:
                    self.view_account()

                elif choice == 3:
                    self.view_all_accounts()

                elif choice == 4:
                    self.deposit_money()

                elif choice == 5:
                    self.withdraw_money()

                elif choice == 6:
                    self.transfer_money()

                elif choice == 7:
                    self.transaction_history()

                elif choice == 8:
                    account = self.get_account()
                    if account:
                        account.check_balance()

                elif choice == 9:
                    print("Thank you for using ABC Bank!")
                    break

                else:
                    print("Invalid choice. Select from 1 to 9.")

            except ValueError:
                print("Please enter a valid menu number.")


# ==========================================
# MAIN PROGRAM
# ==========================================
if __name__ == "__main__":
    bank = Bank()
    bank.menu()