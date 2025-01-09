import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Ensures the CSV file exists and has the correct format."""
        try:
            df = pd.read_csv(cls.CSV_FILE)
            if list(df.columns) != cls.COLUMNS:
                raise ValueError("CSV columns do not match the expected format.")
        except (FileNotFoundError, pd.errors.ParserError, ValueError):
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def clean_csv(cls):
        """Cleans the CSV file by removing invalid rows or columns."""
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df = df[cls.COLUMNS]  # Keep only expected columns
            df.dropna(subset=cls.COLUMNS, inplace=True)  # Drop rows with missing values
            df.to_csv(cls.CSV_FILE, index=False)  # Save the cleaned file
            print("CSV cleaned successfully.")
        except (FileNotFoundError, pd.errors.ParserError):
            print("Error reading the CSV file. Reinitializing...")
            cls.initialize_csv()

    @classmethod
    def add_entry(cls, date, amount, category, description):
        cls.initialize_csv()
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        cls.clean_csv()
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, errors="coerce")
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
            df.dropna(subset=["date", "amount"], inplace=True)

            start_date = datetime.strptime(start_date, CSV.FORMAT)
            end_date = datetime.strptime(end_date, CSV.FORMAT)

            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            if filtered_df.empty:
                print("No transactions found in the given date range.")
                return pd.DataFrame()

            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum() or 0
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum() or 0
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

            return filtered_df
        except pd.errors.ParserError:
            print("Error reading the CSV file. Please check its format.")
            return pd.DataFrame()


def add():
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    if df.empty:
        print("No data to plot.")
        return

    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            try:
                start_date = get_date("Enter the start date (dd-mm-yyyy): ")
                end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            except ValueError:
                print("Invalid date format. Please try again.")
                continue

            df = CSV.get_transactions(start_date, end_date)
            if not df.empty and input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")


if __name__ == "__main__":
    main()

