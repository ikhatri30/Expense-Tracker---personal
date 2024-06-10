import csv
from datetime import datetime
from collections import defaultdict

class Transaction:
    def __init__(self, transaction_type, date, time, month, year, amount, category=""):
        self.transaction_type = transaction_type
        self.date = date
        self.time = time
        self.month = month
        self.year = year
        self.amount = amount
        self.category = category

class FinanceTracker:
    def __init__(self):
        self.transactions = []
        self.budgets = {}  # Dictionary to store budgets (month/year: {'expense': amount, 'investment': amount})
        self.load_data_from_csv("finance_data.csv")  # Load existing data on startup

    def add_transaction(self, transaction_type, date, time, amount, category=""):
        month = date.month
        year = date.year
        transaction = Transaction(transaction_type, date, time, month, year, amount, category)
        self.transactions.append(transaction)

        # Check for budget exceedance
        budget = self.budgets.get((month, year), {})
        if transaction_type in ("expense", "investment"):
            budget_amount = budget.get(transaction_type, 0)
            if amount > budget_amount:
                print(f"Warning: Budget for {transaction_type} in {month}/{year} exceeded by {amount - budget_amount:.2f}")

        self.save_data_to_csv("finance_data.csv")  # Save data after each transaction

    def display_transactions(self):
        print("Transactions:")
        for transaction in self.transactions:
            print(f"{transaction.transaction_type} - {transaction.date.strftime('%Y-%m-%d %H:%M:%S')} - Amount: ${transaction.amount:.2f} ({transaction.category})")

    def calculate_monthly_totals(self, month, year):
        income = 0
        expense = 0
        investment = 0
        for transaction in self.transactions:
            if transaction.month == month and transaction.year == year:
                if transaction.transaction_type == "income":
                    income += transaction.amount
                elif transaction.transaction_type == "expense":
                    expense += transaction.amount
                elif transaction.transaction_type == "investment":
                    investment += transaction.amount
        balance = income - expense
        return income, expense, investment, balance

    def set_budget(self, month, year, expense_budget, investment_budget):
        self.budgets[(month, year)] = {"expense": expense_budget, "investment": investment_budget}

    def save_data_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Transaction Type", "Date", "Time", "Month", "Year", "Amount", "Category"])
            for transaction in self.transactions:
                writer.writerow([transaction.transaction_type, transaction.date.strftime('%Y-%m-%d'), transaction.time.strftime('%H:%M:%S'), transaction.month, transaction.year, transaction.amount, transaction.category])

    def load_data_from_csv(self, filename):
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row
                for row in reader:
                    transaction_type, date_str, time_str, month, year, amount, category = row
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    time = datetime.strptime(time_str, '%H:%M:%S')
                    amount = float(amount)
                    transaction = Transaction(transaction_type, date, time, int(month), int(year), amount, category)
                    self.transactions.append(transaction)
        except FileNotFoundError:
            print("No existing data found. Starting fresh.")

#Main Function
def main():
    tracker = FinanceTracker()

    while True:
        print("\nFinance Tracker Menu:")
        print("1. Add Transaction")
        print("2. Display Transactions")
        print("3. Calculate Monthly Totals")
        print("4. Set Budget")
        print("5. Save Data ")  
        print("6. Load Data ")  
        print("7. Exit")


        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            # Add Transaction
            print("NOTE: SET/UPDATE MONTHLY BUDGET BEFORE ADDING EXPENSE AND INVESTMENT TRANSACTIONS !")
            transaction_type = input("Enter transaction type (income, expense, investment): ")
            try:
                date_str = input("Enter date (YYYY-MM-DD): ")
                date = datetime.strptime(date_str, '%Y-%m-%d')
                time_str = input("Enter time (HH:MM:SS): ")
                time = datetime.strptime(time_str, '%H:%M:%S')
                amount = float(input("Enter amount: "))
                category = input("Enter category (optional): ")
                tracker.add_transaction(transaction_type, date, time, amount, category)
                print("Transaction added successfully!")
            except ValueError:
                print("Invalid date or time format. Please try again.")

        elif choice == '2':
            # Display Transactions
            tracker.display_transactions()

        elif choice == '3':
            # Calculate Monthly Totals
            try:
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year: "))
                income, expense, investment, balance = tracker.calculate_monthly_totals(month, year)
                print(f"\nMonthly Totals for {month}/{year}:")
                print(f"Income: ${income:.2f}")
                print(f"Expense: ${expense:.2f}")
                print(f"Investment: ${investment:.2f}")
                print(f"Balance: ${balance:.2f}")
            except ValueError:
                print("Invalid month or year. Please try again.")

        elif choice == '4':
            # Set Budget
            try:
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year: "))
                expense_budget = float(input("Enter expense budget: "))
                investment_budget = float(input("Enter investment budget: "))
                tracker.set_budget(month, year, expense_budget, investment_budget)
                print("Budget set successfully!")
            except ValueError:
                print("Invalid month, year, or budget amount. Please try again.")

        elif choice == '5':
            # Save Data (Manual)
            tracker.save_data_to_csv("finance_data.csv")
            print("Data saved successfully!")

        elif choice == '6':
            # Load Data (Manual)
            tracker.load_data_from_csv("finance_data.csv")
            print("Data loaded successfully!")

        elif choice == '7':
            # Exit
            print("Exiting Finance Tracker.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
