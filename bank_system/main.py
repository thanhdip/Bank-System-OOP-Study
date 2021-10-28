import re
from account import Account
from account import OverdraftError
from service import CreditLimitError, OverpayedError
from person import Person
from service import Service
from database import BankDatabase
from person import Employee, Customer
from service import Loan, CreditCard
from account import Checking, Savings

import cmd2
import sys
import pprint


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
service_parser = cmd2.Cmd2ArgumentParser()
service_subparser = service_parser.add_subparsers(
    title="Available Service Commands",
    help="use these commands to admin customer's services."
)

# Create subcommand
s_create_parser = service_subparser.add_parser(
    'create', help='create service for customer.')
s_create_parser.add_argument(
    'type',  type=str, help="Type of service",
    choices=["loan", "credit"])
s_create_parser.add_argument('ba', type=float, help="borrowed amount")
s_create_parser.add_argument('int', type=float, help="interest rate")

# Find subcommand
s_find_parser = service_subparser.add_parser(
    'find', help='find services of customers.')
s_find_parser.add_argument('cid', type=int, help="Customer ID")

# Delete subcommand
s_delete_parser = service_subparser.add_parser(
    'delete', help='delete services of customers.')
s_delete_parser.add_argument('id', type=int, help="Service ID")

# Update subcommand
sl_update_parser = service_subparser.add_parser(
    'update_loan', help='update loans of a customer.')
sl_update_parser.add_argument('id', type=int, help="loan's service id")
sl_update_parser.add_argument('-int', type=float, help="interest rate")
sl_update_parser.add_argument('-te', type=float, help="term")
sl_update_parser.add_argument('-pay', type=float, help="pay()")

sc_update_parser = service_subparser.add_parser(
    'update_credit', help='update credit cards of a customer.')
sc_update_parser.add_argument('id', type=int, help="credit's service id")
sc_update_parser.add_argument('-int', type=float, help="interest rate")
sc_update_parser.add_argument('-max', type=int, help="credit max limit.")
sc_update_parser.add_argument('-fee', type=int, help="annual fee")
sc_update_parser.add_argument('-pay', type=float, help="pay()")
sc_update_parser.add_argument('-borrow', type=float, help="borrow()")

# ACCOUNTS
account_parser = cmd2.Cmd2ArgumentParser()
account_subparser = account_parser.add_subparsers(
    title="Available Account Commands",
    help="use these commands to admin customer's accounts."
)

# Create subcommand
a_create_parser = account_subparser.add_parser(
    'create', help='create account of customer.')
a_create_parser.add_argument(
    'type',  type=str, help="Type of Account",
    choices=["checking", "savings"])
a_create_parser.add_argument('ba', type=float, help="balance")
a_create_parser.add_argument(
    '-min', type=int, help="minimum blance for checkings.")

# Find subcommand
a_find_parser = account_subparser.add_parser(
    'find', help='find account of customer'
)
a_find_parser.add_argument('cid', type=int, help="Customer ID")

# Delete subcommand
a_delete_parser = account_subparser.add_parser(
    'delete', help='delete account of customer'
)
a_delete_parser.add_argument('cid', type=int, help="Customer ID")

# Update subcommand
a_update_parser = account_subparser.add_parser(
    'update', help='update account of customer'
)
a_update_parser.add_argument('id', type=float, help="Account ID.")
a_update_parser.add_argument('-dep', type=float, help="Deposit to account.")
a_update_parser.add_argument('-wit', type=float, help="Withdraw from account.")
a_update_parser.add_argument(
    '-sav', type=float, help="Savings rate for account.")
a_update_parser.add_argument(
    '-min', type=int, help="Min balance for account.")


class BankSystemShell(cmd2.Cmd):
    intro = ("=============================================================\n"
             "Welcome to the Bank System, Administrator.\n....\n...\n..\n"
             "Type help or ? to see available commands. "
             "Type \"help [command]\" to describe it.")

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
        if args.l is not None:
            self.employee_load(args.l)
        if self._employee_obj is None:
            self.poutput(
                "Please load an employee to update. 'employee update -l [ID]'")
        else:
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

    @ cmd2.with_argparser(employee_parser)
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

    # Services
    def service_find(self, args):
        res = self._main_db.get_services(args.cid)
        if res == []:
            self.poutput("Nothing found. Try with -h for help.")
        else:
            for ser in res:
                self.poutput(pprint.pformat(ser))

    def service_create(self, args):
        if self._customer_obj is None:
            self.poutput(
                ("Please load a customer to add service."
                 "\n'customer update -l [ID]'"))
        else:
            if args.type == "loan":
                serv = Loan(args.ba, args.int, self._customer_obj.customer_id)
            else:
                serv = CreditCard(args.ba, args.int,
                                  self._customer_obj.customer_id)
            res = self._main_db.save_data(
                type(serv).__name__, serv.data_dict)
            self.poutput("Service ID: " + str(res[0]))
            self.poutput(
                f"Added to customer {self._customer_obj._customer_id}")

    def service_update_loan(self, args):
        res = self._main_db.get_services(aco_ser_id=args.id)
        if res == []:
            self.poutput("Loan not found.")
        else:
            if res[0]["service_type"] == "CreditCard":
                self.poutput("Not a loan.")
                return
            resL = res[0]
            del resL["service_type"]
            del resL["max_limit"]
            del resL["annual_fee"]
            loan = Loan(**resL)
            if args.int is not None:
                loan.interest_rate = args.int
            if args.te is not None:
                loan.term = args.te
            if args.pay is not None:
                try:
                    total = loan.pay(args.pay)
                    self.poutput(f"Paying {args.pay}")
                    self.poutput(f"Loan Left: {total}")
                except OverpayedError:
                    self.poutput("Overpaying, try again and pay less!")
            self._main_db.save_data(type(loan).__name__, loan.data_dict)
            self.poutput(
                (f"Customer {loan.customer_id}"
                 f"\nLoan {loan.id} updated."))

    def service_update_credit(self, args):
        res = self._main_db.get_services(aco_ser_id=args.id)
        if res == []:
            self.poutput("Credit card not found.")
        else:
            if res[0]["service_type"] == "Loan":
                self.poutput("Not a Credit card.")
                return
            resL = res[0]
            del resL["service_type"]
            del resL["term"]
            del resL["payed"]
            credit = CreditCard(**resL)
            if args.int is not None:
                credit.interest_rate = args.int
            if args.max is not None:
                credit.max_limit = args.max
            if args.fee is not None:
                credit.annual_fee = args.fee
            if args.pay is not None:
                total = credit.pay(args.pay)
                self.poutput(f"Paying {args.pay}")
                self.poutput(f"Balance: {total}")
            if args.borrow is not None:
                try:
                    total = credit.borrow(args.borrow)
                    self.poutput(f"Borrowing {args.borrow}")
                    self.poutput(f"Balance: {total}")
                except CreditLimitError:
                    self.poutput(
                        "Credit Limit Hit. Pay off more or borrow less.")
                    return
            self._main_db.save_data(type(credit).__name__, credit.data_dict)
            self.poutput(
                (f"Customer {credit.customer_id}"
                 f"\nCredit card {credit.id} updated."))

    def service_delete(self, args):
        self.poutput(args.id)
        # Delete works with both
        self._main_db.delete_data(Loan.__name__, args.id)
        self.poutput(f"Deleting {args.id} if exists.")

    s_find_parser.set_defaults(func=service_find)
    s_create_parser.set_defaults(func=service_create)
    sl_update_parser.set_defaults(func=service_update_loan)
    sc_update_parser.set_defaults(func=service_update_credit)
    s_delete_parser.set_defaults(func=service_delete)

    @ cmd2.with_argparser(service_parser)
    def do_service(self, args):
        "Administrate Customer's services. Add, Update, Delete, Find."
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('service')

    # Accounts
    def account_find(self, args):
        res = self._main_db.get_accounts(args.cid)
        if res == []:
            self.poutput("Nothing found. Try with -h for help.")
        else:
            for acc in res:
                self.poutput(pprint.pformat(acc))

    def account_create(self, args):
        if self._customer_obj is None:
            self.poutput(
                ("Please load a customer to add service."
                 "\n'customer update -l [ID]'"))
        else:
            if args.type == "checking":
                if args.min is None:
                    self.poutput(
                        "Enter a minimum balance for checking accounts.")
                    return
                acco = Checking(args.ba, args.min,
                                self._customer_obj.customer_id)
            else:
                acco = Savings(args.ba, self._customer_obj.customer_id)
            res = self._main_db.save_data(
                type(acco).__name__, acco.data_dict)
            self.poutput("Account ID: " + str(res[0]))
            self.poutput(
                f"Added to customer {self._customer_obj._customer_id}")

    def account_update(self, args):
        res = self._main_db.get_accounts(aco_ser_id=args.id)
        if res == []:
            self.poutput("Account not found. Try searching first.")
        else:
            resL = res[0]
            if res[0]["account_type"] == "Checking":
                del resL["account_type"]
                del resL["savings_rate"]
                acc = Checking(**resL)
                if args.min is not None:
                    acc.min_balance = args.min
            else:
                del resL["account_type"]
                del resL["min_balance"]
                acc = Savings(**resL)
                if args.sav is not None:
                    acc.savings_rate = args.sav
            if args.dep is not None:
                bal = acc.deposit(args.dep)
                self.poutput(f"Deposited: {args.dep}")
                self.poutput(f"Balance: {bal}")
            if args.wit is not None:
                try:
                    bal = acc.withdraw(args.wit)
                    self.poutput(f"Withdrew: {args.wit}")
                    self.poutput(f"Balance: {bal}")
                except OverdraftError:
                    self.poutput(
                        "Over withdrawing. Withdraw less or deposit more.")
                    return
            self._main_db.save_data(
                type(acc).__name__, acc.data_dict)
            self.poutput(
                "Data saved, account:\n" + pprint.pformat(acc.data_dict))

    def account_delete(self, args):
        self.poutput(args.cid)
        # Delete works with both
        self._main_db.delete_data(Checking.__name__, args.cid)
        self.poutput(f"Deleting {args.cid} if exists.")

    a_find_parser.set_defaults(func=account_find)
    a_create_parser.set_defaults(func=account_create)
    a_update_parser.set_defaults(func=account_update)
    a_delete_parser.set_defaults(func=account_delete)

    @ cmd2.with_argparser(account_parser)
    def do_account(self, args):
        "Administrate Customer's accounts. Add, Update, Delete, Find."
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('account')


def main():
    main_db = BankDatabase("main")
    cli = BankSystemShell(main_db)
    sys.exit(cli.cmdloop())


if __name__ == "__main__":
    main()
