from account import Account
from person import Person
from service import Service
from database import BankDatabase
from person import Employee, Customer
from service import Loan, CreditCard
from account import Checking, Savings

# Initialize database
# Initialize bank system
# Give bank system database
# Bank system can create employees, customers, accounts, and services
# Employees
main_db = BankDatabase("main")

objs = []
objs2 = []
objs.append(Employee("Soren", "Kierke", "Germany", "Teller", 50000))
objs.append(Customer("Gregory", "Nyssa", "Georgia"))
objs.append(Loan(50000, .01, 1))
objs.append(CreditCard(40000, .02, 1))
objs.append(Checking(10000, 500, 1))
objs.append(Savings(20000, 1))


for obj in objs:
    res = main_db.save_data(type(obj).__name__, obj.data_dict)
    print(res)
    obj.id = res[0]
    obj.created_at = res[1]

for obj in objs:
    if isinstance(obj, Person):
        obj.first_name = obj.first_name + "NEW!!"
    if isinstance(obj, Service):
        obj.pay(1)
    if isinstance(obj, Account):
        obj.withdraw(1)
    res = main_db.save_data(type(obj).__name__, obj.data_dict)
    print(res)

print(main_db.find_customer("Gregory", None, None))
print(main_db.find_employee("Soren", None, None))

print(main_db.get_accounts(1))
main_db.delete_data("Employee", 1)
