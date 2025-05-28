import streamlit as st
from bank import Bank
import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^0\d{10}$", phone)

def main():
    st.title("Welcome to DrazzyDre Bank!")

    # Initialize session state variables
    if 'bank' not in st.session_state:
        st.session_state.bank = Bank()
    bank = st.session_state.bank

    if 'account_number' not in st.session_state:
        st.session_state.account_number = None
    if 'account_created' not in st.session_state:
        st.session_state.account_created = False
    if 'show_menu' not in st.session_state:
        st.session_state.show_menu = True
    if 'selected_action' not in st.session_state:
        st.session_state.selected_action = None
    if 'first_name' not in st.session_state:
        st.session_state.first_name = ""
    if 'last_name' not in st.session_state:
        st.session_state.last_name = ""
    if 'last_message' not in st.session_state:
        st.session_state.last_message = None
    if 'last_message_type' not in st.session_state:
        st.session_state.last_message_type = None

    # Account creation form (only if not created)
    if not st.session_state.account_created:
        st.header("Create Account")
        with st.form("create_account_form"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            account_type = st.selectbox("Account Type", ["Savings", "Current"])
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            submitted = st.form_submit_button("Create Account")
            if submitted:
                if not all([first_name, last_name, account_type, email, phone_number]):
                    st.error("Please fill in all fields.")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                elif not is_valid_phone(phone_number):
                    st.error("Please enter a valid Nigerian phone number (e.g., 08012345678).")
                else:
                    account_number = bank.create_account(first_name, last_name, account_type, email, phone_number)
                    st.session_state.account_number = account_number
                    st.session_state.account_created = True
                    st.session_state.show_menu = True
                    st.session_state.first_name = first_name
                    st.session_state.last_name = last_name
                    st.rerun()  # Immediately rerun to hide the form and show welcome

    # Show welcome message after account creation
    if st.session_state.account_created and st.session_state.account_number:
        st.success(
            f"Welcome {st.session_state.first_name} {st.session_state.last_name}! "
            f"Your account number is: {st.session_state.account_number}"
        )

        # Main menu and banking operations
        if st.session_state.show_menu:
            # Show last message if exists
            if st.session_state.last_message:
                if st.session_state.last_message_type == "success":
                    st.success(st.session_state.last_message)
                elif st.session_state.last_message_type == "error":
                    st.error(st.session_state.last_message)
                elif st.session_state.last_message_type == "info":
                    st.info(st.session_state.last_message)
                # Clear after showing
                st.session_state.last_message = None
                st.session_state.last_message_type = None

            st.header("Main Menu")
            action = st.selectbox(
                "What would you like to do?",
                ["Deposit", "Withdraw", "Transfer", "Check Balance", "Check Account Number", "Check Account Details", "Exit"]
            )
            if st.button("Proceed", key="proceed_btn"):
                st.session_state.selected_action = action
                st.session_state.show_menu = False
                st.rerun()

        else:
            action = st.session_state.selected_action

            if action == "Deposit":
                amount = st.number_input("Enter amount to deposit:", min_value=0.0, key="deposit_amount")
                if st.button("Deposit", key="deposit_btn"):
                    new_balance = bank.deposit(st.session_state.account_number, amount)
                    if new_balance is not None:
                        st.session_state.last_message = f"Deposited! New balance: {new_balance}"
                        st.session_state.last_message_type = "success"
                    else:
                        st.session_state.last_message = "Deposit failed."
                        st.session_state.last_message_type = "error"
                    st.session_state.show_menu = True
                    st.session_state.selected_action = None
                    st.rerun()

            elif action == "Withdraw":
                amount = st.number_input("Enter amount to withdraw:", min_value=0.0, key="withdraw_amount")
                if st.button("Withdraw", key="withdraw_btn"):
                    result = bank.withdraw(st.session_state.account_number, amount)
                    if result == 'Insufficient funds':
                        st.session_state.last_message = "Insufficient funds"
                        st.session_state.last_message_type = "error"
                    elif result is not None:
                        st.session_state.last_message = f"Withdrawn! New balance: {result}"
                        st.session_state.last_message_type = "success"
                    else:
                        st.session_state.last_message = "Withdrawal failed."
                        st.session_state.last_message_type = "error"
                    st.session_state.show_menu = True
                    st.session_state.selected_action = None
                    st.rerun()

            elif action == "Transfer":
                recipient = st.text_input("Enter recipient account number:", key="transfer_recipient")
                amount = st.number_input("Enter amount to transfer:", min_value=0.0, key="transfer_amount")
                if st.button("Transfer", key="transfer_btn"):
                    result = bank.transfer(st.session_state.account_number, recipient, amount)
                    if result == 'Insufficient funds':
                        st.session_state.last_message = "Insufficient funds"
                        st.session_state.last_message_type = "error"
                    elif result is None:
                        st.session_state.last_message = "Invalid account number(s)"
                        st.session_state.last_message_type = "error"
                    else:
                        st.session_state.last_message = f"Transferred! Your new balance: {result}"
                        st.session_state.last_message_type = "success"
                    st.session_state.show_menu = True
                    st.session_state.selected_action = None
                    st.rerun()

            elif action == "Check Balance":
                if st.button("Check Balance", key="balance_btn"):
                    balance = bank.check_balance(st.session_state.account_number)
                    st.session_state.last_message = f"Your current balance is: {balance}"
                    st.session_state.last_message_type = "info"
                    st.session_state.show_menu = True
                    st.session_state.selected_action = None
                    st.rerun()

            elif action == "Check Account Number":
                if st.button("Check Account Number", key="accnum_btn"):
                    st.session_state.last_message = f"Your account number is: {st.session_state.account_number}"
                    st.session_state.last_message_type = "info"
                    st.session_state.show_menu = True
                    st.session_state.selected_action = None
                    st.rerun()

            elif action == "Check Account Details":
                if st.button("Show Details", key="details_btn"):
                    details = bank.get_account_details(st.session_state.account_number)
                    if details:
                        msg = (
                            f"**Account Details:**\n\n"
                            f"**First Name:** {details['first_name']}\n"
                            f"**Last Name:** {details['last_name']}\n"
                            f"**Account Type:** {details['account_type']}\n"
                            f"**Email:** {details['email']}\n"
                            f"**Phone Number:** {details['phone_number']}\n"
                            f"**Balance:** {details['balance']}"
                        )
                        st.session_state.last_message = msg
                        st.session_state.last_message_type = "info"
                    else:
                        st.session_state.last_message = "Account details not found."
                        st.session_state.last_message_type = "error"
                    st.session_state.show_menu = True
                    st.session_state.selected_action = None
                    st.rerun()

            elif action == "Exit":
                st.success("Thank you for banking with us! You may close this tab.")
                # Optionally, reset session state here if you want to allow new account creation
                # for k in ['account_number', 'account_created', 'show_menu', 'selected_action', 'first_name', 'last_name']:
                #     if k in st.session_state:
                #         del st.session_state[k]

if __name__ == "__main__":
    main()