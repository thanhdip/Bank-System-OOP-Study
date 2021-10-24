from account import Account
from person import Person
from service import Service
from database import BankDatabase
from person import Employee, Customer
from service import Loan, CreditCard
from account import Checking, Savings

import cmd2
import sys
import argparse


class BankSystemShell(cmd2.Cmd):
    intro = ("=============================================================\n"
             "Welcome to the Bank System, Administrator.\n....\n...\n..\n"
             "Type help or ? to see available commands. "
             "Type \"help [command]\" to describe it.")

    def __init__(self, database):
        super().__init__()
        self._main_db = database
        # Delete uneeded commands
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_history
        del cmd2.Cmd.do_run_script
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_shortcuts
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_macro
        del cmd2.Cmd.do_set

    doc_header = 'All Bank Commands'
    prompt = "[Admin] > "
    ruler = "="

    # EMPLOYEES
    employee_parser = cmd2.Cmd2ArgumentParser()
    employee_subparser = employee_parser.add_subparsers(
        title="Available Commands",
        help="use these commands to admin employees")

    # Find subcommand
    find_parser = employee_subparser.add_parser(
        'find', help='search for employees and returns a list of employees')
    find_parser.add_argument(
        "first_name", type=str, help="first name")
    find_parser.add_argument(
        "last_name", default=None, type=str, help="last name")
    find_parser.add_argument(
        "address", default=None, type=str, help="address")
    find_parser.add_argument(
        "id", default=None, type=int, help="id as integer")

    def employee_search(self, args):
        self.poutput(
            (f"Finding {args.first_name} {args.last_name}")
            (f" {args.address} {args.id}"))

    # Set function to subcommand
    find_parser.set_defaults(func=employee_search)

    @cmd2.with_argparser(employee_parser)
    def do_employee(self, args):
        "Adminitrate Employees. Add, Update, Delete, Search"
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('employee')


def main():
    main_db = BankDatabase("main")
    cli = BankSystemShell(main_db)
    sys.exit(cli.cmdloop())


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


def user_input_string(prompt, data_validation):
    inp = get_user_input(prompt)
    if inp in data_validation:
        return str(inp)
    else:
        return None


def get_user_input(prompt):
    inp = input(prompt)
    return inp


def print_choices(choice_list):
    for i, choice in enumerate(choice_list):
        print(f"[{i}] {choice}")


def print_linebreak():
    for _ in range(100):
        print('=', end='')
    print('')


if __name__ == "__main__":
    main()
