from account import Account
from person import Person
from service import Service
from database import BankDatabase
from person import Employee, Customer
from service import Loan, CreditCard
from account import Checking, Savings


def main():
    main_db = BankDatabase("main")

    print_linebreak()
    print("Welcome to the Bank System, Administrator.\n....\n...\n..")
    print("What would you like to administate:")
    choices = ["Employees", "Customers", "Accounts", "Services"]
    print_choices(choices)


def admin_employees():
    print_linebreak()
    print("Administrate EMPLOYEES..")
    print("Choose one:")
    employee_choices = ["Create", "Update", "Remove"]
    print_choices(employee_choices)

    print("Please enter the Employee details seperated by a space \
         in the form:")
    print("[first_name] [last_name] [address] [title] [salary as number]")


def admin_customers():
    customer_choices = ["Create", "Update", "Remove", "Administrate Accounts",
                        "Administrate Services"]


def admin_accounts():
    account_choices = ["Add to customer", "Remove from customer",
                       "Check Balance", "Withdraw", "Deposit"]


def admin_services():
    services_choices = ["Add to customer", "Remove from customer",
                        "Check Details", "Deposit"]


def print_choices(choice_list):
    for i, choice in enumerate(choice_list):
        print(f"[{i}] {choice}")


def print_linebreak():
    for _ in range(100):
        print('=', end='')
    print('')


if __name__ == "__main__":
    main()
