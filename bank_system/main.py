from database import BankDatabase
from person import Employee, Customer
from service import Loan, CreditCard
from account import Checking, Savings

# Initialize database
# Initialize bank system
# Give bank system database
# Bank system can create employees, customers, accounts, and services
# Employees
main_db = BankDatabase("main_db")

emp1 = Employee("Soren", "Kierke", "Germany", "Teller", 50000)

res = main_db.save_data(type(emp1).__name__, emp1.data_dict)

print(res)
