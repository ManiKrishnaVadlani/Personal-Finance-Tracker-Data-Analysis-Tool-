from datetime import datetime

date_format = "%d-%m-%Y"  # Correct date format
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    """Prompts the user for a date in dd-mm-yyyy format."""
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)


def get_amount():
    """Prompts the user for a valid amount (positive, non-zero)."""
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a positive, non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    """Prompts the user to select a category (Income or Expense)."""
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()


def get_description():
    """Prompts the user for a transaction description (optional)."""
    return input("Enter a description (optional): ").strip()
