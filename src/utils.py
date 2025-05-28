def format_amount(amount):
    return "{:,.2f}".format(amount)

def validate_positive_amount(amount):
    if amount <= 0:
        raise ValueError("Amount must be positive.")

def validate_account_number(account_number):
    if len(account_number) != 10 or not account_number.isdigit():
        raise ValueError("Account number must be a 10-digit number.")

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format.")