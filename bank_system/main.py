import re
from account import Account
from person import Person
from service import Service
from database import BankDatabase
from person import Employee, Customer
from service import Loan, CreditCard
from account import Checking, Savings

import cmd2
import sys
import pprint
import argparse


# EMPLOYEES
employee_parser = cmd2.Cmd2ArgumentParser()
employee_subparser = employee_parser.add_subparsers(
    title="Available Employee Commands",
    help="use these commands to admin employees")

# Find subcommand
e_find_parser = employee_subparser.add_parser(
    'find', help='search for the employee and returns a list')
e_find_parser.add_argument('-fn',  type=str, help="first name")
e_find_parser.add_argument('-ln',  type=str, help="last name")
e_find_parser.add_argument('-ad',  type=str, help="address")
e_find_parser.add_argument('-id',  type=int, help="id as integer")

# Create subcommand
e_create_parser = employee_subparser.add_parser(
    'create', help='create employees and returns ID to reference later.')
e_create_parser.add_argument(
    '-l', action='store_true', help="create and load.")
e_create_parser.add_argument('fn',  type=str, help="first name")
e_create_parser.add_argument('ln',  type=str, help="last name")
e_create_parser.add_argument('ad',  type=str, help="address")
e_create_parser.add_argument('ti',  type=str, help="title")
e_create_parser.add_argument('sa',  type=int, help="salary")

# Update subcommand
e_update_parser = employee_subparser.add_parser(
    'update',
    help='update employees.')
e_update_parser.add_argument("-l", type=int, help="Load employee with ID")
e_update_parser.add_argument('-fn',  type=str, help="first name")
e_update_parser.add_argument('-ln',  type=str, help="last name")
e_update_parser.add_argument('-ad',  type=str, help="address")
e_update_parser.add_argument("-ti", type=str, help="title")
e_update_parser.add_argument("-sa", type=int, help="salary")

# Delete subcommand
e_delete_parser = employee_subparser.add_parser(
    'delete',
    help='delete employee'
)
e_delete_parser.add_argument('id',  type=int, help="id as integer")

# CUSTOMER
customer_parser = cmd2.Cmd2ArgumentParser()
customer_subparser = customer_parser.add_subparsers(
    title="Available Customer Commands",
    help="use these commands to admin customers."
)

# Find subcommand
c_find_parser = customer_subparser.add_parser(
    'find', help='search for the customer and returns a list')
c_find_parser.add_argument('-fn',  type=str, help="first name")
c_find_parser.add_argument('-ln',  type=str, help="last name")
c_find_parser.add_argument('-ad',  type=str, help="address")
c_find_parser.add_argument('-id',  type=int, help="id as integer")

# Create subcommand
c_create_parser = customer_subparser.add_parser(
    'create', help='create customer and returns ID to reference later.')
c_create_parser.add_argument(
    '-l', action='store_true', help="create and load.")
c_create_parser.add_argument('fn',  type=str, help="first name")
c_create_parser.add_argument('ln',  type=str, help="last name")
c_create_parser.add_argument('ad',  type=str, help="address")

# Update subcommand
c_update_parser = customer_subparser.add_parser(
    'update',
    help='update customer.')
c_update_parser.add_argument("-l", type=int, help="Load customer with ID")
c_update_parser.add_argument('-fn',  type=str, help="first name")
c_update_parser.add_argument('-ln',  type=str, help="last name")
c_update_parser.add_argument('-ad',  type=str, help="address")

# Delete subcommand
c_delete_parser = customer_subparser.add_parser(
    'delete',
    help='delete customer'
)
c_delete_parser.add_argument('id',  type=int, help="id as integer")

# SERVICES


class BankSystemShell(cmd2.Cmd):
    intro = ("=============================================================\n"
             "Welcome to the Bank System, Administrator.\n....\n...\n..\n"
             "Type help or ? to see available commands. "
             "Type \"help [command]\" to describe it.")

    # TO DO
    # Services Create - load customer create service, search,
    # update - load customer, update service, delete
    # Accounts Create - load customer create service, search,
    # update - load customer, update service, delete

    def __init__(self, database):
        super().__init__()
        self._main_db = database
        # Store Load
        self._employee_obj = None
        self._customer_obj = None
        # Delete uneeded commands
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_history
        del cmd2.Cmd.do_run_script
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_shortcuts
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_macro
        # del cmd2.Cmd.do_set

    doc_header = 'All Bank Commands'
    prompt = "[Admin] > "
    ruler = "="

    # Employee
    def employee_create(self, args):
        emp = Employee(args.fn, args.ln, args.ad, args.ti, args.sa)
        res = self._main_db.save_data(type(emp).__name__, emp.data_dict)
        self.poutput("ID: " + str(res[0]))
        if args.l:
            self.employee_load(res[0])

    def employee_search(self, args):
        res = self._main_db.find_employee(args.fn, args.ln, args.ad, args.id)
        if res == []:
            self.poutput("Nothing Found. Try with -h for help.")
        else:
            for emp in res:
                self.poutput(pprint.pformat(emp))

    def employee_load(self, id):
        res = self._main_db.find_employee(id=id)
        if res == []:
            self.poutput("Employee not found. Cannot load.")
        for emp in res:
            self._employee_obj = Employee(
                emp["first_name"],
                emp["last_name"],
                emp["address"],
                emp["title"],
                emp["salary"],
                emp["id"],
                emp["created_at"])
            self.poutput(f"Employee {emp['id']} loaded.")

    def employee_update(self, args):
        # Load employee, change base on context.
        if args.l is not None:
            self.employee_load(args.l)
        if self._employee_obj is None:
            self.poutput(
                "Please load an employee to update. 'employee update -l [ID]'")
        else:
            # Inner loop
            if args.fn is not None:
                self._employee_obj.first_name = args.fn
                self.poutput("First name updated.")
            if args.ln is not None:
                self._employee_obj.last_name = args.ln
                self.poutput("Last name updated.")
            if args.ad is not None:
                self._employee_obj.address = args.ad
                self.poutput("Address updated.")
            if args.ti is not None:
                self._employee_obj.title = args.ti
                self.poutput("Title updated.")
            if args.sa is not None:
                self._employee_obj.salary = args.sa
                self.poutput("Salary updated.")
            self._main_db.save_data(
                type(self._employee_obj).__name__,
                self._employee_obj.data_dict)
            self.poutput(self._employee_obj.data_dict)

    def employee_delete(self, args):
        self._main_db.delete_data(Employee.__name__, args.id)
        self.poutput(f"Deleting {args.id} if exists.")

    # Set function to subcommand
    e_find_parser.set_defaults(func=employee_search)
    e_create_parser.set_defaults(func=employee_create)
    e_update_parser.set_defaults(func=employee_update)
    e_delete_parser.set_defaults(func=employee_update)

    @cmd2.with_argparser(employee_parser)
    def do_employee(self, args):
        "Adminitrate Employees. Create, Update, Delete, Find."
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('employee')

    # Customer
    def customer_load(self, id):
        res = self._main_db.find_customer(id=id)
        if res == []:
            self.poutput("Customer not found. Cannot load.")
        for cus in res:
            self._customer_obj = Customer(
                cus["first_name"],
                cus["last_name"],
                cus["address"],
                cus["created_at"],
                cus["id"]
            )
            self.poutput(f"Customer {cus['id']} loaded.")

    def customer_create(self, args):
        cus = Customer(args.fn, args.ln, args.ad)
        res = self._main_db.save_data(type(cus).__name__, cus.data_dict)
        self.poutput("ID: " + str(res[0]))
        if args.l:
            self.customer_load(res[0])

    def customer_search(self, args):
        res = self._main_db.find_customer(args.fn, args.ln, args.ad, args.id)
        if res == []:
            self.poutput("Nothing Found. Try with -h for help.")
        else:
            for cus in res:
                self.poutput(pprint.pformat(cus))

    def customer_update(self, args):
        if args.l is not None:
            self.customer_load(args.l)
        if self._customer_obj is None:
            self.poutput(
                "Please load a customer to update. 'customer update -l [ID]'")
        else:
            # Inner loop
            if args.fn is not None:
                self._customer_obj.first_name = args.fn
                self.poutput("First name updated.")
            if args.ln is not None:
                self._customer_obj.last_name = args.ln
                self.poutput("Last name updated.")
            if args.ad is not None:
                self._customer_obj.address = args.ad
                self.poutput("Address updated.")
            self._main_db.save_data(
                type(self._customer_obj).__name__,
                self._customer_obj.data_dict)
            self.poutput(self._customer_obj.data_dict)

    def customer_delete(self, args):
        self.poutput(args.id)
        self._main_db.delete_data(Customer.__name__, args.id)
        self.poutput(f"Deleting {args.id} if exists.")

    # Set function to subcommand
    c_find_parser.set_defaults(func=customer_search)
    c_create_parser.set_defaults(func=customer_create)
    c_update_parser.set_defaults(func=customer_update)
    c_delete_parser.set_defaults(func=customer_delete)

    @ cmd2.with_argparser(customer_parser)
    def do_customer(self, args):
        "Administrate Customers. Create, Update, Delete, Find."
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('customer')

    @ staticmethod
    def print_choices(choice_list):
        for i, choice in enumerate(choice_list):
            print(f"[{i}] {choice}")


def main():
    main_db = BankDatabase("main")
    # print(main_db.find_employee())
    cli = BankSystemShell(main_db)
    sys.exit(cli.cmdloop())


def admin_accounts():
    account_choices = ["Add to customer", "Remove from customer",
                       "Check Balance", "Withdraw", "Deposit"]


def admin_services():
    services_choices = ["Add to customer", "Remove from customer",
                        "Check Details", "Deposit"]


if __name__ == "__main__":
    main()
