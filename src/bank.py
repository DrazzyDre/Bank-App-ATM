import random

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, first_name, last_name, account_type, email, phone_number):
        account_number = str(random.randint(1000000000, 9999999999))
        self.accounts[account_number] = {
            'first_name': first_name,
            'last_name': last_name,
            'account_type': account_type,
            'email': email,
            'phone_number': phone_number,
            'balance': 0
        }
        return account_number

    def deposit(self, account_number, amount):
        if account_number in self.accounts:
            self.accounts[account_number]['balance'] += amount
            return self.accounts[account_number]['balance']
        else:
            return None

    def withdraw(self, account_number, amount):
        if account_number in self.accounts:
            if amount <= self.accounts[account_number]['balance']:
                self.accounts[account_number]['balance'] -= amount
                return self.accounts[account_number]['balance']
            else:
                return 'Insufficient funds'
        else:
            return None

    def transfer(self, from_account, to_account, amount):
        if from_account in self.accounts and to_account in self.accounts:
            if amount <= self.accounts[from_account]['balance']:
                self.accounts[from_account]['balance'] -= amount
                self.accounts[to_account]['balance'] += amount
                return self.accounts[from_account]['balance']
            else:
                return 'Insufficient funds'
        else:
            return None

    def check_balance(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]['balance']
        else:
            return None

    def get_account_details(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]
        else:
            return None